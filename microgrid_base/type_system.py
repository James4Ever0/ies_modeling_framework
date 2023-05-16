import pandas

output_path = "microgrid_type_system.xlsx"

sheet1_name = "类型连接矩阵"
sheet2_name = "设备端口类型表"

# 母线输入 = 0
# 母线输出 = 0
# 储能端输入输出 = 1
# 双向变流器输入输出 = 1
# 可连接母线 = 2
# 不可连接母线 = 2
# 可连接供电端母线 = 3
# 不可连接供电端母线 = 3
# 可连接储能端母线 = 4
# 不可连接储能端母线 = 4
# 供电端输出,变流器输入= 0

coax_triplets = [
    ("供电端输出", "变流器输入", "供电端母线"),
    ("储能端输入输出", "双向变流器输入输出", "储能端母线"),
    ("母线输入", "母线输出", "母线"),
]

matrix

for start, end, wire_name in coax_triplets:
    connectable_wire_name, unconnectable_wire_name = (
        f"可连接{wire_name}",
        f"不可连接{wire_name}",
    )
    