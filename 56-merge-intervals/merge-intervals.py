class Solution(object):
    def merge(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[List[int]]
        """
        
        intervals.sort(key=lambda x: x[0])

        prev_start = intervals[0][0]
        prev_end = intervals[0][1]
        new_interval = []

        for i in range(1,len(intervals)):
            start, end = intervals[i]

            if start <= prev_end:
                prev_end = max(end, prev_end)
            else:
                new_interval.append([prev_start, prev_end])
                prev_start = start
                prev_end = end

        new_interval.append([prev_start, prev_end])
        return new_interval