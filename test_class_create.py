
class new_class(test_class):
    def __init__(self,data, value):
        self.data = data
        self.value = value
        self.execute_init(2)
    def execute_init(self,val):
        self.val = val
        """
        some hint of val?
        """

a = new_class(4,5)
print('VAL', a.val)