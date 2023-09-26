from pyomo.environ import *

model = ConcreteModel()
model.a = Var()
model.b = Var(bounds = (-10,10))
model.c = Var()


model.con1 = Constraint(expr = model.a <=model.b)
model.con2 = Constraint(expr = model.a >=model.c)
model.con3 = Constraint(expr = model.c >=-20)
model.con4 = Constraint(expr = model.c <=20)

model.nl_con = Constraint(expr = model.b * model.c >=10) # not convex?
# model.nl_con = Constraint(expr = model.a * model.b * model.c >=10)
model.obj = Objective(expr = 0, sense=minimize)
# TransformationFactory('core.tighten_constraints_from_vars').apply_to(model)

# not working.
print(model.a.bounds)
print(model.c.bounds)

# TransformationFactory('contrib.induced_linearity').apply_to(model)
# new_model = TransformationFactory('core.radix_linearization').create_using(model) # this is python2 code. you need to replace 'iter...' with '...'
# not working!

solver = SolverFactory("cplex")
# solver.solve(new_model)
solver.solve(model, tee=True)
m = model

print('a:',m.a())
print('b:',m.b())
print('c:',m.c())