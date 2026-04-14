class Solution(object):
    def evalRPN(self, tokens):
        """
        :type tokens: List[str]
        :rtype: int
        """
        answer = 0
        stack = []
        for value in tokens:
            if value == '+':
                b = int(stack.pop())
                a = int(stack.pop())
                stack.append(a + b)
            elif value == '-':
                b = int(stack.pop())
                a = int(stack.pop())
                stack.append(a - b)
            elif value == '*':
                b = int(stack.pop())
                a = int(stack.pop())
                stack.append(a * b)
            elif value == '/':
                b = int(stack.pop())
                a = int(stack.pop())
                stack.append(int(float(a) / b))
            else:
                stack.append(int(value))
        return stack[0]

        