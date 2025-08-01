string= 'daddad'
n=len(string)

palindrome= True

for i in range(n//2):
    if string[i]!=string[n-1-i]:
        palindrome= False
        

if palindrome :
    print("it is palindrome")
else:
    print("not palindrome")



        