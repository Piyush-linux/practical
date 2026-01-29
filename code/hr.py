import numpy as np

# patterns from the PDF
x1 = np.array([1, 1, 1, -1, 1, -1, 1, 1, 1])
x2 = np.array([1, 1, 1, 1, -1, 1, 1, 1, 1])
targets = np.array([1, -1])  # y = [1, -1]
wt = np.zeros(9, dtype=int)
bias = 0
print("First input with target = 1")
wt = wt + x1 * targets[0]
bias += targets[0]
print("new wt =", wt)
print("Bias value", bias)
print("Second input with target = -1")
wt = wt + x2 * targets[1]
bias += targets[1]
print("new wt =", wt)
print("Bias value", bias)
