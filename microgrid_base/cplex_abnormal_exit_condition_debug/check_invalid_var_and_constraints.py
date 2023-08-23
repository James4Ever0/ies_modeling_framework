# assign invalid values to var and constraints.
# see if the system can detect bounds/constraint violations

from pyomo.environ import *

model = ConcreteModel()

model.a = Var(within=Binary)
model.b = Var(within=NonNegativeReals)
model.c = Var(within=NonNegativeIntegers)
model.d = Var(bounds=(-10, 10))
model.e = Var()

model.con1 = Constraint(expr=model.d >= model.c)
model.con2 = Constraint(expr=model.b >= model.c)
model.con3 = Constraint(expr=model.a + model.b <= model.c)

model.pw = Piecewise(
    model.c, model.e, pw_pts=[-100, 0, 100], pw_repn="MC", f_rule=[100, 0, -100]
)

from pyomo.util.infeasible import log_infeasible_constraints
log_infeasible_constraints(model)