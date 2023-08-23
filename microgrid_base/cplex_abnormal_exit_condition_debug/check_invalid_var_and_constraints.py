# assign invalid values to var and constraints.
# see if the system can detect bounds/constraint violations

from pyomo.environ import *

# advanced logical expression linearization using pyomo.GDP
# ref: https://pyomo.readthedocs.io/en/latest/modeling_extensions/gdp/modeling.html
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

# you might need to sort it out. check how much further it goes.
from pyomo.util.infeasible import log_infeasible_constraints, log_infeasible_bounds
from pydantic import BaseModel
from typing import Union, Literal


class ConstraintInfo(BaseModel):
    variables: List[VarInfo]
    violation: float


def get_violation_of_infeasible_constraints(model: ConcreteModel, tol=1e-6):
    ...


class VarViolation(BaseModel):
    bound_violation: float
    vartype_violation: float


class VarInfo(BaseModel):
    varName: str
    val: float
    varType: Literal[""]
    lower_bound: Union[float, None]
    upper_bound: Union[float, None]
    violation: VarViolation


def get_violation_of_infeasible_bounds_and_vartype(model: ConcreteModel, tol=1e-6):
    ...


def get_violation_of_infeasible_bounds_and_vartype(model: ConcreteModel, tol=1e-6):
    checkers = {}
    results = []
    for var in model.component_data_objects(ctype=Var, descend_into=True):
        vartype = ...
        varname = ...
        val = value(var)
        if vartype in checkers.keys():
            checker = checkers[vartype]
            violation = checker(
                val, tol
            )  # violation shall be positive when actual violation is greater than tolerance, otherwise zero.
            if violation:
                results.append()


log_infeasible_constraints(model)
