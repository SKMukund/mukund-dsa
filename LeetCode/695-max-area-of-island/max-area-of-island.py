class Solution(object):
    def maxAreaOfIsland(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        rows = len(grid)
        cols = len(grid[0])
        max_size = 0

        def dfs(r, c):
            size = 0
            if r < 0 or c < 0 or r >= rows or c >= cols:
                return 0 
            if grid[r][c] == 0:
                return 0

            size += 1
            grid[r][c] = 0 
            
            size += dfs(r + 1, c)
            size += dfs(r - 1, c)
            size += dfs(r, c + 1)
            size += dfs(r, c - 1)
            
            return size

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    max_size = max(dfs(r,c), max_size)
        
        return max_size