arr= [2, 3, -2, 4,5,3]

maxp=arr[0]
minp=arr[0]
output=arr[0]

for i in arr:
    if 0>i:
        maxp,minp=minp,maxp

    maxp= max(i,maxp*i)
    minp= min(i,minp*i)

output=max(output,maxp)

print(output)
    