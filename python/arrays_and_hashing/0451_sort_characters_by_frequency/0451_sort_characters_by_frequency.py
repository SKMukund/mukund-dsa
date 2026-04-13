class Solution(object):
    def frequencySort(self, s):
        """
        :type s: str
        :rtype: str
        """
        seen = {}

        for char in s:
            if char in seen:
                seen[char] += 1
            else:
                seen[char] = 1
        
        bucket = [[] for _ in range(len(s) + 1)]

        for key, value in seen.items():
            bucket[value].append(key)

        answer = ""

        for i in range(len(bucket)-1, 0 , -1):
            for char in bucket[i]:
                answer += char * seen[char]
        
        return answer

        