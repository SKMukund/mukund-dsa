class Solution(object):
    def longestSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        l = 0
        r = 0
        max_size = 0
        zeros = 0

        while r < len(nums):
            if nums[r] == 0:
                zeros += 1
            
            while zeros > 1:
                if nums[l] == 0:
                    zeros -= 1
                l += 1
            if r - l > max_size:
                max_size = r - l
            r += 1
        return max_size