# Program to find factorial

num = int(input("Enter a number: "))
fact = 1

if num < 0:
    print("Factorial not defined for negative numbers")
elif num == 0:
    print("Factorial = 1")
else:
    for i in range(1, num + 1):
        fact *= i
    print("Factorial =", fact)
