# from integratedEnergySystemPrototypes import Linearization
from docplex.mp.model import Model
from docplex.mp.vartype import VarType
from typing import List

bigNumber = 1e10


def max_zeros_2(num_hour: int, model: Model, x: List[VarType], y: List[VarType]):
    x_positive = model.binary_var_list([i for i in range(num_hour)], name="x_positive")
    model.add_constraints(
        (1 - x_positive[i]) * bigNumber + x[i] >= 0 for i in range(num_hour)
    )
    model.add_constraints(
        x_positive[i] * bigNumber - x[i] >= 0 for i in range(num_hour)
    )
    # flag == 1 -> positive x
    # flag == 0 -> negative x
    model.add_constraints(
        y[h] <= x[h] + (1 - x_positive[h]) * bigNumber for h in range(0, num_hour)
    )
    model.add_constraints(
        y[h] >= x[h] - (1 - x_positive[h]) * bigNumber for h in range(0, num_hour)
    )
    model.add_constraints(
        y[h] <= x_positive[h] * bigNumber for h in range(0, num_hour)
    )
    
    model.add_constraints(
        y[h] >= -x_positive[h] * bigNumber for h in range(0, num_hour)
    )



model_name = "max_zeros_test"

model = Model(model_name)

num_hours = 24

b = model.continuous_var(lb=-100, ub=100, name="b")
x = model.continuous_var_list(
    lb=-100, ub=100, keys=list(range(num_hours + 1)), name="x_n"
)
y = model.continuous_var_list(
    lb=-100, ub=100, keys=list(range(num_hours + 1)), name="y_n"
)
import math

model.add_constraints(
    x[i] == b + math.sin(i * math.pi / 12) for i in range(num_hours + 1)
)

# this FAILS!

# linearization = Linearization()
# linearization.max_zeros(num_hour=num_hours + 1, model=model, x=x, y=y)

# let's define the `max_zeros` ourselves.
max_zeros_2(num_hour=num_hours + 1, model=model, x=x, y=y)

objective = model.abs(model.sum(x[i] + y[i] for i in range(num_hours + 1)))

solution = model.minimize(objective)
if solution:
    print("HAVE SOLUTION?")
    breakpoint()
else:
    print("NO SOLUTION")
