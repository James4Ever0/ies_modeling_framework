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


trough = True

data ={}

for i, r in table.iterrows():
    rlist = [(e.strip() if type(e) == str else e) for e in r.tolist()]
    first_elem, second_elem = rlist[0], rlist[1]
    
    if is_empty(first_elem):
        trough = True
    elif not is_empty(first_elem) and is_empty(second_elem):
        trough = True
        key = first_elem
    elif not is_empty(first_elem) and not is_empty(second_elem):
        if trough:
            ...
            trough = False
        else:
            ...