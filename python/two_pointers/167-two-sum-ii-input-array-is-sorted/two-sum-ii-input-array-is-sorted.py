class Solution(object):
    def twoSum(self, numbers, target):
        """
        :type numbers: List[int]
        :type target: int
        :rtype: List[int]
        """
        l = 0
        r = len(numbers) - 1
        sol = []
        
        while l < r:
            temp = numbers[l] + numbers[r]
            if temp < target:
                l += 1
            elif temp > target:
                r -= 1
            else:
                sol.append(l + 1)
                sol.append(r + 1)
                return sol