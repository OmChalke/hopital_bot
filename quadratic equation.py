import math
a=int(input('enter a = '))
b=int(input('enter b = '))
c=int(input('enter c = '))

root1 = (-b + math.sqrt(b**2 - 4*a*c))/2*a
root2 = (-b - math.sqrt(b**2 - 4*a*c))/2*a

print('roots of the equation are : root 1 = ',root1,root2)



