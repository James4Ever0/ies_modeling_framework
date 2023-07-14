from pyomo.environ import *

model = ConcreteModel()

model.v = Var(initialize=1)

model.e = 2 * model.v * model.v + 2

# import pyomo.core.expr as E
from pyomo.core.expr.sympy_tools import sympyify_expression

# to sympy.

objmap, vis = sympyify_expression(model.e)
import rich
rich.print(objmap)
from sympy import Mul
# 'getPyomoSymbol', 'getSympySymbol', 'i', 'pyomo2sympy', 'sympy2pyomo', 'sympyVars'
rich.print(vis) # sympy expression.
breakpoint()
rich.print(vis.as_terms()) # ([(2, ((2.0, 0.0), (0,), ())), (2*x0**2, ((2.0, 0.0), (2,), ()))], [x0])
# (terms, symbols)
# terms = [(expr, deg, pow)]