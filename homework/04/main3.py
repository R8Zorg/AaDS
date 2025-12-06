def two_sum(array, target):
    seen_nums = {}
    for index, value in enumerate(array):
        num = target - value
        if num in seen_nums:
            return (seen_nums[num], index)
        seen_nums[value] = index


target = 14
nums = [1, 2, 4, 15, 7, 52, 26, 17, 5, 2, 7]
print(two_sum(nums, target))
