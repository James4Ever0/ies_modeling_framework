filepath ="ies_optim.py"
with open(filepath, 'r') as f:
    content = f.read()
    
import ast

mfile = ast.parse(content)
print(mfile, dir(mfile))
# breakpoint()

import astor

TS = lambda ast_tree: astor.code_gen.to_source(ast_tree)

for elem in mfile.body:
    if type(elem) == ast.ClassDef:
        cname = elem.name
        print(cname)
        if cname.endswith('模型'):
            ...
    elif type(elem) == ast.FunctionDef:
        funcName = elem.name