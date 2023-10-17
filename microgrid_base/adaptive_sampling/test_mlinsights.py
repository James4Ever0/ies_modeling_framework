import numpy
import numpy.random as npr
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.dummy import DummyRegressor
from mlinsights.mlmodel import PiecewiseRegressor


X = npr.normal(size=(1000, 4))
alpha = [4, -2]
t = (X[:, 0] + X[:, 3] * 0.5) > 0
switch = numpy.zeros(X.shape[0])
switch[t] = 1
y = alpha[0] * X[:, 0] * t + alpha[1] * X[:, 0] * (1 - t) + X[:, 2]
fig, ax = plt.subplots(1, 1)
ax.plot(X[:, 0], y, ".")
ax.set_title("Piecewise examples")

X_train, X_test, y_train, y_test = train_test_split(X[:, :1], y)
model = PiecewiseRegressor(
    verbose=True, binner=DecisionTreeRegressor(min_samples_leaf=300)
)
model.fit(X_train, y_train)

pred = model.predict(X_test)
# pred[:5]
fig, ax = plt.subplots(1, 1)
ax.plot(X_test[:, 0], y_test, ".", label="data")
ax.plot(X_test[:, 0], pred, ".", label="predictions")
ax.set_title("Piecewise Linear Regression\n2 buckets")
ax.legend()

plt.show()