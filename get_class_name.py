class A:
    property = 1
    def __init__(self):
        A.property +=1
        assert A.property == self.__class__.property
        print("CLASS NAME?", self.__class__.__name__)
        self.__dict__.update({'someProperty':1})
        val = self.someProperty # type: ignore 
        print("VALUE?",val)

A()