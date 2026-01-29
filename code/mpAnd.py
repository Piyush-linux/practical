# Implement AND-NOT (output 1 only if x1=1 and x2=0)
num_ip = int(input("Enter number of input pairs: "))

pairs = []
for i in range(num_ip):
    x1 = int(input(f"pair {i + 1} x1 = "))
    x2 = int(input(f"pair {i + 1} x2 = "))
    pairs.append((x1, x2))

# weights: w1 = +1 (excitatory), w2 = -1 (inhibitory), threshold theta = 1
w1, w2, theta = 1, -1, 1
Yin = [w1 * p[0] + w2 * p[1] for p in pairs]
print("Yin = ", Yin)
Y = [1 if y >= theta else 0 for y in Yin]
print("Y (AND-NOT outputs) =", Y)
