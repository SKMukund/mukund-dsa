class Solution(object):
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """

        l = 0
        r = x

        while l <= r:
            mid = l + (r - l)//2
            if mid*mid <= x:
                l = mid + 1
            else:
                r = mid - 1
        return r