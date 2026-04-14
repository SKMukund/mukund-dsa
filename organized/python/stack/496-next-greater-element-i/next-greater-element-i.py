class Solution(object):
    def nextGreaterElement(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """

        stack = []
        seen = {}
        result = []

        for i in range(len(nums2)):
            while stack and nums2[i] > nums2[stack[-1]]:
                prev = stack.pop()
                seen[nums2[prev]] = nums2[i]

            stack.append(i)
        
        for i in range(len(stack)):
            seen[nums2[stack[i]]] = -1

        for num in nums1:
            result.append(seen[num])

        return result

        