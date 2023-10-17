import pyomo_patch
from pyomo.environ import *
from pyomo.gdp import *
from config import ies_env


def checkDisjunctive(model:ConcreteModel):
    for _ in model.component_data_objects(ctype=Disjunct):
        return True
    return False
    

def transformDisjunctiveModel(model, bigM = 1e8):
    is_disjunctive = checkDisjunctive(model)
    if is_disjunctive: 
        TransformationFactory("gdp.bigm").apply_to(model, bigM=bigM)
    return is_disjunctive