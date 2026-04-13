class Solution(object):
    def longestOnes(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        l = 0 
        r = 0
        max_size = 0
        window_size = 0

        while r < len(nums):
            if nums[r] == 0:
                k -= 1
            while k < 0:
                if nums[l] == 0:
                    k += 1
                l += 1
            if max_size < (r - l + 1):
                max_size = r - l + 1
            r += 1
        return max_size
         
        