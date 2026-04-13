class Solution(object):
    def largestRectangleArea(self, heights):
        """
        :type heights: List[int]
        :rtype: int
        """
        if len(heights) == 1:
            return heights[0]

        stack = []
        max_size = 0
        
        for i in range(len(heights)):
            height = heights[i]
            width = 0
            while stack and height <= heights[stack[-1]]:
                prev = stack.pop()
                if not stack:
                    width = i   
                else:
                    width = i - stack[-1] - 1 
                
                size = heights[prev] * width

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
            size = heights[prev] * width
            if size > max_size:
                max_size = size
        return max_size
                    
                
                
            
            
        