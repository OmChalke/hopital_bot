array=[1,2,3,4,2,9,8]
n=len(array)

newarr=[]

for i in range(1,(n-1)):
    if array[i]>array[i-1] and array[i]>array[i+1]:
        
        newarr.append(array[i])

print(newarr)
    