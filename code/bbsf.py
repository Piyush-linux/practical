# practical1b_net_sigmoid.py
import math
n = int(input("Enter number of elements: "))
inputs = []
print("Enter the inputs (one per line):")
for _ in range(n):
    inputs.append(float(input()))
weights = []
print("Enter the weights (one per line):")
for _ in range(n):
    weights.append(float(input()))
# compute net (Yin)
yin = sum(i * w for i, w in zip(inputs, weights))
print("Yin (net input) =", round(yin, 6))
# binary sigmoid (0..1)
def binary_sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))
# bipolar sigmoid (-1..1)
def bipolar_sigmoid(x):
    return (2.0 / (1.0 + math.exp(-x))) - 1.0
print("Binary sigmoid output =", round(binary_sigmoid(yin), 6))
print("Bipolar sigmoid output =", round(bipolar_sigmoid(yin), 6))
