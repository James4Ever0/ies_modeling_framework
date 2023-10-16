from pyomo.environ import *
from pyomo.gdp import *

model = ConcreteModel()
# model.decision = Var(within=Integers, bounds=(0, 2))

# x_points = [-2, 0.5, 1]
# y_points = [2, 1.5, 0]

model.x = Var(bounds=(-10, 10))
model.y = Var(bounds=(-10, 10))

disj0 = Disjunct()
# model.disj0.decision = Constraint(expr=model.decision == 0)
disj0.definition_x = Constraint(expr=model.x == -2)
disj0.definition_y = Constraint(expr=model.y == 2)

model.disj0 = disj0

model.disj1 = Disjunct()
# model.disj1.decision = Constraint(expr=model.decision == 1)
model.disj1.definition_x = Constraint(expr=model.x == 0)
model.disj1.definition_y = Constraint(expr=model.y == 1)

model.disj2 = Disjunct()
# model.disj2.decision = Constraint(expr=model.decision == 2)
model.disj2.definition_x = Constraint(expr=model.x == 1)
model.disj2.definition_y = Constraint(expr=model.y == 0)

# remember to use the expr argument.
model.disj_unite = Disjunction(expr = [model.disj0, model.disj1, model.disj2])

# model.pw = Piecewise(model.b, model.a, pw_pts = , f_rule = [2, 1.5, 0],pw_repn = 'MC' ,pw_constr_type='EQ')

# model.obj = Objective(expr=0, sense=minimize)
# model.obj = Objective(expr=model.x + model.y, sense=maximize)
model.obj = Objective(expr=model.x + model.y, sense=minimize)

# TransformationFactory("gdp.bigm").apply_to(model)

def checkDisjunctive(model:ConcreteModel):
    for _ in model.component_data_objects(ctype=Disjunct):
        return True
    return False
    

def transformDisjunctiveModel(model, bigM = 1e7):
    is_disjunctive = checkDisjunctive(model)
    if is_disjunctive: 
        TransformationFactory("gdp.bigm").apply_to(model, bigM=bigM)
    return is_disjunctive

transformed = transformDisjunctiveModel(model)

solver = SolverFactory("cplex")
solver.solve(model, tee=True)
print("x:", value(model.x))
print("y:", value(model.y))
print("obj:", value(model.obj))
print("disj0 bin_ind", value(model.disj0.binary_indicator_var)) # 1.0
print("disj0 ind", value(model.disj0.indicator_var)) # True, most likely to be logical
# print("disj1", value(model.disj1.binary_indicator_var))
# print("disj2", value(model.disj2.binary_indicator_var))
# print("decision:", value(model.decision))
# print([mret])
# 
print("transformed:", transformed)

