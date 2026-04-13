class Solution(object):
    def rob(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if len(nums) == 1:
            return nums[0]

        def rob_line(houses):

            n = len(houses)

            dp = [0] * (n + 1)

            dp[0] = 0
            dp[1] = houses[0]

            for i in range(2, n + 1):
                dp[i] = max(dp[i-1], dp[i-2] + houses[i-1])
            
            return dp[n]
        

        return max(rob_line(nums[:-1]), rob_line(nums[1:]))

        