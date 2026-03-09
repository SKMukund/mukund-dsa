class Solution(object):
    def totalFruit(self, fruits):
        """
        :type fruits: List[int]
        :rtype: int
        """
        l = 0
        r = 0
        max_size = 0
        seen = {}

        while r < len(fruits):
            if fruits[r] in seen:
                seen[fruits[r]] += 1
            else:
                seen[fruits[r]] = 1

            current = fruits[l]
            if len(seen) > 2:
                while fruits[l] in seen and fruits[l] == current:
                    seen[fruits[l]] -= 1
                    if seen[fruits[l]] == 0:
                        del seen[fruits[l]]
                    l += 1
            if (r - l + 1) > max_size:
                max_size = (r - l + 1)
            r += 1
        return max_size


        