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


def revert_dict(mdict: dict):
    result = {e: k for k, v in mdict.items() for e in v}
    return result


def check_valid_type_base_name(type_base_name):
    try:
        assert "输" not in type_base_name
        assert "出" not in type_base_name
        assert "入" not in type_base_name
    except:
        raise Exception("Invalid type base name:", type_base_name)
    return type_base_name.strip()


def Input(type_base_name):
    type_base_name = check_valid_type_base_name(type_base_name)
    return f"{type_base_name.strip()}输入"


def Output(type_base_name):
    type_base_name = check_valid_type_base_name(type_base_name)
    return f"{type_base_name.strip()}输出"


def IO(type_base_name):
    type_base_name = check_valid_type_base_name(type_base_name)
    return f"{type_base_name.strip()}输入输出"


coax_triplets = {  # Input, Output, ConnectionBaseName
    "电": [
        ("变流器", "供电端", "供电端母线"),
        ("电母线", "电母线", "电母线"),
        ("负荷电", "变压器", "负荷电母线"),
    ],
    "柴油": [
        ("柴油", "柴油", "柴油母线"),
    ],
}

# IO_1, IO_2, ConnectionBaseName
io_coax_triplets = {"电": [("电储能端", "双向变流器储能端", "电储能端母线")]}

#
io_to_wire = {"电": [("双向变流器线路端", "电母线")]}

types = {}  # {str: set()}
wire_types = {}

types_connectivity_matrix = {}  # {frozenset([start, end]): generated_type}


def triplets_with_supertype(triplet_map, length=3):
    for supertype, triplet_list in triplet_map.items():
        for triplet in triplet_list:
            assert len(triplet) == length
            yield (*triplet, supertype)


def get_types(is_wire):
    if is_wire:
        return wire_types
    else:
        return types


def get_other_sets(supertype, is_wire=False):
    mtypes = get_types(is_wire)

    other_sets = set([e for k in mtypes.keys() if k != supertype for e in types[k]])
    return other_sets


def add_to_types(supertype, typename, is_wire=False):
    mtypes = get_types(is_wire)
    if mtypes.get(supertype, None) is None:
        mtypes[supertype] = set()
    if is_wire:
        other_sets = set([e for k, v in types.items() for e in v])
        wire_other_sets = get_other_sets(supertype, is_wire=is_wire)
    else:
        other_sets = get_other_sets(supertype)
        wire_other_sets = set([e for k, v in wire_types.items() for e in v])
    if typename not in other_sets:
        if typename not in wire_other_sets:
            mtypes[supertype].add(typename)
        else:
            raise Exception(
                f"{'Wire ' if is_wire else ''}Type {typename} in category {supertype} appeared to be duplicated with wire types."
            )
    else:
        raise Exception(
            f"{'Wire ' if is_wire else ''}Type {typename} in category {supertype} appeared to be duplicated with device types."
        )


def Connectable(wire_name):
    return f"可连接{wire_name}"


def Unconnectable(wire_name):
    return f"不可连接{wire_name}"


for (io, wire_name, supertype) in triplets_with_supertype(io_to_wire, length=2):
    start = IO(io)
    end = Connectable(wire_name)
    created = Unconnectable(wire_name)

    add_to_types(supertype, start)
    add_to_types(supertype, end, is_wire=True)
    add_to_types(supertype, created, is_wire=True)

    types_connectivity_matrix.update({frozenset([start, end]): created})

