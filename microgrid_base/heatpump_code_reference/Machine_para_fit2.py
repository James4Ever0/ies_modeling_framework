import numpy as np
from sklearn.linear_model import LinearRegression


class Set_Para_Fit(object):
    def __init__(self, para):
        """
        Initializes a new instance of the Set_Para_Fit class.

        Args:
            para (list[list[float]]): A list of parameter values for the instance. Each element is a list of four float
            values representing the output temperature (Tout), input temperature (Tin), rated heat/cooling power output correlation coefficient (parr), and
            rated electricity input correlation coefficient (PWarr).

        Returns:
            None
        """
        # para=[[Tout,Tin,parr,PWarr],[],[]]
        self.X_train = []
        y_train = []
        self.Tout = []
        self.Tin = []
        self.parr = []
        self.pwarr = []
        self.row, self.col = np.shape(para)
        self.pk_coeff = []
        self.pwk_coeff = []
        self.pwk_coeff_without_rate = []
        self.pwk_rate_coeff = []
        for i in range(self.row):
            self.Tout.append(para[i][0])
            self.Tin.append(para[i][1])
            self.parr.append(para[i][2])
            self.pwarr.append(para[i][3])
            self.X_train.append(
                [
                    1,
                    self.Tout[i],
                    self.Tout[i] * self.Tout[i],
                    self.Tin[i],
                    self.Tin[i] * self.Tin[i],
                    self.Tout[i] * self.Tin[i],
                ]
            )
        self.pk_regression = LinearRegression(fit_intercept=False)
        self.pwk_regression = LinearRegression(fit_intercept=False)
        self.pwk_regression_without_rate = LinearRegression(fit_intercept=False)
        self.pwk_rate_regression = LinearRegression(fit_intercept=False)

    def fit_pkcoeff(self):
        # print(self.X_train)
        self.pk_regression.fit(self.X_train, self.parr)

        self.pk_coeff = self.pk_regression.coef_

    def get_pkcoeff(self):
        return self.pk_coeff

    def get_pk(self, tout, tin):
        """
        Calculates the current cooling/heating power correction coefficient.

        Args:
            tout (float): Output temperature value.
            tin (float): Input temperature value.

        Returns:
            float: The cooling/heating power correction coefficient.
        """
        xtest = np.array([1, tout, tout * tout, tin, tin * tin, tout * tin])
        return self.pk_regression.predict(xtest.reshape(1, -1))[0]

    ####################################3

    def fit_pwkcoeff_without_rate(self):
        self.pwk_regression_without_rate.fit(self.X_train, self.pwarr)
        self.pwk_coeff_without_rate = self.pwk_regression_without_rate.coef_

    def get_pwkcoeff_without_rate(self):
        return self.pwk_coeff_without_rate

    def get_pwk_without_rate(self, tout, tin):
        """
        Parameters:
            tout: output temperature
            tin: input temperature
        Returns:
            rated electricity input correlation coefficient at given temperature
        """
        xtest = np.array([1, tout, tout * tout, tin, tin * tin, tout * tin])
        return self.pwk_regression_without_rate.predict(xtest.reshape(1, -1))[0]

    ###################################33

    # deprecated
    def fit_pwkcoeff(self, load_rate_arr):
        # load_rate_arr=[[0.25,1.2],[0.5,1.3],[0.75,1.5],[1,1]
        row_rate = np.shape(load_rate_arr)[0]
        xwtrain = []
        ywtrain = []

        for i in range(self.row):
            for j in range(row_rate):
                """
                xwtrain.append([1, load_rate_arr[j][0] * self.parr[i],
                                (load_rate_arr[j][0] * self.parr[i]) * (load_rate_arr[j][0] * self.parr[i]),
                                self.Tout[i], self.Tin[i], self.Tout[i] * self.Tin[i],
                                self.Tout[i] * (load_rate_arr[j][0] * self.parr[i]),
                                self.Tin[i] * (load_rate_arr[j][0] * self.parr[i])])
                """
                xwtrain.append(
                    [
                        1,
                        load_rate_arr[j][0],
                        (load_rate_arr[j][0]) * (load_rate_arr[j][0]),
                        self.Tout[i],
                        self.Tin[i],
                        self.Tout[i] * self.Tin[i],
                        self.Tout[i] * (load_rate_arr[j][0]),
                        self.Tin[i] * (load_rate_arr[j][0]),
                    ]
                )

                ywtrain.append(
                    self.pwarr[i] * load_rate_arr[j][0] / load_rate_arr[j][1]
                )

        self.pwk_regression.fit(xwtrain, ywtrain)
        self.pwk_coeff = self.pwk_regression.coef_

    def get_pwkcoeff(self):
        return self.pwk_coeff

    def get_pwk(self, tout, tin, load_rate):
        xtest = np.array(
            [
                1,
                load_rate,
                load_rate * load_rate,
                tout,
                tin,
                tout * tin,
                tout * load_rate,
                tin * load_rate,
            ]
        )
        res = self.pwk_regression.predict(xtest.reshape(1, -1))

        return res[0]

    def fit_pwk_rate_coeff(self, load_rate_arr):
        """
        Fit parameters for: f(1, load_rate, load_rate^2) = load_rate/normalized_cop (actual cop/cop at max load rate)
        """
        # load_rate_arr=[[0.25,1.2],[0.5,1.3],[0.75,1.5],[1,1]
        row_rate = np.shape(load_rate_arr)[0]
        xwtrain = []
        ywtrain = []
        for j in range(row_rate):
            xwtrain.append( # 1 is probably for bias
                [1, load_rate_arr[j][0], load_rate_arr[j][0] * load_rate_arr[j][0]]
            )
            ywtrain.append(load_rate_arr[j][0] / load_rate_arr[j][1]) # f(1, load_rate, load_rate^2) = load_rate/normalized_cop
        self.pwk_rate_regression.fit(xwtrain, ywtrain)
        self.pwk_rate_coeff = self.pwk_rate_regression.coef_

    def get_pwk_rate_coeff(self):
        """
        Get parameters for: f(1, load_rate, load_rate^2) = load_rate/normalized_cop
        """
        return self.pwk_rate_coeff

    def get_pwk_rate(self, rate):
        xtest = np.array([1, rate, rate * rate])
        return self.pwk_rate_regression.predict((xtest.reshape(1, -1)))[0]

        # (1)
        # (2)
        # (3)
