filepath ="ies_optim.py"
with open(filepath, 'r') as f:
    content = f.read()
    
import ast

mfile = ast.parse(content)
print(mfile, dir(mfile))
# breakpoint()

import astor

astor.code_gen.pretty_source
for elem in mfile.body:
    if type(elem) == ast.ClassDef:
        cname = elem.name
        print(cname)