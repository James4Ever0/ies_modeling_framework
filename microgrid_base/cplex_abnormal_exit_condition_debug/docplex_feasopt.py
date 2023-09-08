from docplex.mp.model import Model
from docplex.mp.model_reader import ModelReader

# import cplex
model_fpath = "converted.mps"
import cplex

mdl: Model = ModelReader.read(model_fpath, model_name="InfeasibelLP")
print("model loaded successfully from: %s" % model_fpath)


class GenericCB:
    def invoke(self, context):
        print("context?", context)


cb = GenericCB()
mdl.cplex.set_callback(cb)  # Register callback.

import sys

# there you go.
mdl.cplex.set_error_stream(sys.stderr)
mdl.cplex.set_log_stream(sys.stderr)
mdl.cplex.set_results_stream(sys.stderr)
mdl.cplex.set_warning_stream(sys.stderr)
# help(mdl.cplex.feasopt)
# breakpoint()
feasopt = mdl.cplex.feasopt
# breakpoint()
# quadratic & indicator shall never be used.
# if detected, please show us what names they have.
# all constraints shall be linear.
# feasopt.all_constraints()
from typing import Literal, List, Dict, Callable

group_mode = Literal["linear", "upper_bound", "lower_bound"]
# transfunc_map: Dict[group_mode, Callable] = {}


def group_items(namelist: List[str], mode: group_mode):
    return getattr(feasopt, "")(namelist)


constraint_type_constant_map = feasopt.constraint_type._get_constant_map()
# first count our constraints stat.
constraint_instance_count_map = {}
# mdl.iter_indicator_constraints()
# mdl.iter_quadratic_constraints()
for it in mdl.iter_linear_constraints():
    print(it)
    breakpoint()

for ctype, type_const in constraint_type_constant_map.items():
    constraint_instance_count_map[ctype] = feasopt._getnum(type_const)
    transfunc_map[ctype] = feasopt._getconvfunc(type_const)


feasopt(feasopt.all_constraints())
# cplex._internal._aux_functions._group
# feasopt._make_group
sol = mdl.cplex.solution  # this is taking eternal. we need to check progress!
print("*" * 60)
print(sol)
# relatex_sol =
