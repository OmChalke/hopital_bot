str= 'abc'
s=list(str)
n=len(str)
permutation=[]


for i in range(n):
    for j in range(n):
        for k in range(n):
            if i!=j and j!=k and k!=i:
                new=s[i]+ s[j]+ s[k]
                permutation.append(new)

print(permutation)