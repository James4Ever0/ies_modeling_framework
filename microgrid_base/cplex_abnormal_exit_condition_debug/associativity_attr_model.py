from pyomo.environ import *

model = ConcreteModel()
model.a = Var()
model.b = Var([1, 2])
model.pw = Piecewise(
    model.b[1],
    model.a,
    pw_pts=[1, 2, 3],
    pw_repn="MC",
    f_rule=[3, 2, 1],
    pw_constr_type="EQ",
    unbounded_domain_var=True,
)
model.g = Var([1, 2, 3], [4, 5, 6])

model.subm = model.clone()
model.cons = Constraint(expr=model.a >= model.b[2] + model.g[1, 4] - model.subm.b[1])
model.obj = Objective(expr=0, sense=minimize)


import re

BRACKETS_RE = re.compile(r"\[.*?\]")


def getBaseAndOriginalObjectName(obj) -> tuple[str, str]:
    objname = obj.name
    base_objname, _ = BRACKETS_RE.subn("", objname)
    return objname, base_objname


for obj in model.component_data_objects():
    print("\t".join(getBaseAndOriginalObjectName(obj)))

model.write("associativity_output.lp")
print("_" * 60)

for it in model.solutions.symbol_map.values():
    for k, v in it.bySymbol.items():
        print(k, v().name)  # strip away rectangular brackets
# if it is not block, just keep the base name
# if it is, keep its names of components
# for c in [model.b, model.pw]:
for c in [model.a, model.b, model.pw, model.cons, model.subm]:
    if (func := getattr(c, "component_data_objects", None)) is not None:
        for obj in func():
            print("\t".join(getBaseAndOriginalObjectName(obj)))
    else:
        print(c.name)
