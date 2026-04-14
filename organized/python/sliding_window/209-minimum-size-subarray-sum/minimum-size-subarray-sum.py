class Solution(object):
    def minSubArrayLen(self, target, nums):
        """
        :type target: int
        :type nums: List[int]
        :rtype: int
        """
        l = 0
        r = 0
        min_size = sys.maxsize
        window = 0


        while r < len(nums):
            window += nums[r]
            while window >= target:
                if (r - l + 1) < min_size:
                    min_size = r - l + 1
                window -= nums[l]
                l += 1
            r += 1
        if min_size > len(nums):
            return 0
        return min_size

        