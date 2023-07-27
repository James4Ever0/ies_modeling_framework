import pyomo

pyomo_version = pyomo.__version__
assert pyomo_version == (
    expected_pyomo_version := "6.5.0"
), f"Expected Pyomo version: {expected_pyomo_version}\nActual: {pyomo_version}"

pyomo.environ