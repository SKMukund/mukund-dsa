class Solution(object):
    def backspaceCompare(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        stack_s = []
        stack_t = []
        for c in s:
            if c == "#" and stack_s:
                stack_s.pop()
            elif c != "#":
                stack_s.append(c)

        for c in t:
            if c == "#" and stack_t:
                stack_t.pop()
            elif c != "#":
                stack_t.append(c)

        return True if stack_s == stack_t else False
        