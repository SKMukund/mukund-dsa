class Solution(object):
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        l = 0
        r = len(nums) - 1

        if target > nums[r]:
            return len(nums)
        
        while l < r:
            mid = l + (r - l) // 2   
            if nums[mid] < target:
                l = mid + 1
            else:
                r = mid
        
        return l