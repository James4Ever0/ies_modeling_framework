# first get the titles.
import openpyxl

filepath = "设备信息库各参数.xlsx"

excel_file = openpyxl.load_workbook(filepath)

sheet1 = excel_file["设备参数"]

dims = sheet1.row_dimensions, sheet1.column_dimensions

uniqs = {}

def getColumnRangePerRow(start, end):
    flag = True
    for index, row in enumerate(sheet1.rows):
        if flag:
            flag = False
            continue
        yield index, [col.value for col in row[start:end]]

heads = getColumnRangePerRow(0, 1)

for i, cvals in heads:
    print(i)
    print(cvals)
    print()