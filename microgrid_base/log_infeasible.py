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
import logging

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

solver = SolverFactory("cplex")
# solver = SolverFactory("glpk")
solution = solver.solve(m, tee=False)
log_infeasible_constraints(m, log_expression=True, log_variables=True)
import io
mstream = io.StringIO()
import sys
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
# logging.basicConfig(stream=mstream, level=logging.INFO)
# logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
print(value(m.z))

logging_data = mstream.read()
print("LOGGING DATA:", logging_data)