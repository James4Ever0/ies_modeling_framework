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
from pyomo.environ import units as u

u.load_definitions_from_file("currency_units.txt")

model = ConcreteModel()

x_ub = 0
x_lb = 3

x_ub/=1000
x_lb/=1000

model.x = Var(bounds=(x_ub,x_lb))
model.y = Var(bounds=(0, 2 * pi))
model.z = Var()
# convert_result =  u.convert(model.x, to_units=u.m)
# print("CONVERT RESULT:",convert_result)
# model.x = model.x*convert_result

model.c1 = Constraint(expr=model.z == model.x * sin(model.y))

# from pyomo.opt import SolverFactory # not good!

model.obj = Objective(expr=model.z, sense=minimize)

opt = SolverFactory("mindtpy")  # <- this thing does not support.

opt.solve(model, mip_solver="cplex",
        #   nlp_solver="SHOT",
          nlp_solver="ipopt",
        #  Error: value SHOT not in domain ['ipopt', 'appsi_ipopt', 'gams', 'baron']
          tee=True)

model.obj.display()
model.x.display()
model.y.display()
model.z.display()
breakpoint()
