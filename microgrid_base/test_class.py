class A:
    def __init__(self):
        ...
    
    def B(self):
        return B(self)

class B:
    def __init__(self, a:A):
        self.a = a
        print("CLASS NAME?", self.__class__.__name__)
        print("CREATING B")

a = A()
b = a.B()
