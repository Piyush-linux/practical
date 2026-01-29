# Practical 8A: Membership without using 'in'

# Function to check overlapping without using 'in'
def overlapping(list1, list2):
    c = len(list1)
    d = len(list2)

    for i in range(c):
        for j in range(d):
            if list1[i] == list2[j]:
                return 1  # Overlap found
    return 0  # No overlap


list1 = [1, 2, 3, 4, 5]
list2 = [6, 7, 8, 9]

if overlapping(list1, list2):
    print("overlapping")
else:
    print("not overlapping")
