from pyomo.environ import *
from math import pi

# this will not work.

model = ConcreteModel()

x = Var(bounds=(0, 3))
y = Var(bounds=(0, 2 * pi))
z = Var()

model.add_component("z_0",z)
model.add_component("x_0",x)
model.add_component("y_0",y)
# model.c1 = Constraint(expr=model.z == model.x+model.y)

import pint

ureg = pint.UnitRegistry()


c1 = Constraint( # add some unit?
    expr=z == x * sin(y)
)  # this is not working. sorry!
model.add_component("c1_1",c1)

obj = Objective(expr=z, sense=minimize)
model.add_component("obj_0",obj)

opt = SolverFactory("ipopt") # not working!
opt.solve(model)

obj.display()
x.display()
y.display()
