Here i took into account of L293D motor driver and INA219 Sensor
current offset=0.02A
Sensor Noise (EMI due to motor noise+ADC noise)= i used Guassian noise cause it follows BELL Curve= noise ~ N(0,0.02)
PWM noise due to Motor driver=noise ~ N(0,0.05)
DC motor start spike= 5% probabilty random from 0.5A to 2A
Timing error= random from -0.2sec to +0.2 sec


## printed output
Maximum SOC error = 3.4119816407934422
Average SOC error = 1.5597676367958881
