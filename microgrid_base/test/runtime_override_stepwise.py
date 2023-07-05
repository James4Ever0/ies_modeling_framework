class MyClass:
    def myfunc(self):
        print("abc")
        print("def")
        assert False, "you cannot pass"
        print("hjk")


c = MyClass()

import inspect
import ast

def overwrite_func(func):
    # get definition and return a new func.
    # test: add "yield" after every line.
    func_source = inspect.getsource(func)
    print("SOURCE CODE".center(70, "="))
    print(func_source)
    print()
    # return new_func
    func_ast = ast.parse(func_source)
    print(func_ast) # unexpected indent.


# c.myfunc()

new_func = overwrite_func(c.myfunc)
c.myfunc = new_func
