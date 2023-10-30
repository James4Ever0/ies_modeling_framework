# you can delegate the dynamic topo checking to pypy. might be more efficient.
# target output: STATUS_LIST

"""
[
    [['electricity', ['input', 'output', 'input']]],
    [['electricity', ['output', 'output', 'input']]],
    [['electricity', ['idle', 'output', 'input']]],
    [['electricity', ['output', 'idle', 'input']]],
    [['electricity', ['input', 'output', 'idle']]],
    [['electricity', ['idle', 'idle', 'idle']]],
]
"""

port_name_list = ["bat_port1", "generator_port1", "load_port1"]

port_name_to_possible_states = {
    "bat_port1": ["idle", "input", "output"],
    "generator_port1": [
        "idle",
        "input",
    ],
    "load_port1": ["idle", "output"],
}

port_name_to_possible_energy_types = {
    "bat_port1": ["electricity"],
    "generator_port1": ["electricity"],
    "load_port1": ["electricity"],
}

device_name_list = ["battery1", "generator1", "load1"]

device_name_to_port_names = {
    "battery1": ["bat_port1"],
    "generator1": ["generator_port1"],
    "load1": ["load_port1"],
}

adder_name_list = ['adder1']

adder_name_to_port_names = {
    "adder1": ["bat_port1", "generator_port1", "load_port1"]
}

possible_simutaneous_adder_energy_types = set()

adder_name_to_possible_adder_energy_types = {}

for adder_name, _port_name_list in adder_name_to_port_names.items():
    paet = set()
    for pn in _port_name_list:
        ets = port_name_to_possible_energy_types[pn]
        paet.update(ets)
    adder_name_to_possible_adder_energy_types[adder_name] = paet

possible_simutaneous_adder_energy_types = []

import itertools

possible_simutaneous_adder_energy_types = list(itertools.product(*adder_name_to_possible_adder_energy_types.values()))

result = []

# get `possible_adder_energy_types` from prolog?
for simutaneous_adder_energy_types in possible_simutaneous_adder_energy_types:
    simutaneous_state = []
    # all idle, otherwise at least one input one output
    aet_to_ps_l = []
    for adder_index, aet in enumerate(simutaneous_adder_energy_types):
        sasp = []
        adder_name = adder_name_list[adder_index]
        _port_name_list = adder_name_to_port_names[adder_name]
        psl = []
        for pn in _port_name_list:
            ppet = port_name_to_possible_energy_types[pn]
            pps = port_name_to_possible_states[pn]
            if aet in ppet:
                ps = pps
            else:
                assert 'idle' in pps
                ps = ['idle']
            psl.append(ps)
        for elem in itertools.product(*psl):
            if all([e == 'idle' for e in elem]) or ('input' in elem and 'output' in elem):
                sasp.append([aet, elem])
        aet_to_ps_l.append(sasp)
        
    for elem in itertools.product(*aet_to_ps_l):
        simutaneous_state.append(elem)
    result.append(simutaneous_state)

import rich
rich.print(result)