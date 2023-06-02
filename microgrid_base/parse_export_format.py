excel_path ="设备信息库各参数.xlsx"

import pandas

table_name = "仿真结果"

table = pandas.read_excel(excel_path, sheet_name=  table_name)

# print(table)
for i, r in table.iterrows():
    print(i)
    print(r)