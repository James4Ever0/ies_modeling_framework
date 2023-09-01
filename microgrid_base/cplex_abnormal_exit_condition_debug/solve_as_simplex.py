# define a milp problem, convert integer variables into reals, solve it as lp

from pyomo.environ import *


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


domainDelegationTable = {
    "NonNegativeIntegers": NonNegativeReals,
    "NonPositiveIntegers": NonPositiveReals,
    "Boolean": Reals,
}

domainDelegationBoundsTable = {"Boolean": (0, 1)}

from contextlib import contextmanager


@contextmanager
def simplexDelegationContext(model: ConcreteModel):
    """
    This context manager is used to delegate the domain and bounds of integer variables to the reals.

    Delegation will be cancelled if exiting the manager.
    """
    delegationRestoreTable = {}
    for v in model.component_data_objects(Var, active=True):
        varName = v.name
        domainName = v.domain.name
        lb, ub = v.lb, v.ub
        if domainName in domainDelegationTable.keys():
            delegationRestoreTable[varName] = {
                "domain": v.domain,
                "lb": v.lb,
                "ub": v.ub,
            }
            v.domain = domainDelegationBoundsTable[domainName]
            if domainName in domainDelegationBoundsTable.keys():
                domain_lb, domain_ub = domainDelegationBoundsTable[domainName]
                if lb is None:
                    lb = domain_lb
                if ub is None:
                    ub = domain_ub
                v.setlb(max(lb, domain_lb))
                v.setub(min(ub, domain_ub))
    try:
        yield
    finally:
        # recover model variable domain & bounds.
        for v in model.component_data_objects(Var, active=True):
            varName = v.name
            if varName in delegationRestoreTable.keys():
                restoreInfo = delegationRestoreTable[varName]
                v.setlb(restoreInfo["lb"])
                v.setub(restoreInfo["ub"])
                v.domain = restoreInfo["domain"]
        del delegationRestoreTable


solver = SolverFactory("cplex")


def solver_solve(model):
    ret = solver.solve(model, tee=True)
    sol = getModelSolution(model)
    return ret, sol


model = ConcreteModel()
model.a = Var(domain=Integers, bounds=(-0.5, 5.5))
model.b = Var(domain=Boolean, bounds=(0.3, 1.1))  # feasible, if value(model.b) == 1

model.o = Objective(expr=model.a + model.b, sense=minimize)


ret = solver_solve(model)

model_clone = model.clone()

TransformationFactory("core.relax_integrality").apply_to(model_clone)
# working
ret_clone = solver_solve(model_clone)

with simplexDelegationContext(model):
    # not working
    ret_delegated = solver_solve(model)


results = {"ret": ret, "ret_clone": ret_clone, "ret_delegated": ret_delegated}

import rich

for res_name, res in results.items():
    ret, sol = res
    print("result name:", res_name)
    rich.print(res)
    print(sol)
