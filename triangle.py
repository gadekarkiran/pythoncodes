import math

a = float(input("Enter the rectangle side a : "))
b = float(input("Enter the rectangle side b : "))
c = float(input("Enter the rectangle side c : "))

# Semi-perimeter
s = (a + b + c) / 2

# Area calculation
area = math.sqrt(s * (s - a) * (s - b) * (s - c))

print("Area of the triangle is:", area)