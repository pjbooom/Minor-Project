## SOC vs Time
The true SOC decreases steadily due to constant discharge current.
The estimated SOC deviates because voltage-based estimation is affected by internal resistance drop.
The difference between true and estimated SOC increases mainly in the mid-SOC region where voltage sensitivity is low.

## SOC Error vs Time
The SOC estimation error increases during discharge because the measured voltage remains consistently lower than the open circuit voltage due to internal resistance.
In the mid-SOC region, small voltage variations correspond to large SOC changes, causing rapid error growth.
The error reduces near low SOC where voltage becomes more sensitive to SOC variations.

## Voltage vs Time
The open circuit voltage decreases gradually as the battery discharges.
The terminal voltage remains lower than OCV because of the constant internal resistance drop caused by load current.
This demonstrates how load conditions affect voltage-based SOC estimation.

## SOC vs Voltage Curve
The SOC–Voltage relationship is nonlinear, with a relatively flat region in the middle SOC range.
In this region, large SOC changes produce very small voltage variations.
This limits the reliability of voltage-based SOC estimation under practical operating conditions.
