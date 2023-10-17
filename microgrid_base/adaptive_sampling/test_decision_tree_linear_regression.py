# we can use the pure endpoint average method, instead of solving the intersection, which can be undecidable in nature
# TODO: free memory after fitting
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Generate sample data

# TODO: ensure start & end points are preserved.

x_start, x_end, sample_size = 0, 5000, 100
x = np.linspace(x_start, x_end, sample_size)

# x = np.linspace(0, 10, 100)

# y = np.sin(x)
# y = np.sin(x) + np.random.normal(0, 0.2, 100)
# x = np.linspace(10, 1e5, 10000)

y = x**2

# Define the number of turning points and segments
num_turning_points = 3
num_segments = num_turning_points + 1

# Fit a decision tree to segment the data
# 2 -> 4
tree_model = DecisionTreeRegressor(max_depth=4)  # 4 -> 16
# tree_model = DecisionTreeRegressor(max_depth=20)  # 4 -> 16
# tree_model = DecisionTreeRegressor(max_depth=12)  # 4 -> 16
# tree_model = DecisionTreeRegressor(max_depth=10)  # 4 -> 16
# tree_model = DecisionTreeRegressor(max_depth=3)  # 4 -> 16
# tree_model = DecisionTreeRegressor(max_depth=1) # 3 -> 8
# tree_model = DecisionTreeRegressor(max_depth=num_segments)
tree_model.fit(x.reshape(-1, 1), y)

# Perform piecewise linear regression within each segment
segment_indices = tree_model.apply(x.reshape(-1, 1))
# print(segment_indices)
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

for segment in range(actual_segments+1):
    segment_x = x[segind == segment]
    segment_y = y[segind == segment]
    # print('seg_x', segment_x)
    # print('seg_y', segment_y)
    linear_model = LinearRegression()
    linear_model.fit(segment_x.reshape(-1, 1), segment_y)
    linear_models.append(linear_model)

# Generate predictions for the piecewise approximation
x_pred = np.linspace(x_start, x_end, sample_size)
# x_pred = np.linspace(0, 10, 100)
# x_pred = np.linspace(0, 10, 1000)
y_pred = np.zeros_like(x_pred)

print("SEGCOUNT:", actual_segments+1)
for segment in range(actual_segments+1):
    segment_indices = segind == segment
    # print("segind", segment_indices)
    # segment_indices = tree_model.predict(x_pred.reshape(-1, 1)) == segment
    y_pred[segment_indices] = linear_models[segment].predict(
        x_pred[segment_indices].reshape(-1, 1)
    )

# Plot the original data and the piecewise approximation
plt.scatter(x, y, label="Original Data")
plt.plot(x_pred, y_pred, label="Piecewise Approximation")
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Piecewise Function Approximation")
plt.show()
