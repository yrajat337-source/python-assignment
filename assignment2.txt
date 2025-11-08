num = int(input("Enter an integer: "))
if num % 2 == 0:
    print(f"{num} is an even number.")
else:
    print(f"{num} is an odd number.")
total = 0
for i in range(1, 51):
    total += i
print("The sum of numbers from 1 to 50 is:", total)

