from docplex.mp.model import Model
from docplex.mp.model_reader import ModelReader
from cplex._internal._subinterfaces import _group

# import cplex
model_fpath = "converted.mps"
# import cplex

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

# feasopt.upper_bound_constraints()._gp
# feasopt.lower_bound_constraints()._gp
# feasopt.linear_constraints()._gp
from typing import List  # , Dict, Callable
from typing_extensions import Literal

group_mode = Literal["linear", "upper_bound", "lower_bound"]
# transfunc_map: Dict[group_mode, Callable] = {}


def group_items(namelist: List[str], mode: group_mode):
    # TODO: fix this!
    which = getattr(feasopt.constraint_type, mode)
    conv = feasopt._getconvfunc(which)
    # max_num = feasopt._getnum(which)
    nameset = set(namelist)
    gp = [(1.0, ((which, conv(name)))) for name in nameset]
    ret = _group(gp)
    # return getattr(feasopt, f"{mode}_constraints")(list(set(namelist)))
    return ret


from functools import reduce


def merge_groups(*args: _group):
    gp = reduce(lambda x, y: getattr(x, "_gp", x) + y._gp, args)
    ret = _group(gp)
    return ret


import pdb

# pdb.set_trace()
constraint_type_constant_map = {
    key: value
    for key, value in feasopt.constraint_type.__class__.__dict__.items()
    if not key.startswith("_")
}

# first count our constraints stat.
# constraint_instance_count_map = {}
# mdl.iter_indicator_constraints()
# mdl.iter_quadratic_constraints()

# for it in mdl.iter_linear_constraints():
#     # print(it)
#     it_name = it.name
#     print("linear constraint %s" % it_name)
#     # do you have to view it here?
#     # breakpoint()
#     # pdb.set_trace()

forbidden_constraint_types = ["quadratic", "indicator"]

for ctype, type_const in constraint_type_constant_map.items():
    # constraint_instance_count_map[ctype] = feasopt._getnum(type_const)
    instance_count = feasopt._getnum(type_const)
    print(f"{ctype}:\t{instance_count} instances")
    # transfunc_map[ctype] = feasopt._getconvfunc(type_const)

lb_group = group_items(["x4487", "x4488"], "lower_bound")
ub_group = group_items(["x4487", "x4488"], "upper_bound")
linear_group = group_items(["c_e_x4508_", "c_e_x4507_"], "linear")
constraints_group = merge_groups(lb_group, ub_group, linear_group)
print(constraints_group)
# pdb.set_trace()
# feasopt(constraints_group)
feasopt(feasopt.all_constraints())
# cplex._internal._aux_functions._group
# feasopt._make_group
sol = mdl.cplex.solution  # this is taking eternal. we need to check progress!
print("*" * 60)
print(sol)
# relatex_sol =
