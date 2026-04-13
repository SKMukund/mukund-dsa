class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        sorted_nums = sorted(nums)
        answers = []
        for i in range(len(sorted_nums)):
            if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
                continue

            x = i + 1
            y = len(sorted_nums) - 1
            while x < y:
                total = sorted_nums[x] + sorted_nums[y] + sorted_nums[i]
                
                
                if total == 0:
                    answers.append([sorted_nums[i],sorted_nums[x],sorted_nums[y]])
                    y -= 1
                    x += 1
                    while x < y and sorted_nums[x] == sorted_nums[x - 1]:
                        x += 1
                    while x < y and sorted_nums[y] == sorted_nums[y + 1]:
                        y -= 1

                elif total < 0:
                    x += 1
                else:
                    y -= 1
    
        return answers

            
