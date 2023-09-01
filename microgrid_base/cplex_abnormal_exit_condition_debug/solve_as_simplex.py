# define a milp problem, convert integer variables into reals, solve it as lp

from pyomo.environ import *


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
                v.setlb()
                v.setub()
                v.domain = ...
        


model = ConcreteModel()
model.a = Var(domain=Integers, bounds=(-0.5, 5.5))
model.b = Var(domain=Boolean, bounds=(0.3, 1.1))  # feasible, if value(model.b) == 1


# breakpoint()
model.o = Objective(expr=model.a + model.b, sense=minimize)

solver = SolverFactory("cplex")

ret = solver.solve(model, tee=True)

model_clone = model.clone()

TransformationFactory('core.relax_integrality').apply_to(model_clone)

ret_clone = solver.solve(model_clone, tee=True)

with simplexDelegationContext(model):
    ret_delegated = solver.solve(model, tee=True)


results = {"ret": ret, "ret_clone": ret_clone, "ret_delegated": ret_delegated}

for res_name, res in results.items():
    ...