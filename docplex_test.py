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
