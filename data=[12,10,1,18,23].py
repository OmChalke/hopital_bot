data = [12, 10, 1, 18, 23]
sortedlist = []
max_num = data[0]
while data:
    max_num = data[0]
    for i in data:
        if i < max_num:
            max_num = i

    sortedlist.append(max_num)
    data.remove(max_num)


print("final sorted list:", sortedlist)
