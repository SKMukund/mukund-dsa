class Solution(object):
    def eraseOverlapIntervals(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: int
        """
        intervals.sort(key=lambda x: x[1])
        prev_end = intervals[0][1]
        count = 0

        for i in range(1,len(intervals)):
            start = intervals[i][0]
            if start < prev_end:
                count += 1
            else:
                prev_end = max(prev_end, intervals[i][1])
        return count
        