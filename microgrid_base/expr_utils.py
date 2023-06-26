# lineno = 45381

# with open("error.log", 'r') as f:
#     for index, line in enumerate(f.readlines()):
#         if index == lineno-1:
#             with open("test_data.log", 'w+') as f1:
#                 f1.write(line)
#                 break
import sys
from sympy import sympify
# import sympy
from progressbar import progressbar

try:
    from typing import Literal
except:
    from typing_extensions import Literal
# shall you simplify expressions in some way.


def find_parentheses(s):
    stack = []
    result = []  # EIPList
    for i, c in enumerate(progressbar(s)):
        if c == "(":
            stack.append(i)  # 记录左括号的位置
        elif c == ")":
            if stack:  # 如果栈不为空
                start = stack.pop()  # 弹出最近的左括号位置
                if not stack:  # 如果栈为空，说明找到了一个最外层的括号对
                    result.append(s[start : i + 1])  # 将括号对加入结果列表
    return result


import re
from typing import ContextManager


class RecursionContext(ContextManager):
    def __init__(self, recursion_limit=10**9):
        self.recursion_limit = recursion_limit
        self.sys_recursion_limit = sys.getrecursionlimit()

    def __enter__(self):
        """Return `self` upon entering the runtime context."""
        sys.setrecursionlimit(self.recursion_limit)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Raise any exception triggered within the runtime context."""
        sys.setrecursionlimit(self.sys_recursion_limit)
        return None

def getExprStrParsedToExprList(data:str, approach: Literal[1, 2] = 1):
    regex = re.compile(r"(\[\d+\])")
    subs = regex.findall(data)
    print(len(subs))

    # for sub in set(subs):
    #     data = data.replace(sub,"_Array")
    data = regex.sub("_Array", data)

    #######################
    # EXPR SIMPLIFICATION #
    #######################

    """
    APP1: subexpr (-> full_expr)
    APP2: full_expr -> subexpr

    APP1 is faster than APP2.
    """

    import time

    starting_time = time.time()
    if approach == 1:
        #####################APPROACH 1#####################
        """
        parse and substitude terms.
        """
        regex2 = re.compile(r"(((?P<term>\w+_Array) \+ )+((?P=term)))")
        summation = [(e[0], e[2]) for e in regex2.findall(data)]
        summation.sort(key=lambda x: -len(x[0]))
        # print(len(summation))
        # summation = set(summation)

        # expr = ""
        # breakpoint()
        for e0, e2 in summation:
            suffix = f"_SUM_OF_{e0.count('+')+1}"
            data = data.replace(e0, e2+suffix)

        # print(data)
        expr_repr = data
        from sympy.polys.polytools import Poly

        # recursion error!
        # expr = sympify(data)
        EIPList = find_parentheses(data)
        elems_in_parentheses = set(EIPList)

        EIPMAP = {e: f"EIP_{i}" for i, e in enumerate(elems_in_parentheses)}
        EIPMAP_REV = {v: k for k, v in EIPMAP.items()}
        for EIP, EIP_CODE in EIPMAP.items():
            expr_repr = expr_repr.replace(EIP, EIP_CODE)

        subexpr_strs = expr_repr.replace("-", "+ -").split("+")

        expr_list = []
        with RecursionContext() as RC:
            for subexpr in subexpr_strs:
                print()
                sympify_expr = sympify(subexpr)
                sympify_expr = sympify_expr.simplify()
                _p = Poly(sympify_expr)
                fs = _p.free_symbols
                print(f"FS: {fs}")
                print()
                for s in fs:
                    sname = str(s)
                    if sname in EIPMAP_REV.keys():
                        eip = EIPMAP_REV[sname]
                        eip_expr = sympify(eip)
                        eip_expr = eip_expr.simplify()
                        print(f"{sname} = {eip_expr}")
                        sympify_expr = sympify_expr.subs(sympify(sname), eip_expr)
                print("TERM EXPR:", sympify_expr)
                expr_list.append(sympify_expr)
        # breakpoint()
        final_expr = sum(expr_list)
        print("FINAL EXPR:")
        print(final_expr)
        #####################APPROACH 1#####################
        endtime = time.time()
        print("APP1_TIME:", endtime - starting_time)
        return expr_list
        # APP1_TIME: 4.300285339355469
        # APP1_TIME: 4.084861993789673
    elif approach == 2:
        #####################APPROACH 2#####################
        """
        use template to generate symbols and code.
        """
        # import sys
        # sys.setrecursionlimit(10*100000)
        # sys.getrecursionlimit()
        regex = re.compile(r"\w+")
        words = regex.findall(data)
        words = set(words)
        mwords = []

        codeLines = []
        # codeLines.append("import sympy")
        for word in words: # do not use progressbar in here!
            try:
                float(word)
            except:
                codeLines.append(f'{word} = sympify("{word}")')
                # mwords.append(word)
        # exec(code)
        # codeLines.append(f"sympy_expr = {data}")
        for line in codeLines:
            print("EXCECUTING: ", line[:200] + ("" if len(line) < 200 else "..."))
            exec(line)
        print("GETTING EXPR")
        with RecursionContext() as RC:
            sympy_expr = eval(data)
            print("SIMPLIFYING EXPR")
            sympy_expr = sympy_expr.simplify()
            print()
            print(sympy_expr)
        #####################APPROACH 2#####################
        
        print("FINAL EXPR:")
        print(sympy_expr)
        terms = sympy_expr.as_terms()
        termlist = []
        
        for t in terms:
            term = t[0]
            termlist.append(term)
            
        endtime = time.time()
        print("APP2_TIME:", endtime - starting_time)
        # APP2_TIME: 12.695726156234741
        # APP2_TIME: 11.072844982147217
        return termlist
    else:
        assert False, f"Bad approach: {approach}"


if __name__ == "__main__":
    data = open("test_data.log", "r").read()  # entry: for test
    