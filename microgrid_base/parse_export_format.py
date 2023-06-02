excel_path = "设备信息库各参数.xlsx"

import json
import pandas

table_name = "仿真结果"

table = pandas.read_excel(excel_path, sheet_name=table_name, header=None)

# print(table)
def is_empty(elem):
    if type(elem) is str:
        return elem.strip() == ""
    else:
        return True


trough = 0

data = {}

for i, r in table.iterrows():
    rlist = [(e.strip() if type(e) == str else "") for e in r.tolist()]
    first_elem, second_elem = rlist[0], rlist[1]

    if is_empty(first_elem):
        trough = 0
    elif not is_empty(first_elem) and is_empty(second_elem):
        if trough == 0:
            trough = 1
            key = first_elem
        elif trough == 2:
            device = rlist[0]
            data[key][-1]["devices"].append(device)
    elif not is_empty(first_elem) and not is_empty(second_elem):
        headings = rlist[: rlist.index("")]
        trough = 2
        data[key] = data.get(key, []) + [{"headings": headings, "devices": []}]

import rich

# need processing.
rich.print(data)

output_path = "export_format.json"

print("writing to:", output_path)

new_data = {k:{} for k in data.keys()}


def convert_format(h_array):
    result_array = []
    return result_array

new_data['仿真结果']['ALL'] = convert_format(data['仿真结果'][0]['headings'])

from param_base import 设备接口集合
all_device_names = list(设备接口集合.keys())

print()
print(new_data)
with open(output_path, "w+") as f:
    f.write(json.dumps(new_data, indent=4, ensure_ascii=False))

# type? sum or array.
# unit conversion? divide by conversion rate.
# in unit conversion exception list? check.
# matched to which port?