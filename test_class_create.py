
class new_class:
    def __init__(self,data, value):
        self.data = data
        self.value = value
        """
        hint of value
        """
        self.execute_init(2)
    def execute_init(self,val):
        self.val = val
        """
        some hint of val? will not be displayed
        """

a = new_class(4,5)
print('VAL', a.val)