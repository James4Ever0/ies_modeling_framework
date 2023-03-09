# no enviroment tweaks. (will not work at all) just create shim for scoop.

# from pyomo.contrib.simplemodel import SimpleModel
from math import pi # do not use `sin` from here!

# pip install pyomocontrib_simplemodel

# from pyomo.core.expr import current as EXPR
from pyomo.core import ConcreteModel, Var, Objective, minimize, sin

model = ConcreteModel()
model.x = Var(bounds=(0, 3))
model.y = Var(bounds=(0, 2 * pi))


def ObjRule(model):
    return model.x * sin(model.y)

from pyomo.opt import SolverFactory

model.obj2 = Objective(rule=ObjRule, sense=minimize)

opt = SolverFactory('mindtpy')
solution = opt.solve(model)
breakpoint()