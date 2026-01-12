def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

num = int(input("Enter a number: "))
print("The factorial of", num, "is:", factorial(num))
import math

num = float(input("Enter a number: "))

sqrt_value = math.sqrt(num)
log_value = math.log(num)
sine_value = math.sin(num)

print("Square root of", num, "is:", sqrt_value)
print("Natural logarithm of", num, "is:", log_value)
print("Sine of", num, "is:", sine_value)


