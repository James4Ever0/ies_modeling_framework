# first get the titles.
import openpyxl

filepath = "设备信息库各参数.xlsx"

wb = openpyxl.load_workbook(filepath)
wb.