from ortools.linear_solver import pywraplp

# GLPK not working.
# solver = pywraplp.Solver.CreateSolver(solver_name:='GLPK')

# builtin backends:
solver = pywraplp.Solver.CreateSolver(solver_name:='SAT')
# solver = pywraplp.Solver.CreateSolver(solver_name:="CBC")
# solver = pywraplp.Solver.CreateSolver(solver_name:="SCIP")

if not solver:
    raise Exception("SOLVER %s NOT WORKING" % solver_name)

# breakpoint()

costs = [
    [90, 80, 75, 70],
    [35, 85, 55, 65],
    [125, 95, 90, 95],
    [45, 110, 95, 115],
    [50, 100, 90, 100],
]
num_workers = len(costs)
num_tasks = len(costs[0])

# x[i, j] is an array of 0-1 variables, which will be 1
# if worker i is assigned to task j.
x = {}
for i in range(num_workers):
    for j in range(num_tasks):
        x[i, j] = solver.IntVar(0, 1, "")

# Each worker is assigned to at most 1 task.
for i in range(num_workers):
    solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1)

# Each task is assigned to exactly one worker.
for j in range(num_tasks):
    solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1)

objective_terms = []
for i in range(num_workers):
    for j in range(num_tasks):
        objective_terms.append(costs[i][j] * x[i, j])
solver.Minimize(solver.Sum(objective_terms))

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f"Total cost = {solver.Objective().Value()}\n")
    for i in range(num_workers):
        for j in range(num_tasks):
            # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
            if x[i, j].solution_value() > 0.5:
                print(f"Worker {i} assigned to task {j}." + f" Cost: {costs[i][j]}")
else:
    print("STATUS?", status)
    print("No solution found.")

print("ITERATIONS?", solver.iterations())