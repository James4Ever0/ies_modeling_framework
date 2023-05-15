
from lib_parse_params import main_parser, csv_parser

xlsx_worklist = [
    ("设备信息库各参数", "设备参数", "device_params_intermediate"),
    # cannot work with all excel. damn it.
    # ("设备接口", "微电网参数", "microgrid_device_params_intermediate"),
]

for (filepath, sheet_name, output_path) in xlsx_worklist:
    main_parser(f"{filepath}.xlsx", sheet_name, f"{output_path}.json")
    print("____")

csv_worklist = [
("设备接口-微电网参数", "microgrid_device_params_intermediate"),
]

for (filepath, output_path) in csv_worklist:
    csv_parser(filepath, output_path)
    print("____")