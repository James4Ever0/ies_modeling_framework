import pint

# similar projects: https://pint.readthedocs.io/en/stable/getting/faq.html
ureg = pint.UnitRegistry(filename = "currency_units.txt")
ureg.enable_contexts()
# myGroup = ureg.Group("new_group")
# ureg.define("元 = [currency]")
# ureg.define("dollar = 7 元")
# ureg.load_definitions("currency_units.txt")
# ureg.define("dollar = [currency]")
# ureg.define("million_dollar = 10000000 dollar")

# error! 

# File "D:\ProgramFiles\anaconda\envs\py37\lib\site-packages\pint\registry.py", line 939, in _get_compatible_units
#     return self._cache.dimensional_equivalents[src_dim]

print("EQUIVS:")
print(ureg._cache.dimensional_equivalents)

# compatible_units = ureg.get_compatible_units("元") # maybe in different unit system?

# compatible_units = ureg.get_compatible_units("dollar")
# print("COMPAT:", compatible_units)