class MyClass:
    def myfunc(self):
        print("abc")
        print("def")
        assert False, "you cannot pass"
        print("hjk")


c = MyClass()

import inspect
import ast
import re

def overwrite_func(func):
    # get definition and return a new func.
    # test: add "yield" after every line.
    func_source = inspect.getsource(func)
    print("SOURCE CODE".center(70, "="))
    print(func_source)
    print()
    # return new_func
    func_ast = ast.parse(func_source)
    find_def = r"^(\_+)def"
    FDRegex = re.compile(find_def, flags=re.MULTILINE)
    strip_blanks = FDRegex.findall(func_source)[0]
    blank_count = len(strip_blanks)
    indent_replace = r"^\_"+("{%d}" % blank_count)
    IRRegex = 
    print(func_ast) # unexpected indent.


# c.myfunc()

new_func = overwrite_func(c.myfunc)
c.myfunc = new_func
