arr1 = [1, 3]
arr2 = [2, 3]

m = len(arr1)
n = len(arr2)

a = [0] * (m + n)
i = j = k = 0

while i < m and j < n:
    if arr1[i] < arr2[j]:

        a[k] = arr1[i]
        i += 1

    else:
        a[k] = arr2[j]
        j += 1
    k += 1


while i < m:
    a[k] = arr1[i]
    i += 1
    k += 1

while j < n:
    a[k] = arr2[j]
    j += 1
    k += 1


if (m + n) % 2 == 0:
    print((a[(m + n) // 2] + a[(m + n) // 2 - 1]) / 2)
    
else:

    print(a[(m + n) // 2])
