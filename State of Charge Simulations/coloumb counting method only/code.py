#USING COLMB COUNTING ONLY
#BABY BATTERY
import numpy as np
import matplotlib.pyplot as plt
# battery parameters
bat_cap = 2.0 * 3600      # 2Ah → Coulombs
SOC_O = 100.0             # starting SOC (%)
I = 1.0                   # discharge current (A)
dt = 5.0                  # timestep = 5 seconds
total_time = 3600         # simulate 1 hour   
measured_SOC=SOC_O        #initally measured SOC is the initial SOC which is 100 percent
# variables that store basic parameters later needed for plotting graphs
time_list = []
true_soc_list = []
measured_soc_list=[]
# assumption before robot starts to draw current
true_SOC = SOC_O
time = 0
# looping each interval of time(5 seconds)
while true_SOC > 0 and time <= total_time:
    true_SOC = true_SOC - ((I * dt) / bat_cap) * 100
    #errors in calculation
    current_offset=0.02      #0.02A offset
    sensor_noise=np.random.normal(0,0.02)      #Gusassian model for sensor noise(EMI+ADC noise)
    pwm_noise=np.random.normal(0,0.05)
    spike=0
    if np.random.rand() <0.05:
      spike = np.random.uniform(0.5 , 2.0)       #applying proabblity of 5 percent that there is DC motor start spike
    measured_current=I+current_offset+sensor_noise+pwm_noise+spike  
    change_dt=dt+np.random.normal(0 , 0.2)      
    #columb counting to get measured SOC
    measured_SOC=measured_SOC- ((measured_current *change_dt) / bat_cap) * 100
    # next timestep
    time_list.append(time)
    true_soc_list.append(true_SOC)
    measured_soc_list.append(measured_SOC)
    time = time+dt
#Error
error_list = []
for i in range(len(true_soc_list)):
    error = abs(true_soc_list[i] - measured_soc_list[i])
    error_list.append(error)
print("Maximum SOC error =", np.max(error_list))
print("Average SOC error =", np.mean(error_list)) 
#Plotting it
plt.figure()
plt.plot(time_list,true_soc_list,label="true SOC")
plt.plot(time_list,measured_soc_list,label="measured SOC from columb counting with any error")
plt.xlabel("time(sec)")
plt.ylabel("SOC(%)")
plt.legend()
plt.title("SOC vs time graph")
plt.show()
