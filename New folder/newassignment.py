array=[2,-4,3,5,1,10]
n=len(array)
target=6
newarray=[]
pairs=[]

# Correct sorting logic
for j in range(n):
    minnum = array[0]
    for i in array:
        if i < minnum:
            minnum = i
    newarray.append(minnum)
    array.remove(minnum)

print(newarray)

# Now newarray has n elements properly
for i in range(n):
    for j in range(i + 1, n):
        if newarray[i] + newarray[j] == target:
            pairs.append((newarray[i], newarray[j]))

print(pairs)

   