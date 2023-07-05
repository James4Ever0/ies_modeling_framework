def dec(f): return f
class MyClass:
    @dec
    def myfunc(self):
        print("abc")
        print("def")
        # mycomment
        assert False, "you cannot pass"
        print("hjk")
        return "abc"


c = MyClass()

import inspect
import ast
import re

def overwrite_func(func):
    # get definition and return a new func.
    # test: add "yield" after every line.
    func_source = inspect.getsource(func)
    # return new_func
    find_def = r"^( +)def"
    FDRegex = re.compile(find_def, flags=re.MULTILINE)
    strip_blanks = FDRegex.findall(func_source)[0]
    blank_count = len(strip_blanks)
    # print("BLANK COUNT:", blank_count) # BLANK COUNT: 4
    indent_replace = r"^ "+("{%d}" % blank_count)
    # print(repr(indent_replace))
    IRRegex = re.compile(indent_replace, flags=re.MULTILINE)
    func_source_cleaned = IRRegex.sub("", func_source)
    print("SOURCE CODE CLEANED".center(70, "="))
    print(func_source_cleaned)
    print()
    func_ast = ast.parse(func_source_cleaned, type_comments=True)
    print(func_ast) # unexpected indent, if not cleaned.
    print(func_ast.body) # [<_ast.FunctionDef object at 0x1048a1a00>]
    # for cn in ast.iter_child_nodes(func_ast):
    #     print(cn)
    funcdef = func_ast.body[0]
    print(funcdef.body) # no comment?
    print(dir(funcdef))
    print(funcdef.decorator_list) # [<_ast.Name object at 0x103081b50>]
    # [<_ast.Expr object at 0x105359550>, <_ast.Expr object at 0x105368100>, <_ast.Assert object at 0x105395790>, <_ast.Expr object at 0x105395a60>]


# c.myfunc()

new_func = overwrite_func(c.myfunc)
c.myfunc = new_func
