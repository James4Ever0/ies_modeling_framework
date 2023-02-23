from integratedEnergySystemPrototypes import Linearization
from docplex.mp.model import Model

model_name = "max_zeros_test"

model = Model(model_name)

num_hours = 24

b = model.continuous_var(name="b")
x = model.continuous_var_list(keys=list(range(num_hours + 1)), name="x_n")
y = model.continuous_var_list(keys=list(range(num_hours + 1)), name="y_n")
import math

model.add_constraints(
    x[i] == b + math.sin(i * math.pi / 12) for i in range(num_hours + 1)
)

linearization = Linearization()
linearization.max_zeros(num_hour=num_hours + 1, model=model, x=x, y=y)

objective = model.sum(model.abs(x[i] + y[i]) for i in range(num_hours + 1))

solution = model.minimize(objective)
if solution:
    print("HAVE SOLUTION?")
    breakpoint()
else:
    print("NO SOLUTION")
