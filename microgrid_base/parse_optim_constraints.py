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

def walkElemAndPrintConstraint(elem: ast.AST, TYPE:str, NAME: str):
    printTypeAndNameHint(TYPE, NAME)
    for w in ast.walk(elem):
        if type(w) == ast.Call:
            callName = astor.to_source(w.func).strip()
            if "constraint" in callName.lower() and "register" not in callName:
                callCode = astor.to_source(w).strip()
                print(callCode)


for elem in mfile.body:
    if type(elem) == ast.ClassDef:
        cname = elem.name
        # print(cname)
        if cname.endswith('模型'):
            print()
            print("CLASS","cname")
            if cname == "设备模型":
                for e in elem.body:
                    if type(e) == ast.FunctionDef:
                        walkElemAndPrintConstraint
            walkElemAndPrintConstraint(elem)
    elif type(elem) == ast.FunctionDef:
        funcName = elem.name
        if funcName == "compute":
            print()
            print(f"[FUNC]========================[{funcName}]")
            walkElemAndPrintConstraint(elem)