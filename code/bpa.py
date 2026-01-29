# practical4a_backprop.py
import math

import numpy as np

v1 = np.array([0.6, 0.3])
v2 = np.array([-0.1, 0.4])
w = np.array([-0.2, 0.4, 0.1])  # w[0] is bias term for output in the PDF code
b1 = 0.3
b2 = 0.5
x1 = 0.0
x2 = 1.0
alpha = 0.25

# forward pass (hidden)
zin1 = round(b1 + x1 * v1[0] + x2 * v2[0], 4)
zin2 = round(b2 + x1 * v1[1] + x2 * v2[1], 4)
z1 = 1.0 / (1.0 + math.exp(-zin1))
z2 = 1.0 / (1.0 + math.exp(-zin2))
yin = w[0] + z1 * w[1] + z2 * w[2]
y = 1.0 / (1.0 + math.exp(-yin))

# compute deltas and updates (as in PDF)
fyin = y * (1 - y)
dk = (1 - y) * fyin  # note: PDF used (1-y) as desired-y? We follow text
dw1 = alpha * dk * z1
dw2 = alpha * dk * z2
dw0 = alpha * dk

din1 = dk * w[1]
din2 = dk * w[2]

fzin1 = z1 * (1 - z1)
fzin2 = z2 * (1 - z2)
d1 = din1 * fzin1
d2 = din2 * fzin2

dv11 = alpha * d1 * x1
dv21 = alpha * d1 * x2
dv01 = alpha * d1
dv12 = alpha * d2 * x1
dv22 = alpha * d2 * x2
dv02 = alpha * d2

# update weights
v1[0] += dv11
v1[1] += dv12
v2[0] += dv21
v2[1] += dv22
w[1] += dw1
w[2] += dw2
b1 += dv01
b2 += dv02
w[0] += dw0

print("Updated v1:", v1)
print("Updated v2:", v2)
print("Updated w:", w)
print("Updated biases b1, b2:", b1, b2)
