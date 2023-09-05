import dill
import pickle
from pyomo.environ import *
# ensure you load all files from pyomo_environ


def serializeObjectToFile(obj, filename: str, module=pickle):
    with open(filename, "wb") as f:
        module.dump(obj, f)


def deserializeObjectFromFile(filename: str, module=pickle):
    with open(filename, "rb") as f:
        obj = module.load(f)
        return obj


if __name__ == "__main__":
    fpath = "model.pickle"
    # mode = 'create'
    mode = "load"
    if mode == "create":
        model = ConcreteModel()
        model.a = Var()
        model.b = Var([1, 2])
        model.const = Constraint(expr=model.a <= model.b[1])
        model.obj = Objective(expr=model.a + model.b[1], sense=minimize)

        model.subm = model.clone()

        model.pprint()
        print("-" * 60)
        print("writing model to file: ", fpath)
        print("-" * 60)
        serializeObjectToFile(model, fpath)
    elif mode == "load":
        subm: ConcreteModel = deserializeObjectFromFile(fpath)
        subm.pprint()
    else:
        raise Exception("Unable to determine action from mode '%s'" % mode)
