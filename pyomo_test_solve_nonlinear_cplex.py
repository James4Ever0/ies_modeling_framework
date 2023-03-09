# no enviroment tweaks. (will not work at all) just create shim for scoop.

# MINLP open source solvers:
# https://pyomo.readthedocs.io/en/stable/contributed_packages/mindtpy.html
# SHOT
# https://projects.coin-or.org/Couenne
# https://projects.coin-or.org/Bonmin

# from pyomo.contrib.simplemodel import SimpleModel
from math import pi  # do not use `sin` from here!

# pip install pyomocontrib_simplemodel
from pyomo.environ import *  # different approaches gives different import paths. may not always share all solvers.

# from pyomo.core.expr import current as EXPR
# from pyomo.core import ConcreteModel, Var, Objective, minimize, sin

model = ConcreteModel()
model.x = Var(bounds=(0, 3))
model.y = Var(bounds=(0, 2 * pi))
model.z = Var()

model.c1 = Constraint(expr=model.z == model.x * sin(model.y))


# from pyomo.opt import SolverFactory # not good!

model.obj = Objective(expr=model.z, sense=minimize)

opt = SolverFactory("mindtpy")
opt.solve(model, mip_solver="cplex", nlp_solver="ipopt", tee=True)  # nothing returned?
model.obj.display()
model.x.display()
model.y.display()
# breakpoint()
