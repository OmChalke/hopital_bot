s1= 'abcd'
s2= 'cdab'


n1=len(s1)
n2=len(s2)

if n1 != n2:
    print("error")

rotatedstring= s1+s1


if s2 in rotatedstring:
    print("s2 is the rotation of s1")