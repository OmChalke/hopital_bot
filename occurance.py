string= input("enter a string : ")
count=input("enter a letter you want to search: ")
wcount=input("enter word: ")
repeat=0
wrepeat=0
for letter in string:
    if letter== count:
        repeat += 1

for word in string:
    if word == wcount:
        wrepeat+= 1


print("letter is repeated: " ,repeat)
print("word is repeated: " ,wrepeat)