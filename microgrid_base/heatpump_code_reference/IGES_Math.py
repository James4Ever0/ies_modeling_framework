from docplex.mp.model import Model
import math
import threading
# shall we abandon and rewrite these methods.

valLUT = {}

class RRproduct(object):
    index = 0

    def __init__(self, mdl, x, y, x_min, x_max, y_min, y_max, K):
        """
        Linearize f(x,y) = x*y

        Parameters:
            mdl: Model
            x: continuous variable
            x_min: min value for x
            x_max: max value for x
            y: continuous variable
            y_min: min value for y
            y_max: max value for y
            K: piecewise resolution parameter, which determines the real resolution step count (2**K)
        """
        RRproduct.index += 1
        z = mdl.binary_var_list(
            [i for i in range(K)], name="RRz{0}".format(RRproduct.index)
        )
        vk = mdl.continuous_var_list(
            [i for i in range(K)], name="RRvk{0}".format(RRproduct.index)
        )
        mdl.add_constraints(x_min * (1 - z[k]) <= x - vk[k] for k in range(K))
        mdl.add_constraints(x - vk[k] <= x_max * (1 - z[k]) for k in range(K))
        mdl.add_constraints(x_min * z[k] <= vk[k] for k in range(K))
        mdl.add_constraints(vk[k] <= x_max * z[k] for k in range(K))
        delta_y = (y_max - y_min) / (math.pow(2, K))
        self.result = x * y_min + delta_y * sum(
            [math.pow(2, k) * vk[k] for k in range(K)]
        )
        self.yei = mdl.continuous_var(name="RR.yei{0}".format(RRproduct.index), lb=-1e6)
        mdl.add_constraint(
            y + self.yei
            == y_min + delta_y * sum([math.pow(2, k) * z[k] for k in range(K)])
        )
        smallB = 1e-8
        mdl.add_constraint(self.yei <= 0.5 * delta_y - smallB)
        mdl.add_constraint(self.yei >= -0.5 * delta_y + smallB)

        self.ei = mdl.continuous_var(name="RR.ei{0}".format(RRproduct.index), lb=-1e6)
        mdl.add_constraint(self.ei <= 0.5 * delta_y * x - smallB)
        mdl.add_constraint(self.ei >= -0.5 * delta_y * x + smallB)

    def getxy(self):
        """
        Returns the linearized version of x*y
        """
        return self.result + self.ei

    def gety(self):
        return self.y


# problematic. shall handle the case of x<0, or just add x_min to parameter
# this is just univariate piecewise function. no need for this!
class RRSqure(object):
    index = 0

    def __init__(self, mdl, x, x_max, K):
        """
        Linearize f(x) = x^2

        Parameters:
            mdl: Model
            x: continuous variable
            x_max: max value for x
            K: piecewise resolution parameter, which determines the real resolution step count (2**K)
        """
        # let's override the K.
        # print("OVERRIDING K")
        # this is one of the major problems with speed.
        K = 3
        RRSqure.index += 1
        z = mdl.binary_var_list(
            [i for i in range(K)], name="RRSz{0}".format(RRSqure.index)
        )
        v, table2 = self.var_matrix_init(mdl, K)
        xsqure = mdl.continuous_var(name="RRSxsqure{0}".format(RRSqure.index))

        delta_x = (x_max) / (math.pow(2, K))
        self.xei = mdl.continuous_var(name="RRS.xei{0}".format(RRSqure.index), lb=-1e6)
        self.power_related_method(mdl, x, K, z, delta_x)
        smallB = 1e-8
        mdl.add_constraint(self.xei <= 0.5 * delta_x - smallB)
        mdl.add_constraint(self.xei >= -0.5 * delta_x + smallB)
        self.ei = mdl.continuous_var(name="RRs.ei{0}".format(RRSqure.index), lb=-1e6)
        mdl.add_constraint(
            self.ei <= 0.25 * delta_x * delta_x + 2 * 0.5 * delta_x * (x) - smallB
        )
        mdl.add_constraint(self.ei >= -delta_x * x + smallB)

        self.xsqure0 = []
        self.deep_nested_loop(mdl, K, z, v, table2, delta_x)

    def var_matrix_init(self, mdl, K):
        v = mdl.binary_var_matrix(
            [i for i in range(K)],
            [j for j in range(K)],
            name="RRSv{0}".format(RRSqure.index),
        )

        table2 = mdl.continuous_var_matrix(
            [i for i in range(K)],
            [j for j in range(K)],
            name="RRStable{0}".format(RRSqure.index),
        )

        return v, table2

    def power_related_method(self, mdl, x, K, z, delta_x):
        mdl.add_constraint(
            x + self.xei == delta_x * sum([math.pow(2, k) * z[k] for k in range(K)])
        )

    def deep_nested_loop(self, mdl:Model, K, z, v, table2, delta_x):
        for i in range(2 * K):
            if i not in valLUT.keys():
                valLUT[i] = math.pow(2, i)

        def getval(i, j):
            return valLUT[i + j]
        
        self.deep_constraints(mdl, K, z, v, table2, getval)

        for i in range(K):
            self.xsqure0.append(sum([table2[i, j] for j in range(K)]))

        self.xsqure = mdl.sum(self.xsqure0) * delta_x * delta_x

    def deep_constraints(self, mdl, K, z, v, table2, getval):
        mdl.add_constraints(v[i, j] <= z[i] for i in range(K) for j in range(K))
        mdl.add_constraints(v[i, j] <= z[j] for i in range(K) for j in range(K))
        mdl.add_constraints(v[i, j] >= z[i] + z[j] - 1 for i in range(K) for j in range(K))
        mdl.add_constraints(table2[i, j] == getval(i, j) * v[i, j] for i in range(K) for j in range(K))

    def getxx(self):
        """
        Returns the linearized version of x^2
        """
        return self.xsqure + self.ei

    def getx(self):
        return self.x
