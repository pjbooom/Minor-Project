## SOC vs Time graph
This graph compares the true battery State of Charge (SOC) with the SOC estimated using only terminal voltage measurement. The estimation error increases under load because voltage is affected by internal resistance and polarization effects. It demonstrates the limitation of voltage-only SOC estimation during continuous discharge.

## SOC Error vs Time Graph
This graph shows the absolute SOC estimation error over time. Error increases due to voltage drops caused by internal resistance and dynamic polarization voltage (Vrc), which shift terminal voltage away from the true OCV-SOC relationship. It highlights why voltage-based SOC estimation becomes unreliable under load conditions.

## Voltage vs Time (Terminal Voltage vs OCV)
This graph compares the battery open circuit voltage (OCV) with the measured terminal voltage during discharge. The terminal voltage remains lower due to internal resistance and polarization losses. The difference between these voltages explains the SOC estimation error in voltage-based methods.

## SOC vs Voltage Curve (OCV Curve)
This graph represents the OCV–SOC lookup table used for interpolation during SOC estimation. It shows the nonlinear relationship between battery voltage and SOC, including the relatively flat mid-region where voltage changes minimally. This flat region makes voltage-only SOC estimation sensitive to small measurement errors.

## Polarization Voltage (Vrc) vs Time 
This graph shows the evolution of polarization voltage caused by electrochemical dynamics inside the battery. Vrc increases during sustained current draw and introduces additional voltage drop beyond internal resistance. It models transient battery behavior using an RC network equivalent circuit.
