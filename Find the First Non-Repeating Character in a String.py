string='howareyouom'
frequency={}

newfreq={}

for i in string:
    if i in frequency:
        frequency[i] +=1
    
    else:
        frequency[i]=1

print(frequency)

for i in string:

    if i in frequency:
        frequency[i]==1
        newfreq[i]=frequency[i]
        break

print(newfreq)

        
