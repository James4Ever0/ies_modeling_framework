import openpyxl

filepath = "device_parameters_v3.3.xlsx"

excel_file =openpyxl.load_workbook(filename=filepath)
# print(excel_file.sheetnames) # ['Sheet1']

sheet1 = excel_file['Sheet1']

print(sheet1)
print(dir(sheet1))
breakpoint()

cell1 = sheet1.cell(row=1, column=1)

cell1_fill = cell1.fill
cell1_value = cell1.value
cell1_

cell1_column_letter = cell1.column_letter