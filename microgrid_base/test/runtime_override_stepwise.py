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
from collections import namedtuple

FuncSourceWithName = namedtuple("FuncSourceWithName", ["changed_source", "funcname"])
# it is a small function which can be run as commandline tool.
# just invoke conda while testing. do not try to run the whole environment in python3.9

# for compatibility, better use python3.9
# though using "redbaron" or some other code refactor tool also works.

# refs:
# https://github.com/python-rope/rope
# https://redbaron.readthedocs.io/en/latest/
# https://pybowler.io/
# https://libcst.readthedocs.io/en/stable/why_libcst.html
# try:
#     from pydantic import field_validator as validator
# except:
#     from pydantic import validator
from pydantic import validator

import os


def iterate_till_keyword(iterator, keyword: str):
    """
    Iterate through the given iterator until the specified keyword is found.

    Parameters:
        - iterator: An iterator object.
        - keyword: A string representing the keyword to stop the iteration.

    Returns:
        None
    """
    while True:
        it = next(iterator)
        if it == keyword:
            print(f"Stopped iteration at keyword: '{keyword}'")
            break


class ExchangePaths:
    input = "input.json"
    output = "output.json"

    @staticmethod
    def getInputPath(basedir: str):
        """
        A static method that takes a base directory as input and returns the path to the input file.
        
        Parameters:
            basedir (str): The base directory.
        
        Returns:
            str: The path to the input file.
        """
        return os.path.join(basedir, ExchangePaths.input)

    @staticmethod
    def getOutputPath(basedir: str):
        """
        Get the output path by joining the base directory with the output path.

        Args:
            basedir (str): The base directory.

        Returns:
            str: The output path.
        """
        return os.path.join(basedir, ExchangePaths.output)


class SourceCodeExchange(BaseModel):
    source_code: str
    processed: bool
    funcname: str = ""
    keywords: set = set()  # validation values follows the order.

    @validator("keywords")
    def validate_keywords(cls, v, values):
        """
        Validate the "keywords" field.

        Args:
            cls: The class itself.
            v: The value of the "keywords" field.
            values: The values of all the fields in the model.

        Returns:
            The validated value of the "keywords" field.
        """
        # print(values)
        # breakpoint()
        if processed := values.get("processed"):  # ERROR
            assert (
                len(v) == 0
            ), "Processed: {}\nInvalid keywords: {} (Shall be empty)".format(
                processed, v
            )
        else:
            assert (
                len(v) != 0
            ), "Processed: {}\nInvalid keywords: {} (Shall not be empty)".format(
                processed, v
            )
        return v

    @validator("funcname")
    def validate_funcname(cls, v, values):
        """
        Validate the funcname parameter.

        Parameters:
            cls (class): The class object.
            v (Any): The value to be validated.
            values (Dict[str, Any]): The dictionary of values.

        Returns:
            Any: The validated value.
        """
        if processed := values.get("processed"):
            assert (
                v != ""
            ), "Processed: {}\nInvalid funcname: {} (Shall not be empty)".format(
                processed, repr(v)
            )
        else:
            assert (
                v == ""
            ), "Processed: {}\nInvalid funcname: {} (Shall be empty)".format(
                processed, repr(v)
            )
        return v


import sys

if sys.version_info >= (3, 9):

    def add_stepwise_lines_to_func_source(func_source_cleaned, keywords: set):
        """
        Adds stepwise lines to the given function source code.

        Parameters:
            func_source_cleaned (str): The cleaned source code of the function.
            keywords (set): A set of keywords to search for in the function source code.

        Returns:
            FuncSourceWithName: An object containing the changed source code and the function name.
        """
        import ast_comments as ast

        # import astunparse
        # no comment support!
        # unparse_func = astor.to_source
        # unparse_func = astunparse.unparse
        unparse_func = ast.unparse

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
            if _k:  # only use that keyword one time.
                # can't you preserve comments in ast?
                # pip3 install ast-comments
                keywords.remove(_k)
        funcdef.body = new_body
        changed_source = unparse_func(funcdef)  # cannot convert comment back to source.
        print("CHANGED SOURCE".center(70, "="))
        print(changed_source)
        return FuncSourceWithName(changed_source=changed_source, funcname=funcname)

else:

    def add_stepwise_lines_to_func_source(func_source_cleaned, keywords: set):
        """
        Adds stepwise lines to the function source code.

        Args:
            func_source_cleaned (str): The cleaned source code of the function.
            keywords (set): A set of keywords.

        Returns:
            FuncSourceWithName: An object containing the changed source code and function name.
        """
        # implement it by calling conda.
        # use temporary directory.
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:  # str!
            # tmpdir_name = tmpdir.name
            data = SourceCodeExchange(
                source_code=func_source_cleaned, keywords=keywords, processed=False
            )
            input_path = ExchangePaths.getInputPath(tmpdir)
            output_path = ExchangePaths.getOutputPath(tmpdir)
            with open(input_path, "w+") as f:
                content = data.json()
                f.write(content)
            commandline = "conda run -n base --no-capture-output --live-stream python {filename} -i '{input_path}'".format(
                filename=os.path.basename(__file__), input_path=input_path
            )
            print("EXCUTING: {}".format(commandline))
            os.system(commandline)
            processed_data = SourceCodeExchange.parse_file(output_path)
            return FuncSourceWithName(
                changed_source=processed_data.source_code,
                funcname=processed_data.funcname,
            )


