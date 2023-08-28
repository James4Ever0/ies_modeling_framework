import math


class RRproduct(object):
    index = 0

    def __init__(self, mdl, x, y, x_min, x_max, y_min, y_max, K):
        RRproduct.index += 1
        z = mdl.binary_var_list([i for i in range(K)], name='RRz{0}'.format(RRproduct.index))
        vk = mdl.continuous_var_list([i for i in range(K)], name='RRvk{0}'.format(RRproduct.index))
        mdl.add_constraints(x_min * (1 - z[k]) <= x - vk[k] for k in range(K))
        mdl.add_constraints(x - vk[k] <= x_max * (1 - z[k]) for k in range(K))
        mdl.add_constraints(x_min * z[k] <= vk[k] for k in range(K))
        mdl.add_constraints(vk[k] <= x_max * z[k] for k in range(K))
        delta_y = (y_max - y_min) / (math.pow(2, K))
        self.result = x * y_min + delta_y * sum([math.pow(2, k) * vk[k] for k in range(K)])
        self.yei = mdl.continuous_var(name='RR.yei{0}'.format(RRproduct.index), lb=-1e6)
        mdl.add_constraint(y + self.yei == y_min + delta_y * sum([math.pow(2, k) * z[k] for k in range(K)]))
        smallB = 1e-8
        mdl.add_constraint(self.yei <= 0.5 * delta_y - smallB)
        mdl.add_constraint(self.yei >= -0.5 * delta_y + smallB)

        self.ei = mdl.continuous_var(name='RR.ei{0}'.format(RRproduct.index),lb=-1e6)
        mdl.add_constraint(self.ei <= 0.5*delta_y * x-smallB)
        mdl.add_constraint(self.ei >= -0.5*delta_y * x+smallB)

    def getxy(self):
        return self.result+self.ei

    def gety(self):
        return self.y


class RRSqure(object):
    index = 0

    def __init__(self, mdl, x, x_max, K):
        RRSqure.index += 1
        z = mdl.binary_var_list([i for i in range(K)], name='RRSz{0}'.format(RRSqure.index))
        v = mdl.binary_var_matrix([i for i in range(K)], [j for j in range(K)], name='RRSv{0}'.format(RRSqure.index))

        table2 = mdl.continuous_var_matrix([i for i in range(K)], [j for j in range(K)],
                                           name='RRStable{0}'.format(RRSqure.index))
        xsqure = mdl.continuous_var(name='RRSxsqure{0}'.format(RRSqure.index))

        delta_x = (x_max) / (math.pow(2, K))
        self.xei = mdl.continuous_var(name='RRS.xei{0}'.format(RRSqure.index), lb=-1e6)
        mdl.add_constraint(x + self.xei == delta_x * sum([math.pow(2, k) * z[k] for k in range(K)]))
        smallB = 1e-8
        mdl.add_constraint(self.xei <= 0.5 * delta_x - smallB)
        mdl.add_constraint(self.xei >= -0.5 * delta_x + smallB)
        self.ei = mdl.continuous_var(name='RRs.ei{0}'.format(RRSqure.index), lb=-1e6)
        mdl.add_constraint(self.ei <= 0.25 * delta_x * delta_x+2*0.5*delta_x*(x) - smallB)
        mdl.add_constraint(self.ei >= - delta_x * x + smallB)

        self.xsqure0 = []
        for i in range(K):
            for j in range(K):
                mdl.add_constraint(v[i, j] <= z[i])
                mdl.add_constraint(v[i, j] <= z[j])
                mdl.add_constraint(v[i, j] >= z[i] + z[j] - 1)
                mdl.add_constraint(table2[i, j] == math.pow(2, i + j) * v[i, j])
            self.xsqure0.append(sum([table2[i, j] for j in range(K)]))
        self.xsqure = mdl.sum(self.xsqure0) * delta_x * delta_x

    def getxx(self):
        return self.xsqure+self.ei
    def getx(self):
        return self.x
