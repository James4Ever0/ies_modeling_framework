import pint

def unitFactorCalculator(ureg:pint.UnitRegistry, old_unit_name:str): # like "元/kWh"
    ## now, the classic test?
    try:
        quantity = ureg.Quantity(1, old_unit_name)
    except:
        raise Exception("Unknown unit name:", old_unit_name)
    # quantity = ureg.Quantity(1, ureg.元/ureg.kWh)
    magnitude, units = quantity.to_tuple()

    standard_units = frozenset([ureg.万元])

    new_units_list = []
    for unit, power in units:
        # if type(unit)!=str:
        print("UNIT?", unit, "POWER?", power)
        compat_units = ureg.get_compatible_units(unit)  # frozen set.
        intersection = compat_units.intersection(standard_units)
        if len(intersection) != 0:
            if len(intersection) == 1:
                # ready to convert?
                unit = str(list(intersection)[0])
            else:
                raise Exception("Too many intersections with standard units:", intersection)
        new_units_list.append((unit, power))

    print("NEW UNITS LIST:", new_units_list)
    new_unit = ureg.UnitsContainer(tuple(new_units_list))

    new_quantity = quantity.to(new_unit)

    print("OLD QUANTITY:", quantity)
    print("NEW QUANTITY:", new_quantity)

    # get the magnitude?
    new_magnitude = new_quantity.magnitude # you multiply that.
    print("FACTOR:", new_magnitude)
    new_unit_name = str(new_unit)
    print("NEW UNIT NAME:", new_unit_name)
    return new_magnitude, new_unit_name