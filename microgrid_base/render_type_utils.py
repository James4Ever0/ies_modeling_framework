from log_utils import logger_print
from jinja_utils import *
from parse_params import TYPE_UTILS_MICROGRID_PORTS, TYPE_UTILS_EXTRA_PORTS
import json


def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


output_path, template_path = code_and_template_path("type_utils")

render_params = {}


def assert_is_nonempty_dict(d):
    assert isinstance(d, dict)
    assert d != {}


for fpath in [TYPE_UTILS_MICROGRID_PORTS, TYPE_UTILS_EXTRA_PORTS]:
    logger_print("Loading:", fpath)
    dat = load_json(fpath + ".json")
    for devType, devDict in dat.items():
        logger_print("parsing devType:", devType)
        assert_is_nonempty_dict(devDict)
        for devSubType, devDef in devDict.items():
            assert devSubType != "null"
            assert len(devSubType) > 0
            logger_print("parsing devSubType:", devSubType)
            ports = devDef["ports"]
            assert_is_nonempty_dict(ports)
            rules = devDef["rules"]
            requirements = devDef["requirements"]

load_render_and_format(
    template_path,
    output_path,
    render_params=render_params,
    banner="GENERATING TYPE UTILS",
)
