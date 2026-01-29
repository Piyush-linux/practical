# practical4b_ebpa.py
import math

a0 = -1.0
t = -1.0
w10 = float(input("Enter weight first network (w10): "))
b10 = float(input("Enter base first network (b10): "))
w20 = float(input("Enter weight second network (w20): "))
b20 = float(input("Enter base second network (b20): "))
c = float(input("Enter learning coefficient (c): "))

n1 = float(w10 * c + b10)
a1 = math.tanh(n1)
n2 = float(w20 * a1 + b20)
a2 = math.tanh(n2)

e = t - a2
s2 = -2 * (1 - a2 * a2) * e
s1 = (1 - a1 * a1) * w20 * s2

w21 = w20 - (c * s2 * a1)
w11 = w10 - (c * s1 * a0)
b21 = b20 - (c * s2)
b11 = b10 - (c * s1)

print("The updated weight of first n/w w11=", w11)
print("The updated weight of second n/w w21=", w21)
print("The updated base of first n/w b11=", b11)
print("The updated base of second n/w b21=", b21)
