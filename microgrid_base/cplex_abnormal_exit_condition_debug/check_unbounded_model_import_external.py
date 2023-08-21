import sys

sys.path.append("../")

from ies_optim import ModelWrapper

from debug_utils import checkInfeasibleOrUnboundedModel
from pyomo.environ import *

import os

log_dir = "logs"
os.system(f"mkdir {log_dir}")

mw = ModelWrapper()

x = mw.Var("变量x")
y = mw.Var("变量y")
mw.Constraint(expr=x + y >= 10)

x.setlb(-10)
x.setub(10)

obj_expr = 2 * x - 5 + y

obj = mw.Objective(expr=obj_expr, sense=minimize)

solver = SolverFactory('cplex')

checkInfeasibleOrUnboundedModel(mw, solver, log_dir)