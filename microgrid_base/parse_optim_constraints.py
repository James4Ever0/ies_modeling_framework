filepath ="ies_optim.py"
with open(filepath, 'r') as f:
    content = f.read()
    
import ast

mfile = ast.parse(content)
# print(mfile, dir(mfile))
# breakpoint()

import astor

TS = lambda ast_tree: astor.code_gen.to_source(ast_tree)

def printTypeAndNameHint(TYPE:str, NAME: str):
    print()
    print(f"[{TYPE}]========================[{NAME}]")

def walkElemAndPrintConstraint(elem: ast.AST, TYPE:str, NAME: str, trial=True):
    if not trial:
        printTypeAndNameHint(TYPE, NAME)
    else:
    hasCode = False
    for w in ast.walk(elem):
        if type(w) == ast.Call:
            callName = astor.to_source(w.func).strip()
            if "constraint" in callName.lower() and "register" not in callName:
                callCode = astor.to_source(w).strip()
                hasCode=True
                if not trial:
                    print(callCode)
    return hasCode


for elem in mfile.body:
    if type(elem) == ast.ClassDef:
        cname = elem.name
        # print(cname)
        if cname.endswith('模型'):
            printTypeAndNameHint("CLASS","cname")
            if cname == "设备模型":
                for e in elem.body:
                    if type(e) == ast.FunctionDef:
                        walkElemAndPrintConstraint(e, "FUNC", e.name)
            walkElemAndPrintConstraint(elem, 'CLASS',cname)
    elif type(elem) == ast.FunctionDef:
        funcName = elem.name
        if funcName == "compute":
            walkElemAndPrintConstraint(elem, 'FUNC', funcName)