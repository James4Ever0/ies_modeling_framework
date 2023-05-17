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

types = set()

types_connectivity_matrix = {} # {frozenset([start, end]): generated_type}

for start, end, wire_name in coax_triplets:
    connectable_wire_name, unconnectable_wire_name = (
        f"可连接{wire_name}",
        f"不可连接{wire_name}",
    )
    
    types.add(start)
    types.add(end)
    types.add(connectable_wire_name)
    types.add(unconnectable_wire_name)
    
    types_connectivity_matrix.update({frozenset([start, end]):connectable_wire_name})
    types_connectivity_matrix.update({frozenset([start, connectable_wire_name]): unconnectable_wire_name})

import rich
# rich.print(types)

# {
#     '母线输入',
#     '不可连接母线',
#     '可连接储能端母线',
#     '不可连接供电端母线',
#     '母线输出',
#     '供电端输出',
#     '不可连接储能端母线',
#     '双向变流器输入输出',
#     '可连接供电端母线',
#     '储能端输入输出',
#     '可连接母线',
#     '变流器输入'
# }

import json

# keys = []
# with open("microgrid_device_params_intermediate.json",'r') as f:
#     data = json.load(f)
#     for k,v in data.items():
#         for k0, v0 in v.items():
#             keys.append(k0)
            
# rich.print(keys)
csv_path = "设备接口-离网型微电网.csv"

lines = []
line_sep_count_list = []
with open(csv_path,'r') as f:
    for line in f.readlines():
        line_sep_count = line.count(",")
        if line_sep_count == 0:
            continue
        lines.append(line)
        line_sep_count_list.append(line_sep_count)

line_sep_count_max = max(line_sep_count_list)
for index, line_sep_count in enumerate(line_sep_count_list):
    lines[index]= lines[index].strip()+","*(line_sep_count_max-line_sep_count)

with open(csv_path, 'w+') as f:
    for line in lines:
        f.write(line+"\n")

port_df = pandas.read_csv(csv_path, header=None, on_bad_lines='warn')

# print(port_df)

for row in port_df.iterrows():
    