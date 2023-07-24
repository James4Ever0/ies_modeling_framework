from lib_parse_params import main_parser, csv_parser

# FLAGS = {"XLSX": False, "CSV": True}
FLAGS = {"XLSX": True, "CSV": True}

xlsx_worklist = [
    ("设备信息库各参数_23_7_24", "基础参数", "device_params_intermediate"),
    # ("设备信息库各参数", "基础参数", "device_params_intermediate"),
    # ("设备信息库各参数", "设备参数", "device_params_intermediate"),
    # cannot work with all excel. damn it.
    # ("设备接口", "微电网参数", "microgrid_device_params_intermediate"),
]

csv_worklist = [
    ("设备接口-微电网参数", "microgrid_device_params_intermediate"),  # this is not enough.
]

MAKEFILE = dict(
    inputs=[e[0] + ".csv" for e in csv_worklist]
    + [e[0] + ".xlsx" for e in xlsx_worklist],
    outputs=[e[-1] + ".json" for e in csv_worklist + xlsx_worklist],
    args=[],
)

if FLAGS["XLSX"]:
    for (filepath, sheet_name, output_path) in xlsx_worklist:
        main_parser(f"{filepath}.xlsx", sheet_name, f"{output_path}.json")
        print("____")


if FLAGS["CSV"]:
    for (filepath, output_path) in csv_worklist:
        csv_parser(f"{filepath}.csv", f"{output_path}.json")
        print("____")
