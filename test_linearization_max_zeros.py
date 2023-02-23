from docplex.mp.model import Model
from docplex.mp.vartype import VarType
from typing import List

bigNumber = 1e10


def max_zeros_2(num_hour: int, model: Model, x: List[VarType], y: List[VarType]):
    helpers = model.binary_var_list([i for i in range(num_hour)], name="x_flags")
    for i in range(num_hour):
        eps = 1e-10
        model.add_if_then(helpers[i] == 0, x[i] >= 0)
        model.add_if_then(helpers[i] == 1, x[i] <= 0 - eps)
        model.add_if_then(helpers[i] == 0, y[i] == x[i])
        model.add_if_then(helpers[i] == 1, y[i] == 0)
    # x_positive = model.binary_var_list([i for i in range(num_hour)], name="x_positive")
    # model.add_constraints(
    #     (1 - x_positive[i]) * bigNumber + x[i] >= 0 for i in range(num_hour)
    # )
    # model.add_constraints(
    #     x_positive[i] * bigNumber - x[i] >= 0 for i in range(num_hour)
    # )
    # # flag == 1 -> positive x
    # # flag == 0 -> negative x
    # model.add_constraints(
    #     y[h] <= x[h] + (1 - x_positive[h]) * bigNumber for h in range(0, num_hour)
    # )
    # model.add_constraints(
    #     y[h] >= x[h] - (1 - x_positive[h]) * bigNumber for h in range(0, num_hour)
    # )
    # model.add_constraints(
    #     y[h]>=0 for h in range(0, num_hour)
    # )


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

# this works. but this will not show the value of zeroed elements in y.
# from integratedEnergySystemPrototypes import Linearization

# linearization = Linearization()
# linearization.max_zeros(num_hour=num_hours + 1, model=model, x=x, y=y)

# let's define the `max_zeros` ourselves.
max_zeros_2(num_hour=num_hours + 1, model=model, x=x, y=y)

# objective =model.sum(x[i] + y[i] for i in range(num_hours + 1))
objective = model.abs(model.sum(x[i] + y[i] for i in range(num_hours + 1)))

model.minimize(objective)
solution = model.solve()

if solution:
    print("HAVE SOLUTION?")
    # breakpoint()
    print(solution)
else:
    print("NO SOLUTION")
