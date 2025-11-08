students = {
    "Ravi": 85,
    "Neha": 92,
    "Amit": 78,
    "Priya": 88,
    "Rajat": 95
}

name = input("Enter the student's name: ")

if name in students:
    print(f"{name}'s marks are: {students[name]}")
else:
    print("Student not found in the record.")
numbers = list(range(1, 11))

first_five = numbers[:5]
reversed_list = first_five[::-1]

print("First five elements:", first_five)
print("Reversed list:", reversed_list)
