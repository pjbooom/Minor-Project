## SOC vs Time graph
As time increases, we can see SOC with error getting drifted away from true SOC, due to the erros mentioned above. and it increases casue COLOUMB counting means integrating current. SO current with errors means the errors also gets integrated and hence it grows as time grows since we are integrating with respect to time.

## SOC vs Current (Scatter Plot)
This scatter plot compares true SOC (blue) and measured SOC from Coulomb counting (orange) against instantaneous battery current.
SOC depends on total charge used over time, not instantaneous current. Therefore the same current values appear at many SOC levels, forming vertical clusters.
Dense vertical cloud → normal robot operation near average motor load.
Sparse high-current points → random motor start spikes.
Blue dots → ideal battery discharge.
Orange dots → SOC estimated using noisy current measurements.
orange drifts apart form blue cause, Coulomb counting integrates current. Small errors such as:
sensor offset,timing uncertainty,noise, accumulate over time, causing measured SOC to slowly drift away from the true SOC. (integration)

## Coulomb Counting SOC Error Growth Over Time
This plot shows how SOC estimation error increases during discharge.
At the start, error is nearly zero because measured SOC equals true SOC.
Small measurement bias is continuously integrated, causing gradual drift. Noise averages out, but offset error dominates long-term behaviour.
Sudden increases occur due to simulated motor start current spikes, which introduce large short-term integration errors.
Coulomb counting works well short term but develops increasing error over long operation without correction methods.
