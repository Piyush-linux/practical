# practical9b_tipping.py
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

quality = ctrl.Antecedent(np.arange(0, 11, 1), "quality")
service = ctrl.Antecedent(np.arange(0, 11, 1), "service")
tip = ctrl.Consequent(np.arange(0, 26, 1), "tip")

quality.automf(3)
service.automf(3)

tip["low"] = fuzz.trimf(tip.universe, [0, 0, 13])
tip["medium"] = fuzz.trimf(tip.universe, [0, 13, 25])
tip["high"] = fuzz.trimf(tip.universe, [13, 25, 25])

rule1 = ctrl.Rule(quality["poor"] | service["poor"], tip["low"])
rule2 = ctrl.Rule(service["average"], tip["medium"])
rule3 = ctrl.Rule(service["good"] | quality["good"], tip["high"])

tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

tipping.input["quality"] = 6.5
tipping.input["service"] = 9.8
tipping.compute()
print("Suggested tip:", tipping.output["tip"])

"""
Fuzzy Control Systems: The Tipping Problem
The 'tipping problem' is commonly used to illustrate the power of fuzzy logic
principles to generate complex behavior from a compact, intuitive set of
expert rules.
If you're new to the world of fuzzy control systems, you might want
to check out the 'Fuzzy Control Primer
<./userguide/fuzzy_control_primer.html>
before reading through this worked example.
The Tipping Problem
We would formulate this problem as:
* Antecednets (Inputs)
- service'
* Universe (ic, crisp value range): How good was the service of the wait
staff, on a scale of 0 to 10?
* Fuzzy set (ie, fuzzy value range): poor, acceptable, amazing
- 'food quality'
* Universe: How tasty was the food, on a scale of 0 to 10?
* Fuzzy set: bad, decent, great
* Consequents (Outputs)
- "tip'
* Universe: How much should we tip, on a scale of 0% to 25%
* Fuzzy set: low, medium, high
* Rules
- IF the *service* was good *or* the *food quality* was good,
THEN the tip will be high.
- IF the *service* was average, THEN the tip will be medium.
- IF the *service* was poor *and* the *food quality* was poor
THEN the tip will be low.
* Usage
- If I tell this controller that I rated:
* the service as 9.8, and
* the quality as 6.5,
- it would recommend I leave:
* a 20.2% tip.
"""
