class Solution(object):
    def nextGreaterElement(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        stack = []
        result = []
        next_map = {}
        for num in nums2:
            while stack and num > stack[-1]:
                prev = stack.pop()
                next_map[prev] = num
            stack.append(num)
        
        while stack:
            next_map[stack.pop()] = -1

        for num in nums1:
            result.append(next_map[num])
        
        return result
    


        