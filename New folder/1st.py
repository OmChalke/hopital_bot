num1 = int(input("enter no1: "))
#print("number1 is:", num1)

num2 = int(input("enter no2: "))
#print("number1 is:", num2)

print("Select: addition, multiplication, substraction, division")
opp= input("enter operation: ")

addition = num1+num2
multiplication = num1*num2
division = num1/num2
substracrtion = num1-num2

if opp == "addition":
    print("addition is: ", addition)

elif opp == "multiplication":
    print("multiplication is: ", multiplication)

elif opp == "division":
    print("division is: ", division)

elif opp == "substraction":
    print("substraction is: ", substracrtion)

else: print("Error")


