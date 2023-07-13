# from sympy import symbols

# TODO: create more readable constraint names for easy debugging
# TODO: extract infeasible constraints with relevant solver message

# use pyomo
from pyomo.environ import *

x_bounds = []

for sense in [minimize, maximize]:
    model = ConcreteModel()
    x = model.变量x = Var()
    y = model.变量y = Var()
    z = model.变量z = Var()
    h = model.变量h = Var()
    # z = model.z = Var()
    # x, y, z = symbols("x y z")
    # infeasible on y.
    # unbounded
    # expressions = [y >= z, y <= 20, y >= 10, z <= 0, z >= -10, x <= 100 - y]
    # feasible
    # expressions = [y >= z, y <= 20, y >= 10, z <= 0, z >= -10, x <= 100 - y, x >= y - z]
    # infeasible
    # expressions = [y >= z, y >= 20, y <= 10, z <= 0, z >= -10, x <= 100 - y, x >= y - z]
    # double infeasible (will not show both)
    expressions = [y >= z, y >= 20, y <= 10, h >= 20, h <= 10, z <= 0, z >= -10, x <= 100 - (h+y)/2, x >= (h+y)/2 - z]
    # Bound infeasibility column '变量y'.
    # check if is unbounded or infeasible.
    # try to comment that out, see if it can solve
    # red = reduce_inequalities(expresssions, [x])
    for i, _expr in enumerate(expressions):
        model.__setattr__(f"expr_{i}", Constraint(expr=_expr))
    # print(red)
    obj = model.obj = Objective(expr=x, sense=sense)
    io_options = dict(symbolic_solver_labels=True)
    model.write(filename="your_model_name.lp", io_options=io_options)

    solver = SolverFactory("cplex")
    # 求解器变量乱码,影响求解
    solver.options["read fileencoding"] = 'utf-8'
    result = solver.solve(model, tee=True, io_options=io_options)

    TC = result.solver.termination_condition
    import rich
    rich.print(result)
    normalTCs = [
        TerminationCondition.globallyOptimal,
        TerminationCondition.locallyOptimal,
        TerminationCondition.feasible,
        TerminationCondition.optimal,
    ]
    if TC == TerminationCondition.infeasible:
        raise Exception("infeasible constraint found. please check expression")
    elif TC == TerminationCondition.unbounded:
        raise Exception("unbounded constraint found. please check expression")
    elif TC not in normalTCs:
        raise Exception(f"abnormal solver exit condition: {TC}")
    print("val? %s, sense? %s" % (val_x := value(x), sense))
    x_bounds.append(val_x)

print("x bounds:", x_bounds)
