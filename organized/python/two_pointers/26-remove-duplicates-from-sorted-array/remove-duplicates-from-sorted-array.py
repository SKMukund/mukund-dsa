class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        l = 0
        r = 1
        count = 0
        while r < len(nums):
            while nums[l] != nums[r]:
                l += 1
                nums[l] = nums[r]
            r += 1
        return l + 1


        