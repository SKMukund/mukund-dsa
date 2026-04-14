class Solution(object):
    def findMaxAverage(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: float
        """
        l = 0
        r = k
        window_sum = 0
        max_sum = 0

        for i in range(k):
            window_sum += nums[i]

        max_sum = window_sum

        while r < len(nums):
            window_sum = window_sum - nums[l] + nums[r]
            if max_sum < window_sum:
                max_sum = window_sum
            l += 1
            r += 1
        return float(max_sum)/k

            
        