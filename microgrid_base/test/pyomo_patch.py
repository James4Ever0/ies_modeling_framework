import pyomo

pyomo_version = pyomo.__version__
assert pyomo_version == (expected_pyomo_version:= ""), "Expected Pyomo version: {}\nActual: {}"