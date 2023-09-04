from pyomo.environ import *

solver = SolverFactory("coptampl")

model = ConcreteModel()
model.a = Var(bounds=(-1, 1))
model.b = Var(bounds=(-1, 1))

model.obj = Objective(expr=model.a+model.b, sense=minimize)

# print(dir(model.obj.expr))
# breakpoint()

ret = solver.solve(model, tee=True)

import rich

rich.print(ret)
