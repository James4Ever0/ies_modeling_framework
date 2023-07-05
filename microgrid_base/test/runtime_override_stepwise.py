# shall not use shebang.
#!/usr/bin/env conda run -n base --live-stream --no-capture-output python --
# ref: https://www.baeldung.com/linux/shebang-types

# import os
# filename = os.path.basename(__file__)
# __doc__ = """Stepwise source code manipulation for testing.

# Usage:
#     -t
# """.format(filename=filename)

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

import sys

if sys.version_info >= (3, 9):
    def add_stepwise_lines_to_func_source(func_source, keywords:set): ...
    
    def overwrite_func(func, c_locals, c_globals, keywords:set):  # nameclash warning!
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
        
        changed_source = add_stepwise_lines_to_func_source(func_source_cleaned)
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
    # import docopt
    
    # print(__doc__)
    # arguments = docopt.docopt(__doc__, help=False, version='Stepwise Test Util 1.0')
    import argparse
    argparser =  argparse.ArgumentParser()
    argparser.add_argument('-t', '--test', action='store_true', default=False)
    argparser.add_argument('-i', '--input', type=str, default=None)
    # print(arguments)
    # breakpoint()
    arguments = argparser.parse_args()
    
    if arguments.test:
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
        
        keywords = {'def', "has_keyword"}

        new_func = overwrite_func(c.myfunc, c_locals, c_globals, keywords)
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
    elif arguments.input:
        print("INPUT FILE PATH:", arguments.input)
    else:
        argparser.print_help()