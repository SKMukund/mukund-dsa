class Solution(object):
    def findMinArrowShots(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """
        points.sort(key=lambda x: x[1])
        prev_end = points[0][1]
        count = 1
        
        for i in range(1, len(points)):
            start, end = points[i]

            if start > prev_end:
                count += 1
                prev_end = end
        
        return count
        