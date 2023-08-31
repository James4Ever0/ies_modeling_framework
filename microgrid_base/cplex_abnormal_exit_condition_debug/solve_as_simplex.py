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
    for v in model.component_data_objects(Var, active=True):
    try:
        yield
    finally:
        # recover model variable domain & bounds.
        ...


model = ConcreteModel()
model.a = Var(domain=Integers, bounds=(-0.5, 5.5))
model.b = Var(domain=Boolean, bounds=(0.3, 1.1))  # feasible, if value(model.b) == 1


model.o = Objective(expr=model.a + model.b, sense=minimize)

solver = SolverFactory("cplex")
