from ortools.sat.python import cp_model
# https://github.com/google/or-tools/issues/973

model = cp_model.CpModel()
solver = cp_model.CpSolver()

a = model.NewIntVar(0,15, 'a')
b = model.NewIntVar(0,15, 'b')
c = model.NewIntVar(0,15, 'c')
d = model.NewIntVar(0,15, 'd')
e = model.NewBoolVar('e')
f = model.NewIntervalVar(0,10,10,'f')

model.AddMaxEquality(d, [a,b,c]).OnlyEnforceIf(e)

status = solver.Solve(model)
print(status)
print(solver.ObjectiveValue())