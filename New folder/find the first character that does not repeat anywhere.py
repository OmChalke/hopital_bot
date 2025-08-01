string= [1,-2,0,3,4,-5,0]
new=0
newstr=[]
newstring=[]


for i in string:
    if i == 0:
        new += 1

for i in string:
    if i != 0:
        newstr.append(i)

n=len(newstr)

for i in range(new):
    newstr.append(0)

print(newstr)

