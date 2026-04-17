class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """

        def expand(l, r):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return s[l+1:r]
        
        result = ""
        for i in range(len(s)):
            p1 = expand(i,i)
            p2 = expand(i,i+1)

            if len(p1) > len(result):
                result = p1
            if len(p2) > len(result):
                result = p2
        
        return result