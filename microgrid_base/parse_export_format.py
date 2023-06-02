excel_path = "设备信息库各参数.xlsx"

from paddle import tolist
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

data ={}

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
            example = rlist[0]
            data[key][-1]['examples'].append(example)
    elif not is_empty(first_elem) and not is_empty(second_elem):
        headings = rlist[:rlist.index("")]
        trough = 2
        data[key] = data.get(key,[])+[{'headings':headings, 'examples':[]}]

import rich
rich.print(data)