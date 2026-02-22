import numpy as np
import matplotlib.pyplot as plt
content=np.loadtxt('/content/lithium.txt')
SOC_table=content[:,0]
voltage_table=content[:,1]
SOC_table = SOC_table[::-1]      #reversing order cause initially it was in decreasing order but for linear interpoation we need it in increasing order
voltage_table = voltage_table[::-1]   #same as above comment
OCV=0                              #just defining open circuit volatge
R_int=0.2        #0.2 ohms of internal resistance
Vrc=0          #We start with battery relaxed, no polarisation initially
R1,C1=0.5,200          #thevenin model for polarisation calculation
tau=R1*C1              #polarisation time
dt=5    #5 seconds of step time
a=np.exp(-dt/tau)
V_terminal=OCV                #initially voltage the robot reads(terminal voltage) will be equal to OCV
##Timing loop and ROBOT state
state=0  #stores the robot state   WAIT-0, SEARCH-1, SOLAR STOP-2, RETURN-3, COOLDOWN-4
time=0        #ticking time
total_time=3600   #Total time for 1 hour
cycle_length=270
WAIT,SEARCH,SOLAR_CHARGING_STOP,RETURN,COOLDOWN = 0,1,2,3,4      #robot state meaning
motor_OFF,motor_ON=0,1                                           #motor state meaning
battery_capacity=2.2  *3600        #2200mAh capacity
true_SOC=100                  #initally battery is at 100%
SOC_cc=100               #initally SOC due to columb counting will be 100%
SOC_v=100                       #initially SIC due to volatge measurent will be 100%
min_rest_delay=10        #Wait 10seconds for polarisation to decay, cause when motor is OFF< we are doing blend which inreases(trust voltage more) even though just after as motor turns off, there will still be polarisation(thast why we saw spikes earilier), so now wait 10seconds before we make blend some value

#DEFINING LISTS
time_list=[]
true_SOC_list=[]
SOC_cc_list=[]
SOC_v_list=[]
SOC_est_list=[]
blend_list=[]
#BLEND
blend=0               #OUR NOVELTY
rest_time=0           #defining how long has robot not moved

#Adding LOW PASS FILTER TO REMOVE EVEN MORE SPIKES CAUSED BY TRUSTING SOC_v even after delay like die to that -0.3A
SOC_v_filter=100
alpha=0.15 

# NEW: Add low-pass filter for measured_current to smooth spikes and noise
alpha_current = 0.8  
measured_current_filtered = 0.0

#smoothing of spikes 
SOC_est_prev=100

for time in range(0,total_time,dt):
  cycle_time=time%cycle_length   #helps me reset after every 260 seconds or after full ACTION
  if cycle_time<10:
    robot_state=WAIT
    battery_current=0.1           #to power only sensors
    motor_state=motor_OFF
  elif cycle_time<130:
    robot_state=SEARCH
    battery_current=1.5          #to power both sensor and motor
    motor_state=motor_ON
  elif cycle_time<140:
    robot_state=SOLAR_CHARGING_STOP
    battery_current=-0.3    #Since its charging, the SOC accutualy increases
    motor_state=motor_OFF
  elif cycle_time<260:
    robot_state=RETURN
    battery_current=1.5    #this is retrun so same as searching
    motor_state=motor_ON
  else:
    robot_state=COOLDOWN
    battery_current=0.1
    motor_state=motor_OFF

#CALCULATING TRUE SOC for simulation inside battery that only battery knows not us in real life
  true_SOC=true_SOC-(battery_current*dt)/battery_capacity*100
  true_SOC = max(0, min(100, true_SOC))           #GOOD practice since for long simulations, this might overshoot. so this line will keep it in range
  OCV=np.interp(true_SOC,SOC_table, voltage_table)     #doing linear interpolation to get OCV from lithium document when true SOC is inbetween
  Vrc = a*Vrc + R1*(1-a)*battery_current              #Thevenin model RC for polarisation
  V_terminal=OCV-battery_current*R_int-Vrc
#ERRORS in CURRENT SENSOR
  current_offset=0.02      #0.02A offset
  sensor_noise=np.random.normal(0,0.02)      #Gusassian model for sensor noise(EMI+ADC noise)
  pwm_noise=np.random.normal(0,0.05)
  spike=0
  if motor_state == motor_ON and np.random.rand() < 0.05:           #HEre spike only happens when MOTOR is ON
    spike = np.random.uniform(0.5 , 2.0) * np.sign(battery_current)      #applying proabblity of 5 percent that there is DC motor start spike and keeping in mind of sign chnage cause during solar charging discharge current is -ve
  measured_current=battery_current+current_offset+sensor_noise+pwm_noise+spike       #current measured by sensor for battery with errors
  #apply low pass filter 
  measured_current_filtered = alpha_current * measured_current_filtered + (1 - alpha_current) * measured_current
  measured_current=measured_current_filtered
  change_dt=dt+np.random.normal(0 , 0.2)
#CALCULATING SOC USING COLUMB COUNTING METHODS THAT ROBOT MEASURES
  SOC_cc=SOC_cc-((measured_current *change_dt) / battery_capacity) * 100
  SOC_cc = max(0, min(100, SOC_cc))
