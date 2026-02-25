class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        l = 0
        r = len(height) - 1 
            
        max_volume = 0
        while l < r:
            width = r - l
            if height[l] > height[r]:
                volume = width * height[r]
            else:
                volume = width * height[l]

            if volume > max_volume:
                max_volume = volume
            elif height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return max_volume
            


        