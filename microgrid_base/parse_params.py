from log_utils import logger_print
# FLAGS = {"XLSX": False, "CSV": True}
import os

type_utils_resdir = "type_utils_resources"
fpath_under_type_utils_resdir = lambda fpath: os.path.join(type_utils_resdir, fpath)

TYPE_UTILS_MICROGRID_PORTS = fpath_under_type_utils_resdir("microgrid_ports")
TYPE_UTILS_EXTRA_PORTS = fpath_under_type_utils_resdir("extra_ports")

if __name__ == "__main__":
    FLAGS = {"XLSX": True, "CSV": True}

    from lib_parse_params import main_parser, csv_parser

    xlsx_worklist = [
        ("设备信息库各参数_23_10_11_from_7_24", "基础参数", "device_params_intermediate"),
        # ("设备信息库各参数_23_7_24", "基础参数", "device_params_intermediate"),
        (
            fpath_under_type_utils_resdir("设备接口_10_11"),
            "微电网接口",
            TYPE_UTILS_MICROGRID_PORTS,
        ),
        (
            fpath_under_type_utils_resdir("设备接口_10_11"),
            "新增设备接口",
            TYPE_UTILS_EXTRA_PORTS,
        ),
        # ("设备信息库各参数", "基础参数", "device_params_intermediate"),
        # ("设备信息库各参数", "设备参数", "device_params_intermediate"),
        # cannot work with all excels. damn it.
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
        for filepath, sheet_name, output_path in xlsx_worklist:
            type_utils_parser = False
            if filepath.startswith(type_utils_resdir):
                type_utils_parser = True
            main_parser(f"{filepath}.xlsx", sheet_name, f"{output_path}.json",type_utils_parser)
            logger_print("____")


    if FLAGS["CSV"]:
        for filepath, output_path in csv_worklist:
            csv_parser(f"{filepath}.csv", f"{output_path}.json")
            logger_print("____")
