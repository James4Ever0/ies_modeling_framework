excel_path ="设备信息库各参数.xlsx"

from paddle import tolist
import pandas

table_name = "仿真结果"

table = pandas.read_excel(excel_path, sheet_name=  table_name, header=None)

# print(table)
def is_empty(elem):
    if type(elem) is str:
        return elem.strip() == ""
    else:
        return True

for i, r in table.iterrows():
    rlist = r.tolist()