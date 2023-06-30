from pyomo.environ import (
    Param,
    ConcreteModel,
    Var,
    Objective,
    ConstraintList,
    value,
    minimize,
)
from pyomo.opt import SolverFactory
from pyomo.util.infeasible import log_infeasible_constraints

m = ConcreteModel()
m.LE = set([1, 2, 3])
m.x = Var(m.LE, initialize=0)
m.M = Param(initialize=1000000)


def obj_rule(m):
    return sum(m.x[i] * 1 for i in m.LE)


m.z = Objective(rule=obj_rule, sense=minimize)
m.cons1 = ConstraintList()

for i in m.LE:
    m.cons1.add(10**2 * m.x[i] >= m.M)
    m.cons1.add(10**2 * m.x[i] <= -3)

import io
mstream = io.StringIO()

import sys
import logging
# logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logging.basicConfig(stream=mstream, level=logging.INFO)

solver = SolverFactory("cplex")
# solver = SolverFactory("glpk")
solution = solver.solve(m, tee=True)
# after solving.
log_infeasible_constraints(m, log_expression=True, log_variables=True)
print()
print("SOLVER STATUS?",solution.solver.status)
print("TERMINATION CONDITION?",solution.solver.termination_condition) # infeasible.

# logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
print(value(m.z))

mstream.seek(0)
logging_data = mstream.read()
# alternative:
# logging_data = mstream.getvalue()
mstream.truncate(0)
print("LOGGING DATA:")
print(logging_data)