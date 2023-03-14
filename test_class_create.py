class test_class:
    data:int
    value:str

class new_class(test_class):
    def __init__(self,data, value):
        self.data = data
        self.value = value