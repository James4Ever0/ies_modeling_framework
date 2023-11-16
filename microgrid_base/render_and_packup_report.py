from log_utils import logger_print
import json


def load_json(filename):
    with open(filename, "r") as f:
        content = f.read()
    return json.loads(content)


input_data_fpath = "microgrid_topo_check_test_input.json"
output_data_fpath = "microgrid_test_output_full.json"

input_data = load_json(input_data_fpath)
output_data = load_json(output_data_fpath)

report_output_path = "report_output.md"
report_template_path = f"{report_output_path}.j2"
from jinja_utils import *
import tempfile, os
import shutil

assert shutil.which("7z") is not None, "7z is not installed"

packup_file = "calculation_report.7z"

if os.path.isfile(packup_file):
    logger_print("removing old report file")
    os.remove(packup_file)
elif os.path.exists(packup_file):
    raise Exception(
        'Unable to create file "%s" because of unknown entity occupying the path'
        % packup_file
    )
basepath = os.path.abspath(os.curdir)

input_data_fpath_full = os.path.join(basepath, input_data_fpath)
output_data_fpath_full = os.path.join(basepath, output_data_fpath)
template_path_abs = os.path.join(basepath, report_template_path)
packup_file_full = os.path.join(basepath, packup_file)

from plot_utils import plotMultipleTopologiesFromFile

with tempfile.TemporaryDirectory() as td:
    os.chdir(td)
    report_dir = "report"
    os.mkdir(report_dir)
    report_dir_full = os.path.join(td, report_dir)
    plotMultipleTopologiesFromFile(input_data_fpath_full, report_dir)
    shutil.copy(input_data_fpath_full, report_dir_full)
    shutil.copy(output_data_fpath_full, report_dir_full)
    render_params = dict(
        input_data=input_data,
        output_data=output_data,
        topo_graph_list=[],
        data_dict_list={},
    )
    load_render_and_format(
        template_path_abs,
        report_output_path,
        render_params=render_params,
        banner="Rendering Markdown Report",
        needFormat=False,
    )

    os.system(f"7z a {packup_file} {report_dir}")
    shutil.copy(packup_file, packup_file_full)
    os.chdir(basepath)  # fix the occupation error.

logger_print(f"Packed up at: {packup_file}")
