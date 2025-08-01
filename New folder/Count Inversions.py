arr = [2, 3, -2, 4, 5, 3]
n=len(arr)
inver= 0
pairs=[]


for i in range(n):
    for j in range(i+1,n):
        if arr[i]>arr[j]:
            inver+=1
            pair=(i,j)
            pairs.append(pair)

print(inver)
print(pairs)