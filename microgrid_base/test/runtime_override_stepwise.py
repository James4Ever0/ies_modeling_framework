class MyClass:
    def myfunc(self):
        print('abc')
        print('def')
        assert False, "you cannot pass"
        print("hjk")

c = MyClass()

def overwrite_func(func):
    # get definition and return a new func.
    return new_func

c.myfunc()