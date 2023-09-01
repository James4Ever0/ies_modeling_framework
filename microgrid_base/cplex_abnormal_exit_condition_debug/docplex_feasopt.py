from docplex.mp.model import Model
from docplex.mp.model_reader import ModelReader
# import cplex
model_fpath = "converted.mps"

mdl: Model = ModelReader.read(model_fpath, model_name="InfeasibelLP")
print("model loaded successfully from: %s" % model_fpath)


class GenericCB():
    def invoke(self, context):
        print(context)
cb = GenericCB()
mdl.cplex.set_callback(cb)  # Register callback.

import sys
mdl.cplex.set_log_stream(sys.stdout)
# help(mdl.cplex.feasopt)
# breakpoint()
feasopt = mdl.cplex.feasopt
feasopt(feasopt.all_constraints())
sol = mdl.cplex.solution # this is taking eternal. we need to check progress!
print(sol)
# relatex_sol = 