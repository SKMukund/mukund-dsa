class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        l = 0
        r = 1
        max_size = 0

        if len(s) == 0:
            return 0
        if len(s) == 1:
            return 1

        seen = {s[0]}

        while r < len(s):
            if s[r] not in seen:
                seen.add(s[r])
                r += 1
            else:
                seen.remove(s[l])
                l += 1
            if max_size < (r - l):
                max_size = r - l
        return max_size
        