#CALCULATING SOC USING VOLTAGE MEASUREMENT THAT ROBOT MEASURES
  V_terminal = np.clip(V_terminal,voltage_table.min(),voltage_table.max())     #just safety line so that terminal volatge doesnt go out of range in tbale due to spikes, so we are essentially clipping it
  SOC_v=np.interp(V_terminal,voltage_table, SOC_table)            #reverse interpolation so from terminal volatge we will get SOC from the lithium table
  SOC_v = max(0, min(100, SOC_v))
  SOC_v_filter=alpha*SOC_v_filter+(1-alpha)*SOC_v
  SOC_v=SOC_v_filter
#BLEND LOGIC
  if motor_state==motor_ON:
    blend=0
    rest_time=0
  elif motor_state==motor_OFF and robot_state==SOLAR_CHARGING_STOP:
    tau_eff=25                       #effective confidence recovery speed of polarisation
    rest_time=rest_time+dt
    if rest_time<min_rest_delay:
      blend=0
    else:
      effective_time = rest_time - min_rest_delay
      blend=0.7*(1-np.exp(-effective_time/tau_eff))
    blend = min(0.7 , blend)             #FOR safety so even in rare cases, blend never reaches 0.7 casue if motor off stays for only 10sec, then like cmon even 0.7 is too much for blend
  elif motor_state==0 and (robot_state==COOLDOWN or robot_state==WAIT):
    tau_eff=45
    rest_time=rest_time+dt
    if rest_time<min_rest_delay:
      blend=0
    else:
      effective_time = rest_time - min_rest_delay
      blend=0.7*(1-np.exp(-effective_time/tau_eff))
    blend = min(0.7 , blend)
  SOC_est=(1-blend)*SOC_cc+blend*SOC_v
  #REDUCES SPIKES LIKE MAKES SOC_v not to affect SO_est by making SOC_est move smoothly even if diff between SOC_cc and SOc_v is big. its realsitic cause in real life, SOc_v cannot suddenly jump so.
  max_change = 0.3   # SOC allowed to change only ±0.3% every 5 seconds. (realistic cause this is what happend physcially)
  delta = SOC_est - SOC_est_prev  # You calculate: how much estimator wants to change. 
  delta = np.clip(delta,-max_change,max_change)   #if theres big delta then clip() keeps it within 0.3 range(-0.3 to +0.3) and if smth like 0.1, then clip doesnt do anything it just takes 0.1 as it as no chnages only when it corsses the range here its 0.3, then any higher number is bought to limit->0.3
  SOC_est = SOC_est_prev + delta    #rebuild SOC, like adjust wrt delta
  SOC_est_prev = SOC_est     #updating SOC_est_prev for next loop so it stores latest value

  #appending to the lists
  time_list.append(time)
  true_SOC_list.append(true_SOC)
  SOC_cc_list.append(SOC_cc)
  SOC_v_list.append(SOC_v)
  SOC_est_list.append(SOC_est)
  blend_list.append(blend)

#ERROR
# convert lists to numpy arrays
true_SOC_arr=np.array(true_SOC_list)
SOC_est_arr=np.array(SOC_est_list)
SOC_cc_arr=np.array(SOC_cc_list)
# absolute error
error=np.abs(true_SOC_arr-SOC_est_arr)
error_cc=np.abs(true_SOC_arr-SOC_cc_arr)
# max error
max_error = np.max(error)
# average error
avg_error = np.mean(error)
print("Max Error =", max_error, "%")
print("Average Error =", avg_error, "%")

#PLOTTING BABYYY
#time vs TRUE_SOC and SOC_est
plt.figure()
plt.plot(time_list,true_SOC_list,label="true SOC")
plt.plot(time_list,SOC_est_list,label="measured SOC")
plt.xlabel("time(sec)")
plt.ylabel("SOC(%)")
plt.legend()
plt.title("SOC vs time graph")
plt.show()
#time vs SOC_cc
plt.figure()
plt.plot(time_list,SOC_cc_list,label="SOC_cc")
plt.xlabel("time(sec)")
plt.ylabel("SOC(%)")
plt.legend()
plt.title("SOC columb couting vs time graph")
plt.show()
#time vs SOC_v
plt.figure()
plt.plot(time_list,SOC_v_list,label="SOC_v")
plt.xlabel("time(sec)")
plt.ylabel("SOC(%)")
plt.legend()
plt.title("SOC voltage measurement vs time graph")
plt.show()
#time vs true_SOC
plt.figure()
plt.plot(time_list,true_SOC_list,label="true SOC")
plt.xlabel("time(sec)")
plt.ylabel("SOC(%)")
plt.legend()
plt.title("TRUE SOC vs time graph")
plt.show()
#time vs SOC error
plt.figure()
plt.plot(time_list,error,label="error graph for estimated SOC")
plt.plot(time_list,error_cc,label="graph for SOC coloumb counting")
plt.xlabel("time(sec)")
plt.ylabel("SOC error(%)")
plt.legend()
plt.title("SOC vs error graph")
plt.show()
#time vs blend
plt.figure()
plt.plot(time_list,blend_list,label="blend")
plt.xlabel("time(sec)")
plt.ylabel("blend")
plt.legend()
plt.title("blend vs time graph")
plt.show()
#SOC ERROR HISTOGRAM
plt.figure()
plt.hist(error, bins=30)
plt.xlabel("SOC Error (%)")
plt.ylabel("Frequency")
plt.title("Histogram of Hybrid SOC Estimation Error")
plt.grid(True)
plt.show()
