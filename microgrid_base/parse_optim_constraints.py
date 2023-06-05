filepath ="ies_optim.py"
with open(filepath, 'r') as f:
    content = f.read()
    
import ast

mfile = ast.parse(content)
# print(mfile, dir(mfile))
# breakpoint()

import astor

TS = lambda ast_tree: astor.code_gen.to_source(ast_tree)

def printTypeAndNameHint(TYPE:str, NAME: str, indent:int=0):
    print()
    print(f"{' '*indent}[{TYPE}]========================[{NAME}]")

def walkElemAndPrintConstraint(elem: ast.AST, TYPE:str, NAME: str, trial=True, indent = 0):
    if not trial:
        printTypeAndNameHint(TYPE, NAME, indent = indent)
    hasCode = False
    for w in ast.walk(elem):
        if type(w) == ast.Call:
            callName = astor.to_source(w.func).strip()
            if "constraint" in callName.lower() and "register" not in callName:
                callCode = astor.to_source(w).strip().replace(callName, callName.split(".")[-1])
                hasCode=True
                if not trial:
                    print(" "*(indent+4)+callCode)
    if trial:
        if hasCode:
            walkElemAndPrintConstraint(elem, TYPE, NAME, trial=False, indent=indent)
    return hasCode


for elem in mfile.body:
    if type(elem) == ast.ClassDef:
        cname = elem.name
        # print(cname)
        if cname.endswith('模型'):
            if cname == "设备模型":
                printTypeAndNameHint("CLASS", cname)
                for e in elem.body:
                    if type(e) == ast.FunctionDef:
                        walkElemAndPrintConstraint(e, "FUNC", e.name, indent=4)
            else:
                walkElemAndPrintConstraint(elem, 'CLASS',cname)
    elif type(elem) == ast.FunctionDef:
        funcName = elem.name
        if funcName == "compute":
            walkElemAndPrintConstraint(elem, 'FUNC', funcName)