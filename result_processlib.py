import docplex
# from docplex.mp.model import Model
import numpy


class Value(object):
    def __init__(self, sol):
        self.sol = sol

    def value(self, x):
        if isinstance(x, int):
            return x
        elif isinstance(x, float):
            print('float')
            return x
        elif isinstance(x, list) and isinstance(x[0], docplex.mp.dvar.Var):
            return self.sol.get_values(x)
        elif isinstance(x, docplex.mp.dvar.Var):
            return self.sol.get_value(x)
        elif isinstance(x, list) and isinstance(x[0], int):
            return x
        elif isinstance(x, list) and isinstance(x[0], float):
            return x
        elif isinstance(x, numpy.ndarray):
            return x

        else:
            print('type error')
            return None
