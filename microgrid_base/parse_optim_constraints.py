filepath ="ies_optim.py"
with open(filepath, 'r') as f:
    content = f.read()
    
import ast

ast.parse(content)