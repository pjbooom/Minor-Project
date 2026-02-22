## Solar Aware Hybrid SOC Estimation Simulation

## Code Explanation
This project simulates a solar powered wire traversal inspection robot that estimates battery State of Charge (SOC) using a physics based hybrid estimator without Machine Learning or Kalman filtering.
TRUE SOC represents the ground truth battery charge and is updated using ideal Coulomb counting physics:
SOC = SOC − (I × dt) / Capacity.
The robot never has access to TRUE SOC and it is used only for performance evaluation.
Battery terminal voltage is generated using an Open Circuit Voltage (OCV) lookup table combined with internal resistance drop and a single RC Thevenin polarization model. The RC network simulates electrochemical relaxation behaviour which causes voltage sag during motor load and gradual recovery during rest.
Robot behaviour follows a repeating operational cycle consisting of WAIT, SEARCH, SOLAR CHARGING STOP, RETURN and COOLDOWN states. Each state determines motor activity and battery current including solar charging during peak detection.
Measured current includes realistic sensor imperfections such as offset drift, Gaussian noise, PWM interference, timestep jitter and probabilistic motor start spikes.
SOC is estimated using two independent methods.
SOC_cc is obtained using Coulomb counting with noisy measured current which produces long term drift.
SOC_v is obtained using reverse interpolation from measured terminal voltage which becomes unreliable during load due to IR drop and polarization.
A behaviour aware blend variable controls confidence in voltage estimation. Motor operation forces blend to zero while rest periods allow exponential confidence recovery. Solar charging accelerates recovery while cooldown and wait states recover more slowly.
Final hybrid estimation:
SOC_est = (1 − blend) × SOC_cc + blend × SOC_v.
--- 

## Graph Explanation

## SOC vs Time
This graph compares TRUE SOC with the hybrid SOC estimate. The hybrid estimator closely tracks ground truth while correcting Coulomb counting drift during rest periods.
## Coulomb Counting SOC vs Time
SOC_cc gradually deviates from TRUE SOC due to accumulated sensor offset and measurement noise, demonstrating long term drift typical in practical systems.
## Voltage Based SOC vs Time
SOC_v fluctuates strongly during motor operation because terminal voltage is affected by instantaneous IR drop and polarization. This illustrates why voltage based estimation alone is unreliable under load.
## SOC Error vs Time
Absolute estimation error highlights the difference between hybrid estimation and Coulomb counting drift. Error spikes appear when voltage correction is applied before full battery relaxation.
## Blend vs Time
Blend represents adaptive confidence in voltage estimation. It resets during motion and increases only during rest, with faster recovery during solar charging compared to idle cooldown.
## Error Histogram
The histogram shows the distribution of hybrid SOC estimation error. Most values cluster at low error indicating stable long term estimation while occasional outliers correspond to transient voltage relaxation effects.
