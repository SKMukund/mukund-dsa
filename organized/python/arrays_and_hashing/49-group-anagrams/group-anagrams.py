class Solution(object):
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """


        seen = {}
        for i in range(len(strs)):
            current = {}
            for char in strs[i]:
                if char in current:
                    current[char] += 1
                else:
                    current[char] = 1
            key = tuple(sorted(current.items()))
            
            if key not in seen:
                seen[key] = [strs[i]]
            else:
                seen[key].append(strs[i])

        return list(seen.values())

        