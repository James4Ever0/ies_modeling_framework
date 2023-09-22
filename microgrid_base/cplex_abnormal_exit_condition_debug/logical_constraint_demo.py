from pyomo.environ import *
from pyomo.gdp import *

# Create a concrete model
m = model =  ConcreteModel()

# m.x1 = Var(within=Integers, bounds=(-10,10))
# m.x2 = Var(within=Integers, bounds=(-10,10))
# m.x3 = Var(within=Integers, bounds=(-10,10))
# m.x4 = Var(within=Integers, bounds=(-10,10))

m.x1 = Var(within=Integers)
m.x2 = Var(within=Integers)
m.x3 = Var(within=Integers)
m.x4 = Var(within=Integers)

m.unit1 = Disjunct()
m.unit1.inout = Constraint(expr=2*m.x2 - 2 == m.x1)
# m.unit1.inout = Constraint(expr=exp(m.x2) - 1 == m.x1)
m.unit1.no_unit2_flow1 = Constraint(expr=m.x3 == 0)
m.unit1.no_unit2_flow2 = Constraint(expr=m.x4 == 0)
m.unit2 = Disjunct()
m.unit2.inout = Constraint(expr=2*m.x4 - 1 <= m.x3) # linear
# m.unit2.inout = Constraint(expr=exp(m.x4 / 1.2) - 1 == m.x3) # ipopt only!
m.unit2.no_unit1_flow1 = Constraint(expr=m.x1 == 0)
m.unit2.no_unit1_flow2 = Constraint(expr=m.x2 == 0)
m.use_unit1or2 = Disjunction(expr=[m.unit1, m.unit2])

# Set the objective
# model.obj = Objective(expr=model.x[4]+model[1]+model.x[2]+model.x[3])
model.obj = Objective(expr=0, sense=minimize)
# model.obj = Objective(expr=m.x1+m.x2+m.x3+m.x4, sense=minimize)
# model.obj = Objective(expr=quicksum(model.x), sense=minimize)
# Solve the problem
# apply to logical constraints, not gdp!
# TransformationFactory('core.logical_to_linear').apply_to(m)
TransformationFactory('gdp.bigm').apply_to(m, bigM = 1e7)

solver = SolverFactory('cplex')
# solver = SolverFactory('ipopt')
results = solver.solve(model)

# Print the results
for i in range(1,5):
    print(f"x{i} =", value(getattr(model,f"x{i}"), exception=False))
print("obj =", value(model.obj, exception=False))
