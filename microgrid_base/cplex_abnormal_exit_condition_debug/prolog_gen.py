import sys

# frontend topo code -> generate names & render params & user defined disjunctive constraints -> render prolog code -> execute and verify -> get possible states -> add constraints to model

sys.path.append("../")
import jinja_utils

template_path = "prolog_gen.pro.j2"
output_path = "prolog_gen.pro"
# portList = [{'name':..., 'possible_states': [...]]

# render_params = dict(portList = [], deviceTypes = [], deviceNameToDeviceType = {}, deviceNameToPorts = {}, energyTypes = [], portNameToPortEnergyTypes = {}, adderNameToAdderPortNames = {})

render_params = dict(
    portNameToPortPossibleStates={
        "bat_port1": ["idle", "input", "output"],
        "generator_port1": ["idle", "output"],
        "load_port1": ["idle", "input"],
    },
    deviceTypes=["battery", "load", "generator"],
    deviceTypeToDeviceNames={
        "battery": ["battery1"],
        "load": ["load1"],
        "generator": ["generator1"],
    },
    deviceNameToPorts={
        "battery1": ["bat_port1"],
        "generator1": ["generator_port1"],
        "load1": ["load_port1"],
    },
    energyTypes=["electricity"],
    energyTypeToPortNames={
        "electricity": ["bat_port1", "load_port1", "generator_port1"]
    },
    adderNameToAdderPortNames={
        "adder1": ["bat_port1", "generator_port1", "load_port1"]
    },
)

jinja_utils.load_render_and_format(
    template_path,
    output_path,
    render_params=render_params,
    banner="Generating Prolog Dynamic Verification Code",
    needFormat=False,
)
