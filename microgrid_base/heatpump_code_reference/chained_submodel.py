from pyomo.environ import *


def abstractInitParam(initParam: dict):
    return {None: {k: {None: v} for k, v in initParam.items()}}


model = ConcreteModel()
subm_abs = AbstractModel()
subm_abs.a = Var()
# immutable.
# subm_abs.p1 = Param()
# subm_abs.p2 = Param()

subm_abs.p1 = Param(mutable=True)
subm_abs.p2 = Param(mutable=True)
subm_abs.cons1 = Constraint(expr=subm_abs.a <= subm_abs.p1)
subm_abs.cons2 = Constraint(expr=subm_abs.a >= subm_abs.p2)
model.sub = subm_abs.create_instance(
    abstractInitParam({"p2": 10, "p1": 20}), report_timing=True
)
print("================================")
sub2 = subm_abs.create_instance(
    abstractInitParam({"p2": -10, "p1": 10}), report_timing=True
)
model.sub2 = sub2
print("================================")
model.sub3 = sub2.clone()
model.sub3.p1.set_value(30)
model.sub3.p2.set_value(-30)
# inherited?
# still printing timing?

model.a = Var(bounds=(-10, 5))

subm_concrete = ConcreteModel()
subm_concrete.a = Var(bounds=(10, 20))

model.subm_concrete = subm_concrete

# obj_expr =  model.subm_concrete.a + model.a
obj_expr = model.sub.a + model.sub2.a + model.subm_concrete.a + model.a + model.sub3.a

model.obj = Objective(expr=obj_expr, sense=minimize)

solv = SolverFactory("cplex")

ret = solv.solve(model, tee=True)
print(ret)
print()

for c in model.sub.a, model.sub2.a, model.sub3.a, model.subm_concrete.a, model.a:
    print("val?", value(c))
    print("name?", c.name)  # sub.a, sub2.a, subm_concrete.a, a
    print()
