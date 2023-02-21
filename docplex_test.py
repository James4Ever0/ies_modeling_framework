# https://blog.csdn.net/VickyVivan/article/details/116429954

from docplex.mp.model import Model
from docplex.mp.conflict_refiner import ConflictRefiner
from docplex.mp.conflict_refiner import ConflictRefinerResult
import numpy as np

# 构建路径-路段相关矩阵
path = 20
link = 20

relevance = np.zeros((path,link))
# list记录每条path对应的link序列，list[i]表示第i条path
list = [[1,11,14,18,20],
        [2,35,14,18,20],
        [2,36,20],
        [1,11,14,19,31],
        [1,11,15,29,31],
        [1,12,25,29,31],
        [1,12,26,37],
        [2,35,14,19,31],
        [2,35,15,29,31],
        [1,11,14,18]]
for i in range(path):
    for j in list[i]:
        relevance[i][j-1]=1
print(relevance)

# 定义模型变量下标
links = [i for i in range(1,link+1)]

# 定义模型类型
mdl = Model('IP')

# 定义变量
x = mdl.binary_var_dict(links, name='x')
print(x[1]) # 注意，x[1]=x_1, 而不是x[0]=x_1

# 定义目标函数
mdl.minimize(mdl.sum(x[j] for j in links))

# 定义约束函数
num = 1 # 约束下标
for i in range(path):
    for k in range(i+1,path):
        mdl.add_constraint(mdl.sum(x[j + 1] * abs(relevance[i, j] - relevance[k, j]) for j in range(link)) >= 1, 'c' + str(num))
        num+=1
for i in range(path):
    mdl.add_constraint(mdl.sum(x[j+1] * relevance[i, j] for j in range(link)) >= 1, 'c' + str(num))
    num+=1

# 检查冲突约束，返回conflicts
conflicts = ConflictRefiner().refine_conflict(mdl)
result = ConflictRefinerResult(conflicts)
result.display()

# # 移除冲突约束，具体情况由上一步检查结果决定
# list = ['c11','c14'] # 手动输入（目前没找到其他方法）
# for item in list:
#     mdl.remove_constraint(item)

# 求解模型
solution = mdl.solve()
print(solution)

