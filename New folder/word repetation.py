new=input("enter sentence: ")

string=new.split()

wordcount={}

for word in string:
    if word in wordcount:
        wordcount[word] += 1
    
    else:
        wordcount[word] = 1

for word in wordcount:
    print(word, ":", wordcount[word])