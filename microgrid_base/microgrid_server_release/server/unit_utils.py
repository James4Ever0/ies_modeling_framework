from log_utils import logger_print

import pint
from os.path import abspath, dirname, join

unit_def_path = f"{join(dirname(abspath(__file__)), '../merged_units.txt')}"
# unit_def_path = "../merged_units.txt"
ureg = pint.UnitRegistry(unit_def_path)

import parse


def unitParser(val):
    return parse.parse("{val_name}({val_unit})", val)


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
        logger_print("UNIT?", unit, "POWER?", power)
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

    logger_print("NEW UNITS LIST:", new_units_list)
    new_unit = ureg.UnitsContainer(tuple(new_units_list))

    new_quantity = quantity.to(new_unit)

    logger_print("OLD QUANTITY:", quantity)
    logger_print("NEW QUANTITY:", new_quantity)

    # get the magnitude?
    new_magnitude = new_quantity.magnitude  # you multiply that.
    logger_print("MAGNITUDE TO STANDARD:", new_magnitude)
    new_unit_name = str(new_unit)
    logger_print("STANDARD:", new_unit_name)
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
    # TODO: make "kelvin" into standard unit, not celsius.
    "celsius",
    "metric_ton",  # this is weight.
    # "p_u_",
    "dimensionless",
]

standard_units = frozenset(
    [ureg.Unit(unit_name) for unit_name in standard_units_name_list]
)


BASE_UNIT_TRANSLATION_TABLE = {
    "percent": ["%"],
    "m2": ["m²"],
    "/hour": [
        "/h",
    ],
    "m3": ["m³", "Nm3", "Nm³"],
    "p_u_": [
        "p.u.",
    ],
    # "次": ["one"],
}


def revert_dict(mdict: dict):
    result = {e: k for k, v in mdict.items() for e in v}
    return result


UNIT_TRANSLATION_TABLE = revert_dict(BASE_UNIT_TRANSLATION_TABLE)


def getSingleUnitConverted(default_unit, val_unit):
    logger_print("DEFAULT UNIT:", default_unit)
    default_unit_real = ureg.Unit(default_unit)
    default_unit_compatible = ureg.get_compatible_units(default_unit_real)
    # logger_print("TRANS {} -> {}".format(val_name, base_class)) # [PS]
    if val_unit is None:
        val_unit = default_unit
        logger_print("USING DEFAULT UNIT")
    logger_print("UNIT", val_unit)
    unit = ureg.Unit(val_unit)
    compatible_units = ureg.get_compatible_units(unit)
    # logger_print("COMPATIBLE UNITS", compatible_units)
    if default_unit_compatible == frozenset():
        raise Exception("Compatible units are zero for default unit:", default_unit)
    if compatible_units == frozenset():
        raise Exception("Compatible units are zero for value unit:", val_unit)
    if not default_unit_compatible == compatible_units:
        has_exception = True
        logger_print(
            "Unit {} not compatible with default unit {}".format(val_unit, default_unit)
        )
    else:
        has_exception = False
    return has_exception, val_unit


def translateUnit(_val_unit):
    for (
        trans_source_unit,
        trans_target_unit,
    ) in UNIT_TRANSLATION_TABLE.items():
        _val_unit = _val_unit.replace(trans_source_unit, trans_target_unit)
    return _val_unit


def unitCleaner(val):
    val = (
        val.replace("（", "(")
        .replace("）", ")")
        .replace(" ", "")
        .replace(";", "")
        .replace("；", "")
    )
    val = val.strip("*").strip(":").strip("：").strip()
    return val


from typing import Tuple, Union


def unitParserWrapper(val: str) -> Tuple[str, Union[str, None]]:
    val = unitCleaner(val)
    if parsed_val := unitParser(val):
        return (parsed_val["val_name"], parsed_val["val_unit"])
    return (val, None)


try:
    from typing import TypeAlias
except:
    from typing_extensions import TypeAlias
VAL_WITH_UNIT: TypeAlias = Tuple[Union[float, int], str]

import beartype
@beartype.beartype
def valueWithUnitToQuantity(val_with_unit:VAL_WITH_UNIT) -> pint.Quantity:
    quantity = val_with_unit[0] * ureg.Unit(val_with_unit[1])
    return quantity

@beartype.beartype
def multiplyWithUnit(val_with_unit_0: VAL_WITH_UNIT, val_with_unit_1: VAL_WITH_UNIT) -> VAL_WITH_UNIT:
    q0 = valueWithUnitToQuantity(val_with_unit_0)
    q1 = valueWithUnitToQuantity(val_with_unit_1)
    
    q_result = q0*q1
    magnitude = q_result.magnitude
    unit_str = str(q_result.u)
    return (magnitude, unit_str)
