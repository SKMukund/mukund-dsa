class Solution(object):
    def largestRectangleArea(self, heights):
        """
        :type heights: List[int]
        :rtype: int
        """
        stack = []
        max_size = 0
        smallest = sys.maxsize
        for i in range(len(heights)):  
            size = 0
            width = 0
            while stack and heights[i] < heights[stack[-1]]:
                prev = stack.pop()
                if not stack:
                    width = i
                else:
                    width = i - stack[-1] - 1
                height = heights[prev]
                size = height * width
                if size > max_size:
                    max_size = size
            stack.append(i)

        i = len(heights)
        while stack:
            prev = stack.pop()
            if not stack:
                width = i
            else:
                width = i - stack[-1] - 1
            height = heights[prev]
            size = height * width
            if size > max_size:
                max_size = size
        
        return max_size

        