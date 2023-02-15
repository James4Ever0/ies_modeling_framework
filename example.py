# The MIP problem solved in this example is:
#
#   Maximize  x1 + 2 x2 + 3 x3 + x4
#   Subject to
#      - x1 +   x2 + x3 + 10 x4 <= 20
#        x1 - 3 x2 + x3         <= 30
#               x2      - 3.5x4  = 0
#   Bounds
#        0 <= x1 <= 40
#        0 <= x2
#        0 <= x3
#        2 <= x4 <= 3
#   Integers
#       x4

import cplex
from cplex.exceptions import CplexError

# 首先实现定义各参数，包括变量和变量约束等
# 用来在之后方便地添加到优化器里面

# obj 指的是objective 意为目标，
# 也就是要优化的目标（函数x1 + 2 x2 + 3 x3 + x4 的最小值）的系数
my_obj = [1.0, 2.0, 3.0, 1.0]

#ub Upper Bound，上界，分别表示x1,x2,x3,x4的上界，infinity就是无穷大
#（计算机类无穷大是有穷的，所以这个数可以事先修改为一个很大的数如 cplex.infinity = 2147483647
my_ub = [40.0, cplex.infinity, cplex.infinity, 3.0]

#lb Lower Bound，下界，同上理
my_lb = [0.0, 0.0, 0.0, 2.0]

#变量类型，详见https://www.ibm.com/support/knowledgecenter/SSSA5P_12.9.0/ilog.odms.cplex.help/refpythoncplex/html/cplex._internal._subinterfaces.VarTypes-class.html
#ctrlF搜索Class Variables即可
#分别表示4各变量的变量类型，C表示Continuous 连续值（浮点数），I表示Integer
my_ctype = "CCCI"

#给4个变量起个名字
my_colnames = ["x1", "x2", "x3", "x4"]

#约束规则
#rows是约束集的左值，数组类型
#每一个元素为一条约束规则，也为一个数组类型，包含2个元素，前者为约束变量的名称列表，后者为系数关系
my_rows = [[["x1", "x2", "x3", "x4"], [-1.0, 1.0, 1.0, 10.0]],
            [["x1", "x2", "x3"], [1.0, -3.0, 1.0]],
            [["x2", "x4"], [1.0, -3.5]]]

#rhs是约束规则集的右值
my_rhs = [20.0, 30.0, 0.0]

#约束规则集的左右值关系，详见https://www.ibm.com/support/knowledgecenter/SSSA5P_12.9.0/ilog.odms.cplex.help/refcallablelibrary/cpxapi/getsense.html
#L表示小于等于，E表示等于
my_sense = "LLE"

#给各条约束规则起名字
my_rownames = ["r1", "r2", "r3"]

try:
    #实例化一个cplex优化器
    prob = cplex.Cplex()

    #求解的目标为目标函数的最小值
    prob.objective.set_sense(prob.objective.sense.maximize)

    #添加变量：变量在目标函数里的系数，变量的上下界，变量类型，名称
    prob.variables.add(obj=my_obj, lb=my_lb, ub=my_ub, types=my_ctype,
                       names=my_colnames)

    #添加约束：约束左值，等式/不等式符号，右值，名称
    prob.linear_constraints.add(lin_expr=my_rows, senses=my_sense,
                                rhs=my_rhs, names=my_rownames)

    #求解
    prob.solve()

    #显示最优情况下的变量值
    x = prob.solution.get_values()
    print(x)

    #显示最优情况下的目标值
    objective_value = prob.solution.get_objective_value()
    print(objective_value)


except CplexError as exc:
    print(exc)

