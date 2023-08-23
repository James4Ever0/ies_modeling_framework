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
from typing import Union, Literal, List


class VarViolation(BaseModel):
    bound_violation: float
    vartype_violation: float


# import math

def moderate_violation(violation,tol):
    violation = abs(violation)
    if violation <= tol:
        violation = 0
    return violation

def get_bounds_violation(val, 
    lower_bound: Union[float, None],
    upper_bound: Union[float, None], tol):
    if all([bound is not None for bound in [lower_bound, upper_bound]]):
        assert lower_bound <= upper_bound, "invalid bound ({lower_bound}, {upper_bound})"
    violation = 0
    if lower_bound:
        if val<
    violation = moderate_violation(violation)


def get_boolean_or_integer_violation(val, tol):
    violation = val % 1
    if violation != 0:
        violation = min([violation, 1 - violation])



class VarInfo(BaseModel):
    varName: str
    val: float
    varDomain: Literal[  # usually, just need to check if it is boolean/binary/integer.
        "Reals",
        "PositiveReals",
        "NonPositiveReals",
        "NegativeReals",
        "NonNegativeReals",
        "Integers",
        "PositiveIntegers",
        "NonPositiveIntegers",
        "NegativeIntegers",
        "NonNegativeIntegers",
        "Boolean",
        "Binary",
    ]
    lower_bound: Union[float, None]
    upper_bound: Union[float, None]
    violation: VarViolation


class ConstraintInfo(BaseModel):
    variables: List[VarInfo]
    violation: float
    representation: str


def get_violation_of_infeasible_constraints(model: ConcreteModel, tol=1e-6):
    ...


def get_violation_of_infeasible_bounds_and_vartype(model: ConcreteModel, tol=1e-6):
    ...


def get_violation_of_infeasible_bounds_and_vartype(model: ConcreteModel, tol=1e-6):
    checkers = {}
    results = []
    for var in model.component_data_objects(ctype=Var, descend_into=True):
        varDomain = ...
        varName = var.name
        val = value(var)
        if varDomain in checkers.keys():
            checker = checkers[varDomain]
            violation = checker(
                val, tol
            )  # violation shall be positive when actual violation is greater than tolerance, otherwise zero.
            if violation:
                results.append()
        else:
            raise Exception("unknown vartype: %s" % varDomain)


log_infeasible_constraints(model)
