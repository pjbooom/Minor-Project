#BABY BATTERY
import numpy as np
import matplotlib.pyplot as plt
# battery parameters
bat_cap = 2.0 * 3600      # 2Ah → Coulombs
R_int = 0.2               # internal resistance (ohm)
SOC_O = 100.0             # starting SOC (%)
I = 1.0                   # discharge current (A)
dt = 5.0                  # timestep = 5 seconds
total_time = 3600         # simulate 1 hour
# getting that OCV table
content = np.loadtxt('/content/lithium.txt')
SOC_table = content[:,0]
voltage_table = content[:,1]
# variables that store basic parameters later needed for plotting graphs
time_list = []
true_soc_list = []
est_soc_list = []
voltage_list = []
OCV_list=[]
# assumption before robot starts to draw current
true_SOC = SOC_O
time = 0
# looping each interval of time(5 seconds)
while true_SOC > 0 and time <= total_time:
    # voltage estimation from true SOC (THIS IS FOR BATTERY AND THIS IS TO SIMULATE BATTERY giving volatge that robot measures, but take care that in real life we only get that 'V' variable when robot sense, all this below is for simualtion like how battery thinks so we can simulate it. here also robot doesnt know all this TRUE SOC, we use TRUE SOC to get error here from robot SOC which gets it from variable 'V' t.)
    # columb counting to get true SOC that only battery knows in real life we dont know this, but we need this for simulations so as to get error, accuarcy i mean thats the whole of simulating this in the first place DUMMYYY
    true_SOC = true_SOC - ((I * dt) / bat_cap) * 100
    # this is just protecting from edge handling error like if SOC<0% or SOC>100% then just use OCV of max or min frommtable. WE MIGHT encounter this later, so just for safety.
    if true_SOC >= SOC_table[0]:
        OCV = voltage_table[0]
    elif true_SOC <= SOC_table[-1]:
        OCV = voltage_table[-1]
    #we use linear interpolation here cause in table we have 60% and 65% but not inbetween so we use this formula to get inbetween. THIS IS NOT ESTIMATION, its just pure math.    
    else:
        for i in range(len(SOC_table)-1):
            if true_SOC < SOC_table[i] and true_SOC > SOC_table[i+1]:
                gap_SOC = SOC_table[i] - SOC_table[i+1]
                measure_SOC_gap = true_SOC - SOC_table[i+1]
                measure_SOC = measure_SOC_gap / gap_SOC
                voltage_gap = voltage_table[i] - voltage_table[i+1]
                OCV = voltage_table[i+1] + (measure_SOC * voltage_gap)
                break  
    OCV_list.append(OCV)            
    # putting internal resistance volatge drop here to simulate real battery.
    V = OCV - I * R_int
    # SOC estimation from voltage V (thisd what we do in real life, robot detects V from battery and estimates SOC and we check how accurate this SOC is from TRUE SOC thats simualtion. and we try to reduce it later)
    #edge handling 
    if V >= voltage_table[0]:
        SOC = SOC_table[0]
    elif V <= voltage_table[-1]:
        SOC = SOC_table[-1]
    #Linear interpolation for robot to get SOC from V(reverse of wt we did before)    
    else:
        for i in range(len(voltage_table)-1):
            if V < voltage_table[i] and V > voltage_table[i+1]:
                gap_V = voltage_table[i] - voltage_table[i+1]
                measure_V_gap = V - voltage_table[i+1]
                measure_V = measure_V_gap / gap_V
                SOC_gap = SOC_table[i] - SOC_table[i+1]
                SOC = SOC_table[i+1] + (measure_V * SOC_gap)
                break
    # since this is for first 5 seconds, we store all parameters here in array so we can store next 5 seconds duration,etc
    time_list.append(time)
    true_soc_list.append(true_SOC)
    est_soc_list.append(SOC)
    voltage_list.append(V)
    # next timestep
    time = time+dt
# calculating how much ERROR we get
error_list = []
for i in range(len(true_soc_list)):
    error = abs(true_soc_list[i] - est_soc_list[i])
    error_list.append(error)
print("Maximum SOC error =", np.max(error_list))
print("Average SOC error =", np.mean(error_list))
# PLOTTING IT.
# SOC vs time
plt.figure()
plt.plot(time_list,true_soc_list,label="true SOC")
plt.plot(time_list,est_soc_list,label="estimated SOC")
plt.xlabel("time(sec)")
plt.ylabel("SOC(%)")
plt.legend()
plt.title("SOC vs time graph")
plt.show()
# Error vs time
plt.figure()
plt.plot(time_list,error_list)
plt.xlabel("time(sec)")
plt.ylabel("SOC erorr(%)")
plt.title("SOC error graph")
plt.show()
# Voltage vs time
plt.figure()
plt.plot(time_list,voltage_list,label='terminal voltage')
plt.plot(time_list,OCV_list,label='OCV')
plt.xlabel("time(sec)")
plt.ylabel("voltage(V)")
plt.legend()
plt.title("Voltaage vs time")
plt.show()
# SOC vs Voltage curve from table (OCV curve)
plt.figure()
plt.plot(SOC_table,voltage_table)
plt.xlabel("SOC(%)")
plt.ylabel("Voltage(V)")
plt.title("SOC vs Voltage (OCV Curve)")
plt.show()
