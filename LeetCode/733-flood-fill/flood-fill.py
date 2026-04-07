class Solution(object):
    def floodFill(self, image, sr, sc, color):
        """
        :type image: List[List[int]]
        :type sr: int
        :type sc: int
        :type color: int
        :rtype: List[List[int]]
        """
        
        rows = len(image)
        cols = len(image[0])
        start = image[sr][sc]

        if start == color:
            return image

        q = deque([(sr, sc)])
        dirs = [[1,0],[-1,0],[0,1],[0,-1]]

        while q:
            r, c = q.popleft()
            image[r][c] = color

            for dr, dc in dirs:
                nr = r + dr
                nc = c + dc

                if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == start:
                    q.append((nr,nc))

        return image
        

        