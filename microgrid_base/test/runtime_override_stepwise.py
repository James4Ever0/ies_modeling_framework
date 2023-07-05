#!/usr/bin/env conda run -n base --live-stream --no-capture-output python
# ref: https://www.baeldung.com/linux/shebang-types

import os
filename = os.path.basename(__file__)
__doc__ = """Stepwise source code manipulation for testing.

Note:
    Some functions only works with Python 3.9 and above.

Usage:
    {filename} -i <file>, --input <file>
    {filename} -t, --test

Options:
    -i --input <file>     Input json file for parsing, 
    -t --test             Run test cases.

""".format(filename=filename)

# doc = __doc__
from pydantic import BaseModel

# it is a small function which can be run as commandline tool.
# just invoke conda while testing. do not try to run the whole environment in python3.9

# for compatibility, better use python3.9
# though using "redbaron" or some other code refactor tool also works.

# refs:
# https://github.com/python-rope/rope
# https://redbaron.readthedocs.io/en/latest/
# https://pybowler.io/
# https://libcst.readthedocs.io/en/stable/why_libcst.html


def overwrite_func(func, c_locals, c_globals, keywords = {'def', "has_keyword"}):  # nameclash warning!
    
    import inspect
    # import ast
    import ast_comments as ast
    import re

    # import astunparse
    # no comment support!
    # unparse_func = astor.to_source
    # unparse_func = astunparse.unparse
    unparse_func = ast.unparse
    
    # get definition and return a new func.
    # test: add "yield" after every line.
    # func_ast = astor.code_to_ast(func)
    # print(func_ast)
    # deprecated?

    # what is the name of the function?

    func_source = inspect.getsource(func)
    # return new_func
    find_def = r"^( +)def"  # not async
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
    # func_ast = ast.parse(func_source_cleaned, type_comments=True)
    func_ast = ast.parse(func_source_cleaned)
    print(func_ast)  # unexpected indent, if not cleaned.
    print(func_ast.body)  # [<_ast.FunctionDef object at 0x1048a1a00>]
    # for cn in ast.iter_child_nodes(func_ast):
    #     print(cn)
    funcdef = func_ast.body[0]
    funcname = funcdef.name
    print(funcdef.body)  # no comment?
    # breakpoint()
    # [<_ast.Expr object at 0x105359550>, <_ast.Expr object at 0x105368100>, <_ast.Assert object at 0x105395790>, <_ast.Expr object at 0x105395a60>]
    print(dir(funcdef))
    print(funcdef.decorator_list)  # [<_ast.Name object at 0x103081b50>]

    # changed_source = ast.dump(funcdef)
    new_body = []
    for item in funcdef.body:
        new_body.append(item)
        item_code = unparse_func(item)
        _k = None
        for keyword in keywords:
            if keyword in item_code:
                stepwise_expr = ast.parse("yield '{}'".format("myflag")).body[0]
                new_body.append(stepwise_expr)
                _k = keyword
                break
        if _k: # only use that keyword one time.
            # can't you preserve comments in ast?
            # pip3 install ast-comments
            keywords.remove(_k)
    funcdef.body = new_body
    changed_source = unparse_func(funcdef) # cannot convert comment back to source.
    print("CHANGED SOURCE".center(70, "="))
    print(changed_source)
    exec(changed_source, c_locals, c_globals)
    print(locals().keys())

    new_func = eval(funcname)  # not in locals.
    # new_func = locals()[funcname]
    return new_func

from types import MethodType

def inspect_locals_and_globals(c):
    c.locals = MethodType(lambda self: locals(), c)
    c.globals = MethodType(lambda self: globals(), c)

if __name__ == "__main__":
    import docopt
    
    # print(__doc__)
    arguments = docopt.docopt(__doc__, version='Stepwise Test Util 1.0')
    print(arguments)
    
    if test:
        def dec(f):
            return f

        class MyClass:
            val = 1

            @staticmethod
            def newfunc():
                return "a"

            def inspect_class(self):
                print(locals().keys())
                print(globals().keys())

            @dec
            def myfunc(self):
                print("abc")
                print("def")
                # mycomment
                # mycomment_has_keyword
                for _ in range(20):
                    print("in range")
                assert False, "you cannot pass"
                print("hjk")
                # every comment shall be ignored.
                # yield "myflag"  # you may yield flag.
                return "abc"

        c = MyClass()

        inspect_locals_and_globals(c)
        c_locals = c.locals()
        c_globals = c.globals()

        print(c_locals.keys())
        print(c_globals.keys())

        new_func = overwrite_func(c.myfunc, c_locals, c_globals)
        c.myfunc = MethodType(new_func, c)

        exec_result = c.myfunc()
        print(type(exec_result))
        # c.inspect_class()
        # for flag in exec_result:
        #     print("RECEVICED FLAG:", flag)
        # AssertionError: you cannot pass

        def myiterator():
            yield 2
            return 1 # stopped iteration.
            # if you want to "return", just don't insert any "yield" statements.

        a = myiterator()  # generator.
        print(a)
        print()

        for it in a:
            print(it)