class Solution(object):
    def coinChange(self, coins, amount):
        """
        :type coins: List[int]
        :type amount: int
        :rtype: int
        """
        dp = [amount + 1] * (amount + 1)

        dp[0] = 0

        for i in range(1, amount + 1):
            for coin in coins:
                remaining = i - coin
                if remaining >= 0:
                    dp[i] = min(dp[i], dp[remaining] + 1)

        if dp[amount] > amount:
            return -1
        return dp[amount]