a = [(e, True) for e in triplets_with_supertype(io_coax_triplets)]
print(a)
breakpoint()
for (i, o, wire_name, supertype), is_io in ([
    (e, False) for e in triplets_with_supertype(coax_triplets)
] + [(e, True) for e in triplets_with_supertype(io_coax_triplets)]):
    if is_io:
        start = IO(o)
        end = IO(o)
    else:
        start = Input(i)
        end = Output(o)
    connectable_wire_name, unconnectable_wire_name = (
        Connectable(wire_name),
        Unconnectable(wire_name),
    )

    # if types.get(supertype, None) is None:
    #     types[supertype] = set()
    # other_sets = set([e for k in types.keys() if k!=supertype for e in types[k]])
    # if "储能端" in start:
    #     breakpoint()
    add_to_types(supertype, start)
    add_to_types(supertype, end)
    add_to_types(supertype, connectable_wire_name, is_wire=True)
    add_to_types(supertype, unconnectable_wire_name, is_wire=True)

    types_connectivity_matrix.update({frozenset([start, end]): connectable_wire_name})
    types_connectivity_matrix.update(
        {frozenset([start, connectable_wire_name]): unconnectable_wire_name}
    )

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
with open(csv_path, "r") as f:
    for line in f.readlines():
        line_sep_count = line.count(",")
        if line_sep_count == 0:
            continue
        lines.append(line)
        line_sep_count_list.append(line_sep_count)

line_sep_count_max = max(line_sep_count_list)
for index, line_sep_count in enumerate(line_sep_count_list):
    lines[index] = lines[index].strip() + "," * (line_sep_count_max - line_sep_count)

with open(csv_path, "w+") as f:
    for line in lines:
        f.write(line + "\n")

port_df = pandas.read_csv(csv_path, header=None, on_bad_lines="warn")

# print(port_df)
import numpy

mycat = None
device_port_dict = {}
mydevice = None
content_split = True

# 能源端
output_device_with_single_port_to_port_type = revert_dict(
    {
        "柴油": ["柴油"],
        "供电端": ["光伏发电", "风力发电", "柴油发电-电接口"],
        "电母线": ["变流器-电输出","传输线-电输出"],
        "变压器": ["变压器-电输出"],
    }
)


# 负荷端
input_device_with_single_port_to_port_type = revert_dict(
    {"负荷电": ["电负荷"], "柴油": ["柴油发电-燃料接口"], "电母线": ["变压器-电输入", "传输线-电输入"], "变流器": ["变流器-电输入"]}
)

# 储能端
io_device_with_single_port_to_port_type = revert_dict(
    {"电储能端": ["锂电池"], "双向变流器储能端": ["双向变流器-储能端"], "双向变流器线路端": ["双向变流器-线路端"]}
)

device_with_single_port_to_port_type = {
    k: Input(v) for k, v in input_device_with_single_port_to_port_type.items()
}

device_with_single_port_to_port_type.update(
    {k: Output(v) for k, v in output_device_with_single_port_to_port_type.items()}
)


device_with_single_port_to_port_type.update(
    {k: IO(v) for k, v in io_device_with_single_port_to_port_type.items()}
)

mapped_types = set()

rich.print(device_with_single_port_to_port_type)

for index, row in port_df.iterrows():
    # print(row.tolist())
    # print(row.tolist())
    cat, content = row.tolist()[:2]
    print([cat, content])
    if not (cat is numpy.nan or cat is None):
        mycat = cat
        device_port_dict[mycat] = {}  # init
    if mycat:
        if content is numpy.nan or content is None:
            content_split = True
        elif content_split:
            content_split = False
            mydevice = content.replace("（", "(").split("(")[0]
            device_port_dict[mycat][mydevice] = {}
        else:
            # append port?
            port_type = device_with_single_port_to_port_type.get(mydevice, None)
            if port_type:
                device_with_single_port_to_port_type[mydevice] = None
            else:
                port_id = f"{mydevice}-{content}"
                port_type = device_with_single_port_to_port_type.get(port_id, None)
                if port_type:
                    device_with_single_port_to_port_type[port_id] = None
            if port_type is not None:
                device_port_dict[mycat][mydevice][content] = port_type
                mapped_types.add(port_type)
            else:
                # rich.print(device_port_dict)
                # breakpoint()
                raise Exception(
                    "No port type definition for:", (mycat, mydevice, content)
                )
print()
rich.print(device_port_dict)
print()
rich.print(types_connectivity_matrix)
print()
rich.print(types)
if not mapped_types == types:
    mtypes = set([e for k,v in types.items() for e in v])
    print("MAPPED TYPES UNIQ:" ,mapped_types.difference(mtypes))
    print("DEVICE TYPES UNIQ:",mtypes.difference(mapped_types))
    raise Exception("Mapped types does not equal to existing device types")