def dec(f):
    return f

class MyClass:
    val = 1
    
    @staticmethod
    def newfunc(): return 'a'
    
    def inspect_class(self):
        print(locals())
        print(globals())

    @dec
    def myfunc(self):
        print("abc")
        print("def")
        # mycomment
        for _ in range(20):
            print('in range')
        assert False, "you cannot pass"
        print("hjk")
        yield "myflag"  # you may yield flag.
        return "abc"


c = MyClass()

import inspect
import ast
import astor
import re


def overwrite_func(func, c_locals, c_globals):
    # get definition and return a new func.
    # test: add "yield" after every line.
    # func_ast = astor.code_to_ast(func)
    # print(func_ast)
    # deprecated?
    
    # what is the name of the function?

    func_source = inspect.getsource(func)
    # return new_func
    find_def = r"^( +)def"
    FDRegex = re.compile(find_def, flags=re.MULTILINE)
    strip_blanks = FDRegex.findall(func_source)[0]
    blank_count = len(strip_blanks)
    # print("BLANK COUNT:", blank_count) # BLANK COUNT: 4
    indent_replace = r"^ " + ("{%d}" % blank_count)
    # print(repr(indent_replace))
    IRRegex = re.compile(indent_replace, flags=re.MULTILINE)
    func_source_cleaned = IRRegex.sub("", func_source)
    print("SOURCE CODE CLEANED".center(70, "="))
    print(func_source_cleaned)
    print()
    func_ast = ast.parse(func_source_cleaned, type_comments=True)
    print(func_ast)  # unexpected indent, if not cleaned.
    print(func_ast.body)  # [<_ast.FunctionDef object at 0x1048a1a00>]
    # for cn in ast.iter_child_nodes(func_ast):
    #     print(cn)
    funcdef = func_ast.body[0]
    funcname = funcdef.name
    print(funcdef.body) # no comment?
    # [<_ast.Expr object at 0x105359550>, <_ast.Expr object at 0x105368100>, <_ast.Assert object at 0x105395790>, <_ast.Expr object at 0x105395a60>]
    print(dir(funcdef))
    print(funcdef.decorator_list) # [<_ast.Name object at 0x103081b50>]

    changed_source = ast.dump(funcdef)
    print("CHANGED SOURCE".center(70, "="))
    print(changed_source)
    # new_func = exec()
    # return new_func

# c.myfunc()

from types import MethodType

c.locals = MethodType(lambda self: locals(), c)
c.globals = MethodType(lambda self: globals(), c)
# c.__setattr__("__locals__", lambda self: locals())
# c.__setattr__("__globals__", lambda self: globals())
c_locals = c.locals()
c_globals = c.globals()

print(c_locals)
print(c_globals)

new_func = overwrite_func(c.myfunc, c_locals, c_globals)
# c.myfunc = MethodType(new_func, c)

# mycode = """
# def newfunc(): return None
# """

# exec(mycode)
print()
# c.inspect_class()