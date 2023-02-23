from integratedEnergySystemPrototypes import Linearization
from docplex.mp.model import Model

model_name = "max_zeros_test"

model = Model(model_name)

b = model.continuous_var()


linearization = Linearization()
linearization.max_zeros(num_hour=24, model=model, x=..., y=...)

objective = ...
