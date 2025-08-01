nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

max_current=nums[0]
max_total=nums[0]

for i in nums:
    max_current= max(i,max_current+i)
    
    if max_current>max_total:
        max_total=max_current

print("sum of contigous subarray is:", max_total)
