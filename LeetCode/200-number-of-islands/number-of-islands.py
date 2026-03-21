class Solution(object):
    def numIslands(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: int
        """
        row = len(grid)
        col = len(grid[0])
        islands = 0

        def bfs(r, c):
            if r < 0 or c < 0 or r >= row or c >= col:
                return
            if grid[r][c] == '0':
                return
            
            grid[r][c] = '0'

            bfs(r + 1, c)
            bfs(r - 1, c)
            bfs(r, c + 1)
            bfs(r, c - 1)
        
        for r in range(row):
            for c in range(col):
                if grid[r][c] == '1':
                    bfs(r, c)
                    islands += 1
        return islands