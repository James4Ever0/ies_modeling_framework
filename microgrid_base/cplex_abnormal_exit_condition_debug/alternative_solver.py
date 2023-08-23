# ref: https://yalmip.github.io/debuggingunbounded
# solve the model without objective?

# add bounds to objective expression
# note that won't indicate all infinite rays
# you spot one, you fix one.
MAX_BOUND = 1e8

# pyomo can utilize any solver without version specific libraries.
from pyomo.environ import *
import os


solver_name = os.environ['SOLVER_NAME']

# that is during presolve, not during solve.
# from pyomo.contrib.iis import write_iis

model = ConcreteModel()
x = model.变量x = Var()
y = model.变量y = Var()
model.constraint_x_y = Constraint(expr=x + y >= 10)
z = model.z = Var([0, 1])

x.setlb(-10)
x.setub(10)

obj_expr = 2 * x - 5 + y + z[0] + z[1] + 3 * (z[0] + y) + 10


obj = model.obj = Objective(expr=obj_expr, sense=minimize)
model.write(filename="no_bound.lp")

# warning: shall not be NaN
# from cmath import nan
# no_obj = model.no_obj = Objective(expr=nan, sense=minimize) # treated as 0
no_obj = model.no_obj = Objective(expr=0)

# write_iis(model, "no_bound.ilp", "cplex")
# no conflict! how comes? it is unbounded.

solver = SolverFactory(solver_name)

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
result_no_obj = solver.solve(model, tee=True, logfile=f"no_obj_solver_{solver_name}.log")
smap_ids.append(solver._smap_id)
print(f"X={value(x)}, Y={value(y)}")
print()
print("=" * 70)

model.no_obj.deactivate()
model.obj.activate()
# model.bound_obj.deactivate()
result_unbound = solver.solve(model, tee=True, logfile=f"unbound_solver_{solver_name}.log")
smap_ids.append(solver._smap_id)

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
result_bound = solver.solve(model, tee=True, logfile=f"bound_solver_{solver_name}.log")
smap_ids.append(solver._smap_id)

# you still need to set time limit options over this.

print("UNBOUND TERMINATION CONDITION:", result_unbound.solver.termination_condition)
print("BOUND TERMINATION CONDITION:", result_bound.solver.termination_condition)

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

print("solver smap ids:", smap_ids) # three unique ids.
# pick up the most recent one to translate the log and exported model (lp format).