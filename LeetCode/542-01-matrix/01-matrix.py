class Solution(object):
    def updateMatrix(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: List[List[int]]
        """
        
        row = len(mat)
        col = len(mat[0])
        q = deque()

        for r in range(row):
            for c in range(col):
                if mat[r][c] == 0:
                    q.append((r,c))
                else:
                    mat[r][c] = -1

        
        dirs = [[1,0],[-1,0],[0,1],[0,-1]]
        while q:
            r, c = q.popleft()

            for dr, dc in dirs:
                nr = r + dr
                nc = c + dc

                if 0 <= nr < row and 0 <= nc < col and mat[nr][nc] == -1:
                    q.append((nr, nc))
                    mat[nr][nc] = mat[r][c] + 1

        return mat




        
