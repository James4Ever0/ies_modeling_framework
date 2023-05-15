from lib_parse_params import main_parser

worklist = [("设备信息库各参数", "设备参数", "device_params_intermediate"), ("", "", "microgrid_device_params")]

for (filepath, sheet_name, output_path) in worklist:
    main_parser(f"{filepath}.xlsx", sheet_name, f"{output_path}.json")
