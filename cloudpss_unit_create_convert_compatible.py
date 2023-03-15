import pint

# similar projects: https://pint.readthedocs.io/en/stable/getting/faq.html
ureg = pint.UnitRegistry()

# myGroup = ureg.Group("new_group")
ureg.define("元 = [currency]")
ureg.define("dollar = 7 元")

compatible_units = ureg.get_compatible_units("元") # maybe in different unit system?