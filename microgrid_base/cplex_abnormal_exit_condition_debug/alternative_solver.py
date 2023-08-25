# ref: https://yalmip.github.io/debuggingunbounded
# solve the model without objective?

# add bounds to objective expression
# note that won't indicate all infinite rays
# you spot one, you fix one.
MAX_BOUND = 1e8

# pyomo can utilize any solver without version specific libraries.
from pyomo.environ import *
import os


from contextlib import contextmanager
import weakref


def getModelSolution(model: ConcreteModel):
    solution = {}
    for v in model.component_data_objects(ctype=Var, active=True, descend_into=True):
        varName = v.name
        val = value(v, exception=None)
        if val is not None:
            solution[varName] = val
        else:
            return None
    return solution


NULL_SOLUTIONS = [None, {}]

is_null_solution = lambda sol: sol in NULL_SOLUTIONS

def model_write(model:ConcreteModel, name):
    # for fmt in 'lp', 'nl':
    for fmt in ['lp', 'nl']:
        model.write(filename=f"{name}.{fmt}")

def checkIfSolved(sol_before, sol_after):
    if is_null_solution(sol_after):
        return False
    elif is_null_solution(sol_before):
        return True
    else:
        return sol_before != sol_after


from copy import deepcopy


@contextmanager
def modelSolutionContext(model):
    class ModelSolutionChecker:
        def __init__(self, model_wr):
            self.model_wr = model_wr
            self.previous_solution = None
            self.update()

        @property
        def model(self):
            return self.model_wr()

        @property
        def solution(self):
            return getModelSolution(self.model)

        def update(self):
            self.previous_solution = deepcopy(self.solution)

        def check(self, update=False):
            ret = checkIfSolved(self.previous_solution, self.solution)
            if update:
                self.update()
            return ret

    modelSolutionChecker = ModelSolutionChecker(weakref.ref(model))
    try:
        yield modelSolutionChecker
    finally:
        del modelSolutionChecker


def clearModelVariableValues(model: ConcreteModel):
    for v in model.component_data_objects(ctype=Var, active=True, descend_into=True):
        v: Var
        v.clear()  # clear value.


import pytz

# with respect to our dearly Py3.6
timezone_str = "Asia/Shanghai"
# timezone = pytz.timezone(timezone_str:='Asia/Shanghai')
timezone = pytz.timezone(timezone_str)
# import logging
import datetime

now = datetime.datetime.now(tz=timezone)
print("Current time: " + now.isoformat())
print("=" * 60)

solver_name = os.environ["SOLVER_NAME"]
warm_start = os.environ.get("WARM_START", None) is not None

print("running solver " + solver_name)
print(f"warm start? {repr(warm_start)}")
print("=" * 60)
# that is during presolve, not during solve.
# from pyomo.contrib.iis import write_iis

model = ConcreteModel()
x = model.变量x = Var()
y = model.变量y = Var()
if warm_start:
    x.set_value(0.5)
    y.set_value(0.5)
model.constraint_x_y = Constraint(expr=x + y >= 10)
model.constraint_x_y_inv = Constraint(expr=x + y <= 9)
model.constraint_x_y_inv.deactivate()
z = model.z = Var([0, 1])

x.setlb(-10)
x.setub(10)

obj_expr = 2 * x - 5 + y + z[0] + z[1] + 3 * (z[0] + y) + 10


obj = model.obj = Objective(expr=obj_expr, sense=minimize)
model_write(model, "no_bound")

# warning: shall not be NaN
# from cmath import nan
# no_obj = model.no_obj = Objective(expr=nan, sense=minimize) # treated as 0
no_obj = model.no_obj = Objective(expr=0)

# write_iis(model, "no_bound.ilp", "cplex")
# no conflict! how comes? it is unbounded.

solver = SolverFactory(solver_name)
if warm_start:
    solver_name += "_warmstart"
# switch lp algorithm
# ref: https://www.ibm.com/docs/en/icos/20.1.0?topic=parameters-algorithm-continuous-linear-problems"
# working?
# solver.options['lpmethod'] = 1  # 0(automatic)-6(concurrent)

