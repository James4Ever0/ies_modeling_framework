# first get the titles.
import openpyxl

filepath = "设备信息库各参数.xlsx"

excel_file = openpyxl.load_workbook(filepath)

sheet1 = excel_file["设备参数"]

