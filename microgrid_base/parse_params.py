from lib_parse_params import main_parser, csv_parser

# FLAGS = {"XLSX": False, "CSV": True}
FLAGS = {"XLSX": True, "CSV":True}

xlsx_worklist = [
    ("设备信息库各参数", "设备参数", "device_params_intermediate"),
    # cannot work with all excel. damn it.
    # ("设备接口", "微电网参数", "microgrid_device_params_intermediate"),
]

csv_worklist = [
    ("设备接口-微电网参数", "microgrid_device_params_intermediate"), # this is not enough.
]

if FLAGS["XLSX"]:
    for (filepath, sheet_name, output_path) in xlsx_worklist:
        main_parser(f"{filepath}.xlsx", sheet_name, f"{output_path}.json")
        print("____")


if FLAGS["CSV"]:
    for (filepath, output_path) in csv_worklist:
        csv_parser(f"{filepath}.csv", f"{output_path}.json")
        print("____")
