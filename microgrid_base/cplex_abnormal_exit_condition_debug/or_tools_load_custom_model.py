
from ortools.linear_solver.python import model_builder, model_builder_helper
# from ortools.sat.python.cp_model.
# breakpoint()
# not working for docplex exported format.
mps_path ='converted.mps' 
# working? but how do we get result?
# mps_path ='exported.mps'

model = model_builder.ModelBuilder()
# model.import_from_lp_file("no_bound.lp")
# error reading file.
model.import_from_mps_file(mps_path)

solver = model_builder.ModelSolver('SAT')
# solver = model_builder.ModelSolver('SCIP')
status = solver.solve(model)

from ortools.linear_solver import pywraplp

if status == model_builder_helper.SolveStatus.OPTIMAL or status == model_builder_helper.SolveStatus.FEASIBLE:
    print(f"Total objective = {solver.objective_value}\n")
    for var in model.get_variables():
        val = solver.value(var)
        print(f"{var} = {val}")
elif status == model_builder_helper.SolveStatus.MODEL_INVALID:
    breakpoint()
else:
    print("STATUS?", status)
    print("No solution found.")