# solver.options["timelimit"] = 15
# solver.options["conflict display"] = 2  # detailed display
# not working.
# solver.options['feasopt tolerance'] = 100 # seems not working.
# solver.options['feasopt mode'] = 5 # 0(default)-5
# cannot be too big.
# solver.options['simplex tolerances optimality'] = 1e-1
smap_ids = []
model.obj.deactivate()

solver_name_base = solver_name.split("_")[0]
# pass interactive options instead of commandline option.
# solver.options["warm_start_init_point"] = True

# scan for "Number of Iterations" in output. get the number and set it here. (n-1)
# ref: https://coin-or.github.io/Ipopt/OPTIONS.html#OPT_Termination
if solver_name_base == "ipopt":
    # solver.options['acceptable_iter'] = 10
    # solver.options['max_iter'] = 10
    solver.options["max_iter"] = 3000
    # solver.options['max_iter'] = 33-1
    # solver.options['diverging_iterates_tol'] = 1e10
    # solver.options['tol'] = 1e30
    # solver.options['inf_pr_output'] = 'internal'


def solver_solve(model: ConcreteModel, **kwargs):
    with modelSolutionContext(model) as modelSolutionChecker:
        ret = solver.solve(
            model,
            **kwargs,
            **(
                dict(warmstart=True)
                if warm_start
                # if warm_start and solver_name_base not in ["ipopt"]
                else {}
            ),
        )
        solved = modelSolutionChecker.check()
        ret["solved"] = solved
        return ret


import traceback

try:
    result_no_obj = solver_solve(
        model,
        tee=True,
        logfile=f"no_obj_solver_{solver_name}.log",
    )
except:
    traceback.print_exc()
    raise Exception(f"solver {solver_name.split('_')[0]} does not support warmstart")
smap_ids.append(solver._smap_id)
print(f"X={value(x)}, Y={value(y)}")
print()
print("=" * 70)

model.no_obj.deactivate()
model.obj.activate()
# model.bound_obj.deactivate()
result_unbound = solver_solve(
    model, tee=True, logfile=(unbound_logfile := f"unbound_solver_{solver_name}.log")
)
import re

smap_ids.append(solver._smap_id)

ITERATION_KW = "Number of Iterations"
if solver_name_base == "ipopt":
    # these are forced exits. could get results nevertheless.
    if result_unbound.solver.termination_condition not in [
        TerminationCondition.maxIterations,
        TerminationCondition.maxTimeLimit,
        TerminationCondition.maxEvaluations,  # what is this?
    ]:
        with open(unbound_logfile, "r") as f:
            content = f.read()
            content_lines = content.split("\n")
            for line in content_lines:
                if ITERATION_KW in line:
                    iteration = re.search(r"\d+", line).group()
                    print("ITERATION: ", iteration)
                    solver.options["max_iter"] = int(iteration) - 1
                    result_unbound_rerun = solver_solve(
                        model,
                        tee=True,
                        logfile=(
                            unbound_logfile := f"unbound_solver_{solver_name}_rerun.log"
                        ),
                    )
                    smap_ids.append(solver._smap_id)
                    break


print()
print("=" * 70)

# no need to create new objective. just limit the objective expression to bounds.
mobjVar = model.mobjVar = Var()
mobjVar.setub(MAX_BOUND)
mobjVar.setlb(-MAX_BOUND)
model.constraint_bound_obj = Constraint(expr=mobjVar == obj_expr)
# bound_obj = model.bound_obj = Objective(expr=mobjVar, sense=minimize)

# model.obj.deactivate()
# model.bound_obj.activate()
clearModelVariableValues(model)
result_bound = solver_solve(model, tee=True, logfile=f"bound_solver_{solver_name}.log")
smap_ids.append(solver._smap_id)

# if solver_name_base == "ipopt":
#     breakpoint()

# you still need to set time limit options over this.

solverResultDiagosticInfo = (
    lambda banner, solverResult: "%s TERMINATION CONDITION: %s; SOLVED: %s"
    % (banner, solverResult.solver.termination_condition, solverResult["solved"])
)
printSolverResultDiagosticInfo = lambda banner, solverResult: print(
    solverResultDiagosticInfo(banner, solverResult)
)

printSolverResultDiagosticInfo("UNBOUND", result_unbound)

if solver_name_base == "ipopt":
    if "result_unbound_rerun" in globals().keys():
        printSolverResultDiagosticInfo("UNBOUND RERUN", result_unbound_rerun)

