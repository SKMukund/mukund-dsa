import heapq
class Solution(object):
    def minMeetingRooms(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: int
        """
        if not intervals:
            return 0
        
        intervals.sort(key=lambda x: x[0])
        heap = []
        count = 0
        prev_end = intervals[0][1]

        for start, end in intervals:
            if heap and start >= heap[0]:
                heapq.heappop(heap)

            heapq.heappush(heap, end)
        
        return len(heap)
            

        