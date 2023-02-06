sides = [1, 4, 3]
a = sides[0]
b = sides[1]
c = sides[-1]
D = ((b*b) - (4*a*c))
if D >= 0:
    x1 = ((-b + D ** (1/2)) / (2*a))
    x2 = ((-b - D ** (1/2)) / (2*a))
print(x1, x2)
