from pyomo.environ import *
from math import pi

# this will not work.

model = ConcreteModel()
model.x = Var(bounds=(0, 3))
model.y = Var(bounds=(0, 2 * pi))
model.z = Var()

# model.c1 = Constraint(expr=model.z == model.x+model.y)
model.c1 = Constraint(
    expr=model.z == model.x * sin(model.y)
)  # this is not working. sorry!

model.obj = Objective(expr=model.z, sense=minimize)

# opt = SolverFactory("cplex") # not working!
# opt.solve()

# model.obj.display()
# model.x.display()
# model.y.display()
