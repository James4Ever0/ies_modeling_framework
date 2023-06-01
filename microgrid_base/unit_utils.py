import pint


unit_def_path = "../merged_units.txt"
ureg = pint.UnitRegistry(unit_def_path)


def unitFactorCalculator(
    ureg: pint.UnitRegistry, standard_units: frozenset, old_unit_name: str
):  # like "元/kWh"
    assert old_unit_name != ""
    assert type(old_unit_name) == str
    ## now, the classic test?

    standard_units_mapping = {
        ureg.get_compatible_units(unit): unit for unit in standard_units
    }

    try:
        quantity = ureg.Quantity(1, old_unit_name)  # one, undoubtable.
    except:
        raise Exception("Unknown unit name:", old_unit_name)
    # quantity = ureg.Quantity(1, ureg.元/ureg.kWh)
    magnitude, units = quantity.to_tuple()

    new_units_list = []
    for unit, power in units:
        # if type(unit)!=str:
        print("UNIT?", unit, "POWER?", power)
        compat_units = ureg.get_compatible_units(
            unit
        )  # the frozen set, as the token for exchange.

        target_unit = standard_units_mapping.get(compat_units, None)
        if target_unit:
            # ready to convert?
            unit = str(target_unit)
        else:
            raise Exception("No common units for:", unit)
        new_units_list.append((unit, power))

    print("NEW UNITS LIST:", new_units_list)
    new_unit = ureg.UnitsContainer(tuple(new_units_list))

    new_quantity = quantity.to(new_unit)

    print("OLD QUANTITY:", quantity)
    print("NEW QUANTITY:", new_quantity)

    # get the magnitude?
    new_magnitude = new_quantity.magnitude  # you multiply that.
    print("FACTOR:", new_magnitude)
    new_unit_name = str(new_unit)
    print("NEW UNIT NAME:", new_unit_name)
    return new_magnitude, new_unit_name


standard_units_name_list = [
    "万元",
    "kWh",
    "km",
    "kW",
    "年",
    "MPa",
    "V",
    "Hz",
    "ohm",
    "one",
    # "percent"
    "台",
    "m2",
    "m3",
    # "stere",
    "celsius",
    "metric_ton",  # this is weight.
    # "p_u_",
    "dimensionless",
]

standard_units = frozenset(
    [ureg.Unit(unit_name) for unit_name in standard_units_name_list]
)
