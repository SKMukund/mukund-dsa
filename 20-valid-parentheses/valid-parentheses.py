class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        
        stack = []

        for i in range(len(s)):
            if s[i] in "({[":
                stack.append(s[i])
            else:
                if not stack:
                    return False
                
                top = stack[-1]
                bot = s[i]

                if top == "(" and bot == ")":
                    stack.pop()

                elif top == "{" and bot == "}":
                    stack.pop()
                
                elif top == "[" and bot == "]":
                    stack.pop()
                
                else:
                    return False
        
        return len(stack) == 0