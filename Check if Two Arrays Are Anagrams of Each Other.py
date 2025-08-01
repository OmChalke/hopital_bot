str1= 'add'
str2='dad'
newstr1={}
newstr2={}

for i in str1:
    if i in newstr1:
        newstr1[i]+=1

    else:
        newstr1[i]=1

print(newstr1)

for i in str2:
    if i in newstr2:
        newstr2[i]+=1

    else:
        newstr2[i]=1

print(newstr2)

if newstr1 == newstr2:
    print ("it is an anagram")

else:
    print("not an anagram")



