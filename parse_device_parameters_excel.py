import openpyxl

filepath = "device_parameters_v3.3.xlsx"

excel_file =openpyxl.load_workbook(filename=filepath)
# print(excel_file.sheetnames) # ['Sheet1']
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
sheet1= excel_file['Sheet1']
if type(sheet1) == Worksheet:
    # print(sheet1)
    # print(type(sheet1))
    # breakpoint()
    # print(dir(sheet1))
    # breakpoint()

    cell1 = sheet1.cell(row=1, column=1) # cell or merged cell.
    # need to determine its type.
    if type(cell1) == Cell: 
        # print(type(cell1))
        # breakpoint()
        cell1_fill = cell1.fill
        cell1_value = cell1.value
        cell1_column_letter = cell1.column_letter
    elif type(cell1) == MergedCell:
        ...
    else:
        print("Unknown cell type: %s" % type(cell1))