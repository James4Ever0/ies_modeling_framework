# you can delegate the dynamic topo checking to pypy. might be more efficient.
# target output: STATUS_LIST

"""
[[['electricity', ['input', 'output', 'input']]], [['electricity', ['input', 'output', 'input']]], [['electricity', ['output', 'output', 'input']]], [['electricity', ['output', 'output', 'input']]], [['electricity', ['idle', 'output', 'input']]], [['electricity', ['output', 'idle', 'input']]], [['electricity', ['input', 'output', 'idle']]], [['electricity', ['idle', 'idle', 'idle']]], [['electricity', ['input', 'output', 'input']]], [['electricity', ['input', 'output', 'input']]], [['electricity', ['output', 'output', 'input']]], [['electricity', ['output', 'output', 'input']]], [['electricity', ['idle', 'output', 'input']]], [['electricity', ['output', 'idle', 'input']]], [['electricity', ['input', 'output', 'idle']]], [['electricity', ['idle', 'idle', 'idle']]], [['electricity', ['input', 'output', 'input']]], [['electricity', ['input', 'output', 'input']]], [['electricity', ['output', 'output', 'input']]], [['electricity', ['output', 'output', 'input']]], [['electricity', ['idle', 'output', 'input']]], [['electricity', ['output', 'idle', 'input']]], [['electricity', ['input', 'output', 'idle']]], [['electricity', ['idle', 'idle', 'idle']]], [['electricity', ['input', 'output', 'input']]], [['electricity', ['input', 'output', 'input']]], [['electricity', ['output', 'output', 'input']]], [['electricity', ['output', 'output', 'input']]], [['electricity', ['idle', 'output', 'input']]], [[''electricity', ['idle', 'idle', 'idle']]]]
"""

port_names = ["bat_port1", "generator_port1", "load_port1"]

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

device_names = ["battery1", "generator1", "load1"]

device_name_to_port_names = {
    "battery1": ["bat_port1"],
    "generator1": ["generator_port1"],
    "load1": ["load_port1"],
}

adder_names = ['adder1']

adder_name_to_port_names = {
    "adder1":["bat_port1", "generator_port1", "load_port1"]
}

# get `possible_adder_energy_types` from prolog?
for simutaneous_adder_energy_types in possible_simutaneous_adder_energy_types:
    ...
    # all idle, otherwise at least one input one output
