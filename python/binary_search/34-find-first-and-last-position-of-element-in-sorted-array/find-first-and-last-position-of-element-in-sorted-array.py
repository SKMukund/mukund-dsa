class Solution(object):
    def searchRange(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        l = 0
        r = len(nums) - 1
        results = [-1] * 2
        count = 0

        if r == 0 and nums[l] == target:
            return [0,0]


        while l < r:
            mid = l + (r - l)//2
            if nums[mid] < target:
                l = mid + 1
            else:
                r = mid

        left = l

        if l >= len(nums) or nums[l] != target:
            return [-1,-1]
        
        r = len(nums) - 1

        while l < r:
            mid = l + (r - l + 1)//2
            if nums[mid] > target:
                r = mid - 1
            else:
                l = mid 

        return [left,r]
        