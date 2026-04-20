class Solution(object):
    def lemonadeChange(self, bills):
        """
        :type bills: List[int]
        :rtype: bool
        """
        five = 0
        ten = 0
        for bill in bills:
            if bill == 5:
                five += 1
            elif bill == 10 and five > 0:
                five -= 1
                ten += 1
            elif bill == 20 and five > 0 and ten > 0:
                five -= 1
                ten -= 1
            elif bill == 20 and five >= 3:
                five -= 3
            else:
                return False

        return True
        
        
        