def overwrite_func(func, keywords: set):  # nameclash warning!
    # def overwrite_func(func, c_globals, keywords: set):
    """
    Overwrites a given function with a modified version that inserts "yield" after every line containing given keywords.

    Args:
        func: The function to be overwritten.
        keywords (set): A set of keywords to be inserted after each line in the modified function.

    Returns:
        The modified function.
    """
    # def overwrite_func(func, c_locals, c_globals, keywords: set):
    import inspect

    # import ast
    import re

    # get definition and return a new func.
    # test: add "yield" after every line.
    # func_ast = astor.code_to_ast(func)
    # print(func_ast)
    # deprecated?
    c_globals = func.__globals__

    # what is the name of the function?

    func_source = inspect.getsource(func)
    # return new_func
    find_def = r"^( +)(?:def|async)"  # not async
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

    changed_source, funcname = add_stepwise_lines_to_func_source(
        func_source_cleaned, keywords
    )
    # exec(changed_source, globals=None, locals=None, /)
    # exec(changed_source, c_globals,c_locals, /)
    exec(changed_source, c_globals)
    print(locals().keys())

    new_func = eval(funcname)  # not in locals.
    # new_func = locals()[funcname]
    return new_func


from types import MethodType


def add_locals_and_globals_inspectors_to_instance(c):
    """
    Adds local and global inspectors to the given instance.

    :param c: The instance to add the inspectors to.
    """
    c.locals = MethodType(lambda self: locals(), c)
    c.globals = MethodType(lambda self: globals(), c)


if __name__ == "__main__":
    # import docopt

    # print(__doc__)
    # arguments = docopt.docopt(__doc__, help=False, version='Stepwise Test Util 1.0')
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-t", "--test", action="store_true", default=False)
    argparser.add_argument("-i", "--input", type=str, default=None)
    # print(arguments)
    # breakpoint()
    arguments = argparser.parse_args()

    if arguments.test:

        def dec(f):
            """
            Decorator function that takes a function as input and returns the same function.
            """
            """
            Decorator function that takes a function as input and returns the same function.
            """
            return f

        class MyClass:
            val = 1

            @staticmethod
            def newfunc():
                """
                A static method that returns the string "a".
                """
                return "a"

            def inspect_class(self):
                """
                A method that inspects the current class and prints the keys of the local and global scope.

                Parameters:
                    self: The instance of the class.

                Returns:
                    None
                """
                print(locals().keys())
                print(globals().keys())

            @dec
            def myfunc(self):
                """
                Decorated function that prints "abc", "def", and "in range" 20 times.
                Raises an AssertionError with the message "you cannot pass".
                Returns the string "abc".
                """
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

        # add_locals_and_globals_inspectors_to_instance(c)
        # c_locals = c.locals()
        # c_globals = c.globals()
        # c_globals = c.myfunc.__globals__
        # # c_globals = MyClass.__globals__
        # # c_globals = c.__globals__
        # # print(c_locals.keys())
        # print(c_globals.keys())

        keywords = {"def", "has_keyword"}

        new_func = overwrite_func(c.myfunc, keywords)
        # new_func = overwrite_func(c.myfunc, c_globals, keywords)
        # new_func = overwrite_func(c.myfunc, c_locals, c_globals, keywords)
        c.myfunc = MethodType(new_func, c)

        exec_result = c.myfunc()
        print(type(exec_result))
        # c.inspect_class()
        # for flag in exec_result:
        #     print("RECEVICED FLAG:", flag)
        # AssertionError: you cannot pass

        def myiterator():
            """
            A generator function that yields the value 2 and then returns 1.
            """
            yield 2
            return 1  # stopped iteration.
            # if you want to "return", just don't insert any "yield" statements.

        a = myiterator()  # generator.
        print(a)
        print()

        for it in a:
            print(it)
    elif input_path := arguments.input:
        print("INPUT FILE PATH:", input_path)
        data = SourceCodeExchange.parse_file(input_path)
        output = add_stepwise_lines_to_func_source(
            func_source_cleaned=data.source_code, keywords=data.keywords
        )
        with open(
            output_path := ExchangePaths.getOutputPath(os.path.dirname(input_path)),
            "w+",
        ) as f:
            print("WRITE TO:", output_path)
            output_data = SourceCodeExchange(
                source_code=output.changed_source,
                processed=True,
                funcname=output.funcname,
            )
            content = output_data.json()
            f.write(content)
    else:
        argparser.print_help()
