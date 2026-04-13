class Solution(object):
    def mostCommonWord(self, paragraph, banned):
        """
        :type paragraph: str
        :type banned: List[str]
        :rtype: str
        """
        l = 0
        r = 0
        seen = {}
        highest = 0
        banned = set(banned)

        while r < len(paragraph):
            if paragraph[r].isalpha():
                r += 1
            else:
                word = paragraph[l:r].lower()
                if word and word not in banned:
                    if word in seen:
                        seen[word] += 1
                    else:
                        seen[word] = 1

                    if seen[word] > highest:
                        highest = seen[word]
                l = r + 1
                r += 1
        
        word = paragraph[l:r].lower()
        if word and word not in banned:
            if word in seen:
                seen[word] += 1
            else:
                seen[word] = 1

            if seen[word] > highest:
                highest = seen[word]
            

        key = next((k for k, v in seen.items() if v == highest), None)
        return key
        
        
        