excel_path ="设备信息库各参数.xlsx"

# import openpyxl
import pandas

table_name = "仿真结果"

# excel = openpyxl.load_workbook(excel_path)

table = pandas.read_excel(excel_path, sheet_name=  table_name)

# table = excel[table_name]
print(table)