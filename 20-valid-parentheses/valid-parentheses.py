class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """

        stack = []

        for i in range(len(s)):
            if s[i] in "([{":
                stack.append(s[i])
            else:
                if not stack:
                    return False

                if stack[-1] == "(" and s[i] == ")":
                    stack.pop()

                elif stack[-1] == "{" and s[i] == "}":
                    stack.pop()

                elif stack[-1] == "[" and s[i] == "]":
                    stack.pop()
                
                else:
                    return False
        
        return len(stack) == 0