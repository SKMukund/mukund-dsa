class Solution(object):
    def maximumGap(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if len(nums) < 2:
            return 0

        sorted_nums = sorted(nums)
        difference = []
        for i in range(len(sorted_nums)-1, 0, -1):
            if i > 0:
                difference.append(sorted_nums[i] - sorted_nums[i-1])
        
        return max(difference)
 


        