class Solution(object):
    def checkInclusion(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """
        l = 0
        r = 0
        perm = {}

        for ch in s1:
            if ch in perm:
                perm[ch] += 1
            else:
                perm[ch] = 1
                
        window_perm = {}
        size = 0
        while r < len(s2):
            if s2[r] in window_perm and window_perm[s2[r]] > 0:
                window_perm[s2[r]] += 1
                size += 1
            else:
                window_perm[s2[r]] = 1
            
            if (r-l+1) > len(s1):
                window_perm[s2[l]] -= 1
                if window_perm[s2[l]] == 0:
                    del window_perm[s2[l]]
                l += 1    

            
            if window_perm == perm:
                return True

            r += 1
        return False