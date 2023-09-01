from pyomo.environ import *

solver = SolverFactory("coptampl")

model = ConcreteModel()
model.a = Var(bounds=(-1, 1))

model.obj = Objective(expr=model.a, sense=minimize)

ret = solver.solve(model, tee=True)

import rich

rich.print(ret)
