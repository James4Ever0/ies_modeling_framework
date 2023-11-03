from log_utils import logger_print

import itertools


def get_all_combinations(
    portNameToPortPossibleStates, energyTypeToPortNames, adderNameToAdderPortNames
):
    port_name_to_possible_energy_types = {}

    for k, vlist in energyTypeToPortNames.items():
        for v in vlist:
            if v not in port_name_to_possible_energy_types.keys():
                port_name_to_possible_energy_types[v] = [k]
            port_name_to_possible_energy_types[v].append(k)

    adder_name_list = list(adderNameToAdderPortNames.keys())

    possible_simutaneous_adder_energy_types = set()

    adder_name_to_possible_adder_energy_types = {}

    for adder_name, _port_name_list in adderNameToAdderPortNames.items():
        paet = set()
        for pn in _port_name_list:
            ets = port_name_to_possible_energy_types[pn]
            paet.update(ets)
        adder_name_to_possible_adder_energy_types[adder_name] = paet

    possible_simutaneous_adder_energy_types = []

    possible_simutaneous_adder_energy_types = list(
        itertools.product(*adder_name_to_possible_adder_energy_types.values())
    )

    result = []

    # get `possible_adder_energy_types` from prolog?
    for simutaneous_adder_energy_types in possible_simutaneous_adder_energy_types:
        simutaneous_state = []
        # all idle, otherwise at least one input one output
        aet_to_ps_l = []
        for adder_index, aet in enumerate(simutaneous_adder_energy_types):
            sasp = []
            adder_name = adder_name_list[adder_index]
            _port_name_list = adderNameToAdderPortNames[adder_name]
            psl = []
            for pn in _port_name_list:
                ppet = port_name_to_possible_energy_types[pn]
                pps = portNameToPortPossibleStates[pn]
                if aet in ppet:
                    ps = pps
                else:
                    assert "idle" in pps
                    ps = ["idle"]
                psl.append(ps)
            for elem in itertools.product(*psl):
                if all([e == "idle" for e in elem]) or (
                    "input" in elem and "output" in elem
                ):
                    sasp.append([aet, elem])
            aet_to_ps_l.append(sasp)

        for elem in itertools.product(*aet_to_ps_l):
            simutaneous_state.append(elem)
        result.extend(simutaneous_state)
    return result
