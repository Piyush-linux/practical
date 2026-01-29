# practical2b_xor_fixed.py
import numpy as np


def read_int(prompt, default):
    s = input(f"{prompt} [{default}]: ")
    return int(s) if s.strip() else default


print("Enter integer weights (press Enter to use recommended defaults).")
print("Network architecture: two hidden neurons (y1,y2) -> one output y.")
print("Recommended defaults implement XOR using MP-style thresholds.")

# Hidden neuron 1 (AND): weights w11 (x1->y1), w21 (x2->y1), threshold theta_h1 = 2
w11 = read_int("w11 (x1 -> y1, AND)", 1)
w21 = read_int("w21 (x2 -> y1, AND)", 1)
theta_h1 = read_int("theta_h1 (threshold for y1)", 2)

# Hidden neuron 2 (OR): weights w12 (x1->y2), w22 (x2->y2), threshold theta_h2 = 1
w12 = read_int("w12 (x1 -> y2, OR)", 1)
w22 = read_int("w22 (x2 -> y2, OR)", 1)
theta_h2 = read_int("theta_h2 (threshold for y2)", 1)

# Output neuron: v1 (from y1), v2 (from y2), threshold theta_out = 1
v1 = read_int("v1 (y1 -> out) (recommended: -2)", -2)
v2 = read_int("v2 (y2 -> out) (recommended: 1)", 1)
theta_out = read_int("theta_out (output threshold)", 1)

# Inputs and XOR target
x1 = np.array([0, 0, 1, 1])
x2 = np.array([0, 1, 0, 1])
target = np.array([0, 1, 1, 0])

# Compute pre-activations
zin1 = x1 * w11 + x2 * w21
zin2 = x1 * w12 + x2 * w22

# Hidden outputs (threshold)
y1 = (zin1 >= theta_h1).astype(int)
y2 = (zin2 >= theta_h2).astype(int)

# Output neuron
yin = y1 * v1 + y2 * v2
y = (yin >= theta_out).astype(int)

print()
print("Inputs (x1,x2):", list(zip(x1, x2)))
print("Hidden pre-activations zin1 (AND):", zin1)
print("Hidden outputs y1 (AND):", y1)
print("Hidden pre-activations zin2 (OR):", zin2)
print("Hidden outputs y2 (OR):", y2)
print("Output pre-activation yin:", yin)
print("y", y, " target", target)

if np.array_equal(y, target):
    print("Success: network outputs XOR")
else:
    print(
        "Net is not producing XOR with these weights/thresholds. Try different integers."
    )
