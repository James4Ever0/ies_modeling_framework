import cplex
import docplex

model_fpath = "no_bound.lp"
from docplex.mp.model import Model
from docplex.mp.model_reader import ModelReader

mdl: Model = ModelReader.read(model_fpath, model_name="InfeasibelLP")

mdl.solve()
print(mdl.get_solve_status())
print(mdl.get_solve_details())
print(mdl.solution) # None.
