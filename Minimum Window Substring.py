arr = [2, 3, -2, 4, 5, 3]

maxp = arr[0]
minp = arr[0]
output = arr[0]

for i in arr:
    if i < 0:
        maxp, minp = minp, maxp

    maxp = max(i, maxp * i)
    minp = min(i, minp * i)

output = max(output, maxp)  # outside the loop, only compares initial output (2) and final maxp (60 after loop)

print(output)  # Output: 60 (still 60, not 2)