printSolverResultDiagosticInfo("BOUND", result_bound)

# now analyze what variable is doing havoc to the model.

from pyomo.core.expr import current as EXPR


# class ExpressionDecomposer(EXPR.SimpleExpressionVisitor):
#     def __init__(self):
#         # self.counter = 0
#         self.varmap = {}

#     def visit(self, node):
#         # self.counter += 1
#         print(node)
#         print(type(node))
#         # breakpoint()
#         print("_____")

#     def finalize(self):
#         return self.varmap

# def decomposeExpression(expr):
#     #
#     # Create the visitor object
#     #
#     visitor = ExpressionDecomposer()
#     #
#     # Compute the varmap using the :func:`xbfs` search method.
#     #
#     varmap = visitor.xbfs(expr)
#     return varmap
from typing import TypedDict, Dict


class DecomposedExpression(TypedDict):
    constant: float
    varNameToVarObject: Dict[str, str]
    varNameToVarCoefficient: Dict[str, float]


def decomposeExpression(expr):
    const = 0
    varNameToVarObject = {}
    varNameToVarCoefficient = {}
    is_linear, terms = EXPR.decompose_term(expr)
    if is_linear:
        for coef, var in terms:
            if var is None:
                const += coef
            else:
                varName = str(var)
                varNameToVarObject[varName] = var
                varNameToVarCoefficient[varName] = (
                    varNameToVarCoefficient.get(varName, 0) + coef
                )
        return DecomposedExpression(
            constant=const,
            varNameToVarObject=varNameToVarObject,
            varNameToVarCoefficient=varNameToVarCoefficient,
        )


from typing import List, Tuple


def getValueListFromValueDict(valueDict: Dict[str, float]):
    valueList = list(valueDict.items())
    return valueList


def sortAndDisplayVarValues(
    valueList: List[Tuple[str, float]], banner: str, head_count=10, reverse=False
):
    print(banner.center(70, "="))  # to be commented out
    valueList.sort(key=lambda x: x[1], reverse=reverse)
    head_count = min(len(valueList), head_count)
    message = [f"reversed: {reverse}", ""]
    for i in range(head_count):
        message.append("%s\t%s" % valueList[i])
    output = "\n".join(message)
    print(output)


decomposedResult = decomposeExpression(obj_expr)
if decomposedResult:
    print(decomposedResult)
    varNameToVarValue = {}
    varNameToTermValue = {}
    for varName, varObj in decomposedResult["varNameToVarObject"].items():
        varValue = value(varObj)
        coef = decomposedResult["varNameToVarCoefficient"][
            varName
        ]  # seems to be no typeddict type checking in pyright
        termValue = coef * varValue
        varNameToVarValue[varName] = varValue
        varNameToTermValue[varName] = termValue

    # sort and display
    valueListOfVarNameToVarValue = getValueListFromValueDict(varNameToVarValue)
    valueListOfVarNameToTermValue = getValueListFromValueDict(varNameToTermValue)
    BANNER_VARNAME_TO_VAR_VALUE = "VAR NAME TO VAR VALUE"
    BANNER_VARNAME_TO_TERM_VALUE = "VAR NAME TO TERM VALUE"
    sortAndDisplayVarValues(valueListOfVarNameToVarValue, BANNER_VARNAME_TO_VAR_VALUE)
    sortAndDisplayVarValues(
        valueListOfVarNameToVarValue, BANNER_VARNAME_TO_VAR_VALUE, reverse=True
    )
    sortAndDisplayVarValues(valueListOfVarNameToTermValue, BANNER_VARNAME_TO_TERM_VALUE)
    sortAndDisplayVarValues(
        valueListOfVarNameToTermValue, BANNER_VARNAME_TO_TERM_VALUE, reverse=True
    )
    print()
    obj_val = value(obj_expr)
    obj_const = decomposedResult["constant"]
    print("(OBJ - OBJ_CONST)?", obj_val - obj_const)
    print("OBJ?", obj_val)
    print("OBJ_CONST?", obj_const)
else:
    print("objective expression is non-linear.")

print("solver smap ids:", smap_ids)  # three unique ids.
# pick up the most recent one to translate the log and exported model (lp format).
