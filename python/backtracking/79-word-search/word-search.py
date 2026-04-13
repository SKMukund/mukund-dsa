class Solution(object):
    def exist(self, board, word):
        """
        :type board: List[List[str]]
        :type word: str
        :rtype: bool
        """

        row = len(board)
        col = len(board[0])

        def dfs(r, c, i):
            if i == len(word):
                return True

            if r < 0 or c < 0 or r >= row or c >= col:
                return False

            if board[r][c] != word[i]:
                return False
            
            temp = board[r][c]
            board[r][c] = "#"
            
            if dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1):
                return True

            board[r][c] = temp
            return False
                    
        for r in range(row):
            for c in range(col):
                if board[r][c] == word[0]:
                    if dfs(r, c, 0):
                        return True
        return False

            
        