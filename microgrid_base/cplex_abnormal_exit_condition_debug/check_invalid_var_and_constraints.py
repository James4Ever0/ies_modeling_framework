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
# from pyomo.util.infeasible import log_infeasible_constraints,

from pydantic import BaseModel
from typing import Union, Literal, List


def get_var_or_constraint_bounds(var: Var):
    if var.has_lb():
        lb = value(var.lower, exception=False)
    if var.has_ub():
        ub = value(var.lower, exception=False)
    return lb, ub


class VarViolation(BaseModel):
    bound_violation: float
    vartype_violation: float

    @property
    def has_violation(self):
        return any([v > 0 for v in [self.bound_violation, self.vartype_violation]])


# import math


def moderate_violation(violation, tol):
    violation = abs(violation)
    if violation <= tol:
        violation = 0
    return violation


def get_bounds_violation(
    val: float,
    lower_bound: Union[float, None],
    upper_bound: Union[float, None],
    tol: float,
):
    if all([bound is not None for bound in [lower_bound, upper_bound]]):
        assert (
            lower_bound <= upper_bound
        ), "invalid bound ({lower_bound}, {upper_bound})"
    violation = 0
    if lower_bound is not None:
        if val < lower_bound:
            violation = abs(val - lower_bound)
    if violation == 0:
        if upper_bound is not None:
            if val > upper_bound:
                violation = abs(val - upper_bound)
    return moderate_violation(violation, tol)


def get_boolean_or_integer_violation(val: float, tol: float):
    violation = val % 1
    if violation != 0:
        violation = min([violation, 1 - violation])

    return moderate_violation(violation, tol)


def constructVarChecker(domainName: str, domainBounds):
    def checker(var: Var, tol: float):
        val = value(var)
        var_bounds = get_var_or_constraint_bounds(var)
        bounds_violation = get_bounds_violation(val, *var_bounds, tol)

        vartype_violation = get_bounds_violation(val, *domainBounds, tol)
        if vartype_violation == 0:
            if "Integers" in domainName or domainName in ["Boolean", "Binary"]:
                vartype_violation = get_boolean_or_integer_violation(val, tol)
        varViolation = VarViolation(
            bound_violation=bounds_violation, vartype_violation=vartype_violation
        )
        return varViolation

    return checker


from functools import lru_cache


@lru_cache(maxsize=1)
def getVarCheckers():
    varDomainObjs = [
        Reals,
        PositiveReals,
        NonPositiveReals,
        NegativeReals,
        NonNegativeReals,
        Integers,
        PositiveIntegers,
        NonPositiveIntegers,
        NegativeIntegers,
        NonNegativeIntegers,
        Boolean,
        Binary,
    ]
    checkers = {}
    for varDomainObj in varDomainObjs:
        domainName = varDomainObj.name
        domainBounds = varDomainObj.bounds()
        checker = constructVarChecker(domainName, domainBounds)
        checkers[domainName] = checker
    return checkers


class VarInfo(BaseModel):
    varName: str
    val: float
    domainName: Literal[  # usually, just need to check if it is boolean/binary/integer.
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
    is_linear: bool

    @property
    def has_violation(self):
        # TODO: consider overall violation among variables inside constraint
        return self.violation > 0


from pyomo.core.expr import current as EXPR


def get_violation_of_infeasible_bounds_and_vartype_of_single_var(var: Var, tol=1e-6):
    checkers = getVarCheckers()
    domainName = var.domain._name
    varName = var.name
    val = value(var)
    if domainName in checkers.keys():
        checker = checkers[domainName]
        varViolation, lower_bound, upper_bound = checker(
            var, tol
        )  # violation shall be positive when actual violation is greater than tolerance, otherwise zero.
        if varViolation.has_violation:
            varInfo = VarInfo(
                varName=varName,
                val=val,
                domainName=domainName,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
                violation=varViolation,
            )
            return varInfo
    else:
        raise Exception("unknown domain name: %s" % domainName)


from typing import Dict


def getVarInfoListFromVarInfoDict(varInfoDict: Dict[str, VarInfo]):
    varInfoList = list(varInfoDict.values())
    return varInfoList


def decompose_linear_constraint_from_terms_and_get_variable_info(terms):
    varInfoDict = {}
    for coef, var in terms:
        if var is not None:
            varName = str(var)
            if varName not in varInfoDict.keys():
                varInfoDict[
                    varName
                ] = get_violation_of_infeasible_bounds_and_vartype_of_single_var(var)
    return varInfoDict


from pyomo.core.base.var import *

VarType = Union[Var, _VarData, _GeneralVarData, VarList, SimpleVar, ScalarVar]


def walk_expression(expr: Expression):
    if args := getattr(expr, "args", None) is not None:
        for arg in args:
            if isinstance(arg, VarType):
                yield arg
            else:
                yield from walk_expression(arg)


def decompose_nonlinear_constraint_and_get_variable_info_dict(constr: Constraint):
    varInfoDict = {}
    for term in walk_expression(constr.body):
        ...
    return varInfoDict


def decompose_constraint_and_get_variable_info(constr: Constraint):
    is_linear, terms = EXPR.decompose_term(constr.body)

    # decompose non-linear constraints.
    if is_linear:
        varInfoDict = decompose_linear_constraint_from_terms_and_get_variable_info(
            terms
        )
    else:
        varInfoDict = decompose_nonlinear_constraint_and_get_variable_info_dict(constr)
    varInfoList = getVarInfoListFromVarInfoDict(varInfoDict)
    return is_linear, varInfoList


def get_violation_of_infeasible_constraints(model: ConcreteModel, tol=1e-6):
    results = []
    # you can deactivate some constraints.
    # model.constraint.activate()
    # model.constraint.deactivate()
    for constr in model.component_data_objects(
        ctype=Constraint, active=True, descend_into=True
    ):
        body_value = value(constr.body, exception=False)
        constraint_bounds = get_var_or_constraint_bounds(constr)
        if body_value is not None:
            violation = get_bounds_violation(body_value, constraint_bounds, tol)
            if violation != 0:
                representation = str(constr.expr)
                is_linear, varInfoList = decompose_constraint_and_get_variable_info(
                    constr
                )
                constraintInfo = ConstraintInfo(
                    is_linear=is_linear,
                    variables=varInfoList,
                    violation=violation,
                    representation=representation,
                )
                results.append(constraintInfo)
    return results


def get_violation_of_infeasible_bounds_and_vartype(model: ConcreteModel, tol=1e-6):
    results = []
    for var in model.component_data_objects(ctype=Var, descend_into=True):
        varInfo = get_violation_of_infeasible_bounds_and_vartype_of_single_var(var, tol)
        results.append(varInfo)

    return results


# log_infeasible_constraints(model)
