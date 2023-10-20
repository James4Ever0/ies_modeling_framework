# we can use the pure endpoint average method, instead of solving the intersection, which can be undecidable in nature
# TODO: free memory after fitting

import numpy as np

# from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Generate sample data

# TODO: ensure start & end points are preserved.

# x_start, x_end, sample_size = -500, 500, 100
x_start, x_end, sample_size = 10, 5000, 100
# x_start, x_end, sample_size = 0, 5000, 100
x = np.linspace(x_start, x_end, sample_size)
_y = x**2
# _y = np.sin(x)
# _y = np.sin(x) + np.random.normal(0, 0.2, 100)


# let's take derivative instead.
y_der = np.diff(_y)
# y_der_sqrt = np.sqrt(np.abs(y_der))
# y = np.append(y_der_sqrt, y_der_sqrt[-1])
y = np.append(y_der, y_der[-1])
# print(y)
# must_include_points = [(0,0)]

# still it might misalign

# inversion method:
# total-x
# (total-x)/x
# 1/x


x_start, y_start = x[0], _y[0]
x_end, y_end = x[-1], _y[-1]

# x_start, y_start = x[0], y[0]
# x_end, y_end = x[-1], y[-1]


# Define the number of turning points and segments
# max_depth = 2
# max_depth = 6
max_depth = 3
# max_depth = 5
# max_depth = 4

tree_model = DecisionTreeRegressor(max_depth=max_depth)  # shall you invert the loss
# tree_model = RandomForestRegressor(max_depth=max_depth)
tree_model.fit(x.reshape(-1, 1), y)
# tree_model.fit(x.reshape(-1, 1), y)

# Perform piecewise linear regression within each segment
segment_indices = tree_model.apply(x.reshape(-1, 1))
print(segment_indices)
# breakpoint()

segind = np.zeros(100)
actual_segments = -1
last_segind = -1

for index, i in enumerate(segment_indices.reshape(-1).tolist()):
    if i != last_segind:
        actual_segments += 1
        last_segind = i
    segind[index] = actual_segments


linear_models = []

breakpoints_left = []
breakpoints_right = []

seglens = []

for segment in range(actual_segments + 1):
    segment_x = x[segind == segment]
    seglens.append(len(segment_x))
    segment_y = _y[segind == segment]
    # segment_y = y[segind == segment]
    bx_l, bx_r = segment_x[0], segment_x[-1]
    # print('seg_x', segment_x)
    # print('seg_y', segment_y)
    linear_model = LinearRegression()
    linear_model.fit(segment_x.reshape(-1, 1), segment_y)
    # pred_y = linear_model.predict(np.array([bx_l, bx_r]).reshape(-1,1))
    # print(pred_y, pred_y.shape)
    by_l, by_r = linear_model.predict(np.array([bx_l, bx_r]).reshape(-1, 1))
    # by_l, by_r = ..., ...
    breakpoints_left.append((bx_l, by_l))
    breakpoints_right.append((bx_r, by_r))
    # breakpoint()
    linear_models.append(linear_model)

actual_points = [(x_start, y_start)]

print("segment lengths:",seglens)

for next_left, last_right in zip(breakpoints_left[1:], breakpoints_right[:-1]):
    x_nl, y_nl = next_left
    x_lr, y_lr = last_right
    avg_x, avg_y = (x_nl + x_lr) / 2, (y_nl + y_lr) / 2
    # avg_x, avg_y = (x_nl + x_lr) / 2, (y_nl + y_lr) / 2
    actual_points.append((avg_x, avg_y))

actual_points.append((x_end, y_end))
# actual_points.extend(must_include_points)
# actual_points.sort(key=lambda x: x[0])

actual_points = np.array(actual_points)
x_pred, y_pred = actual_points[:, 0], actual_points[:, 1]

# Plot the original data and the piecewise approximation
plt.plot(x_pred, y_pred, label="Piecewise Approximation", color="red")
plt.scatter(x, _y, label="Original Data")
# plt.scatter(x, y, label="Original Data")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Piecewise Function Approximation")
plt.show()
