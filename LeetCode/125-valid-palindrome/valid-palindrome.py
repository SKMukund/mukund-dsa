class Solution(object):
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        new_s = s.lower()

        l = 0
        r = len(s) - 1

        while l < r:
            while l < r and not new_s[l].isalnum():
                l += 1
            while l < r and not new_s[r].isalnum():
                r -= 1
            if new_s[l] != new_s[r]:
                return False
            l += 1
            r -= 1
        return True

        

        