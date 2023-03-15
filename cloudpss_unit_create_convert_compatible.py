import pint

# similar projects: https://pint.readthedocs.io/en/stable/getting/faq.html
ureg = pint.UnitRegistry()

ureg.define("元 = [currency]")
ureg.define("dollar = 7 元")