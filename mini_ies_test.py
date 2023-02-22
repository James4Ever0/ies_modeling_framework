from integratedEnergySystemPrototypes import GridNet, EnergyStorageSystem, PhotoVoltaic
from demo_utils import LoadGet, ResourceGet
from config import num_hour0

from docplex.mp.model import Model

load = LoadGet()
power_load = load.get_power_load()

model1 = Model(name="microgrid")

resource = ResourceGet()
power_price = resource.get_electricity_price(num_hour0)
intensityOfIllumination0 = resource.get_radiation(path="jinan_changqing-hour.dat",num_hour0=num_hour0)

# 光伏
photoVoltaic = PhotoVoltaic(
    num_hour0,
    model1,
    photoVoltaic_device_max=5000,
    device_price=4500,
    intensityOfIllumination0=intensityOfIllumination0,
    efficiency=0.8,
    device_name="PhotoVoltaic",
)
photoVoltaic.constraints_register(model1)

