n = int(input("Enter number of elements: "))

print("Enter the inputs:")
inputs = []
for i in range(n):
    ele = float(input())
    inputs.append(ele)
print("Inputs:", inputs)

print("Enter the weights:")
weights = []
for i in range(n):
    ele = float(input())
    weights.append(ele)
print("Weights:", weights)

print("The net input can be calculated as: Yin = x1*w1 + x2*w2 + ... + xn*wn")

# Calculate Yin
Yin_list = []
for i in range(n):
    Yin_list.append(inputs[i] * weights[i])

print("Yin =", round(sum(Yin_list), 3))
