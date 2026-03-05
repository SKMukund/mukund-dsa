class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        l = 0
        r = 1
        max_profit = 0

        while r < len(prices):
            profit = prices[r] - prices[l]
            if profit > max_profit:
                max_profit = profit
            if prices[r] < prices[l]:
                l = r
            r += 1
        return max_profit
            

        