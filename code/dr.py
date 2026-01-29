# practical3b_delta.py
import numpy as np

np.set_printoptions(precision=2)
x = np.zeros(3)
weights = np.zeros(3)
desired = np.zeros(3)
actual = np.zeros(3)

for i in range(3):
    x[i] = float(input(f"Initial input x[{i}]: "))
for i in range(3):
    weights[i] = float(input(f"Initial weight w[{i}]: "))
for i in range(3):
    desired[i] = float(input(f"Desired output d[{i}]: "))

alpha = float(input("Enter learning rate: "))

actual = x * weights
print("initial actual:", actual)
print("desired:", desired)

# iterative update until actual == desired (careful: floats; we'll use tolerance)
max_iters = 10000
tol = 1e-6
for epoch in range(max_iters):
    if np.allclose(actual, desired, atol=1e-6):
        break
    for i in range(3):
        weights[i] = weights[i] + alpha * (desired[i] - actual[i])
    actual = x * weights

print("*" * 30)
print("Final output")
print("Corrected weights", weights)
print("actual", actual)
print("desired", desired)
