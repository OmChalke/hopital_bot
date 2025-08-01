list = ['som','om', 'om', 'om', 'som', 'som','om']

candidate = None
count = 0

for i in list:
    if count == 0:
        candidate = i


    if i == candidate:
        count= count + 1

    else:
        count= count - 1

print(candidate)
