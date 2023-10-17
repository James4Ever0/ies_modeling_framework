from hyperopt import hp

x_range = (10,1e5)
supersample_size = 10000

func = lambda x: x**2

import numpy as np

x_points = np.linspace(*x_range, supersample_size)
y_points = func(x_points)

x_points = x_points.tolist()
y_points = y_points.tolist()

y_range = (y_points[0], y_points[-1])



# define an objective function
def objective(args):
    case, val = args
    if case == 'case 1':
        return val
    else:
        return val ** 2

# define a search space
space = hp.choice('a',
    [
        ('case 1', 1 + hp.lognormal('c1', 0, 1)),
        ('case 2', hp.uniform('c2', -10, 10))
    ])

# minimize the objective over the space
from hyperopt import fmin, tpe, space_eval
best = fmin(objective, space, algo=tpe.suggest, max_evals=100)

print(best)
# -> {'a': 1, 'c2': 0.01420615366247227}
print(space_eval(space, best))
# -> ('case 2', 0.01420615366247227}