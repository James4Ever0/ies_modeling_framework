from lib_parse_params import main_parser

worklist = [( "设备信息库各参数.xlsx"
, "设备参数"
, "device_params_intermediate.json"
)]

for (filepath,
sheet_name,
output_path) in worklist:
    