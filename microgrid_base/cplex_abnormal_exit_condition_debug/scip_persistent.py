from pyscipopt import Model

model = Model("Example")  # model name is optional

# print(dir(model))

# help(model.readProblem)
problem_fpath = "no_bound.nl"
# problem_fpath = "no_bound.lp"
model.readProblem(problem_fpath)
# x = model.addVar("x")
# y = model.addVar("y", vtype="INTEGER")
# model.setObjective(x + y)
# model.addCons(2*x - y*y >= 0)
model.optimize()
sol = model.getBestSol()
print(sol)
# print("x: {}".format(sol[x]))
# print("y: {}".format(sol[y]))