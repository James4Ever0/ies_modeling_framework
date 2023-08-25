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
# print(sol)
# breakpoint()
# {'t_x0': 10.0, 't_x1': 100000.00000000001, 't_x2': 0.0, 't_x3': 0.0}
model.writeSol(sol, "no_bound_scip.sol")
# print("x: {}".format(sol[x]))
# print("y: {}".format(sol[y]))