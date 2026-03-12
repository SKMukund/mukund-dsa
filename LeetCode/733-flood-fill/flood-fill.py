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

        def dfs(r, c, og):
            if r < 0 or c < 0 or r >= rows or c >= cols:
                return
            if image[r][c] != og or image[r][c] == color:
                return

            image[r][c] = color

            dfs(r + 1,c, og)
            dfs(r - 1,c, og)
            dfs(r,c + 1, og)
            dfs(r,c - 1, og)
        
        dfs(sr, sc, image[sr][sc])
        return image
