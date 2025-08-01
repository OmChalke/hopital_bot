string= "prathamesh"
list= list(string)
reverse_list=[]
n= len(list)


for i in range(n-1,-1,-1):
    reverse_list.append(list[i])

nstring=  ''.join(reverse_list)


print (nstring)

