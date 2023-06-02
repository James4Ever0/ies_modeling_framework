excel_path ="设备信息库各参数.xlsx"

import openpyxl

table_name = "仿真结果"

excel = openpyxl.load_workbook(excel_path)

table = excel[table_name]
print(table)