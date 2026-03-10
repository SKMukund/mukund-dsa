class Solution(object):
    def nextGreaterElement(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """

        stack = []
        seen = {}
        result = [-1] * (len(nums1))

        for num in nums1:
            if num in seen:
                seen[num] += 1
            else:
                seen[num] = 1

        for i in range(len(nums2)):
            while stack and nums2[i] > nums2[stack[-1]]:
                prev = stack.pop()
                for j in range(len(nums1)):
                    if nums1[j] == nums2[prev]:
                        result[j] = nums2[i]

            
            stack.append(i)
        

        return result

        