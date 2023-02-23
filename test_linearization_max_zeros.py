from integratedEnergySystemPrototypes import Linearization
from docplex.mp.model import Model

model_name = "max_zeros_test"

model = Model(model_name)

num_hours = 24

b = model.continuous_var(lb=-100,ub=100,name="b")
x = model.continuous_var_list(lb=-100,ub=100,keys=[],name="x_n")


linearization = Linearization()
linearization.max_zeros(num_hour=24, model=model, x=..., y=...)

objective = ...
