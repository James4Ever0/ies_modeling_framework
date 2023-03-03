from typing import List
from typing_extensions import Literal
from typing import Iterable, Union
import numpy as np
from docplex.mp.model import Model
from docplex.mp.solution import SolveSolution

from docplex.mp.conflict_refiner import ConflictRefiner

import itertools


class Load:
    def __init__(
        self,
        input_type: Union[
            # Literal["hot_water"],
            # there's no such load.
            Literal["cold_water"],
            Literal["steam"],  # is this one of the load types? not sure.
            Literal["warm_water"],  # is this one of the load types?
            Literal["electricity"],
        ],
        data: Union[List, np.ndarray],
        device_name="load",
    ):
        self.power_of_inputs = {input_type: data}
        self.power_of_outputs = {}
        self.annualized = 0
        self.device_name = f"{input_type}_{device_name}"


# in our sense of "iterable", not "generally iterable".
def checkIterable(values: Iterable):
    return any(
        [
            isinstance(values, subscripableType)
            for subscripableType in [list, np.ndarray, tuple]
        ]
    )


def check_invalid_constraints(
    model: Model,
    filters: List[List[str]] = [
        ["(0,", "GE,", "energy_EnergyStorageSystem"],
        [",0)", "LE,", "energy_EnergyStorageSystem"],
        ["energy_EnergyStorageSystem_1_1 "],
        ["energy_EnergyStorageSystem_1_1,"],
        ["energy_EnergyStorageSystem_1_1 <= 0"],
        # ["0 >= power_of_output_electricity_PhotoVoltaic_1_0"],
    ],
    white_list_filters: List[List[str]] = [
        ["energy_EnergyStorageSystem_1_1 == 0.900"],
        ["energy_EnergyStorageSystem_1_1 >= 0"],
    ],
):
    invalid_constraints = set()
    invalid_flags = []

    def check_if_all(constraint_string, _filter):
        return all([filter_keyword in constraint_string for filter_keyword in _filter])

    for constraint in model.iter_constraints():
        constraint_string = str(constraint)
        for _filter in filters:
            invalid = check_if_all(constraint_string, _filter)
            if invalid:
                white_listed_flags = []
                for white_list_filter in white_list_filters:
                    white_listed = check_if_all(constraint_string, white_list_filter)
                    white_listed_flags.append(white_listed)
                if not any(white_listed_flags):
                    invalid_constraints.add(constraint_string)
                    invalid_flags.append(invalid)
    for invalid_constraint in invalid_constraints:
        print("INVALID CONSTRAINT:")
        print(invalid_constraint)
    return any(invalid_flags)


def check_conflict(model: Model):
    has_conflict = False
    try:
        refiner = ConflictRefiner()  # 先实例化ConflictRefiner类
        res = refiner.refine_conflict(model)  # 将模型导入该类,调用方法
        number_of_conflicts = res.number_of_conflicts
        has_conflict = number_of_conflicts != 0
        if has_conflict:
            res.display()  # 显示冲突约束
        del res
        del refiner
    except:
        pass
    return has_conflict


# decorate class method?


def check_conflict_decorator(class_method):
    def decorated_func(self, *args, **kwargs):
        # class_instance = args[0] # <- this is the 'self'
        # really?
        def display_invoke_info():
            print("_" * 30)
            print("FUNCTION:", class_method)
            print("CLASS INSTANCE:", self)
            print("ALL REMAINING ARGS:", args)
            print("ALL KWARGS:", kwargs)
            print("_" * 30)

        model = self.model  # do we really have conflict?
        debug = self.debug
        # check_conflict()
        if debug:
            if debug == True:
                debug = "DEBUG"
            step = "STEP" in debug
            exception = "EXCEPTION" in debug
        else:
            step = exception = False

        if step:
            display_invoke_info()

        if debug:
            has_conflict = check_conflict(model)
            has_invalid = check_invalid_constraints(model)
            if has_conflict or has_invalid:
                if has_invalid:
                    print("BREAK BECAUSE OF INVALID CONSTRAINS BUILT")
                print("___BEFORE INVOKE___")
                if not step:
                    display_invoke_info()
                if exception:
                    raise Exception("FATAL ERROR WHILE DEBUGGING")

        value = class_method(self, *args, **kwargs)

        if debug:
            has_conflict = check_conflict(model) or check_invalid_constraints(model)
            has_invalid = check_invalid_constraints(model)
            if has_conflict or has_invalid:
                if has_invalid:
                    print("BREAK BECAUSE OF INVALID CONSTRAINS HAS BEEN BUILT")
                print("___AFTER INVOKE___")
                if not step:
                    display_invoke_info()
                if exception:
                    raise Exception("FATAL ERROR WHILE DEBUGGING")
                breakpoint()

        return value

    return decorated_func


from docplex.mp.dvar import Var

from docplex.mp.vartype import (
    VarType,
    BinaryVarType,
    IntegerVarType,
    ContinuousVarType,
    # SemiContinuousVarType,
    # SemiIntegerVarType,
)

from functools import reduce


from config import (
    # localtime1,
    # run,
    # year,
    # node,
    # day_node,
    # debug,
    num_hour,
    simulationTime,
    bigNumber,
    # intensityOfIllumination,
)


# we define some type of "special" type that can convert from and into any energy form, called "energy".

############################UTILS############################


class symbols:
    greater_equal: Literal["greater_equal"] = "greater_equal"
    equal: Literal["equal"] = "equal"


class Linear_absolute(object):  # absolute?
    """
    带绝对值的线性约束类
    """

    # bigNumber = 1e10
    index = 0

    def __init__(
        self, model: Model, x: List[VarType], hourRange: Iterable
    ):  # hourRange?
        """
        初始化带绝对值的线性约束类

        Args:
            model (docplex.mp.model.Model): 求解模型实例
            x (List[VarType]): 存放`xpositive`和`xnegitive`在区间`hourRange`内逐元素相减结果约束得到的变量组`x`
            hourRange (Iterable): 整数区间
        """
        self.__class__.index += 1  # 要增加变量
        self.model = model
        self.classSuffix = f"{self.__class__.__name__}_{self.__class__.index}"
        self.b_positive: List[BinaryVarType] = self.model.binary_var_list(
            [i for i in hourRange],
            name="b_positive_absolute_{0}".format(self.classSuffix),
        )
        """
        一个二进制变量列表,长度为`len(hourRange)`
        
        对于`b_positive`和`b_negitive`,有:
        `b_positive[i] == 1`时,`b_negitive[i] == 0`
        `b_positive[i] == 0`时,`b_negitive[i] == 1`
        
        对于`b_positive`和`x_positive`,有:
        `b_positive[i]` == 1`时,`x_positive[i] >= 0`
        `b_positive[i]` == 0`时,`x_positive[i] == 0`
        """
        self.b_negitive: List[BinaryVarType] = self.model.binary_var_list(
            [i for i in hourRange],
            name="b_negitive_absolute_{0}".format(self.classSuffix),
        )
        """
        一个二进制变量列表,长度为`len(hourRange)`
        
        对于`b_negitive`和`x_negitive`,有:
        `b_negitive[i]` == 1`时,`x_negitive[i] >= 0`
        `b_negitive[i]` == 0`时,`x_negitive[i] == 0`
        """
        self.x_positive: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in hourRange],
            name="x_positive_absolute_{0}".format(self.classSuffix),
        )
        """
        一个实数变量列表,长度为`len(hourRange)`
        
        对于区间`hourRange`的每个数`i`,`x_positive[i]`是非负数,`x_positive[i]`和`x_negitive[i]`中必须有一个为0,另外一个大于0
        """
        self.x_negitive: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in hourRange],
            name="x_negitive_absolute_{0}".format(self.classSuffix),
        )
        """
        一个实数变量列表,长度为`len(hourRange)`
        
        对于区间`hourRange`的每个数`i`,`x_negitive[i]`是非负数,`x_positive[i]`和`x_negitive[i]`中必须有一个为0,另外一个大于0
        """
        self.absolute_x: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in hourRange], name="absolute_x_{0}".format(self.classSuffix)
        )
        """
        一个实数变量列表,长度为`len(hourRange)`
        
        对于`b_positive`、`absolute_x`、`x_positive`、`x_negitive`有:
        `b_positive[i] == 1`时,`absolute_x[i] == x_positive[i]`
        `b_positive[i] == 0`时,`absolute_x[i] == x_negitive[i]`
        """
        self.hourRange = hourRange
        self.x = x

    def absolute_add_constraints(self, hourRange: Iterable):
        """
        对于区间`hourRange`的每个数`i`,`x_positive[i]`、`x_negitive[i]`是非负实数,`b_positive[i]`、`b_negitive[i]`是不同情况对应的二进制变量,约定以下两种情况有且只有一种出现:

        1. `bigNumber >= x_negitive[i] >= 0`,`x_positive[i] == 0`,此时`b_positive[i] == 0`,`b_negitive[i] == 1`,`x[i] == -x_negitive[i]`,`absolute_x[i] == x_negitive[i]`
        2. `bigNumber >= x_positive[i] >= 0`,`x_negative[i] == 0`,此时`b_positive[i] == 1`,`b_negitive[i] == 0`,`x[i] == x_positive[i]`,`absolute_x[i] == x_positive[i]`

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        self.__class__.index += 1
        self.model.add_constraints(
            self.b_positive[i] + self.b_negitive[i] == 1 for i in hourRange
        )
        # b_positive[i]==1时,b_negitive[i]==0
        # b_positive[i]==0时,b_negitive[i]==1
        self.model.add_constraints(
            self.x_positive[i] >= 0 for i in hourRange
        )  # x_positive[i]是非负数
        self.model.add_constraints(
            self.x_positive[i] <= bigNumber * self.b_positive[i] for i in hourRange
        )
        # 当b_positive[i]==1时,x_positive[i]>=0
        # 当b_positive[i]==0时,x_positive[i]==0

        self.model.add_constraints(self.x_negitive[i] >= 0 for i in hourRange)
        # x_negitive[i]是非负数
        self.model.add_constraints(
            self.x_negitive[i] <= bigNumber * self.b_negitive[i] for i in hourRange
        )

        # 当b_negitive[i]==1时,x_negitive[i]>=0
        # 当b_negitive[i]==0时,x_negitive[i]==0
        self.model.add_constraints(
            self.x[i] == self.x_positive[i] - self.x_negitive[i] for i in hourRange
        )
        # x[i] == x_positive[i] - x_negitive[i]
        # 也就是说,如果b_positive[i]==1,x[i] == x_positive[i]
        # 如果b_positive[i]==0,x[i] == -x_negitive[i]
        self.model.add_constraints(
            self.absolute_x[i] == self.x_positive[i] + self.x_negitive[i]
            for i in hourRange
        )

        # absolute_x[i] == x_positive[i] + x_negitive[i]
        # 也就是说,如果b_positive[i]==1,absolute_x[i] == x_positive[i]
        # 如果b_positive[i]==0,absolute_x[i] == x_negitive[i]


class Linearization(object):
    """
    线性化约束类
    """

    # bigNumber = 1e10
    """
    一个非常大的数,默认为10的10次方
    """
    index: int = 0
    """
    线性约束条件编号
    """

    # bin?
    # never used.

    def product_var_bin(
        self, model: Model, var_bin: VarType, var: VarType, bin: BinaryVarType
    ):
        """
        通过二进制变量`bin`的控制,当`bin == 1`,则`var_bin == var`；当`bin == 0`,则`var_bin == 0`

        其中`var`是一个大于0的实数

        每添加一个约束组,编号加一

        Args:
            model (docplex.mp.model.Model): 求解模型实例
            var_bin (Var): 受控变量
            var (Var): 原变量
            bin (BinaryVarType): 控制变量
        """
        self.__class__.index += 1
        model.add_constraint(var_bin >= 0)
        # var_bin 大于等于 0
        model.add_constraint(var_bin >= var - (1 - bin) * bigNumber)
        # 如果bin == 0, var_bin 大于等于 (var - 1 * bigNumber)
        # 如果bin == 1, var_bin 大于等于 var
        model.add_constraint(var_bin <= var)  # var_bin 小于等于 var
        model.add_constraint(var_bin <= bin * bigNumber)
        # 如果bin == 0, var_bin 小于等于 0
        # 如果bin == 1, var_bin 小于等于 1 * bigNumber

    def product_var_bins(
        self,
        model: Model,
        var_bin: List[VarType],
        var: List[VarType],
        bin0: List[BinaryVarType],
        hourRange: Iterable,
    ):  # bins?
        """
        对于区间`self.hourRange`的每个数`i`,通过二进制变量`bin[i]`的控制,当`bin[i] == 1`,则`var_bin[i] == var[i]`；当`bin[i] == 0`,则`var_bin[i] == 0`

        其中`var[i]`是一个大于0的实数

        每添加一个约束组,编号加一

        Args:
            model (docplex.mp.model.Model): 求解模型实例
            var_bin (List[VarType]): 受控变量组
            var (List[VarType]): 原变量组
            bin (List[BinaryVarType]): 控制变量组
            self.hourRange (Iterable): 整数区间
        """
        self.__class__.index += 1
        model.add_constraints(var_bin[i] >= 0 for i in hourRange)
        model.add_constraints(
            var_bin[i] >= var[i] - (1 - bin0[i]) * bigNumber for i in hourRange
        )
        model.add_constraints(var_bin[i] <= var[i] for i in hourRange)
        model.add_constraints(var_bin[i] <= bin0[i] * bigNumber for i in hourRange)

    def product_var_back_bins(
        self,
        model: Model,
        var_bin: List[VarType],
        var: List[VarType],
        bin0: List[BinaryVarType],
        hourRangeback: Iterable,
    ):  # back?
        """
        对于区间`self.hourRange`的每个数`i`,通过二进制变量`bin[i]`的控制,当`bin[i] == 1`,则`var_bin[i] == var[i - 1]`；当`bin[i] == 0`,则`var_bin[i - 1] == 0`

        其中`var[i - 1]`是一个大于0的实数

        每添加一个约束组,编号加一

        Args:
            model (docplex.mp.model.Model): 求解模型实例
            var_bin (List[VarType]): 受控变量组
            var (List[VarType]): 原变量组
            bin (List[BinaryVarType]): 控制变量组
            self.hourRange (Iterable): 整数区间
        """
        self.__class__.index += 1
        model.add_constraints(var_bin[i] >= 0 for i in hourRangeback)
        model.add_constraints(
            var_bin[i] >= var[i - 1] - (1 - bin0[i]) * bigNumber for i in hourRangeback
        )
        model.add_constraints(var_bin[i] <= var[i - 1] for i in hourRangeback)
        model.add_constraints(var_bin[i] <= bin0[i] * bigNumber for i in hourRangeback)

    def max_zeros(  # deprecated?
        self, num_hour: int, model: Model, x: List[VarType], y: List[VarType]
    ):  # max?
        """
        对于区间`range(0, num_hour)`的每个数`h`,`y[h]`是非负实数,`y_flag[h]`是不同情况对应的二进制变量,约定以下两种情况有且只有一种出现:

        1. `y[h] == 0`,`-bigNumber <= x[h] <= 0`,此时`y_flag[h] == 0`
        2. `y[h] == x[h]`,此时`y_flag[h] == 1`

        每添加一个约束组,编号加一

        Args:
            num_hour (int): 一天小时数
            model (docplex.mp.model.Model): 求解模型实例
            x (List[VarType]): 变量组`x`
            y (List[VarType]): 变量组`y`
        """
        self.__class__.index += 1
        y_flag = model.binary_var_list(
            [i for i in range(0, num_hour)],
            name="y_flag_{0}".format(
                f"{self.__class__.__name__}_{self.__class__.index}"
            ),
        )
        model.add_constraints(
            y[h] <= x[h] + (1 - y_flag[h]) * bigNumber for h in range(0, num_hour)
        )
        # 当y_flag[h] == 0, y[h] 小于等于 x[h] + bigNumber (此时 -bigNumber <= x[h] )
        # 当y_flag[h] == 1, y[h] 小于等于 x[h]
        model.add_constraints(
            y[h] >= x[h] - (1 - y_flag[h]) * bigNumber for h in range(0, num_hour)
        )
        # 当y_flag[h] == 0, y[h] 大于等于 x[h] - bigNumber (此时 bigNumber >= x[h] )
        # 当y_flag[h] == 1, y[h] 大于等于 x[h] (y[h] == x[h])
        model.add_constraints(y[h] <= y_flag[h] * bigNumber for h in range(0, num_hour))
        # 当y_flag[h] == 0, y[h] 小于等于 0 (此时y[h] == 0)
        # 当y_flag[h] == 1, y[h] 小于等于 bigNumber
        model.add_constraints(x[h] <= y_flag[h] * bigNumber for h in range(0, num_hour))
        # 当y_flag[h] == 0, x[h] 小于等于 0 (-bigNumber<=x[h]<=0) 非正数？
        # 当y_flag[h] == 1, x[h] 小于等于 bigNumber
        model.add_constraints(y[h] >= 0 for h in range(0, num_hour))
        # y[h] 是非负数

    def add(
        self, num_hour: int, model: Model, x1: List[VarType], x2: List[VarType]
    ) -> List[VarType]:
        """
        对于区间`range(0, num_hour)`的每个数`h`,将两个变量`x1[h]`,`x2[h]`组合为一个变量`add_y[h]`

        每添加一个约束组,编号加一

        Args:
            num_hour (int): 一天小时数
            model (docplex.mp.model.Model): 求解模型实例
            x1 (List[VarType]): 变量组`x1`
            x2 (List[VarType]): 变量组`x2`

        Return:
            add_y (List[VarType]): 两个变量组在指定区间`range(0, num_hour)`内相加的变量
        """
        # looks like two lists.
        self.__class__.index += 1
        add_y = model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name="add_y_{0}".format(
                f"{self.__class__.__name__}_{self.__class__.index}"
            ),
        )
        model.add_constraints(add_y[h] == x1[h] + x2[h] for h in range(0, num_hour))
        return add_y

    def positive_negitive_constraints_register(
        self,
        num_hour: int,
        model: Model,
        x: List[VarType],
        xpositive: List[VarType],
        xnegitive: List[VarType],
    ):
        """
        对于区间`range(0, num_hour)`的每个数`h`,`x[h] == xpositive[h] - xnegitive[h]`,`positive_flag[h]`是不同情况对应的二进制变量,约定以下两种情况有且只有一种出现:

        1. `xpositive[h] == 0`,`0 <= xnegitive[h] <= bigNumber`,此时`positive_flag[h] == 0`,`x[h] == -xnegitive[h]`
        2. `0 <= xpositive[h] <= bigNumber`,`xnegitive[h] == 0`,此时`positive_flag[h] == 1`,`x[h] == xpositive[h]`

        每添加一个约束组,编号加一

        Args:
            num_hour (int): 一天小时数
            model (docplex.mp.model.Model): 求解模型实例
            x (List[VarType]): 存放`xpositive`和`xnegitive`在区间`range(0, num_hour)`内逐元素相减结果约束得到的变量组`x`
            xpositive (List[VarType]): 变量组`xpositive`
            xnegitive (List[VarType]): 变量组`xnegitive`
        """
        self.__class__.index += 1
        # bigNumber = 1e10
        positive_flag = model.binary_var_list(
            [i for i in range(0, num_hour)],
            name="Linearization_positive_flag_{0}".format(
                f"{self.__class__.__name__}_{self.__class__.index}"
            ),
        )
        model.add_constraints(
            x[h] == xpositive[h] - xnegitive[h] for h in range(0, num_hour)
        )
        # 两变量组在区间内逐元素相减 存在传入的元素组x中
        model.add_constraints(xpositive[h] >= 0 for h in range(0, num_hour))
        model.add_constraints(xnegitive[h] >= 0 for h in range(0, num_hour))
        # 两变量组在区间内元素都是非负数
        model.add_constraints(
            xpositive[h] <= bigNumber * positive_flag[h] for h in range(0, num_hour)
        )
        # 当positive_flag[h] == 0,xpositive[h] <= 0 (xpositive[h] == 0)
        # 当positive_flag[h] == 1,xpositive[h] <= bigNumber
        model.add_constraints(
            xnegitive[h] <= bigNumber * (1 - positive_flag[h])
            for h in range(0, num_hour)
        )
        # 当positive_flag[h] == 0,xnegitive[h] <= bigNumber
        # 当positive_flag[h] == 1,xnegitive[h] <= 0 (xnegitive[h] == 0)


############################UTILS############################


class EnergySystemUtils(object):
    def __init__(self, model: Model, num_hour: int, debug: bool = False):
        self.model = model
        self.num_hour = num_hour
        self.hourRange = range(0, self.num_hour)
        self.debug = debug

    from typing import Callable

    @check_conflict_decorator
    def constraint_multiplexer(
        self,
        variables: List[Var],
        values,
        constraint_function: Callable,
        index_range=None,
    ):
        index_range = self.get_index_range(variables, index_range)

        iterable = checkIterable(values)

        for index in index_range:
            if iterable:
                value = values[index]
            else:
                value = values
            constraint_function(variables[index], value)

    @check_conflict_decorator
    def add_lower_bound(self, variable: Var, lower_bound):
        self.model.add_constraint(lower_bound <= variable)  # 最大装机量

    @check_conflict_decorator
    def add_lower_bounds(self, variables: List[Var], lower_bounds, index_range=None):
        index_range = self.get_index_range(variables, index_range)

        self.constraint_multiplexer(
            variables, lower_bounds, self.add_lower_bound, index_range
        )

    @check_conflict_decorator
    def add_upper_bound(self, variable: Var, upper_bound):
        self.model.add_constraint(upper_bound >= variable)  # 最大装机量

    @check_conflict_decorator
    def add_upper_bounds(self, variables: List[Var], upper_bounds, index_range=None):
        index_range = self.get_index_range(variables, index_range)

        self.constraint_multiplexer(
            variables, upper_bounds, self.add_upper_bound, index_range
        )

    @check_conflict_decorator
    def equation(self, variable: Var, value):
        self.model.add_constraint(variable == value)

    @check_conflict_decorator
    def equations(self, variables: List[Var], values, index_range=None):
        self.constraint_multiplexer(
            variables,
            values,
            index_range=index_range,
            constraint_function=self.equation,
        )

    @check_conflict_decorator
    def add_lower_and_upper_bound(self, variables: Var, lower_bound, upper_bound):
        self.add_lower_bound(variables, lower_bound)
        self.add_upper_bound(variables, upper_bound)

    @check_conflict_decorator
    def add_lower_and_upper_bounds(
        self, variables: List[Var], lower_bounds, upper_bounds, index_range=None
    ):
        self.add_lower_bounds(variables, lower_bounds, index_range=index_range)
        self.add_upper_bounds(variables, upper_bounds, index_range=index_range)

        # self.model.add_constraint(self.device_count <= self.device_count_max)  # 最大装机量
        # self.model.add_constraint(self.device_count >= 0)
        # self.model.add_constraint(self.device_count_min<=self.device_count )

    @check_conflict_decorator
    def elementwise_operation(self, variables: List[Var], values, operation_function):
        # iterable = isinstance(values, Iterable)
        iterable = checkIterable(values)
        results = []
        for index, variable in enumerate(variables):
            if iterable:
                value = values[index]
            else:
                value = values
            result = operation_function(variable, value)
            results.append(result)
        return results

    def divide(self, variable: Var, value):
        return variable / value

    def multiply(self, variable: Var, value):
        return variable * value

    def add(self, variable: Var, value):
        return variable + value

    def subtract(self, variable: Var, value):
        return variable - value

    def min(self, variable_a: Var, value):
        return self.model.min(variable_a, value)

    def max(self, variable_a: Var, value):
        return self.model.max(variable_a, value)

    @check_conflict_decorator
    def elementwise_min(self, variables: List[Var], values):
        return self.elementwise_operation(variables, values, self.min)

    @check_conflict_decorator
    def elementwise_max(self, variables: List[Var], values):
        return self.elementwise_operation(variables, values, self.max)

    @check_conflict_decorator
    def elementwise_divide(self, variables: List[Var], values):
        return self.elementwise_operation(variables, values, self.divide)

    @check_conflict_decorator
    def elementwise_multiply(self, variables: List[Var], values):
        return self.elementwise_operation(variables, values, self.multiply)

    @check_conflict_decorator
    def elementwise_add(self, variables: List[Var], values):
        return self.elementwise_operation(variables, values, self.add)

    @check_conflict_decorator
    def elementwise_subtract(self, variables: List[Var], values):
        return self.elementwise_operation(variables, values, self.subtract)

    # @check_conflict_decorator
    def get_index_range(self, variables: List[Var], index_range=None):
        if index_range is None:
            index_range = self.hourRange
            if len(variables) < self.num_hour:
                index_range = range(len(variables))
        return index_range

    @check_conflict_decorator
    def sum_within_range(self, variables: List[Var], index_range=None):
        index_range = self.get_index_range(variables, index_range)
        result = self.model.sum(variables[index] for index in index_range)
        return result


# use the input/output way
from typing import Union, List

# usually. we are talking about something else.
common_numeral_types = [
    int,
    float,
    np.float16,
    np.float32,
    np.float64,
    # np.float80,
    # np.float96,
    # np.float128,
    # np.float256,
    np.int0,
    np.int8,
    np.int16,
    np.int32,
    np.int64,
    # np.int128,
    # np.int256,
    np.double,
]


class EnergyFlowNode:
    def __init__(
        self,
        model: Model,
        num_hour: int,
        energy_type: Union[
            Literal["cold_water"],
            Literal["cold_water_storage"],
            Literal["warm_water"],
            Literal["warm_water_storage"],
            Literal["hot_water"],
            Literal["ice"],
            Literal["steam"],
            Literal["electricity"],
        ],
        factory,  # the factory object.
        # node_type: Union[Literal["equal"], Literal["greater_equal"]] = "equal",
        debug: bool = False,
    ):
        self.util = EnergySystemUtils(model, num_hour, debug=debug)
        # self.node_type = node_type
        self.node_type = "equal"
        self.inputs = []
        self.input_ids = []
        self.outputs = []
        self.output_ids = []
        self.model = model
        self.debug = debug
        self.built = False
        self.energy_type = energy_type
        self.factory = factory

    def check_is_var_list(self, var_list):
        if type(var_list) == list:
            if all([type(var) == Var for var in var_list]):
                return True
        return False

    def __add_port(
        self, port: Union[List, np.ndarray], target_list: List, target_id_list: List
    ):
        assert not self.built
        if self.check_is_var_list(port):
            self.util.add_lower_bounds(port, 0)
        # more advanced checks?
        elif type(port) in common_numeral_types:
            assert port >= 0
        elif type(port) in [np.ndarray, List] and all(
            [(type(input_element) in common_numeral_types) for input_element in port]
        ):
            for input_element in port:
                assert input_element >= 0

        port_id = id(port)
        if (port_id not in target_id_list) or type(port_id) in common_numeral_types:
            target_id_list.append(port_id)
            target_list.append(port)
        # no way to check duplication?

    def add_input(self, input_port, ignore_energy_type: bool = False):
        if ignore_energy_type:
            port_data = input_port
        else:
            port_id = f"{id(input_port)}_output_{self.energy_type}"
            assert port_id not in self.output_ids
            port_data: Union[List, np.ndarray] = input_port.power_of_outputs[
                self.energy_type
            ]
            if (
                input_port.power_of_inputs == {}
            ):  # this is a source, not anything in between. is it?
                self.node_type = "greater_equal"
            self.factory.device_ids.add(id(input_port))
            self.factory.output_ids.add(port_id)
        self.__add_port(port_data, self.inputs, self.input_ids)

    def add_output(self, output_port, ignore_energy_type: bool = False):
        if ignore_energy_type:
            port_data = output_port
        else:
            port_id = f"{id(output_port)}_input_{self.energy_type}"
            assert port_id not in self.input_ids
            port_data: Union[List, np.ndarray] = output_port.power_of_inputs[
                self.energy_type
            ]
            if isinstance(output_port, Load):  # this is a load, the endpoint.
                self.node_type = "greater_equal"
            self.factory.device_ids.add(id(output_port))
            self.factory.input_ids.add(port_id)
        self.__add_port(port_data, self.outputs, self.output_ids)

    def add_input_and_output(self, input_and_output_port):
        self.add_input(input_and_output_port)
        self.add_output(input_and_output_port)

    from typing import Callable

    def multiplexer(self, ports, function: Callable):
        for port in ports:
            function(port)

    def add_inputs(self, *input_ports):
        self.multiplexer(input_ports, self.add_input)

    def add_outputs(self, *output_ports):
        self.multiplexer(output_ports, self.add_output)

    def add_input_and_outputs(self, *input_and_output_ports):
        self.multiplexer(input_and_output_ports, self.add_input_and_output)

    def build_relations(self):
        assert not self.built

        # inputs_deduplicated =  list(set(self.inputs))
        # inputs_count = len(self.inputs)

        # outputs_deduplicated =  list(set(self.outputs))
        # outputs_count = len(self.outputs)
        input_and_output_ids_count = len(
            [port_id for port_id in self.output_ids if port_id in self.input_ids]
        )
        assert len(self.input_ids) - input_and_output_ids_count > 0
        assert len(self.output_ids) - input_and_output_ids_count > 0

        inputs = reduce(self.util.elementwise_add, self.inputs)
        outputs = reduce(self.util.elementwise_add, self.outputs)
        if self.node_type == "equal":
            self.util.equations(inputs, outputs)
        else:
            self.util.add_lower_bounds(inputs, outputs)
        self.built = True


class EnergyFlowNodeFactory:
    def __init__(
        self,
        model: Model,
        num_hour: int,
        debug: bool = False,
    ):
        self.nodes: List[EnergyFlowNode] = []
        self.built = False
        self.model = model
        self.num_hour = num_hour
        self.debug = debug
        self.device_ids = set()
        self.input_ids = set()
        self.output_ids = set()

    def create_node(
        self,
        energy_type: Union[
            Literal["cold_water"],
            Literal["cold_water_storage"],
            Literal["warm_water"],
            Literal["warm_water_storage"],
            Literal["hot_water"],
            Literal["ice"],
            Literal["steam"],
            Literal["electricity"],
        ],
        # node_type: Union[Literal["equal"], Literal["greater_equal"]] = "equal",
    ):
        node = EnergyFlowNode(
            model=self.model,
            num_hour=self.num_hour,
            energy_type=energy_type,
            factory=self,
            # node_type=node_type,
            debug=self.debug,
        )
        self.nodes.append(
            node
        )  # how do you check validity? you can pass the factory object yourself.
        return node

    def check_system_validity(self, devices: List):
        device_ids = set([id(device) for device in devices])
        assert device_ids == self.device_ids

        for device in devices:
            input_ids = [
                f"{id(device)}_input_{key}"
                for key, _ in device.power_of_inputs.items()
            ]
            output_ids = [
                f"{id(device)}_output_{key}"
                for key, _ in device.power_of_outputs.items()
            ]
            fully_connected = all(
                [input_id in self.input_ids for input_id in input_ids]
            ) and all([output_id in self.output_ids for output_id in output_ids])

            if not fully_connected:
                errorMsg = "\n".join(
                        [
                            f"inputs: {[input_id for input_id in input_ids if input_id not in self.input_ids]}",
                            f"outputs: {[output_id for output_id in output_ids if output_id not in self.output_ids]}",
                            f"device: {device.__class__.__name__} not connected.",
                        ]
                    )
                # print(errorMsg)
                # breakpoint()
                raise Exception(
                    errorMsg
                )

    def build_relations(self, devices: List):
        assert self.built is False
        self.check_system_validity(devices)

        for node in self.nodes:
            node.build_relations()
        self.built = True


class NodeUtils:
    index = 0

    def __init__(self, model: Model, num_hour: int):
        self.index = self.__class__.index
        self.__class__.index += 1
        self.model = model
        self.connection_index = 0
        self.num_hour = num_hour
        self.fully_connected_pairs = set()

    def fully_connected(self, *nodes: EnergyFlowNode):  # nodes as arguments.
        assert len(nodes) >= 2
        for two_nodes in itertools.combinations(nodes, 2):
            for node_a, node_b in itertools.permutations(two_nodes, 2):
                node_a_id = id(node_a)
                node_b_id = id(node_b)

                assert node_a_id != node_b_id
                assert not node_a.built
                assert not node_b.built
                assert node_a.energy_type == node_b.energy_type

                if node_a_id > node_b_id:
                    node_pair_id = (node_b_id, node_a_id)
                else:
                    node_pair_id = (node_a_id, node_b_id)

                if (
                    node_pair_id in self.fully_connected_pairs
                ):  # do not connect these two. no need.
                    continue

                self.fully_connected_pairs.add(node_pair_id)

                channel = self.model.continuous_var_list(
                    [i for i in range(self.num_hour)],
                    lb=0,
                    name=f"channel_{self.connection_index}_{self.__class__.__name__}_{self.index}",
                )

                node_a.add_input(channel, ignore_energy_type=True)
                node_b.add_output(channel, ignore_energy_type=True)

                self.connection_index += 1


# another name for IES?
class IntegratedEnergySystem(EnergySystemUtils):
    """
    综合能源系统基类
    """

    device_index: int = 0  # what is this "SET"? device?

    def __init__(
        self,
        model: Model,
        num_hour: int,
        device_name: str,
        device_count_max: float,
        device_count_min: float,
        device_price: float,
        classObject,
        debug: bool = False,
        device_count_as_list: bool = False
        # className: str,
        # classIndex: int,
    ):
        """
        新建一个综合能源系统基类,设置设备名称,设备编号加一,打印设备名称和编号
        """
        IntegratedEnergySystem.device_index += 1
        super().__init__(model, num_hour, debug=debug)
        # self.device_name = device_name
        classObject.index += 1
        self.className = classObject.__name__
        self.classIndex = classObject.index
        self.model = model
        self.device_name = device_name
        self.device_count_max = device_count_max
        assert device_count_min >= 0
        assert device_count_max >= device_count_min
        self.device_count_min = device_count_min
        self.device_price = device_price
        self.classSuffix = f"{self.className}_{self.classIndex}"
        self.device_count_as_list = device_count_as_list

        if self.device_count_as_list:
            self.device_count: List[ContinuousVarType] = self.model.continuous_var_list(
                [i for i in self.hourRange], name=f"device_count_{self.classSuffix}"
            )

        else:
            self.device_count: ContinuousVarType = self.model.continuous_var(
                name=f"device_count_{self.classSuffix}"
            )

        self.annualized: ContinuousVarType = self.model.continuous_var(
            name=f"annualized_{self.classSuffix}"
        )

        # check if all inputs/outputs are connected?
        self.power_of_inputs = {}
        self.power_of_outputs = {}

        print(
            "IntegratedEnergySystem Define a device named:",
            self.device_name,
            ", total device index is:",
            IntegratedEnergySystem.device_index,
        )
        # return self.__class__.device_index

    def build_power_of_inputs(self, energy_types: List[str]):
        for energy_type in energy_types:
            self.power_of_inputs.update(
                {
                    energy_type: self.model.continuous_var_list(
                        [i for i in range(0, self.num_hour)],
                        lb=0,
                        name=f"power_of_input_{energy_type}_{self.classSuffix}",
                    )
                }
            )

    def build_power_of_outputs(self, energy_types: List[str]):
        for energy_type in energy_types:
            self.power_of_outputs.update(
                {
                    energy_type: self.model.continuous_var_list(
                        [i for i in range(0, self.num_hour)],
                        lb=0,
                        name=f"power_of_output_{energy_type}_{self.classSuffix}",
                    )
                }
            )

    def build_flags(self, flag_names: List[str], index_range=None):
        if index_range is None:
            index_range = self.hourRange

        for flag_name in flag_names:
            self.__dict__.update(
                {
                    f"{flag_name}_flags": self.model.binary_var_list(
                        [i for i in index_range],
                        name=f"{flag_name}_flag_{self.classSuffix}",
                    )
                }
            )

    def constraints_register(self):
        if self.device_count_as_list:
            self.add_lower_and_upper_bounds(
                self.device_count, self.device_count_min, self.device_count_max
            )
        else:
            self.add_lower_and_upper_bound(
                self.device_count, self.device_count_min, self.device_count_max
            )
        # print("ADDING LOWER BOUNDS?")
        # breakpoint()


# TODO: 加上输出类型区分校验
class PhotoVoltaic(IntegratedEnergySystem):  # Photovoltaic
    """
    光伏类,适用于光伏及平板式光热
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,  # float?
        intensityOfIllumination: Union[np.ndarray, List],
        efficiency: float,  # efficiency
        device_name: str = "PhotoVoltaic",
        output_type: Union[
            Literal["electricity"], Literal["hot_water"]
        ] = "electricity",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        新建一个光伏类

        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 光伏设备机组最大装机量
            device_price (float): 设备单价
            intensityOfIllumination (Union[np.ndarray, List]): 24小时光照强度
            efficiency (float): 设备运行效率
            device_name (str): 光伏机组名称,默认为"PhotoVoltaic"
        """
        # self.device_name = device_name
        # index += (
        #     1  # increase the index whenever another PhotoVoltaic system is created.
        # )
        # classObject=self.__class__

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
            # className=className,
            # classIndex=classIndex,
        )

        # className = self.__class__.__name__  # better use this instead.
        # classIndex = self.__class__.index

        """
        光伏机组等效单位设备数 大于零的实数
        """
        self.output_type = output_type
        self.build_power_of_outputs([self.output_type])
        """
        初始化每个小时内光伏机组发电量 大于零的实数 一共`num_hour`个变量
        """
        # intensityOfIllumination
        self.intensityOfIllumination = intensityOfIllumination
        self.efficiency = efficiency
        """
        每年消耗的运维成本 大于零的实数
        """
        # return val

    def constraints_register(self):
        """
        定义机组内部约束

        1. 机组设备总数不得大于最大装机量
        2. 机组设备数大于等于0
        3. 每个小时内,输出发电量小于等于机组等效单位设备数 * 效率 * 光照强度
        4. 每年消耗的运维成本 = 机组等效单位设备数 * 单位设备价格/15

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        super().constraints_register()

        self.add_upper_bounds(
            self.power_of_outputs[self.output_type],
            self.elementwise_multiply(
                self.intensityOfIllumination, self.device_count * self.efficiency
            ),
            self.hourRange,
        )
        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][i]  # 输出发电量不得超过最大发电量
        #     <= self.device_count * self.efficiency * self.intensityOfIllumination[i]
        #     for i in range(self.num_hour)
        # )

        self.equation(
            self.annualized, self.device_count * self.device_price / 15
        )  # 每年维护费用？折价？回收成本？利润？

    def total_cost(self, solution: SolveSolution) -> float:  # 购买设备总费用
        """
        Args:
            solution (docplex.mp.solution.SolveSolution): 求解模型的求解结果

        Return:
            购买设备总费用 = 机组等效单位设备数 * 单位设备价格
        """
        return solution.get_value(self.device_count) * self.device_price


# from typing import Literal


# LiBr制冷
class LiBrRefrigeration(IntegratedEnergySystem):
    """
    溴化锂制冷类,适用于制冷机组
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,  # what is this device?
        efficiency: float,
        device_name: str = "LiBrRefrigeration",
        input_type: Union[Literal["steam"], Literal["hot_water"]] = "steam",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 溴化锂制冷设备机组最大装机量
            device_price (float): 设备单价
            efficiency (float): 设备运行效率
            device_name (str): 溴化锂制冷机组名称,默认为"LiBrRefrigeration"
        """
        # self.device_name = device_name
        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # LiBrRefrigeration.index += 1
        # self.num_hour = num_hour

        # device count now.
        # self.device_count: ContinuousVarType =self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        溴化锂制冷机组等效单位设备数 大于零的实数
        """

        # self.power_of_inputs[self.input_type]: List[
        #     ContinuousVarType
        # ] =self.model.continuous_var_list(  # iterate through hours in a day?
        #     [i for i in range(0, self.num_hour)],
        #     name="inputs[self.input_type]{0}".format(self.classSuffix),
        # )
        self.input_type = input_type
        self.build_power_of_inputs([input_type])  # can be either hot water or steam.
        """
        初始化每个小时内溴化锂机组得到的热量 大于零的实数 一共`num_hour`个变量
        """
        # what is the output? cold water?

        # self.cool_LiBr: List[
        #     ContinuousVarType
        # ] =self.model.continuous_var_list(  # the same?
        #     [i for i in range(0, self.num_hour)],
        #     name="heat_LiBr_{0}".format(self.classSuffix),
        # )
        self.output_type = "cold_water"
        self.build_power_of_outputs([self.output_type])
        """
        初始化每个小时内溴化锂机组制冷量 大于零的实数 一共`num_hour`个变量
        """

        # self.device_count_max = device_count_max
        # self.device_price = device_price
        self.efficiency = efficiency
        # # self.annualized: ContinuousVarType =self.model.continuous_var(
        #     name="LiBr_annualized_{0}".format(self.classSuffix)
        # )
        """
        每年消耗的运维成本 大于零的实数
        """
        # return val

    def constraints_register(self):
        """
        定义机组内部约束

        1. 机组设备数大于等于0
        2. 机组设备总数不得大于最大装机量
        3. 每个小时内,得到的热量大于等于0,且不超过溴化锂机组设备数
        4. 每个小时内,制冷量 = 得到的热量 / 效率
        5. 每年消耗的运维成本 = 机组等效单位设备数 * 单位设备价格/15

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        # register constraints
        # self.model.add_constraint(self.device_count >= 0)
        # self.model.add_constraint(self.device_count <= self.device_count_max)
        super().constraints_register()
        self.add_lower_and_upper_bounds(
            self.power_of_inputs[self.input_type], 0, self.device_count, self.hourRange
        )

        # self.model.add_constraints(
        #     self.power_of_inputs[self.input_type][h] >= 0 for h in self.hourRange
        # )  # adding multiple constraints, passed as arguments
        # self.model.add_constraints(
        #     self.power_of_inputs[self.input_type][h] <= self.device_count for h in self.hourRange
        # )  # avaliable/active device count?

        self.equations(
            self.power_of_outputs[self.output_type],
            self.elementwise_divide(
                self.power_of_inputs[self.input_type], self.efficiency
            ),
            self.hourRange,
        )

        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][h]
        #     == self.power_of_inputs[self.input_type][h] / self.efficiency
        #     for h in self.hourRange  # how does this work out? what is the meaning of this?
        # )

        self.equation(self.annualized, self.device_count * self.device_price / 15)


# 柴油发电机
class DieselEngine(IntegratedEnergySystem):
    """
    柴油发电机类,适用于发电机组
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: int,
        device_price: int,
        running_price: int,
        device_name: str = "dieselEngine",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 柴油发电机设备机组最大装机量
            device_price (float): 设备单价
            running_price (float): 运维价格
            device_name (str): 柴油发电机机组名称,默认为"DieselEngine"
        """
        # self.device_name = device_name
        #
        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # DieselEngine.index += 1
        # self.num_hour = num_hour
        # self.device_count: ContinuousVarType =self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        柴油发电机机组等效单位设备数 大于零的实数
        """
        # self.power_of_outputs[self.output_type]: List[ContinuousVarType] =self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],  # keys, not values.
        #     name="self.power_of_outputs[self.output_type]{0}".format(self.classSuffix),
        # )
        self.output_type = "electricity"
        self.build_power_of_outputs([self.output_type])
        """
        初始化每个小时内柴油发电机机组发电量 大于零的实数 一共`num_hour`个变量
        """
        # self.device_count_max = device_count_max
        # self.device_price = device_price
        self.running_price = running_price
        self.electricity_output_sum = self.sum_within_range(
            self.power_of_outputs[self.output_type], self.hourRange
        )
        """
        柴油发电机总发电量
        """
        # # self.annualized: ContinuousVarType =self.model.continuous_var(
        #     name="dieselEngine_annualized_{0}".format(self.classSuffix)
        # )
        """
        每年消耗的运维成本 大于零的实数
        """
        # return val

    def constraints_register(self):
        """
        定义机组内部约束

        1. 机组设备数大于等于0
        2. 机组设备总数不得大于最大装机量
        3. 每个小时内,设备发电量小于等于装机设备实际值
        4. 每年消耗的运维成本 = 机组等效单位设备数 * 单位设备价格/15+设备总发电量 * 设备运行价格 * (365*24)/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        super().constraints_register()

        # self.model.add_constraint(self.device_count <= self.device_count_max)
        # self.model.add_constraint(self.device_count >= 0)
        self.add_lower_and_upper_bounds(
            self.power_of_outputs[self.output_type],
            0,
            self.device_count,
            self.hourRange,
        )
        # in fact, you should add one more?
        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][i]
        #     <= self.device_count  # does this make sense? again active device count per hour?
        #     for i in range(0, self.num_hour)
        # )
        self.equation(
            self.annualized,  # 年运行成本?
            self.device_count * self.device_price / 15
            + self.electricity_output_sum
            * self.running_price
            * (365 * 24)
            / self.num_hour,
        )

    def total_cost(self, solution: SolveSolution) -> float:
        """
        Args:
            solution (docplex.mp.solution.SolveSolution): 求解模型的求解结果

        Return:
            购买设备总费用 = 机组等效单位设备数 * 单位设备价格
        """
        # energyStorageSystem you will have it?
        return solution.get_value(self.device_count) * self.device_price


# 储能系统基类
class EnergyStorageSystem(IntegratedEnergySystem):
    """
    储能系统基类,适用于储能机组
    """

    index: int = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        device_price_powerConversionSystem: float,
        conversion_rate_max: float,
        efficiency: float,
        energy_init: float,
        stateOfCharge_min: float,
        stateOfCharge_max: float,
        device_name: str = "energyStorageSystem",
        device_count_min: int = 0,
        debug: bool = False,
        input_type: str = "energy_storage",
        output_type: str = "energy",
        classObject=None,
        device_count_as_list: bool = False,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 储能系统设备机组最大装机量
            device_price (float): 储能装置的购置价格。
            device_price_powerConversionSystem (float): 储能装置与电网之间的 PCS 转换价格。
            efficiency(float): 储能装置的充放能效率。
            conversion_rate_max (float): 储能装置的最大充放倍率。
            energy_init (float): 储能装置的初始能量。
            stateOfCharge_min (float): 储能装置的最小储能量百分比。
            stateOfCharge_max (float): 储能装置的最大储能量百分比。
            device_name (str): 储能系统机组名称,默认为"energyStorageSystem"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=classObject if classObject else self.__class__,
            debug=debug,
            device_count_as_list=device_count_as_list,
        )
        # EnergyStorageSystem.index += 1

        # self.device_count: ContinuousVarType = self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        储能系统机组等效单位设备数 大于零的实数
        """
        self.power: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, num_hour)],
            lb=-bigNumber,
            name=f"power_{self.classSuffix}",
        )

        # depends on what type of energy you are storing. well. it could be anything. really?

        # self.input_type = input_type
        # self.build_power_of_inputs([self.input_type])

        """
        模型中的连续变量列表,长度为`num_hour`,表示每小时储能装置的充放能功率
        """

        self.input_type = input_type
        self.output_type = output_type

        self.build_power_of_inputs([self.input_type])
        self.build_power_of_outputs([self.output_type])

        # 充能功率
        # input power?
        # self.power_of_inputs[self.input_type]: List[
        #     ContinuousVarType
        # ] =self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],lb=0,
        #     name="power_of_inputs[self.input_type]{0}".format(
        #         EnergyStorageSystem.index
        #     ),
        # )

        """
        模型中的连续变量列表,长度为`num_hour`,表示每小时储能装置的充能功率
        """

        # 放能功率
        # self.power_of_outputs[self.output_type]: List[
        #     ContinuousVarType
        # ] =self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],lb=0,
        #     name="power_of_outputs[self.output_type]{0}".format(
        #         EnergyStorageSystem.index
        #     ),
        # )
        """
        模型中的连续变量列表,长度为`num_hour`,表示每小时储能装置的放能功率
        """
        # 能量
        self.energy: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, num_hour)], name=f"energy_{self.classSuffix}"
        )  # name clash?
        """
        模型中的连续变量列表,长度为`num_hour`,表示每小时储能装置的能量
        """
        # self.device_count_max = device_count_max
        # self.device_price = device_price
        self.device_price_powerConversionSystem = device_price_powerConversionSystem  # powerConversionSystem? power conversion system?
        # self.num_hour = num_hour
        self.device_count_powerConversionSystem: ContinuousVarType = (
            self.model.continuous_var(
                name=f"device_count_powerConversionSystem_{self.classSuffix}"
            )
        )  # powerConversionSystem
        """
        模型中的连续变量,表示 PCS 的容量。
        """
        self.build_flags(["charge", "discharge"])
        # self.charge_flags: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(  # is charging?
        #     [i for i in range(0, num_hour)],
        #     name=f"charge_flag_{self.classSuffix}",
        # )  # 充能
        # """
        # 模型中的二元变量列表,长度为`num_hour`,表示每小时储能装置是否处于充能状态。
        # """
        # self.discharge_flags: List[BinaryVarType] = self.model.binary_var_list(
        #     [i for i in range(0, num_hour)],
        #     name=f"discharge_flag_{self.classSuffix}",
        # )  # 放能
        """
        模型中的二元变量列表,长度为`num_hour`,表示每小时储能装置是否处于放能状态。
        """
        # 效率
        self.efficiency = efficiency
        self.conversion_rate_max = conversion_rate_max  # rate of change/charge?
        self.energy_init = energy_init
        self.stateOfCharge_min = stateOfCharge_min
        self.stateOfCharge_max = stateOfCharge_max
        # # self.annualized: ContinuousVarType =self.model.continuous_var(
        #     name="energyStorageSystem_annualized_{0}".format(self.classSuffix)
        # )
        """
        每年消耗的运维成本 大于零的实数
        """
        # return val

    def constraints_register(
        self, register_period_constraints: int = 1, day_node: int = 24
    ):
        super().constraints_register()

        """
        定义机组内部约束

        1. 机组设备数大于等于0
        2. 机组设备总数不得大于最大装机量
        3. 储能装置功率转化率约束:<br>储能系统设备 * 储能装置的最大倍率大于等于功率转化系统设备,且功率转化系统设备大于等于0
        4. 充能功率和放能功率之间的关系:<br>储能系统功率 = -充能功率+放能功率
        5. 充能功率约束:<br>充能功率大于等于0,小于等于功率转化系统设备,小于等于充能状态 * bigNumber
        6. 放能功率约束:<br>放能功率大于等于0,于等于功率转化系统设备,小于等于放能状态 * bigNumber
        7. 充能功率和放能功率二选一
        8. 储能量守恒约束:<br>储能系统能量 = 上一时段储能量+(当前时段充能 * 效率-当前时段放能/效率) * simulationTime/3600
        9. 最大和最小储能量约束:<br>储能设备数 * 储能装置的最小储能量百分比≦储能系统能量≦储能设备数 * 储能装置的最大储能量百分比
        10. 每年消耗的运维成本 = (储能设备数 * 储能设备价格+功率转化系统设备数 * 功率转化系统价格)/15
        11. 两天之间充放能关系约束: <br>对于`range(day_node-1, num_hour, day_node)`区间每个数`i`，如果`register_period_constraints`参数为1,表示`energyStorageSystem[i] == energyStorageSystem[i - (day_node - 1)]`;如果`register_period_constraints`参数不为1,表示`energyStorageSystem[i] == energyStorageSystem[i - 1] + 充放能变化能量`


        Args:
            model (docplex.mp.model.Model): 求解模型实例
            register_period_constraints (int): 注册周期约束为1
            day_node (int): 一天时间节点为24
        """
        # self.hourRange = range(0, self.num_hour)
        # self.model.add_constraint(self.device_count <= self.device_count_max)
        # self.model.add_constraint(self.device_count >= 0)
        # breakpoint()

        # you don't know the range!

        self.add_lower_and_upper_bounds(
            (
                self.device_count_powerConversionSystem
                if isinstance(self.device_count_powerConversionSystem, Iterable)
                else [self.device_count_powerConversionSystem]
            ),
            0,
            self.device_count * self.conversion_rate_max
            if not (type(self.device_count) == list)
            else self.elementwise_multiply(self.device_count, self.conversion_rate_max),
        )
        # self.model.add_constraint(
        #     self.device_count * self.conversion_rate_max
        #     >= self.device_count_powerConversionSystem  # satisfying the need of power conversion system? power per unit?
        # )
        # self.model.add_constraint(self.device_count_powerConversionSystem >= 0)
        # 功率拆分

        self.equations(
            self.power,
            self.elementwise_subtract(
                self.power_of_outputs[self.output_type],
                self.power_of_inputs[self.input_type],
            ),
            self.hourRange,
        )

        # self.model.add_constraints(
        #     self.power[i]
        #     == -self.power_of_inputs[self.input_type][i]
        #     + self.power_of_outputs[self.output_type][i]
        #     for i in self.hourRange
        # )

        self.add_lower_and_upper_bounds(
            self.power_of_inputs[self.input_type],
            0,
            # self.elementwise_min(
            self.elementwise_multiply(self.charge_flags, bigNumber),
            # self.device_count_powerConversionSystem,
            # ),
            self.hourRange,
        )
        # breakpoint()
        self.add_upper_bounds(
            self.power_of_inputs[self.input_type],
            self.device_count_powerConversionSystem,
        )

        # self.model.add_constraints(
        #     self.power_of_inputs[self.input_type][i] >= 0 for i in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_inputs[self.input_type][i]
        #     <= self.charge_flags[i] * bigNumber  # smaller than infinity?
        #     for i in self.hourRange
        # )

        # self.model.add_constraints(
        #     self.power_of_inputs[self.input_type][i]
        #     <= self.device_count_powerConversionSystem
        #     for i in self.hourRange
        # )

        self.add_lower_and_upper_bounds(
            self.power_of_outputs[self.output_type],
            0,
            # self.elementwise_min(
            self.elementwise_multiply(self.discharge_flags, bigNumber),
            # self.device_count_powerConversionSystem,
            # ),
            self.hourRange,
        )
        self.add_upper_bounds(
            self.power_of_outputs[self.output_type],
            self.device_count_powerConversionSystem,
        )
        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][i] >= 0 for i in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][i]
        #     <= self.discharge_flags[i] * bigNumber
        #     for i in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][i]
        #     <= self.device_count_powerConversionSystem
        #     for i in self.hourRange
        # )

        self.equations(self.elementwise_add(self.charge_flags, self.discharge_flags), 1)
        # self.model.add_constraints(
        #     self.charge_flags[i] + self.discharge_flags[i] == 1 for i in self.hourRange
        # )

        # should we not add these?
        self.model.add_constraint(
            self.power_of_inputs[self.input_type][0]
            == self.power_of_inputs[self.input_type][1]
        )

        # # troublemaker, for battery. fixed?
        self.model.add_constraint(
            self.power_of_outputs[self.output_type][0]
            == self.power_of_outputs[self.output_type][1]
        )
        # 节点必须是24的倍数
        # day_node = 24
        for day in range(1, int(self.num_hour / day_node) + 1):
            self.model.add_constraints(
                self.energy[i]
                == self.energy[i - 1]  # previous state, previous level/state of charge
                + (
                    self.power_of_inputs[self.input_type][i] * self.efficiency
                    - self.power_of_outputs[self.output_type][i] / self.efficiency
                )
                * simulationTime  # TODO: 可以细分到秒进行仿真 需要中间变量进行步长转换
                / 3600
                for i in range(1 + day_node * (day - 1), day_node * day)
            )
        # breakpoint()
        if self.className == EnergyStorageSystemVariable.__name__:
            self.model.add_constraint(
                # self.model.add_constraints(
                self.energy[0]
                == self.energy_init * self.device_count[0]
                # for i in range(1, self.num_hour)
                # since it is init we should not iterate through all variables.
            )
        # print()
        # print("MIN_SOC:", self.stateOfCharge_min)
        # print("MAX_SOC:", self.stateOfCharge_max)
        # print()
        # breakpoint()
        if self.className == EnergyStorageSystemVariable.__name__:
            self.add_lower_and_upper_bounds(
                self.energy,
                self.elementwise_multiply(self.device_count, self.stateOfCharge_min),
                self.elementwise_multiply(self.device_count, self.stateOfCharge_max),
                range(1, self.num_hour),
            )
        else:
            self.add_lower_and_upper_bounds(
                self.energy,
                self.device_count * self.stateOfCharge_min,
                self.device_count * self.stateOfCharge_max,
                range(1, self.num_hour),
            )
        # self.model.add_constraints(
        #     self.energy[i] <= self.device_count * self.stateOfCharge_max
        #     for i in range(1, self.num_hour)
        # )
        # self.model.add_constraints(
        #     self.energy[i] >= self.device_count * self.stateOfCharge_min
        #     for i in range(1, self.num_hour)
        # )

        self.equation(
            self.annualized,
            (
                (
                    (self.device_count * self.device_price)
                    if not (self.className == EnergyStorageSystemVariable.__name__)
                    else (self.model.max(self.device_count) * self.device_price)
                )
                + (
                    self.model.max(self.device_count_powerConversionSystem)
                    if isinstance(self.device_count_powerConversionSystem, Iterable)
                    else self.device_count_powerConversionSystem
                )
                * self.device_price_powerConversionSystem
            )
            / 15,
        )
        # self.model.add_constraint(
        #     self.annualized
        #     == (
        #         self.device_count * self.device_price
        #         + self.device_count_powerConversionSystem
        #         * self.device_price_powerConversionSystem
        #     )
        #     / 15
        # )

        # # 初始值
        # self.model.add_constraint(
        #     self.energy[0]
        #     == self.energy_init * self.device_count
        # )

        # 两天之间直接割裂,没有啥关系
        if register_period_constraints == 1:  # this is a flag, not a numeric value
            # i天的电量等于daynode-1天以前的电量, 当day_node == 24时只考虑i == 23的情况
            self.model.add_constraints(
                self.energy[i] == self.energy[i - (day_node - 1)]  # 1+i-day_node
                for i in range(
                    day_node - 1, self.num_hour, day_node
                )  # what is the day_node? # start, stop, step (23, 24, 24)?
            )
        else:  # what else?
            # TODO: comment out misplaced init statement
            # # 初始值
            if self.className == EnergyStorageSystem.__name__:
                self.equation(self.energy[0], self.energy_init * self.device_count)
            # self.model.add_constraint(
            #     self.energy[0] == self.energy_init * self.device_count
            # )

            # not using this?
            # print(f"MAKING INIT TO `{self.energy_init} * device_count`")
            # breakpoint()
            # 两天之间的连接
            # 上一小时的电量加上这一小时的变化 得到此时的电量
            self.model.add_constraints(
                self.energy[i]
                == self.energy[i - 1]
                + (
                    self.power_of_inputs[self.input_type][i] * self.efficiency
                    - self.power_of_outputs[self.output_type][i] / self.efficiency
                )
                * simulationTime
                / 3600
                for i in range(day_node, self.num_hour, day_node)
            )

    def total_cost(self, solution: SolveSolution) -> float:
        """
        Args:
            solution (docplex.mp.solution.SolveSolution): 求解模型的求解结果

        Return:
            购买设备总费用 = 储能系统设备数 * 储能设备设备价格+功率转化设备数 * 功率转化设备价格
        """
        return (
            solution.get_value(
                self.max(self.device_count)
                if self.className == EnergyStorageSystemVariable.__name__
                else self.device_count
            )
            * self.device_price
            + (
                max(solution.get_values(self.device_count_powerConversionSystem))
                if isinstance(self.device_count_powerConversionSystem, Iterable)
                else solution.get_value(self.device_count_powerConversionSystem)
            )
            * self.device_price_powerConversionSystem
        )


# 可变容量储能
# TODO: 水蓄能
class EnergyStorageSystemVariable(EnergyStorageSystem):
    """
    可变容量储能类,适用于储能机组
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        device_price_powerConversionSystem: float,
        conversion_rate_max: float,
        efficiency: float,
        energy_init: float,
        stateOfCharge_min: float,
        stateOfCharge_max: float,
        device_name: str = "energyStorageSystemVariable",
        input_type: str = "energy",
        output_type: str = "energy",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 储能系统设备机组最大装机量
            device_price (float): 储能装置的购置价格。
            device_price_powerConversionSystem (float): 储能装置与电网之间的 PCS 转换价格。
            efficiency(float): 储能装置的充放能效率。
            conversion_rate_max (float): 储能装置的最大充放倍率。
            energy_init (float): 储能装置的初始储能百分比。
            stateOfCharge_min (float): 储能装置的最小储能量百分比。
            stateOfCharge_max (float): 储能装置的最大储能量百分比。
            device_name (str): 可变容量储能系统机组名称,默认为"energyStorageSystemVariable"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
            stateOfCharge_min=stateOfCharge_min,
            stateOfCharge_max=stateOfCharge_max,
            input_type=input_type,
            output_type=output_type,
            device_price_powerConversionSystem=device_price_powerConversionSystem,
            conversion_rate_max=conversion_rate_max,
            efficiency=efficiency,
            energy_init=energy_init,
            device_count_as_list=True,
        )
        # # self.classSuffix += 1
        # self.input_type = input_type
        # self.output_type = output_type

        # overriding the thing? just do it in the base class.

        # self.device_count: List[ContinuousVarType] = self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],
        #     name="energyStorageSystemVariable_device_{0}".format(self.classSuffix),
        # )
        """
        可变容量储能系统机组每小时等效单位设备数,长度为`num_hour`,大于零的实数列表
        """
        # self.power: List[ContinuousVarType] = self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],
        #     lb=-bigNumber,
        #     name=f"power_{self.classSuffix}",
        # )
        """
        模型中的连续变量列表,长度为`num_hour`,表示每小时储能装置的充放能功率
        """
        # 充能功率
        # self.build_power_of_inputs([self.input_type])
        # self.build_power_of_outputs([self.output_type])
        # self.power_of_inputs[self.input_type]: List[ContinuousVarType] =self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],
        #     name="powerVariable_charge_{0}".format(self.classSuffix),
        # )
        # """
        # 模型中的连续变量列表,长度为`num_hour`,表示每小时储能装置的充能功率
        # """
        # # 放能功率
        # self.power_of_outputs[self.output_type]: List[ContinuousVarType] =self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],
        #     name="powerVariable_discharge_{0}".format(self.classSuffix),
        # )
        """
        模型中的连续变量列表,长度为`num_hour`,表示每小时储能装置的放能功率
        """
        # 能量
        # self.energy: List[ContinuousVarType] = self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)], name=f"energy_{self.classSuffix}"
        # )
        """
        模型中的连续变量列表,长度为`num_hour`,表示每小时储能装置的能量
        """
        # self.device_count_max = device_count_max
        # self.device_price = device_price
        # self.device_price_powerConversionSystem = device_price_powerConversionSystem
        # self.num_hour = num_hour
        self.device_count_powerConversionSystem: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name=f"device_count_powerConversionSystem_{self.classSuffix}",
        )
        # powerConversionSystem
        """
        模型中的连续变量,表示 PCS 的容量
        """
        # paradox? redundancy? both charge and discharge?
        # self.charge_flags: List[BinaryVarType] = self.model.binary_var_list(
        #     [i for i in range(0, num_hour)],
        #     name=f"charge_flag_{0}".format(self.classSuffix),
        # )  # 充能
        """
        模型中的二元变量列表,长度为`num_h`,表示每小时储能装置是否处于充能状态。
        """
        # self.discharge_flags: List[BinaryVarType] = self.model.binary_var_list(
        #     keys=[i for i in range(0, num_hour)],
        #     name="discharge_flag_{0}".format(self.classSuffix),
        # )  # 放能
        """
        模型中的二元变量列表,长度为`num_h`,表示每小时储能装置是否处于放能状态。
        """
        # 效率
        # self.efficiency = efficiency
        # self.conversion_rate_max = conversion_rate_max  # conversion rate? charge rate?
        # self.energy_init = energy_init
        # self.stateOfCharge_min = stateOfCharge_min
        # self.stateOfCharge_max = stateOfCharge_max
        # return val

    # we don't need to define this. it is already covered.
    # def constraints_register(
    #     self,
    #     # model: Model,
    #     register_period_constraints=1,
    #     day_node=24,
    # ):
    #     super().constraints_register()

    #     """
    #     定义机组内部约束

    #     1. 机组设备数大于等于0
    #     2. 机组设备总数不得大于最大装机量
    #     3. 可变容量储能装置功率转化率约束:<br>储能系统设备 * 储能装置的最大倍率大于等于功率转化系统设备,且功率转化系统设备大于等于0
    #     4. 充能功率和放能功率之间的关系:<br>储能系统功率 = -充能功率+放能功率
    #     5. 充能功率约束:<br>充能功率大于等于0,小于等于功率转化系统设备,小于等于充能状态 * bigNumber
    #     6. 放能功率约束:<br>放能功率大于等于0,小于等于功率转化系统设备,小于等于放能状态 * bigNumber
    #     7. 充能功率和放能功率二选一
    #     8. 储能量守恒约束:<br>储能系统能量 = 上一时段储能量+(当前时段充能 * 效率-当前时段放能/效率) * simulationTime/3600
    #     9. 最大和最小储能量约束:<br>储能设备数 * 储能装置的最小储能量百分比≦储能系统能量≦储能设备数 * 储能装置的最大储能量百分比
    #     10. 两天之间充放能关系约束:<br>对于`range(day_node-1, num_hour, day_node)`区间每个数`i`，如果`register_period_constraints`参数为1,表示`energyStorageSystem[i] == energyStorageSystem[i - (day_node - 1)]`;如果`register_period_constraints`参数不为1,表示`energyStorageSystem[i] == energyStorageSystem[i - 1] + 充放能变化能量`

    #     Args:
    #         model (docplex.mp.model.Model): 求解模型实例
    #         register_period_constraints (int): 注册周期约束为1
    #         day_node (int): 一天时间节点为24
    #     """
    #     # bigNumber = 1e10
    #     # self.hourRange = range(0, self.num_hour)
    #     # self.model.add_constraints(
    #     #     self.device_count[i] <= self.device_count_max for i in self.hourRange
    #     # )
    #     # self.model.add_constraints(self.device_count[i] >= 0 for i in self.hourRange)
    #     self.add_lower_and_upper_bounds(
    #         self.device_count_powerConversionSystem,
    #         0,
    #         self.elementwise_multiply(self.device_count, self.conversion_rate_max),
    #         self.hourRange,
    #     )
    #     # self.model.add_constraints(
    #     #     self.device_count[i] * self.conversion_rate_max
    #     #     >= self.device_count_powerConversionSystem[i]
    #     #     for i in self.hourRange
    #     # )
    #     # self.model.add_constraints(
    #     #     self.device_count_powerConversionSystem[i] >= 0 for i in self.hourRange
    #     # )

    #     # 功率拆分
    #     self.equations(
    #         self.power,
    #         self.elementwise_subtract(
    #             self.power_of_outputs[self.output_type],
    #             self.power_of_inputs[self.input_type],
    #         ),
    #         self.hourRange,
    #     )
    #     # self.model.add_constraints(
    #     #     self.power[i]
    #     #     == -self.power_of_inputs[self.input_type][i]
    #     #     + self.power_of_outputs[self.output_type][i]
    #     #     for i in self.hourRange
    #     # )
    #     self.add_lower_and_upper_bounds(
    #         self.power_of_inputs[self.input_type],
    #         0,
    #         # self.elementwise_min(
    #         self.elementwise_multiply(self.charge_flags, bigNumber),
    #         # self.device_count_powerConversionSystem,
    #         # ),
    #         self.hourRange,
    #     )
    #     self.add_upper_bounds(
    #         self.power_of_inputs[self.input_type],
    #         self.device_count_powerConversionSystem,
    #     )
    #     # self.model.add_constraints(
    #     #     self.power_of_inputs[self.input_type][i] >= 0 for i in self.hourRange
    #     # )
    #     # self.model.add_constraints(
    #     #     self.power_of_inputs[self.input_type][i] <= self.charge_flags[i] * bigNumber
    #     #     for i in self.hourRange
    #     # )
    #     # self.model.add_constraints(
    #     #     self.power_of_inputs[self.input_type][i]
    #     #     <= self.device_count_powerConversionSystem[i]
    #     #     for i in self.hourRange
    #     # )

    #     self.add_lower_and_upper_bounds(
    #         self.power_of_outputs[self.output_type],
    #         0,
    #         self.elementwise_multiply(self.discharge_flags, bigNumber),
    #         self.hourRange,
    #     )

    #     self.add_upper_bounds(
    #         self.power_of_outputs[self.output_type],
    #         self.device_count_powerConversionSystem,
    #     )
    #     # self.model.add_constraints(
    #     #     self.power_of_outputs[self.output_type][i] >= 0 for i in self.hourRange
    #     # )
    #     # self.model.add_constraints(
    #     #     self.power_of_outputs[self.output_type][i]
    #     #     <= self.discharge_flags[i] * bigNumber
    #     #     for i in self.hourRange
    #     # )
    #     # self.model.add_constraints(
    #     #     self.power_of_outputs[self.output_type][i]
    #     #     <= self.device_count_powerConversionSystem[i]
    #     #     for i in self.hourRange
    #     # )

    #     self.equations(self.elementwise_add(self.charge_flags, self.discharge_flags), 1)

    #     # self.model.add_constraints(
    #     #     self.charge_flags[i] + self.discharge_flags[i] == 1 for i in self.hourRange
    #     # )

    #     # seems this will discourage the simulation.
    #     # let's not make it zero.

    #     self.model.add_constraint(
    #         self.power_of_inputs[self.input_type][0]
    #         == self.power_of_inputs[self.input_type][1]
    #     )

    #     self.model.add_constraint(
    #         self.power_of_outputs[self.output_type][0]
    #         == self.power_of_outputs[self.output_type][1]
    #     )

    #     # should we not add these statements?

    #     # TODO: fix charge/discharge init value issues
    #     # we should set init charge/discharge value to 1
    #     for day in range(1, int(self.num_hour / day_node) + 1):
    #         self.model.add_constraints(
    #             self.energy[i]
    #             == self.energy[i - 1]
    #             + (
    #                 self.power_of_inputs[self.input_type][i] * self.efficiency
    #                 - self.power_of_outputs[self.output_type][i] / self.efficiency
    #             )
    #             * simulationTime
    #             / 3600
    #             for i in range(
    #                 1 + day_node * (day - 1), day_node * day
    #             )  # not starting from the zero day?
    #         )
    #     # TODO: figure out init (fixing init error)

    #     # init when the type is varianle
    #     self.model.add_constraint(
    #         # self.model.add_constraints(
    #         self.energy[0]
    #         == self.energy_init * self.device_count[0]
    #         # for i in range(1, self.num_hour)
    #         # since it is init we should not iterate through all variables.
    #     )

    #     self.add_lower_and_upper_bounds(
    #         self.energy,
    #         self.device_count * self.stateOfCharge_min,
    #         self.device_count * self.stateOfCharge_max,
    #         range(1, self.num_hour),
    #     )
    #     # self.model.add_constraints(
    #     #     self.energy[i] <= self.device_count[i] * self.stateOfCharge_max
    #     #     for i in range(1, self.num_hour)
    #     # )
    #     # self.model.add_constraints(
    #     #     self.energy[i] >= self.device_count[i] * self.stateOfCharge_min
    #     #     for i in range(1, self.num_hour)
    #     # )

    #     # 两天之间直接割裂,没有啥关系
    #     if register_period_constraints == 1:  # register??
    #         self.model.add_constraints(
    #             self.energy[i] == self.energy[i - (day_node - 1)]
    #             for i in range(day_node - 1, self.num_hour, day_node)
    #         )
    #     else:
    #         # 初始值
    #         # # TODO: figure out init
    #         # self.model.add_constraint(
    #         #     self.energy[0]
    #         #     == self.energy_init * self.device_count[0]
    #         #     # since it is init we should not iterate through all variables.
    #         # )
    #         # breakpoint()
    #         # not breaking here?
    #         # 两天之间的连接
    #         # TODO: (365*24)（一年）设置为num_hour时使用这个条件
    #         self.model.add_constraints(
    #             self.energy[i]
    #             == self.energy[i - 1]
    #             + (
    #                 self.power_of_inputs[self.input_type][i] * self.efficiency
    #                 - self.power_of_outputs[self.output_type][i] / self.efficiency
    #             )
    #             * simulationTime
    #             / 3600
    #             for i in range(day_node, self.num_hour, day_node)
    #         )


# troughPhotoThermal
class TroughPhotoThermal(IntegratedEnergySystem):
    """
    槽式光热类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        device_price_solidHeatStorage: float,  # (csgrgtxr是啥)
        intensityOfIllumination: Union[np.ndarray, List],
        efficiency: float,
        device_name: str = "troughPhotoThermal",
        device_count_min: int = 0,
        debug: bool = False,
        device_price_powerConversionSystem: float = 100,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 槽式光热设备机组最大装机量
            device_price (float): 槽式光热设备的购置价格。
            device_price_solidHeatStorage (float): 槽式光热储能设备价格
            intensityOfIllumination (Union[np.ndarray, List]): 24小时光照强度
            efficiency (float): 效率
            device_name (str): 槽式光热机组名称,默认为"troughPhotoThermal"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # # self.classSuffix += 1
        # self.num_hour = num_hour
        # self.device_count: ContinuousVarType = self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        self.output_type = "steam"
        self.build_power_of_outputs([self.output_type])
        """
        槽式光热机组设备数 实数变量
        """
        self.power_generated_steam: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            lb=0,
            name="power_{0}".format(self.classSuffix),
        )

        self.power_generated_steam_remained: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            lb=0,
            name="power_remained_{0}".format(self.classSuffix),
        )
        """
        槽式光热机组每小时产热功率 实数变量列表
        """
        # self.power_of_outputs['steam']: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_troughPhotoThermal_steam_{0}".format(self.classSuffix),
        # )
        """
        槽式光热机组每小时产蒸汽功率 实数变量列表
        """
        self.device_count_max = device_count_max
        self.device_count_max_solidHeatStorage: float = device_count_max * 6
        """
        固态储热最大设备量 = 槽式光热机组最大装机量 * 6
        """
        self.device_price = device_price
        self.device_price_solidHeatStorage = device_price_solidHeatStorage
        self.intensityOfIllumination = (
            intensityOfIllumination  # intensityOfIllumination
        )
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="troughPhotoThermal_annualized_{0}".format(self.classSuffix)
        # )
        """
        槽式光热年运维成本
        """
        self.efficiency = efficiency

        self.solidHeatStorage = (
            EnergyStorageSystem(  # this shall never be used directly. this is internal.
                num_hour,
                model,
                self.device_count_max_solidHeatStorage,
                self.device_price_solidHeatStorage,
                device_price_powerConversionSystem=device_price_powerConversionSystem,
                conversion_rate_max=2,  # change?
                efficiency=0.9,
                energy_init=1,
                stateOfCharge_min=0,
                stateOfCharge_max=1,
                input_type=self.output_type,
                output_type=self.output_type,
            )
        )
        """
        固态储热设备初始化为`EnergyStorageSystem`
        """
        # return val

    def constraints_register(self):
        """
        定义槽式光热机组约束条件：

        1. 0 <= 槽式光热装机量 <= 最大装机量
        2. 0 <= 槽式光热机组每小时发电功率 <= 槽式光热装机量 * 每小时光照强度 * 机组效率
        3. 槽式光热机组每小时发电功率 + 固体储能机组每小时充放能功率 == 槽式光热机组每小时产蒸汽功率
        4. 槽式光热机组每小时产蒸汽功率 >= 0
        5. 槽式光热年运维成本 == 槽式光热设备数 * 槽式光热设备单价 / 15 + 固体储能机组年运维成本

        Args:
            model (docplex.mp.model.Model): 求解模型实例

        """
        super().constraints_register()

        # self.hourRange = range(0, self.num_hour)
        self.solidHeatStorage.constraints_register()
        # self.model.add_constraint(self.device_count >= 0)
        # self.model.add_constraint(
        #     self.device_count <= self.device_count_max
        # )

        self.add_lower_and_upper_bounds(
            self.power_generated_steam,
            0,
            self.elementwise_multiply(
                self.intensityOfIllumination, self.device_count * self.efficiency
            ),
        )
        # self.model.add_constraints(
        #     self.power_generated_steam[h] >= 0 for h in self.hourRange
        # )

        # self.model.add_constraints(
        #     self.power_generated_steam[h]
        #     <= self.device_count
        #     * self.intensityOfIllumination[h]
        #     * self.efficiency
        #     for h in self.hourRange
        # )  # 与天气相关

        self.equations(
            self.power_generated_steam,
            self.elementwise_add(
                self.power_generated_steam_remained,
                self.solidHeatStorage.power_of_inputs[self.output_type],
            ),
        )

        self.equations(
            self.power_of_outputs[self.output_type],
            self.elementwise_add(
                self.power_generated_steam_remained,
                self.solidHeatStorage.power_of_outputs[self.output_type],
            ),
            self.hourRange,
        )

        # self.model.add_constraints(
        #     self.power_generated_steam[h]
        #     + self.solidHeatStorage.power[h]
        #     == self.power_of_outputs[self.output_type][h]
        #     for h in self.hourRange
        # )  # troughPhotoThermal系统产生的highTemperature

        # self.model.add_constraints(
        #     0 <= self.power_of_outputs[self.output_type][h] for h in self.hourRange
        # )  # 约束能量不能倒流
        self.add_lower_bounds(self.power_of_outputs[self.output_type], 0)
        self.equation(
            self.annualized,
            self.device_count * self.device_price / 15
            + self.solidHeatStorage.annualized,
        )
        # self.model.add_constraint(
        #     self.annualized
        #     == self.device_count * self.device_price / 15
        #     + self.solidHeatStorage.annualized
        # )


# CombinedHeatAndPower设备
# 输入:
# TODO: fix the name issue of CHP devices
class CombinedHeatAndPower(IntegratedEnergySystem):
    """
    热电联产类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        gas_price: Union[np.ndarray, List],
        rated_power: float,
        electricity_to_heat_ratio: float,  # drratio?
        device_name: str = "combinedHeatAndPower",
        device_count_min: int = 0,
        debug: bool = False,
        gas_to_electricity_ratio=3.5,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 表示热电联产机组的最大等效设备数量
            device_price (float): 表示热电联产等效设备的单价
            gas_price (Union[np.ndarray, List]): 表示燃气的单价
            rated_power (float): 表示每台热电联产设备的等效设备数量
            electricity_to_heat_ratio (float): 表示热电联产设备的电热比。
            device_name (str): 热电联产机组名称,默认为"combinedHeatAndPower"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # # self.classSuffix += 1
        # self.num_hour = num_hour
        # self.device_count: ContinuousVarType = self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        实数型,表示热电联产的等效设备数量
        """
        self.build_power_of_outputs(["electricity", "hot_water", "steam"])
        # self.power_of_outputs['electricity']: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_combinedHeatAndPower_{0}".format(self.classSuffix),
        # )
        # """
        self.heat_generated: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in self.hourRange], name=f"heat_generated_{self.classSuffix}"
        )
        # 实数型列表,表示热电联产在每个时段的发电量
        # """
        # self.power_of_outputs['hot_water']: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="heat_combinedHeatAndPower_{0}".format(self.classSuffix),
        # )
        """
        实数型列表,表示热电联产在每个时段的总产热量
        """
        self.gas_consumed: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="gas_consumed_{0}".format(self.classSuffix),
        )  # 时时耗气量? 时时是什么意思 实时？
        """
        实数型列表,表示热电联产在每个时段的耗气量
        """
        self.device_price = device_price
        self.gas_price = gas_price
        self.on_flags: List[BinaryVarType] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="on_flag_{0}".format(self.classSuffix),
        )
        """
        二元变量列表,表示热电联产在每个时段是否启动
        """
        self.output_hot_water_flags: BinaryVarType = self.model.binary_var(
            name="output_hot_water_flag_{0}".format(self.classSuffix)
        )
        """
        二元变量,表示热电联产是否用于供暖热水
        """
        self.output_steam_flags: BinaryVarType = self.model.binary_var(
            name="output_steam_flag_{0}".format(self.classSuffix)
        )
        """
        二元变量,表示热电联产是否用于供热蒸汽
        """
        # 机组数量
        self.device_count_running: List[IntegerVarType] = self.model.integer_var_list(
            [i for i in range(0, self.num_hour)],
            name="device_count_running_{0}".format(self.classSuffix),
        )
        """
        整数型列表,表示每个时段启动的热电联产等效设备数量
        """
        # self.device_count: IntegerVarType = self.model.integer_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        整数型,表示热电联产实际装机数量
        """
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="combinedHeatAndPower_annualized_{0}".format(self.classSuffix)
        # )
        """
        实数型,表示热电联产年化投资成本
        """
        self.gas_cost: ContinuousVarType = self.model.continuous_var(
            name="gas_cost_{0}".format(self.classSuffix)
        )  # 燃气费用统计
        """
        实数型,表示总燃气费用
        """

        self.total_rated_power: ContinuousVarType = self.model.continuous_var(
            name=f"total_rated_power_{self.classSuffix}"
        )
        # self.device_count_max = device_count_max
        self.rated_power = rated_power
        """
        单台机组额定功率
        """
        self.running_ratio_min = (
            0.2  # ? devices cannot be turned down more than 20% ? what is this?
        )
        """
        最低CHP机组开启比率 默认为0.2
        """

        self.electricity_to_heat_ratio = electricity_to_heat_ratio

        # arbitrary settings
        self.hot_water_exchanger_1 = Exchanger(
            self.num_hour,
            model,
            self.device_count * 0.5,
            device_price=300,
            k=0,
            input_type="heat",
            output_type="hot_water",
        )
        """
        燃气轮机热交换器，参数包括时间步数、数学模型实例、可用的设备数量、设备单价和换热系数等。
        """

        self.hot_water_exchanger_2 = Exchanger(
            self.num_hour,
            model,
            self.device_count * 0.5,
            device_price=300,
            k=0,
            input_type="heat",
            output_type="hot_water",
        )

        """
        供暖热水热交换器，参数包括时间步数、数学模型实例、可用的设备数量、设备单价和换热系数等。
        """

        self.steam_exchanger = Exchanger(
            self.num_hour,
            model,
            self.device_count * 0.5,
            device_price=300,
            k=0,
            input_type="heat",
            output_type="steam",
        )

        self.gas_to_electricity_ratio = gas_to_electricity_ratio

        self.power_of_outputs["hot_water"] = self.elementwise_add(
            self.hot_water_exchanger_1.power_of_outputs["hot_water"],
            self.hot_water_exchanger_2.power_of_outputs["hot_water"],
        )

        self.power_of_outputs["steam"] = self.steam_exchanger.power_of_outputs["steam"]

        """
        供暖蒸汽热交换器，参数包括时间步数、数学模型实例、可用的设备数量、设备单价和换热系数等。
        """
        # return val

    def constraints_register(self):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 热电联产装机量 = 热电联产机组数 * 热电联产的装机容量
        3. 每个热电联产的热功率必须大于等于热电联产的最小热功率
        4. 每个热电联产的热功率必须小于等于热电联产的总热功率
        5. 每个热电联产的热功率必须小于等于热电联产开启时的热功率
        6. 确定每个时段热电联产开启的台数,并且每个时段热电联产开启的总功率必须等于热电联产的总热功率
        7. 热电联产的运行台数必须在0到总台数之间
        8. 热电联产的热功率必须等于热电联产的电功率乘以热电比
        9. 热电联产的燃气消耗量必须等于热电联产的总热功率除以燃气发电机组的热效率 3.5
        10. 所有时间段的天燃气消费和天燃气价格的乘积相加来计算总的天燃气成本
        11. 确保了与余气余热系统的热交换只使用一种类型(热水或蒸汽)
        12. 根据二元决策变量output_hot_water_flags和一个大常数bigM来设定与余气余热系统的最大热交换能力。如果output_hot_water_flags为0,该约束就会失去作用。
        13. 根据二元决策变量output_steam_flags和一个大常数bigM来设定蒸汽与余气余热系统的最大热交换能力。如果output_steam_flags为0,该约束就会失去作用。
        14. GTS系统的最大热交换能力限制在所有时间段内热电联产机组额定热输出的50%
        15. 余气余热热水系统的最大换热量限制为所有时段热电联产机组额定热出力的50%
        16. 余气余热蒸汽系统的最大换热能力限制为所有时段热电联产机组额定热出力的50%
        17. 计算年总成本,包括运行CHP机组、GTS系统和余气余热系统的成本以及燃气成本。计算的依据是CHP机组的数量、其额定功率出力、CHP的单位成本、一年中的小时数等相关参数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        super().constraints_register()

        # self.hourRange = range(0, self.num_hour)
        # self.model.add_constraint(self.device_count >= 0)
        # self.model.add_constraint(
        #     self.device_count <= self.device_count_max
        # )

        self.equation(self.total_rated_power, self.device_count * self.rated_power)

        # self.model.add_constraint(
        #     self.total_rated_power
        #     == self.device_count * self.rated_power
        # )

        self.add_lower_and_upper_bounds(
            self.power_of_outputs["electricity"],
            self.elementwise_multiply(
                self.on_flags, self.total_rated_power * self.running_ratio_min
            ),
            # self.elementwise_min(
            self.elementwise_multiply(self.on_flags, bigNumber),
            # self.total_rated_power,
            # ),
        )

        self.add_upper_bounds(
            self.power_of_outputs["electricity"], self.total_rated_power
        )

        # TODO: guess this is not "rated_power" but "total_rated_power"

        # self.model.add_constraints(
        #     self.on_flags[h]
        #     * self.rated_power
        #     * self.running_ratio_min
        #     <= self.power_of_outputs['electricity'][h]
        #     for h in self.hourRange
        # )

        # power_combinedHeatAndPower(1, h) <= device_count * on_flags(1, h) % combinedHeatAndPower功率限制, 采用线性化约束,有以下等效:
        # self.model.add_constraints(
        #     self.power_of_outputs['electricity'][h] <= self.total_rated_power
        #     for h in self.hourRange
        # )

        # self.model.add_constraints(
        #     self.power_of_outputs['electricity'][h]
        #     <= self.on_flags[h] * bigNumber
        #     for h in self.hourRange
        # )

        # power_combinedHeatAndPower[h]>= 0
        # power_combinedHeatAndPower(1, h) >= device_count - (1 - on_flags[h]) * bigNumber

        self.add_lower_and_upper_bounds(
            self.elementwise_multiply(self.device_count_running, self.rated_power),
            self.power_of_outputs["electricity"],
            self.elementwise_add(
                self.power_of_outputs["electricity"], self.rated_power + 1
            ),
        )

        # self.model.add_constraints(
        #     self.device_count_running[h] * self.rated_power
        #     >= self.power_of_outputs["electricity"][h]
        #     for h in self.hourRange
        # )  # 确定CombinedHeatAndPower开启台数
        # self.model.add_constraints(
        #     self.device_count_running[h] * self.rated_power
        #     <= self.power_of_outputs["electricity"][h] + self.rated_power + 1
        #     for h in self.hourRange
        # )  # 确定CombinedHeatAndPower开启台数

        self.add_lower_and_upper_bounds(self.device_count_running, 0, self.device_count)
        # self.model.add_constraints(
        #     0 <= self.device_count_running[h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.device_count_running[h] <= self.device_count for h in self.hourRange
        # )

        self.model.add_constraints(
            self.power_of_outputs["electricity"][h]
            * self.electricity_to_heat_ratio  # power * power_to_heat_coefficient = heat
            == self.heat_generated[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.gas_consumed[h]
            == self.power_of_outputs["electricity"][h] / self.gas_to_electricity_ratio
            for h in self.hourRange
        )
        self.gas_cost = self.sum_within_range(
            self.elementwise_multiply(self.gas_consumed, self.gas_price), self.hourRange
        )
        # self.gas_cost = self.model.sum(
        #     self.gas_consumed[h] * self.gas_price[h] for h in self.hourRange
        # )  # 统计燃气费用
        #
        self.equations(
            self.elementwise_add(self.output_hot_water_flags, self.output_steam_flags),
            1,
        )
        # self.model.add_constraint(
        #     self.output_hot_water_flags + self.output_steam_flags == 1
        # )
        self.add_lower_and_upper_bounds(
            self.hot_water_exchanger_2.power_of_inputs[
                self.hot_water_exchanger_2.input_type
            ],
            0,
            # self.elementwise_min(
            self.elementwise_multiply(self.output_hot_water_flags, bigNumber),
            # self.elementwise_multiply(self.heat_generated, 0.5),
            # ),
            self.hourRange,
        )

        self.add_upper_bounds(
            self.hot_water_exchanger_2.power_of_inputs[
                self.hot_water_exchanger_2.input_type
            ],
            self.elementwise_multiply(self.heat_generated, 0.5),
        )
        # self.model.add_constraint(
        #     self.hot_water_exchanger_2.device_count
        #     <= self.output_hot_water_flags * bigNumber
        # )
        self.add_lower_and_upper_bounds(
            self.steam_exchanger.power_of_inputs[self.steam_exchanger.input_type],
            0,
            # self.elementwise_min(
            self.elementwise_multiply(self.output_steam_flags, bigNumber),
            # self.elementwise_multiply(self.heat_generated, 0.5),
            # ),
            self.hourRange,
        )

        self.add_upper_bounds(
            self.steam_exchanger.power_of_inputs[self.steam_exchanger.input_type],
            self.elementwise_multiply(self.heat_generated, 0.5),
        )
        # self.model.add_constraint(
        #     self.steam_exchanger.device_count <= self.output_steam_flags * bigNumber
        # )
        self.add_lower_and_upper_bounds(
            self.hot_water_exchanger_1.power_of_inputs[
                self.hot_water_exchanger_1.input_type
            ],
            0,
            self.elementwise_multiply(self.heat_generated, 0.5),
            self.hourRange,
        )
        # self.model.add_constraints(
        #     self.hot_water_exchanger_1.heat_exchange[h] <= self.heat_generated[h] * 0.5
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.hot_water_exchanger_2.heat_exchange[h] <= self.heat_generated[h] * 0.5
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.steam_exchanger.heat_exchange[h] <= self.heat_generated[h] * 0.5
        #     for h in self.hourRange
        # )

        self.model.add_constraint(
            self.annualized
            == self.device_count * self.rated_power * self.device_price / 15
            + self.hot_water_exchanger_1.annualized
            + self.hot_water_exchanger_2.annualized
            + self.steam_exchanger.annualized
            + self.gas_cost * (365 * 24) / self.num_hour
        )


# 燃气锅炉:蒸汽,hotWater
class GasBoiler(IntegratedEnergySystem):
    """
    燃气锅炉类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        gas_price: Union[np.ndarray, List],
        efficiency: float,
        device_name: str = "gasBoiler",
        device_count_min: int = 0,
        debug: bool = False,
        output_type: Union[Literal["hot_water"], Literal["steam"]] = "hot_water",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 表示燃气锅炉的最大数量。
            device_price (float): 表示燃气锅炉的单价。
            gas_price (Union[np.ndarray, List]): 表示燃气的单价。
            efficiency (float): 燃气锅炉的热效率
            device_name (str): 燃气锅炉机组名称,默认为"gasBoiler"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # # self.classSuffix += 1
        # self.num_hour = num_hour
        # self.device_count: ContinuousVarType = self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        燃气锅炉机组等效单位设备数 大于零的实数变量
        """
        self.output_type = output_type
        self.build_power_of_outputs([self.output_type])
        # self.power_of_outputs[self.output_type]: List[ContinuousVarType] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="outputs[self.output_type]{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示燃气锅炉在每个时段的热功率
        """
        self.gas_consumed: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="gas_consumed_{0}".format(self.classSuffix),
        )  # 时时耗气量
        """
        连续变量列表,表示燃气锅炉在每个时段的燃气消耗量
        """
        # self.device_count_max = device_count_max
        # self.device_price = device_price
        self.gas_price = gas_price
        self.efficiency = efficiency
        self.gas_cost: ContinuousVarType = self.model.continuous_var(
            name="gas_cost_{0}".format(self.classSuffix)
        )
        """
        连续变量,表示总燃气费用
        """
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="gasBoiler_annualized_{0}".format(self.classSuffix)
        # )
        """
        连续变量,表示燃气锅炉的年化费用
        """
        # return val

    def constraints_register(self):
        super().constraints_register()

        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦燃气锅炉的热功率≦燃气锅炉运行量
        3. 燃气锅炉的燃气消耗量等于热功率除以热效率乘以一个常数（这个常数是热功率和燃气消耗量之间的转化系数）
        4. 燃气锅炉的总燃气成本等于燃气消耗量乘以燃气价格之和
        5. 燃气锅炉的总年化成本等于投资成本和燃气成本之和

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """

        # self.hourRange = range(0, self.num_hour)
        # self.model.add_constraint(self.device_count >= 0)
        # self.model.add_constraint(self.device_count <= self.device_count_max)

        self.add_lower_and_upper_bounds(
            self.power_of_outputs[self.output_type], 0, self.device_count
        )
        # self.model.add_constraints(self.power_of_outputs[self.output_type][h] >= 0 for h in self.hourRange)
        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][h] <= self.device_count for h in self.hourRange
        # )  # 天燃气蒸汽锅炉

        self.equations(
            self.gas_consumed,
            self.elementwise_divide(
                self.power_of_outputs[self.output_type], 10 * self.efficiency
            ),
        )
        # self.model.add_constraints(
        #     self.gas_consumed[h] == self.power_of_outputs[self.output_type][h] / (10 * self.efficiency)
        #     for h in self.hourRange
        # )

        self.gas_cost = self.sum_within_range(
            self.elementwise_multiply(self.gas_consumed, self.gas_price)
        )
        # self.gas_cost = self.model.sum(
        #     self.gas_consumed[h] * self.gas_price[h] for h in self.hourRange
        # )
        self.model.add_constraint(
            self.annualized
            == self.device_count * self.device_price / 15
            + self.gas_cost * (365 * 24) / self.num_hour
        )


# electricBoiler
class ElectricBoiler(IntegratedEnergySystem):
    """
    电锅炉类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        electricity_price: Union[np.ndarray, List],
        efficiency: float,
        device_name: str = "electricBoiler",
        device_count_min: int = 0,
        debug: bool = False,
        output_type: Union[Literal["hot_water"], Literal["steam"]] = "hot_water",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 表示电锅炉的最大数量。
            device_price (float): 表示电锅炉的单价。
            electricity_price (Union[np.ndarray, List]): 表示电的单价。
            efficiency (float): 电锅炉的热效率
            device_name (str): 电锅炉机组名称,默认为"electricBoiler"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # # self.classSuffix += 1
        # self.num_hour = num_hour
        # self.device_count: ContinuousVarType = self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        电锅炉机组等效单位设备数 大于零的实数
        """
        self.output_type = output_type
        self.build_power_of_outputs([self.output_type])
        # self.power_of_outputs[self.output_type]: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(  # h? heat?
        #     [i for i in range(0, self.num_hour)],
        #     name="power_of_outputs[self.output_type]{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示电锅炉在每个时段的热功率
        """
        # self.power_of_inputs[self.input_type]: List[
        #     ContinuousVarType
        # ] = self.model.continuuntous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_of_inputs[self.input_type]{0}".format(self.classSuffix),
        # )  # 时时耗气量
        """
        连续变量列表,表示电锅炉在每个时段的电消耗量
        """
        # self.device_count_max = device_count_max
        # self.device_price = device_price
        self.input_type = "electricity"
        self.build_power_of_inputs([self.input_type])

        self.electricity_price = electricity_price
        self.efficiency = efficiency
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="electricity_cost_{0}".format(self.classSuffix)
        )
        """
        连续变量,表示总用电费用
        """
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="electricBoiler_annualized_{0}".format(self.classSuffix)
        # )
        """
        连续变量,表示电锅炉的年化费用
        """
        # return val

    def constraints_register(self):
        super().constraints_register()

        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦电锅炉的热功率≦电锅炉运行量
        3. 燃气锅炉的电消耗量等于热功率除以热效率
        4. 燃气锅炉的总耗电成本等于电消耗量乘以电价格之和
        5. 燃气锅炉的总年化成本等于投资成本和用电成本之和

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        # self.hourRange = range(0, self.num_hour)
        # self.model.add_constraint(self.device_count >= 0)
        # self.model.add_constraint(self.device_count <= self.gas_device_count_max)

        self.add_lower_and_upper_bounds(
            self.power_of_outputs[self.output_type], 0, self.device_count
        )
        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][h] >= 0 for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][h] <= self.device_count
        #     for h in self.hourRange
        # )  # 天燃气蒸汽锅炉

        self.equations(
            self.power_of_inputs[self.input_type],
            self.elementwise_divide(
                self.power_of_outputs[self.output_type], self.efficiency
            ),
        )
        # self.model.add_constraints(
        #     self.power_of_inputs[self.input_type][h]
        #     == self.power_of_outputs[self.output_type][h] / self.efficiency
        #     for h in self.hourRange
        # )
        self.electricity_cost = self.sum_within_range(
            self.elementwise_multiply(
                self.power_of_inputs[self.input_type], self.electricity_price
            )
        )
        # self.electricity_cost = self.model.sum(
        #     self.power_of_inputs[self.input_type][h] * self.electricity_price[h]
        #     for h in self.hourRange
        # )
        self.model.add_constraint(
            self.annualized
            == self.device_count * self.device_price / 15
            + self.electricity_cost * (365 * 24) / self.num_hour
        )


class Exchanger(IntegratedEnergySystem):
    """
    热交换器类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        k: float,  # 传热系数, 没用在模型里面
        efficiency: float = 1,  # 效率系数为1
        device_name: str = "exchanger",
        device_count_min: int = 0,
        debug: bool = False,
        input_type: str = "heat",  # 进口温度
        output_type: str = "heat",  # 出口温度
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 表示热交换器的最大数量。
            device_price (float): 表示热交换器的单价。
            k (float): 传热系数(暂时没有使用)
            device_name (str): 热交换器机组名称,默认为"exchanger"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # k 传热系数
        # Exchanger.index += 1
        # self.num_hour = num_hour
        # self.device_count: ContinuousVarType = self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        热交换器机组等效单位设备数 大于零的实数变量
        """
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="exchanger_annualized_{0}".format(self.classSuffix)
        # )
        """
        连续变量,表示热交换器的年化费用
        """
        self.device_price = device_price
        self.device_count_max = device_count_max
        self.input_type = input_type
        self.output_type = output_type
        self.efficiency = efficiency
        self.build_power_of_inputs([self.input_type])
        self.build_power_of_outputs([self.output_type])
        # self.heat_exchange: List[ContinuousVarType] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="heat_exchanger_{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示热交换器的每小时热交换量
        """
        # return val

    def constraints_register(self):
        super().constraints_register()

        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦热交换器的热功率≦热交换器总设备量
        3. 热交换器的总年化成本 == 热交换器设备数 * 设备价格/15

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        # self.hourRange = range(0, self.num_hour)
        # self.model.add_constraint(self.device_count >= 0)
        # self.model.add_constraint(self.device_count <= self.device_count_max)

        # self.model.add_constraints(self.heat_exchange[h] >= 0 for h in self.hourRange)
        # self.model.add_constraints(
        #     self.heat_exchange[h] <= self.device_count for h in self.hourRange
        # )  # 天燃气蒸汽锅炉
        self.add_lower_bounds(self.power_of_inputs[self.input_type], 0)
        self.add_lower_and_upper_bounds(
            self.power_of_outputs[self.output_type],
            0,
            self.elementwise_multiply(
                self.power_of_inputs[self.input_type], self.efficiency
            ),
        )
        self.add_upper_bounds(self.power_of_inputs[self.input_type], self.device_count)
        # self.add_lower_and_upper_bounds(self.heat_exchange,0,self.device_count)

        self.model.add_constraint(
            self.annualized == self.device_count * self.device_price / 15
        )


# TODO: 运行效率与温度环境（气温）有关
class AirHeatPump(IntegratedEnergySystem):
    """
    空气源热泵类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        electricity_price: Union[np.ndarray, List],
        device_name: str = "air_heat_pump",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 表示空气热泵的最大数量。
            device_price (float): 表示空气热泵的单价。
            electricity_price (Union[np.ndarray, List]): 每小时的电价
            device_name (str): 空气热泵机组名称,默认为"air_heat_pump"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # self.num_hour = num_hour
        # AirHeatPump.index += 1
        self.electricity_price = electricity_price
        # self.device_count: ContinuousVarType = self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        空气热泵机组等效单位设备数 大于零的实数
        """
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="AirHeatPumpower_annualized_{0}".format(self.classSuffix)
        # )
        """
        连续变量,表示空气热泵的年化费用
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="electricity_cost_{0}".format(self.classSuffix)
        )
        """
        连续变量,表示空气热泵的电价成本
        """
        # 热水，冷水，储存热水，储存冷水
        # self.device_price = device_price
        # self.device_count_max = device_count_max
        self.output_types = [
            "cold_water",
            "cold_water_storage",
            "warm_water",
            "warm_water_storage",
        ]
        self.build_power_of_outputs(self.output_types)
        # self.power_of_outputs['cold_water']: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_of_outputs['cold_water']{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示空气热泵在每个时段的制冷功率
        """
        ################# THIS REPLACE ALL FOUR WORK COND INIT DEFS
        self.build_flags(self.output_types)
        for output_type in self.output_types:
            self.__dict__.update(
                {
                    f"{output_type}_out": self.model.continuous_var_list(
                        [i for i in range(0, self.num_hour)],
                        name=f"{output_type}_out_{self.classSuffix}",
                    ),
                    # f"{output_type}_flags": self.model.binary_var_list(
                    #     [i for i in range(0, self.num_hour)],
                    #     name=f"{output_type}_flag_{self.classSuffix}",
                    # ),
                }
            )
        ################# THIS REPLACE ALL FOUR WORK COND INIT DEFS

        # self.cold_water_out: List[ContinuousVarType] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="cold_water_out_{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示空气热泵在每个时段的制冷出口温度
        """
        # self.cold_water_flags: List[BinaryVarType] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="cold_water_flag_{0}".format(self.classSuffix),
        # )
        """
        二元变量列表,表示空气热泵在每个时段的制冷状态
        """

        # self.power_of_outputs['cold_water_storage']: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_of_outputs['cold_water_storage']{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示空气热泵在每个时段的蓄冷功率
        """
        # self.cold_water_storage_out: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="cold_water_storage_out_{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示空气热泵在每个时段的蓄冷出口温度
        """

        # self.cold_water_storage_flags: List[BinaryVarType] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="cold_water_storage_flag_{0}".format(self.classSuffix),
        # )
        """
        二元变量列表,表示空气热泵在每个时段的蓄冷状态
        """
        # self.power_of_outputs['hot_water']: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_of_outputs['hot_water']{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示空气热泵在每个时段的制热功率
        """
        # self.hot_water_out: List[ContinuousVarType] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="hot_water_out_{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示空气热泵在每个时段的制热出口温度
        """
        # self.hot_water_flags: List[BinaryVarType] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="hot_water_flag_{0}".format(self.classSuffix),
        # )
        """
        二元变量列表,表示空气热泵在每个时段的制热状态
        """
        # self.power_of_outputs['hot_water_storage']: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_of_outputs['hot_water_storage']{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示空气热泵在每个时段的蓄热功率
        """
        # self.hot_water_storage_out: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="hot_water_storage_out_{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示空气热泵在每个时段的蓄热出口温度
        """
        # TODO: 可以调节工作模式 热水温度较高时储存热量 （是否应当作为设备连接约束条件？）
        # self.hot_water_storage_flags: List[BinaryVarType] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="hot_water_storage_flag_{0}".format(self.classSuffix),
        # )
        """
        二元变量列表,表示空气热泵在每个时段的蓄热状态
        """

        self.input_type = "electricity"
        self.build_power_of_inputs([self.input_type])
        # self.power_of_inputs[self.input_type]: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="electricity_heatPump_{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示空气热泵在每个时段的用电量
        """
        self.power: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_{0}".format(self.classSuffix),
        )
        """
        连续变量列表,表示空气热泵在每个时段的总功率
        """

        # TODO: unclear meaning of "cooletStorage" and "heatStorage"
        for output_type in self.output_types:
            self.__dict__.update({f"coefficientOfPerformance_{output_type}": 3})
        # self.coefficientOfPerformance_cold_water = 3  # 表示该组件制冷时的性能系数
        # self.coefficientOfPerformance_cold_water_storage = 3  # 表示该组件蓄冷时的性能系数
        # self.coefficientOfPerformance_hot_water = 3  # 表示该组件供热时的性能系数
        # self.coefficientOfPerformance_hot_water_storage = 3  # 表示该组件蓄热时的性能系数

        # return val

    def constraints_register(self):
        super().constraints_register()

        """
        定义空气热泵机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦空气热泵的制冷功率≦空气热泵制冷出口温度 * 空气热泵设备数 / 100<br>0≦空气热泵的制冷功率≦空气热泵制冷状态 * bigNumber
        3. 0≦空气热泵的蓄冷功率≦空气热泵蓄冷出口温度 * 空气热泵设备数 / 100<br>0≦空气热泵的蓄冷功率≦空气热泵蓄冷状态 * bigNumber
        4. 0≦空气热泵的制热功率≦空气热泵制热出口温度 * 空气热泵设备数 / 100<br>0≦空气热泵的制热功率≦空气热泵制热状态 * bigNumber
        5. 空气0≦热泵的蓄热功率≦空气热泵蓄热出口温度 * 空气热泵设备数 / 100<br>0≦空气热泵的蓄热功率≦空气热泵蓄热状态 * bigNumber
        6. 制冷状态+蓄冷状态+制热状态+蓄热状态=1
        7. 空气热泵用电量 = 设备制冷功率/制冷性能系数+设备蓄冷功率/蓄冷性能系数+设备制热功率/制热性能系数+设备蓄热功率/蓄热性能系数
        8. 空气热泵总功率 = 制冷功率+蓄冷功率+制热功率+蓄热功率
        9. 用电成本 = 每个时刻(设备用电量 * 电价)的总和
        10. 空气热泵的总年化成本 = 空气热泵设备数 * 设备价格/15+用电成本 * (365*24)/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        # self.hourRange = range(0, self.num_hour)
        # self.model.add_constraint(0 <= self.device_count)
        # self.model.add_constraint(self.device_count <= self.device_count_max)

        ########## REPLACE ALL FOUR CONSTRAINS WITH THIS ONE
        for power_of_output, output_mode_flags, output_temperature in [
            (
                self.power_of_outputs[output_type],
                self.__dict__[f"{output_type}_flags"],  # type: ignore
                self.__dict__[f"{output_type}_out"],  # type: ignore
            )
            for output_type in self.output_types
        ]:
            self.add_lower_and_upper_bounds(
                power_of_output,
                0,
                # self.elementwise_min(
                self.elementwise_multiply(output_mode_flags, bigNumber),
                # self.elementwise_multiply(
                #     output_temperature, self.device_count / 100
                # ),
                # ),
            )
            self.add_upper_bounds(
                power_of_output,
                self.elementwise_multiply(output_temperature, self.device_count / 100),
            )
        ########## REPLACE ALL FOUR CONSTRAINS WITH THIS ONE

        # self.add_lower_and_upper_bounds(
        #     self.power_of_outputs['cold_water'],
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(self.cold_water_flags, bigNumber),
        #         self.elementwise_multiply(
        #             self.cold_water_out, self.device_count / 100
        #         ),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_of_outputs['cold_water'][h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs['cold_water'][h]
        #     <= self.cold_water_out[h] * self.device_count / 100
        #     for h in self.hourRange
        # )

        # self.add_lower_and_upper_bounds(
        #     self.power_of_outputs['cold_water'],
        #     0,
        #     self.elementwise_multiply(self.cold_water_flags, bigNumber),
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs['cold_water'][h] <= bigNumber * self.cold_water_flags[h]
        #     for h in self.hourRange
        # )

        # self.add_lower_and_upper_bounds(
        #     self.power_of_outputs['cold_water_storage'],
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.cold_water_storage_out, self.device_count / 100
        #         ),
        #         self.elementwise_multiply(self.cold_water_storage_flags, bigNumber),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_of_outputs['cold_water_storage'][h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs['cold_water_storage'][h]
        #     <= self.cold_water_storage_out[h] * self.device_count / 100
        #     for h in self.hourRange
        # )

        # self.add_upper_bounds(self.power_of_outputs['cold_water_storage'],self.elementwise_multiply(self.cold_water_storage_flags,bigNumber))

        # self.model.add_constraints(
        #     self.power_of_outputs['cold_water_storage'][h]
        #     <= bigNumber * self.cold_water_storage_flags[h]
        #     for h in self.hourRange
        # )

        # self.add_lower_and_upper_bounds(
        #     self.power_of_outputs['hot_water'],
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.hot_water_out, self.device_count / 100
        #         ),
        #         self.elementwise_multiply(self.hot_water_flags, bigNumber),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_of_outputs['hot_water'][h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs['hot_water'][h]
        #     <= self.hot_water_out[h] * self.device_count / 100
        #     for h in self.hourRange
        # )

        # self.add_upper_bounds(
        #     self.power_of_outputs['hot_water'],
        #     self.elementwise_multiply(self.hot_water_flags, bigNumber),
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs['hot_water'][h] <= bigNumber * self.hot_water_flags[h]
        #     for h in self.hourRange
        # )

        # self.add_lower_and_upper_bounds(
        #     self.power_of_outputs['hot_water_storage'],
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(self.hot_water_storage_flags, bigNumber),
        #         self.elementwise_multiply(
        #             self.hot_water_storage_out, self.device_count / 100
        #         ),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_of_outputs['hot_water_storage'][h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs['hot_water_storage'][h]
        #     <= self.hot_water_storage_out[h] * self.device_count / 100
        #     for h in self.hourRange
        # )

        # self.add_upper_bounds(
        #     self.power_of_outputs['hot_water_storage'],
        #     self.elementwise_multiply(self.hot_water_storage_flags, bigNumber),
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs['hot_water_storage'][h]
        #     <= bigNumber * self.hot_water_storage_flags[h]
        #     for h in self.hourRange
        # )

        self.equations(
            reduce(
                self.elementwise_add,
                [
                    self.__dict__[f"{output_type}_flags"]
                    for output_type in self.output_types
                ],
            ),
            1,
        )
        # self.model.add_constraints(
        #     self.cold_water_flags[h]
        #     + self.cold_water_storage_flags[h]
        #     + self.hot_water_flags[h]
        #     + self.hot_water_storage_flags[h]
        #     == 1
        #     for h in self.hourRange
        # )

        self.equations(
            reduce(
                self.elementwise_add,
                [
                    self.elementwise_divide(x, y)
                    for x, y in [
                        (
                            self.power_of_outputs[output_type],
                            self.__dict__[f"coefficientOfPerformance_{output_type}"],
                        )
                        for output_type in self.output_types
                    ]
                ],
            ),
            self.power_of_inputs[self.input_type],
        )
        # self.model.add_constraints(
        #     self.power_of_inputs[self.input_type][h]
        #     # are you sure you want to subscribe?
        #     == self.power_of_outputs['cold_water'][h]
        #     / self.coefficientOfPerformance_cold_water  # [h]
        #     + self.power_of_outputs['cold_water_storage'][h]
        #     / self.coefficientOfPerformance_cold_water_storage  # [h]
        #     + self.power_of_outputs['hot_water'][h]
        #     / self.coefficientOfPerformance_hot_water  # [h]
        #     + self.power_of_outputs['hot_water_storage'][h]
        #     / self.coefficientOfPerformance_hot_water_storage  # [h]
        #     for h in self.hourRange
        # )

        self.equations(
            self.power,
            reduce(
                self.elementwise_add,
                [
                    self.power_of_outputs[output_type]
                    for output_type in self.output_types
                ],
            ),
        )

        # self.model.add_constraints(
        #     self.power[h]
        #     == self.power_of_outputs['cold_water'][h]
        #     + self.power_of_outputs['cold_water_storage'][h]
        #     + self.power_of_outputs['hot_water'][h]
        #     + self.power_of_outputs['hot_water_storage'][h]
        #     for h in self.hourRange
        # )

        self.electricity_cost = self.sum_within_range(
            self.elementwise_multiply(
                self.power_of_inputs[self.input_type], self.electricity_price
            )
        )
        # self.electricity_cost = self.model.sum(
        #     self.power_of_inputs[self.input_type][h] * self.electricity_price[h]
        #     for h in self.hourRange
        # )
        # 年化
        self.model.add_constraint(
            self.annualized
            == self.device_count * self.device_price / 15
            + self.electricity_cost * (365 * 24) / self.num_hour
        )


# waterSourceHeatPumps
class WaterHeatPump(IntegratedEnergySystem):
    """
    水源热泵类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        electricity_price: Union[np.ndarray, List],
        case_ratio: Union[np.ndarray, List],
        device_name: str = "water_heat_pump",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 表示水源热泵的最大数量。
            device_price (float): 表示水源热泵的单价。
            electricity_price (Union[np.ndarray, List]): 每小时的电价
            case_ratio (Union[np.ndarray, List]): 不同工况下热冷效率
            device_name (str): 水源热泵机组名称,默认为"water_heat_pump"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # 不同工况下热冷效率
        # case_ratio 不同工况下制热量/制冷量的比值
        # self.num_hour = num_hour
        # # self.classSuffix += 1
        self.electricity_price = electricity_price
        # self.device_count: ContinuousVarType = self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        水源热泵机组等效单位设备数 大于零的实数
        """
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="WaterHeatPumpower_annualized_{0}".format(self.classSuffix)
        # )
        """
        连续变量,表示水源热泵的年化费用
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="electricity_cost_{0}".format(self.classSuffix)
        )
        """
        连续变量,表示水源热泵的用电成本
        """
        # self.device_price = device_price
        # self.device_count_max = device_count_max
        self.case_ratio = case_ratio

        # again, for some heavy replacements.
        self.output_types = [
            "cold_water",
            "cold_water_storage",
            "warm_water",
            "warm_water_storage",
        ]
        self.build_power_of_outputs(self.output_types)
        self.build_flags(self.output_types)

        # self.power_waterSourceHeatPumps_cool: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_waterSourceHeatPumps_cool_{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示每个时刻水源热泵制冷功率
        """

        # self.waterSourceHeatPumps_cool_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="waterSourceHeatPumps_cool_flag_{0}".format(self.classSuffix),
        # )
        """
        二元变量列表,表示每个时刻水源热泵制冷状态
        """

        # self.power_waterSourceHeatPumps_cooletStorage: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_waterSourceHeatPumps_cooletStorage_{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示每个时刻水源热泵蓄冷功率
        """
        # self.waterSourceHeatPumps_cooletStorage_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="waterSourceHeatPumps_cooletStorage_flag_{0}".format(self.classSuffix),
        # )
        """
        二元变量列表,表示每个时刻水源热泵蓄冷状态
        """
        # self.power_waterSourceHeatPumps_heat: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_waterSourceHeatPumps_heat_{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示每个时刻水源热泵制热功率
        """
        # self.waterSourceHeatPumps_heat_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="waterSourceHeatPumps_heat_flag_{0}".format(self.classSuffix),
        # )
        """
        二元变量列表,表示每个时刻水源热泵制热状态
        """
        # self.power_waterSourceHeatPumps_heatStorage: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_waterSourceHeatPumps_heatStorage_{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示每个时刻水源热泵蓄热功率
        """
        # self.waterSourceHeatPumps_heatStorage_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="waterSourceHeatPumps_heatStorage_flag_{0}".format(self.classSuffix),
        # )
        """
        二元变量列表,表示每个时刻水源热泵蓄热状态
        """
        self.input_type = "electricity"
        self.build_power_of_inputs([self.input_type])

        # self.electricity_waterSourceHeatPumps: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="electricity_waterSourceHeatPumps_{0}".format(self.classSuffix),
        # )
        """
        连续变量列表,表示每个时刻水源热泵用电量
        """
        self.power: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_{0}".format(self.classSuffix),
        )
        """
        连续变量列表,表示每个时刻水源热泵总功率
        """
        for output_type in self.output_types:
            self.__dict__.update({f"coefficientOfPerformance_{output_type}": 5})
        # self.coefficientOfPerformance_waterSourceHeatPumps_cool = 5  # 制冷性能系数
        # self.coefficientOfPerformance_waterSourceHeatPumps_cooletStorage = 5  # 蓄冷性能系数
        # self.coefficientOfPerformance_waterSourceHeatPumps_heat = 5  # 制热性能系数
        # self.coefficientOfPerformance_waterSourceHeatPumps_heatStorage = 5  # 蓄热性能系数
        # return val

    def constraints_register(self):
        super().constraints_register()

        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦水源热泵的制冷功率≦水源热泵设备数 *  (况1)热冷效率,0≦水源热泵的制冷功率≦水源热泵制冷状态 * bigNumber
        3. 0≦水源热泵的蓄冷功率≦水源热泵设备数 *  (况2)热冷效率,0≦水源热泵的蓄冷功率≦水源热泵蓄冷状态 * bigNumber
        4. 0≦水源热泵的制热功率≦水源热泵设备数 *  (况3)热冷效率,0≦水源热泵的制热功率≦水源热泵制热状态 * bigNumber
        5. 0≦水源热泵的蓄热功率≦水源热泵设备数 *  (况4)热冷效率,0≦水源热泵的蓄热功率≦水源热泵蓄热状态 * bigNumber
        6. 制冷状态+蓄冷状态+制热状态+蓄热状态=1
        7. 水源热泵用电量 = 设备制冷功率/制冷性能系数+设备蓄冷功率/蓄冷性能系数+设备制热功率/制热性能系数+设备蓄热功率/蓄热性能系数
        8. 热泵总功率 = 制冷功率+蓄冷功率+制热功率+蓄热功率
        9. 用电成本 = 每个时刻(设备用电量 * 电价)的总和
        10. 水源热泵的总年化成本 = 水源热泵设备数 * 设备价格/15+用电成本 * (365*24)/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        # self.hourRange = range(0, self.num_hour)
        # self.model.add_constraint(0 <= self.device_count)
        # self.model.add_constraint(
        #     self.device_count <= self.device_count_max
        # )

        for index, (power_of_output, output_mode_flag) in enumerate(
            [
                (
                    self.power_of_outputs[output_type],
                    self.__dict__[f"{output_type}_flags"],
                )
                for output_type in self.output_types  # is the order correct?
                # ["cold_water", "cold_water_storage", "hot_water", "hot_water_storage"]
            ]
        ):
            self.add_lower_and_upper_bounds(
                power_of_output,
                0,
                # self.elementwise_min(
                self.elementwise_multiply(output_mode_flag, bigNumber),
                #     self.multiply(self.device_count, self.case_ratio[index]),
                # ),
            )
            self.add_upper_bounds(
                power_of_output,
                self.multiply(self.device_count, self.case_ratio[index]),
            )

        # self.add_lower_and_upper_bounds(
        #     self.power_waterSourceHeatPumps_cool,
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.waterSourceHeatPumps_cool_flag, bigNumber
        #         ),
        #         self.multiply(self.device_count, self.case_ratio[0]),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_waterSourceHeatPumps_cool[h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_waterSourceHeatPumps_cool[h]
        #     <= self.device_count * self.case_ratio[0]
        #     for h in self.hourRange
        # )

        # self.add_upper_bounds(self.power_waterSourceHeatPumps_cool,self.elementwise_multiply(self.waterSourceHeatPumps_cool_flag,bigNumber))
        # self.model.add_constraints(
        #     self.power_waterSourceHeatPumps_cool[h]
        #     <= bigNumber * self.waterSourceHeatPumps_cool_flag[h]
        #     for h in self.hourRange
        # )

        # self.add_lower_and_upper_bounds(
        #     self.power_waterSourceHeatPumps_cooletStorage,
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.waterSourceHeatPumps_cooletStorage_flag, bigNumber
        #         ),
        #         self.multiply(self.device_count, self.case_ratio[1]),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_waterSourceHeatPumps_cooletStorage[h]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_waterSourceHeatPumps_cooletStorage[h]
        #     <= self.device_count * self.case_ratio[1]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_waterSourceHeatPumps_cooletStorage[h]
        #     <= bigNumber * self.waterSourceHeatPumps_cooletStorage_flag[h]
        #     for h in self.hourRange
        # )

        # self.add_lower_and_upper_bounds(
        #     self.power_waterSourceHeatPumps_heat,
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.waterSourceHeatPumps_heat_flag, bigNumber
        #         ),
        #         self.multiply(self.device_count, self.case_ratio[2]),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_waterSourceHeatPumps_heat[h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_waterSourceHeatPumps_heat[h]
        #     <= self.device_count * self.case_ratio[2]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_waterSourceHeatPumps_heat[h]
        #     <= bigNumber * self.waterSourceHeatPumps_heat_flag[h]
        #     for h in self.hourRange
        # )

        # self.add_lower_and_upper_bounds(
        #     self.power_waterSourceHeatPumps_heatStorage,
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.waterSourceHeatPumps_heatStorage_flag, bigNumber
        #         ),
        #         self.multiply(self.device_count, self.case_ratio[3]),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_waterSourceHeatPumps_heatStorage[h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_waterSourceHeatPumps_heatStorage[h]
        #     <= self.device_count * self.case_ratio[3]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_waterSourceHeatPumps_heatStorage[h]
        #     <= bigNumber * self.waterSourceHeatPumps_heatStorage_flag[h]
        #     for h in self.hourRange
        # )

        ##### ADD UP TO 1 ################

        self.equations(
            reduce(
                self.elementwise_add,
                [
                    self.__dict__[f"{output_type}_flags"]
                    for output_type in self.output_types
                ],
            ),
            1,
        )

        # self.model.add_constraints(
        #     self.waterSourceHeatPumps_cool_flag[h]
        #     + self.waterSourceHeatPumps_cooletStorage_flag[h]
        #     + self.waterSourceHeatPumps_heat_flag[h]
        #     + self.waterSourceHeatPumps_heatStorage_flag[h]
        #     == 1
        #     for h in self.hourRange
        # )

        self.equations(
            reduce(
                self.elementwise_add,
                [
                    self.elementwise_divide(x, y)
                    for x, y in [
                        (
                            self.power_of_outputs[output_type],
                            self.__dict__[f"coefficientOfPerformance_{output_type}"],
                        )
                        for output_type in self.output_types
                    ]
                ],
            ),
            self.power_of_inputs[self.input_type],
        )
        # self.model.add_constraints(
        #     self.electricity_waterSourceHeatPumps[h]
        #     == self.power_waterSourceHeatPumps_cool[h]
        #     / self.coefficientOfPerformance_waterSourceHeatPumps_cool
        #     + self.power_waterSourceHeatPumps_cooletStorage[h]
        #     / self.coefficientOfPerformance_waterSourceHeatPumps_cooletStorage
        #     + self.power_waterSourceHeatPumps_heat[h]
        #     / self.coefficientOfPerformance_waterSourceHeatPumps_heat
        #     + self.power_waterSourceHeatPumps_heatStorage[h]
        #     / self.coefficientOfPerformance_waterSourceHeatPumps_heatStorage
        #     for h in self.hourRange
        # )

        self.equations(
            self.power,
            reduce(
                self.elementwise_add,
                [
                    self.power_of_outputs[output_type]
                    for output_type in self.output_types
                ],
            ),
        )
        # self.model.add_constraints(
        #     self.power_waterSourceHeatPumps[h]
        #     == self.power_waterSourceHeatPumps_cool[h]
        #     + self.power_waterSourceHeatPumps_cooletStorage[h]
        #     + self.power_waterSourceHeatPumps_heat[h]
        #     + self.power_waterSourceHeatPumps_heatStorage[h]
        #     for h in self.hourRange
        # )

        self.electricity_cost = self.sum_within_range(
            self.elementwise_multiply(
                self.power_of_inputs[self.input_type], self.electricity_price
            )
        )
        # self.electricity_cost = self.model.sum(
        #     self.electricity_waterSourceHeatPumps[h] * self.electricity_price[h]
        #     for h in self.hourRange
        # )
        # 年化
        self.model.add_constraint(
            self.annualized
            == self.device_count * self.device_price / 15
            + self.electricity_cost * (365 * 24) / self.num_hour
        )


# waterCoolingSpiralMachine
class WaterCoolingSpiral(IntegratedEnergySystem):
    """
    水冷螺旋机
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        electricity_price: Union[np.ndarray, List],
        case_ratio: Union[np.ndarray, List],
        device_name: str = "water_cooled_spiral",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 表示水冷螺旋机的最大数量。
            device_price (float): 表示水冷螺旋机的单价。
            electricity_price (Union[np.ndarray, List]): 每小时电价
            case_ratio (Union[np.ndarray, List]): 不同工况下水冷螺旋机利用率
            device_name (str): 水冷螺旋机机组名称,默认为"water_cooled_spiral"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # self.num_hour = num_hour
        # # self.classSuffix += 1
        self.electricity_price = electricity_price
        # self.device_count: ContinuousVarType = (
        #     self.model.continuous_var(
        #         name="device_count_{0}".format(
        #             self.classSuffix
        #         )
        #     )
        # )
        """
        水冷螺旋机机组等效单位设备数 大于零的实数
        """
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="waterCoolingSpiral_annualized_{0}".format(self.classSuffix)
        # )
        """
        连续变量,表示水冷螺旋机的年化费用
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="electricity_cost_{0}".format(self.classSuffix)
        )
        """
        连续变量,表示水冷螺旋机的用电成本
        """
        self.device_price = device_price
        self.device_count_max = device_count_max
        self.case_ratio = case_ratio  # are they matched?
        self.output_types = ["cold_water", "cold_water_storage"]

        self.build_power_of_outputs(self.output_types)
        self.build_flags(self.output_types)

        # power of outputs total?
        # self.power_of_outputs_cold_water: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_of_outputs_cold_water_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        连续变量列表,表示水冷螺旋机的制冷功率
        """
        # either "cold_water" or "cold_water_storage"
        # self.waterCoolingSpiralMachine_cool_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="waterCoolingSpiralMachine_cool_flag_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        二元变量列表,表示水冷螺旋机的散热状态
        """

        # self.power_of_outputs_coolet_storage: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_of_outputs_coolet_storage_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        连续变量列表,表示水冷螺旋机的蓄冷功率
        """

        # self.waterCoolingSpiralMachine_cooletStorage_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="waterCoolingSpiralMachine_cooletStorage_flag_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        二元变量列表,表示水冷螺旋机的蓄冷状态
        """
        self.input_type = "electricity"
        self.build_power_of_inputs([self.input_type])

        # self.electricity_waterCoolingSpiralMachine: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="electricity_waterCoolingSpiralMachine_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        连续变量列表,表示水冷螺旋机的用电量
        """
        self.power: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_{0}".format(self.classSuffix),
        )
        """
        连续变量列表,表示水冷螺旋机的功率
        """
        for output_type in self.output_types:
            self.__dict__.update({f"coefficientOfPerformance_{output_type}": 5})
        # self.coefficientOfPerformance_waterCoolingSpiralMachine_cool = 5
        # self.coefficientOfPerformance_waterCoolingSpiralMachine_cooletStorage = 5
        # return val

    def constraints_register(self):
        super().constraints_register()

        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦水冷螺旋机的制冷功率≦水冷螺旋机设备数 * (况1)制冷情况下水冷螺旋机利用率<br>0≦水冷螺旋机的制冷功率≦水冷螺旋机制冷状态 * bigNumber
        3. 0≦水冷螺旋机的蓄冷功率≦水冷螺旋机设备数 * (况2)蓄冷情况下水冷螺旋机利用率<br>0≦水冷螺旋机的蓄冷功率≦水冷螺旋机蓄冷状态 * bigNumber
        4. 制冷状态+蓄冷状态=1
        5. 水冷螺旋机用电量 = 设备制冷功率/制冷性能系数+设备蓄冷功率/蓄冷性能系数
        6. 热泵总功率 = 制冷功率+蓄冷功率
        7. 用电成本 = 每个时刻(设备用电量 * 电价)的总和
        8. 水冷螺旋机的总年化成本 = 水源热泵设备数 * 设备价格/15+用电成本 * (365*24)/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        # self.hourRange = range(0, self.num_hour)
        # self.model.add_constraint(0 <= self.device_count)
        # self.model.add_constraint(
        #     self.device_count <= self.device_count_max
        # )

        for index, output_type in enumerate(self.output_types):
            self.add_lower_and_upper_bounds(
                self.power_of_outputs[output_type],
                0,
                # self.elementwise_min(
                self.elementwise_multiply(
                    self.__dict__[f"{output_type}_flags"], bigNumber
                ),
                # self.multiply(self.device_count, self.case_ratio[index]),
                # ),
            )

            self.add_upper_bounds(
                self.power_of_outputs[output_type],
                self.multiply(self.device_count, self.case_ratio[index]),
            )

        ##############
        # self.add_lower_and_upper_bounds(
        #     self.power_of_outputs_cold_water,
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.waterCoolingSpiralMachine_cool_flag, bigNumber
        #         ),
        #         self.multiply(self.device_count, self.case_ratio[0]),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_of_outputs_cold_water[h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs_cold_water[h]
        #     <= self.device_count * self.case_ratio[0]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs_cold_water[h]
        #     <= bigNumber * self.waterCoolingSpiralMachine_cool_flag[h]
        #     for h in self.hourRange
        # )

        # self.add_lower_and_upper_bounds(
        #     self.power_of_outputs_coolet_storage,
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.waterCoolingSpiralMachine_cooletStorage_flag, bigNumber
        #         ),
        #         self.multiply(self.device_count, self.case_ratio[1]),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_of_outputs_coolet_storage[h]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs_coolet_storage[h]
        #     <= self.device_count * self.case_ratio[1]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs_coolet_storage[h]
        #     <= bigNumber * self.waterCoolingSpiralMachine_cooletStorage_flag[h]
        #     for h in self.hourRange
        # )

        self.equations(
            reduce(
                self.elementwise_add,
                [
                    self.__dict__[f"{output_type}_flags"]
                    for output_type in self.output_types
                ],
            ),
            1,
        )
        # self.equations(
        #     self.elementwise_add(
        #         self.waterCoolingSpiralMachine_cool_flag,
        #         self.waterCoolingSpiralMachine_cooletStorage_flag,
        #     ),
        #     1,
        # )
        # self.model.add_constraints(
        #     self.waterCoolingSpiralMachine_cool_flag[h]
        #     + self.waterCoolingSpiralMachine_cooletStorage_flag[h]
        #     == 1
        #     for h in self.hourRange
        # )

        self.equations(
            self.power_of_inputs[self.input_type],
            reduce(
                self.elementwise_add,
                [
                    self.elementwise_divide(
                        self.power_of_outputs[output_type],
                        self.__dict__[f"coefficientOfPerformance_{output_type}"],
                    )
                    for output_type in self.output_types
                ],
            ),
        )

        # self.equations(
        #     self.electricity_waterCoolingSpiralMachine,
        #     self.elementwise_add(
        #         self.elementwise_divide(
        #             self.power_of_outputs_cold_water,
        #             self.coefficientOfPerformance_waterCoolingSpiralMachine_cool,
        #         ),
        #         self.elementwise_divide(
        #             self.power_of_outputs_coolet_storage,
        #             self.coefficientOfPerformance_waterCoolingSpiralMachine_cooletStorage,
        #         ),
        #     ),
        # )

        # self.model.add_constraints(
        #     self.electricity_waterCoolingSpiralMachine[h]
        #     == self.power_of_outputs_cold_water[h]
        #     / self.coefficientOfPerformance_waterCoolingSpiralMachine_cool
        #     + self.power_of_outputs_coolet_storage[h]
        #     / self.coefficientOfPerformance_waterCoolingSpiralMachine_cooletStorage
        #     for h in self.hourRange
        # )

        self.equations(
            self.power,
            reduce(
                self.elementwise_add,
                [
                    self.power_of_outputs[output_type]
                    for output_type in self.output_types
                ],
            ),
        )

        # self.equations(
        #     self.power,
        #     self.elementwise_add(
        #         self.power_of_outputs_cold_water,
        #         self.power_of_outputs_coolet_storage,
        #     ),
        # )

        # self.model.add_constraints(
        #     self.power[h]
        #     == self.power_of_outputs_cold_water[h]
        #     + self.power_of_outputs_coolet_storage[h]
        #     for h in self.hourRange
        # )

        self.electricity_cost = self.sum_within_range(
            self.elementwise_multiply(
                self.power_of_inputs[self.input_type], self.electricity_price
            )
        )
        # self.electricity_cost = self.model.sum(
        #     self.electricity_waterCoolingSpiralMachine[h] * self.electricity_price[h]
        #     for h in self.hourRange
        # )
        # 年化
        self.model.add_constraint(
            self.annualized
            == self.device_count * self.device_price / 15
            + self.electricity_cost * (365 * 24) / self.num_hour
        )


# 双工况机组
# ice must be stored, turned into cold water.
# working conditions: ['cold_water', 'ice']
class DoubleWorkingConditionUnit(IntegratedEnergySystem):
    """
    双工况机组类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        electricity_price: Union[np.ndarray, List],
        case_ratio: Union[np.ndarray, List],
        device_name: str = "doubleWorkingConditionUnit",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 表示双工况机组的最大数量。
            device_price (float): 表示双工况机组的单价。
            electricity_price (Union[np.ndarray, List]): 每小时电价
            case_ratio (Union[np.ndarray, List]): 不同工况下双工况机组利用率
            device_name (str): 双工况机组名称,默认为"doubleWorkingConditionUnit"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # self.num_hour = num_hour
        # # self.classSuffix += 1
        self.output_types = ["cold_water", "ice"]  # matched?
        self.input_type = "electricity"
        self.electricity_price = electricity_price
        # self.device_count: ContinuousVarType = (
        #     self.model.continuous_var(
        #         name="device_count_{0}".format(
        #             self.classSuffix
        #         )
        #     )
        # )
        """
        双工况机组等效单位设备数 大于零的实数
        """
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="DoubleWorkingConditionUnit_annualized_{0}".format(
        #         self.classSuffix
        #     )
        # )
        """
        连续变量,表示双工况机组的年化费用
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="electricity_cost_{0}".format(self.classSuffix)
        )
        """
        连续变量,表示双工况机组的用电成本
        """
        # self.device_price = device_price
        # self.device_count_max = device_count_max
        self.case_ratio = case_ratio
        self.build_power_of_outputs(self.output_types)
        self.build_flags(self.output_types)

        # self.power_cool: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_cool_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        连续变量列表,表示双工况机组的制冷功率
        """

        # self.doubleWorkingConditionUnit_cool_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="doubleWorkingConditionUnit_cool_flag_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        二元变量列表,表示双工况机组的制冷状态
        """

        # self.power_ice: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_ice_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        连续变量列表,表示双工况机组的制冰功率
        """

        # self.doubleWorkingConditionUnit_ice_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="doubleWorkingConditionUnit_ice_flag_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        二元变量列表,表示双工况机组的制冰状态
        """
        self.build_power_of_inputs([self.input_type])
        # self.electricity_doubleWorkingConditionUnit: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="electricity_doubleWorkingConditionUnit_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        连续变量列表,表示双工况机组的用电量
        """
        self.power: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_{0}".format(self.classSuffix),
        )
        """
        连续变量列表,表示双工况机组的功率
        """
        for output_type in self.output_types:
            self.__dict__[f"coefficientOfPerformance_{output_type}"] = 5
        # self.coefficientOfPerformance_doubleWorkingConditionUnit_cool = 5
        # self.coefficientOfPerformance_doubleWorkingConditionUnit_ice = 5

        # 三工况机组
        # return val

    def constraints_register(self):
        super().constraints_register()

        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦双工况机组的制冷功率≦双工况机组设备数 *  (况1)制冷情况下双工况机组利用率<br>0≦双工况机组的制冷功率≦双工况机组制冷状态 * bigNumber
        3. 0≦双工况机组的制冰功率≦双工况机组设备数 *  (况2)制冰情况下双工况机组利用率<br>0≦双工况机组的制冰功率≦双工况机组制冰状态 * bigNumber
        4. 制冷状态+制冰状态=1
        5. 双工况机组用电量 = 设备制冷功率/制冷性能系数+设备制冰功率/制冰性能系数
        6. 热泵总功率 = 制冷功率+制冰功率
        7. 用电成本 = 每个时刻(设备用电量 * 电价)的总和
        8. 双工况机组的总年化成本 = 双工况机组设备数 * 设备价格/15+用电成本 * (365*24)/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        # self.hourRange = range(0, self.num_hour)
        # self.model.add_constraint(0 <= self.device_count)
        # self.model.add_constraint(
        #     self.device_count <= self.device_count_max
        # )

        for index, output_type in enumerate(self.output_types):
            self.add_lower_and_upper_bounds(
                self.power_of_outputs[output_type],
                0,
                # self.elementwise_min(
                self.elementwise_multiply(
                    self.__dict__[f"{output_type}_flags"], bigNumber
                ),
                # self.multiply(self.device_count, self.case_ratio[index]),
                # ),
            )
            self.add_upper_bounds(
                self.power_of_outputs[output_type],
                self.multiply(self.device_count, self.case_ratio[index]),
            )

        #################
        # self.add_lower_and_upper_bounds(
        #     self.power_cool,
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.doubleWorkingConditionUnit_cool_flag, bigNumber
        #         ),
        #         self.multiply(
        #             self.device_count, self.case_ratio[0]
        #         ),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_cool[h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_cool[h]
        #     <= self.device_count * self.case_ratio[0]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_cool[h]
        #     <= bigNumber * self.doubleWorkingConditionUnit_cool_flag[h]
        #     for h in self.hourRange
        # )

        # self.add_lower_and_upper_bounds(
        #     self.power_ice,
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.doubleWorkingConditionUnit_ice_flag, bigNumber
        #         ),
        #         self.multiply(
        #             self.device_count, self.case_ratio[1]
        #         ),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_ice[h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_ice[h]
        #     <= self.device_count * self.case_ratio[1]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_ice[h]
        #     <= bigNumber * self.doubleWorkingConditionUnit_ice_flag[h]
        #     for h in self.hourRange
        # )

        self.equations(
            reduce(
                self.elementwise_add,
                [
                    self.__dict__[f"{output_type}_flags"]
                    for output_type in self.output_types
                ],
            ),
            1,
        )

        # self.equations(
        #     self.elementwise_add(
        #         self.doubleWorkingConditionUnit_cool_flag,
        #         self.doubleWorkingConditionUnit_ice_flag,
        #     ),
        #     1,
        # )
        # self.model.add_constraints(
        #     self.doubleWorkingConditionUnit_cool_flag[h]
        #     + self.doubleWorkingConditionUnit_ice_flag[h]
        #     == 1
        #     for h in self.hourRange
        # )

        self.equations(
            self.power_of_inputs[self.input_type],
            reduce(
                self.elementwise_add,
                [
                    self.elementwise_divide(
                        self.power_of_outputs[output_type],
                        self.__dict__[f"coefficientOfPerformance_{output_type}"],
                    )
                    for output_type in self.output_types
                ],
            ),
        )

        # self.equations(
        #     self.electricity_doubleWorkingConditionUnit,
        #     self.elementwise_add(
        #         self.elementwise_divide(
        #             self.power_cool,
        #             self.coefficientOfPerformance_doubleWorkingConditionUnit_cool,
        #         ),
        #         self.elementwise_divide(
        #             self.power_ice,
        #             self.coefficientOfPerformance_doubleWorkingConditionUnit_ice,
        #         ),
        #     ),
        # )

        # self.model.add_constraints(
        #     self.electricity_doubleWorkingConditionUnit[h]
        #     == self.power_cool[h]
        #     / self.coefficientOfPerformance_doubleWorkingConditionUnit_cool
        #     + self.power_ice[h]
        #     / self.coefficientOfPerformance_doubleWorkingConditionUnit_ice
        #     for h in self.hourRange
        # )

        self.equations(
            self.power,
            reduce(
                self.elementwise_add,
                [
                    self.power_of_outputs[output_type]
                    for output_type in self.output_types
                ],
            ),
        )

        # self.equations(
        #     self.power,
        #     self.elementwise_add(
        #         self.power_cool,
        #         self.power_ice,
        #     ),
        # )
        # self.model.add_constraints(
        #     self.power[h]
        #     == self.power_cool[h]
        #     + self.power_ice[h]
        #     for h in self.hourRange
        # )

        self.electricity_cost = self.sum_within_range(
            self.elementwise_multiply(
                self.power_of_inputs[self.input_type], self.electricity_price
            )
        )
        # self.electricity_cost = self.model.sum(
        #     self.electricity_doubleWorkingConditionUnit[h] * self.electricity_price[h]
        #     for h in self.hourRange
        # )
        # 年化
        self.model.add_constraint(
            self.annualized
            == self.device_count * self.device_price / 15
            + self.electricity_cost * (365 * 24) / self.num_hour
        )


# TODO: 冷水机组效率与带载情况有关 考虑分段拟合
# working conditions: ['cold_water', 'ice', 'warm_water']
class TripleWorkingConditionUnit(IntegratedEnergySystem):
    """
    三工况机组类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        electricity_price: Union[np.ndarray, List],
        case_ratio: Union[np.ndarray, List],
        device_name: str = "tripleWorkingConditionUnit",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 表示三工况机组的最大数量
            device_price (float): 表示三工况机组的单价
            electricity_price (Union[np.ndarray, List]): 每小时电价
            case_ratio (Union[np.ndarray, List]): 不同工况下三工况机组利用率
            device_name (str): 三工况机组名称,默认为"tripleWorkingConditionUnit"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # self.num_hour = num_hour
        # # self.classSuffix += 1
        self.electricity_price = electricity_price
        # self.device_count: ContinuousVarType = (
        #     self.model.continuous_var(
        #         name="device_count_{0}".format(
        #             self.classSuffix
        #         )
        #     )
        # )
        """
        三工况机组等效单位设备数 大于零的实数
        """
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="TripleWorkingConditionUnit_annualized_{0}".format(
        #         self.classSuffix
        #     )
        # )
        """
        连续变量,表示三工况机组的年化费用
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="electricity_cost_{0}".format(self.classSuffix)
        )
        """
        连续变量,表示三工况机组的用电成本
        """
        # self.device_price = device_price
        # self.device_count_max = device_count_max
        self.case_ratio = case_ratio
        self.output_types = ["cold_water", "ice", "warm_water"]
        self.build_power_of_outputs(self.output_types)
        self.build_flags(self.output_types)
        # self.power_cool: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_cool_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        连续变量列表,表示三工况机组的制冷功率
        """

        # self.tripleWorkingConditionUnit_cool_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="tripleWorkingConditionUnit_cool_flag_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        二元变量列表,表示三工况机组的制冷状态
        """

        # self.power_ice: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_ice_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        连续变量列表,表示三工况机组的制冰功率
        """

        # self.tripleWorkingConditionUnit_ice_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="tripleWorkingConditionUnit_ice_flag_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        二元变量列表,表示三工况机组的制冰状态
        """

        # self.power_heat: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_heat_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        连续变量列表,表示三工况机组的制热功率
        """

        # self.tripleWorkingConditionUnit_heat_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="tripleWorkingConditionUnit_heat_flag_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        二元变量列表,表示三工况机组的制热状态
        """
        self.input_type = "electricity"
        self.build_power_of_inputs([self.input_type])
        # self.electricity_tripleWorkingConditionUnit: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="electricity_tripleWorkingConditionUnit_{0}".format(
        #         self.classSuffix
        #     ),
        # )
        """
        连续变量列表,表示三工况机组的用电量
        """
        self.power: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_{0}".format(self.classSuffix),
        )
        """
        连续变量列表,表示三工况机组的功率
        """
        for output_type, coefficientOfPerformance in zip(self.output_types, [5, 4, 5]):
            self.__dict__.update(
                {f"coefficientOfPerformance_{output_type}": coefficientOfPerformance}
            )
        # self.coefficientOfPerformance_tripleWorkingConditionUnit_cool = 5
        # self.coefficientOfPerformance_tripleWorkingConditionUnit_ice = 4
        # self.coefficientOfPerformance_tripleWorkingConditionUnit_heat = 5
        # return val

    def constraints_register(self):
        super().constraints_register()

        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦三工况机组的制冷功率≦三工况机组设备数 *  (况1)制冷情况下三工况机组利用率<br>0≦三工况机组的制冷功率≦三工况机组制冷状态 * bigNumber
        3. 0≦三工况机组的制冰功率≦三工况机组设备数 *  (况2)制冰情况下三工况机组利用率<br>0≦三工况机组的制冰功率≦三工况机组制冰状态 * bigNumber
        4. 0≦三工况机组的制热功率≦三工况机组设备数 *  (况3)制热情况下三工况机组利用率<br>0≦三工况机组的制热功率≦三工况机组制热状态 * bigNumber
        5. 制冷状态+制冰状态+制热状态=1
        6. 三工况机组用电量 = 设备制冷功率/制冷性能系数+设备制冰功率/制冰性能系数+设备制热功率/制热性能系数
        7. 热泵总功率 = 制冷功率+制冰功率+制热功率
        8. 用电成本 = 每个时刻(设备用电量 * 电价)的总和
        9. 三工况机组的总年化成本 = 三工况机组设备数 * 设备价格/15+用电成本 * (365*24)/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        # self.hourRange = range(0, self.num_hour)
        # self.model.add_constraint(0 <= self.device_count)
        # self.model.add_constraint(
        #     self.device_count <= self.device_count_max
        # )

        for index, output_type in enumerate(self.output_types):
            self.add_lower_and_upper_bounds(
                self.power_of_outputs[output_type],
                0,
                # self.elementwise_min(
                self.elementwise_multiply(
                    self.__dict__[f"{output_type}_flags"], bigNumber
                ),
                # self.multiply(self.device_count, self.case_ratio[index]),
                # ),
            )

            self.add_upper_bounds(
                self.power_of_outputs[output_type],
                self.multiply(self.device_count, self.case_ratio[index]),
            )
        ################################

        # self.add_lower_and_upper_bounds(
        #     self.power_cool,
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.tripleWorkingConditionUnit_cool_flag, bigNumber
        #         ),
        #         self.multiply(self.device_count, self.case_ratio[0]),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_cool[h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_cool[h]
        #     <= self.device_count * self.case_ratio[0]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_cool[h]
        #     <= bigNumber * self.tripleWorkingConditionUnit_cool_flag[h]
        #     for h in self.hourRange
        # )

        # self.add_lower_and_upper_bounds(
        #     self.power_ice,
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.tripleWorkingConditionUnit_ice_flag, bigNumber
        #         ),
        #         self.multiply(self.device_count, self.case_ratio[1]),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_ice[h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_ice[h]
        #     <= self.device_count * self.case_ratio[1]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_ice[h]
        #     <= bigNumber * self.tripleWorkingConditionUnit_ice_flag[h]
        #     for h in self.hourRange
        # )

        # self.add_lower_and_upper_bounds(
        #     self.power_heat,
        #     0,
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.tripleWorkingConditionUnit_heat_flag, bigNumber
        #         ),
        #         self.multiply(self.device_count, self.case_ratio[2]),
        #     ),
        # )
        # self.model.add_constraints(
        #     0 <= self.power_heat[h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_heat[h]
        #     <= self.device_count * self.case_ratio[2]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_heat[h]
        #     <= bigNumber * self.tripleWorkingConditionUnit_heat_flag[h]
        #     for h in self.hourRange
        # )

        self.equations(
            reduce(
                self.elementwise_add,
                [
                    self.__dict__[f"{output_type}_flags"]
                    for output_type in self.output_types
                ],
            ),
            1,
        )

        # self.model.add_constraints(
        #     self.tripleWorkingConditionUnit_cool_flag[h]
        #     + self.tripleWorkingConditionUnit_ice_flag[h]
        #     + self.tripleWorkingConditionUnit_heat_flag[h]
        #     == 1
        #     for h in self.hourRange
        # )

        self.equations(
            self.power_of_inputs[self.input_type],
            reduce(
                self.elementwise_add,
                [
                    self.elementwise_divide(
                        self.power_of_outputs[output_type],
                        self.__dict__[f"coefficientOfPerformance_{output_type}"],
                    )
                    for output_type in self.output_types
                ],
            ),
        )

        # self.model.add_constraints(
        #     self.electricity_tripleWorkingConditionUnit[h]
        #     == self.power_cool[h]
        #     / self.coefficientOfPerformance_tripleWorkingConditionUnit_cool
        #     + self.power_ice[h]
        #     / self.coefficientOfPerformance_tripleWorkingConditionUnit_ice
        #     + self.power_heat[h]
        #     / self.coefficientOfPerformance_tripleWorkingConditionUnit_heat
        #     for h in self.hourRange
        # )

        self.equations(
            self.power,
            reduce(
                self.elementwise_add,
                [
                    self.power_of_outputs[output_type]
                    for output_type in self.output_types
                ],
            ),
        )

        # self.model.add_constraints(
        #     self.power[h] == self.power_cool[h] + self.power_ice[h] + self.power_heat[h]
        #     for h in self.hourRange
        # )

        self.electricity_cost = self.sum_within_range(
            self.elementwise_multiply(
                self.power_of_inputs[self.input_type], self.electricity_price
            )
        )
        # self.electricity_cost = self.model.sum(
        #     self.electricity_tripleWorkingConditionUnit[h] * self.electricity_price[h]
        #     for h in self.hourRange
        # )
        # 年化
        self.model.add_constraint(
            self.annualized
            == self.device_count * self.device_price / 15
            + self.electricity_cost * (365 * 24) / self.num_hour
        )


class GeothermalHeatPump(IntegratedEnergySystem):
    """地源热泵类"""

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        electricity_price: Union[np.ndarray, List],
        device_name: str = "geothermal_heat_pump",
        device_count_min: int = 0,
        debug: bool = False,
        output_type: Union[Literal["cold_water"], Literal["warm_water"]] = "warm_water",
    ):
        """新建一个地源热泵类

        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 地源热泵机组最大装机量
            device_price (float): 设备单价
            electricity_price (Union[np.ndarray, List]): 24小时用电价格
            device_name (str): 地源热泵机组名称,默认为"geothermal_heat_pump"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # self.num_hour = num_hour
        # # self.classSuffix += 1
        self.electricity_price = electricity_price
        # self.device_count: ContinuousVarType = self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        地源热泵机组设备数量
        """
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="GeothermalHeatPumpower_annualized_{0}".format(self.classSuffix)
        # )
        """
        地源热泵机组年运维成本
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="electricity_cost_{0}".format(self.classSuffix)
        )
        """
        地源热泵每小时耗电费用
        """
        self.device_price = device_price
        self.device_count_max = device_count_max

        self.input_type = "electricity"
        self.build_power_of_inputs([self.input_type])

        # self.electricity_groundSourceHeatPump: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="electricity_groundSourceHeatPump_{0}".format(self.classSuffix),
        # )
        """
        地源热泵每小时耗电量
        """
        self.output_type = output_type
        self.build_power_of_outputs([self.output_type])
        # self.power_groundSourceHeatPump: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_groundSourceHeatPump_{0}".format(self.classSuffix),
        # )
        """
        地源热泵每小时输出功率
        """
        self.coefficientOfPerformance = 5
        """
        地源热泵设备运行效率参数 默认为5
        """
        # return val

    def constraints_register(self):
        super().constraints_register()

        """
        定义地源热泵机组约束条件:

        1. 0 <= 机组设备数量 <= 最大装机量
        2. 0 <= 每小时输出功率 <= 机组设备数量
        3. 每小时耗电量 = 每小时输出功率 / 运行效率参数
        4. 机组一天用电费用 = sum(每小时耗电量 * 该小时用电价格)
        5. 机组年运维成本 = 机组设备数量 * 设备价格 / 15 + 机组一天用电费用 * (365*24) / 一天小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        # self.hourRange = range(0, self.num_hour)
        # self.model.add_constraint(0 <= self.device_count)
        # self.model.add_constraint(
        #     self.device_count <= self.device_count_max
        # )

        self.add_lower_and_upper_bounds(
            self.power_of_outputs[self.output_type], 0, self.device_count
        )
        # self.model.add_constraints(
        #     0 <= self.power_groundSourceHeatPump[h] for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_groundSourceHeatPump[h] <= self.device_count
        #     for h in self.hourRange
        # )

        self.equations(
            self.power_of_inputs[self.input_type],
            self.elementwise_divide(
                self.power_of_outputs[self.output_type],
                self.coefficientOfPerformance,
            ),
        )
        # self.model.add_constraints(
        #     self.electricity_groundSourceHeatPump[h]
        #     == self.power_groundSourceHeatPump[h]
        #     / self.coefficientOfPerformance_groundSourceHeatPump
        #     for h in self.hourRange
        # )

        self.electricity_cost = self.sum_within_range(
            self.elementwise_multiply(
                self.power_of_inputs[self.input_type], self.electricity_price
            )
        )
        # self.electricity_cost = self.model.sum(
        #     self.electricity_groundSourceHeatPump[h] * self.electricity_price[h]
        #     for h in self.hourRange
        # )
        # 年化
        self.model.add_constraint(
            self.annualized
            == self.device_count * self.device_price / 15
            + self.electricity_cost * (365 * 24) / self.num_hour
        )


# 水蓄能,可蓄highTemperature,可以蓄低温
# inputs: "cold_water_storage", "warm_water_storage", "hot_water_storage"
# outputs: "cold_water", "warm_water", "hot_water"
# waterStorageTank,可变容量的储能体


class WaterEnergyStorage(IntegratedEnergySystem):
    """
    水蓄能类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        # device_count_max: float,
        volume_max: float,  # V?
        # device_price: float,
        volume_price: float,
        device_price_powerConversionSystem: float,
        conversion_rate_max: float,
        efficiency: float,
        energy_init: float,
        stateOfCharge_min: float,
        stateOfCharge_max: float,
        ratio_cold_water: float,
        ratio_warm_water: float,
        ratio_hot_water: float,  # gheat? 工作热量？ geothermal heat?
        device_name: str = "water_energy_storage",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        创建一个水蓄能类

        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            volume_max (float): 单个水罐的最大体积
            volume_price (float): 单位体积储水费用
            device_price_powerConversionSystem (float): 电力转换系统设备价格
            conversion_rate_max (float): 最大充放能倍率
            efficiency (float): 水罐储水效率参数
            energy_init (float): 储能装置的初始能量
            stateOfCharge_min (float): 最小储能量
            stateOfCharge_max (float): 最大储能量
            ratio_cold_water (float): 蓄冷模式下水蓄能罐单位体积的蓄冷效率
            ratio_warm_water (float): 蓄热模式下水蓄能罐单位体积的蓄热效率
            ratio_hot_water (float): 地源热泵模式下水蓄能罐单位体积的蓄热效率
            device_name (str): 水蓄能机组名称,默认为"water_energy_storage",
        """
        # self.device_name = device_name

        device_count_max = device_price = 0
        # this is special. volume determines the price.

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # self.num_hour = num_hour
        self.model = model
        # 对于水蓄能,优化的变量为水罐的体积

        # self.input_types = [
        #     "cold_water_storage",
        #     "warm_water_storage",
        #     "hot_water_storage",
        # ]
        self.output_types = ["cold_water", "warm_water", "hot_water"]
        self.input_types = [
            output_type if output_type == "hot_water" else f"{output_type}_storage"
            for output_type in self.output_types
        ]  # false. we do not have the hot_water_storage option.
        self.waterStorageTank = EnergyStorageSystemVariable(
            num_hour,
            model,
            bigNumber,
            0,
            device_price_powerConversionSystem,
            conversion_rate_max,
            efficiency,
            energy_init,
            stateOfCharge_min,
            stateOfCharge_max,
        )
        """
        水蓄能罐,由可变储能设备'EnergyStorageSystemVariable'创建而来
        """
        # self.index = self.classSuffix
        ratios = [ratio_cold_water, ratio_warm_water, ratio_hot_water]
        for index, output_type in enumerate(self.output_types):
            self.__dict__.update(
                {
                    f"device_count_{output_type}": self.model.continuous_var_list(
                        [i for i in range(0, self.num_hour)],
                        name=f"device_count_{output_type}_{self.classSuffix}",
                    ),
                    f"ratio_{output_type}": ratios[index],
                }
            )
        # self.device_count_cold_water: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="device_count_cold_water_{0}".format(self.classSuffix),
        # )
        """
        每小时水蓄能在蓄冷模式下的储水量
        """
        # self.waterStorageTank_device_heat: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="waterStorageTank_device_heat_{0}".format(self.classSuffix),
        # )
        """
        每小时水蓄能在蓄热模式下的储水量
        """
        # self.waterStorageTank_device_gheat: List[  # generate?
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="waterStorageTank_device_gheat_{0}".format(self.classSuffix),
        # )
        """
        每小时水蓄能在地源热泵模式下的储水量
        """
        self.volume_price = volume_price
        self.volume_max = volume_max
        self.volume: ContinuousVarType = self.model.continuous_var(
            name="volume_{0}".format(self.classSuffix)
        )
        """
        水蓄能机组总体积
        """
        self.build_flags(self.output_types)
        # self.waterStorageTank_cool_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="waterStorageTank_cool_flag_{0}".format(self.classSuffix),
        # )
        """
        每小时水蓄能设备是否处在蓄冷状态下
        """
        # self.waterStorageTank_heat_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="waterStorageTank_heat_flag_{0}".format(self.classSuffix),
        # )
        """
        每小时水蓄能设备是否处在蓄热状态下
        """
        # self.waterStorageTank_gheat_flag: List[
        #     BinaryVarType
        # ] = self.model.binary_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="waterStorageTank_gheat_flag_{0}".format(self.classSuffix),
        # )
        """
        每小时水蓄能设备是否处在高温热水状态下
        """
        # self.ratio_cold_water = ratio_cold_water
        # self.ratio_warm_water = ratio_warm_water
        # self.ratio_hot_water = ratio_hot_water  # 蓄能效率 高温水
        self.build_power_of_inputs(self.input_types)
        self.build_power_of_outputs(self.output_types)
        # self.power_waterStorageTank_cool: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_waterStorageTank_cool_{0}".format(self.classSuffix),
        # )
        # self.waterStorageTank.power_of_inputs['energy'] = ...
        # self.waterStorageTank.power_of_outputs['energy'] = ...
        """
        每小时水蓄能设备储能功率 蓄冷状态下
        """
        # self.power_waterStorageTank_heat: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_waterStorageTank_heat_{0}".format(self.classSuffix),
        # )
        """
        每小时水蓄能设备储能功率 蓄热状态下
        """
        # self.power_waterStorageTank_gheat: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_waterStorageTank_gheat_{0}".format(self.classSuffix),  # gheat?
        # )
        """
        每小时水蓄能设备储能功率 高温热水状态下
        """
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="power_waterStorageTank_annualized_{0}".format(self.classSuffix)
        # )
        """
        水蓄能设备年运维费用
        """
        # return val

    def constraints_register(self, register_period_constraints: int, day_node: int):
        super().constraints_register()

        """
        定义水蓄能类的约束条件:

        1. 0≦机组设备数≦最大设备量
        2. 0≦水蓄能机组总体积≦最大体积量
        3. 水储能罐储能系统设备数=制冷状态下设备数+制热状态下设备数+高温热水状态下设备数
        4. <p>蓄冷下设备数≦水蓄能机组总体积 * 蓄冷模式下水蓄能罐的利用率<br>
           蓄冷下设备数≦水储能罐在蓄冷状态下 * bigNumber<br>
           蓄冷下设备数≧0<br>
           蓄冷下设备数≧水蓄能机组总体积 * 蓄冷模式下水蓄能罐的利用率-(1-水储能罐在蓄冷状态量) * bigNumber</p>
        5. <p>蓄热下设备数≦水蓄能机组总体积 * 蓄热模式下水蓄能罐的利用率<br>
           蓄热下设备数≦水储能罐在蓄热状态下 * bigNumber<br>
           蓄热下设备数≧0<br>
           蓄热下设备数≧水蓄能机组总体积 * 蓄热模式下水蓄能罐的利用率-(1-水储能罐在蓄热状态量) * bigNumber</p>
        6. <p>地源热泵下设备数≦水蓄能机组总体积 * 地源热泵模式下水蓄能罐的利用率<br>
           地源热泵下设备数≦水储能罐在高温热水状态下 * bigNumber<br>
           地源热泵下设备数≧0<br>
           地源热泵下设备数≧水蓄能机组总体积 * 地源热泵模式下水蓄能罐的利用率-(1-水储能罐在高温热水状态冷量) * bigNumber</p>
        7. 水储能罐在制冷状态+水储能罐在制热状态+水储能罐在高温热水状态=1
        8. <p>-bigNumber * 水储能罐在蓄冷状态量≦水储能罐在蓄冷状态下功率≦bigNumber * 水储能罐在蓄冷状态量<br>
           -(1-水储能罐在蓄冷状态量) * bigNumber≦水储能罐在蓄冷状态下功率≦(1-水储能罐在蓄冷状态量) * bigNumber</p>
        9. <p>-bigNumber * 水储能罐在蓄热状态量≦水储能罐在蓄热状态下功率≦bigNumber * 水储能罐在蓄热状态量<br>
           -(1-水储能罐在蓄热状态量) * bigNumber≦水储能罐在蓄热状态下功率≦(1-水储能罐在蓄热状态量) * bigNumber</p>
        10.<p>-bigNumber * 水储能罐在高温热水状态量≦水储能罐在高温热水状态下功率≦bigNumber * 水储能罐在高温热水状态量<br>
           -(1-水储能罐在高温热水状态量) * bigNumber≦水储能罐在高温热水状态下功率≦(1-水储能罐在高温热水状态量) * bigNumber</p>
        11. 水储能机组年化成本 = 水储能罐总体积 * 单位体积价格/20

        Args:
            model (docplex.mp.model.Model): 求解模型实例
            register_period_constraints (int): 注册周期约束为1
            day_node (int): 一天时间节点为24
        """
        # bigNumber = 1e10
        # self.hourRange = range(0, self.num_hour)
        self.waterStorageTank.constraints_register(
            register_period_constraints, day_node
        )
        # waterStorageTank_device[h] == waterStorageTank_cool_flag[h] * volume * ratio_cold_water + waterStorageTank_heat_flag[h] * volume * ratio_warm_water + waterStorageTank_gheat_flag[
        #   h] * volume * ratio_hot_water
        # 用下面的式子进行线性化
        self.add_lower_and_upper_bound(self.volume, 0, self.volume_max)
        # self.model.add_constraint(
        #     self.volume <= self.volume_max
        # )
        # self.model.add_constraint(self.volume >= 0)

        self.equations(
            self.waterStorageTank.device_count,
            reduce(
                self.elementwise_add,
                [
                    self.__dict__[f"device_count_{output_type}"]
                    for output_type in self.output_types
                ],
            ),
        )
        # self.equations(
        #     self.waterStorageTank.device_count,
        #     reduce(
        #         self.elementwise_add,
        #         [
        #             self.device_count_cold_water,
        #             self.waterStorageTank_device_heat,
        #             self.waterStorageTank_device_gheat,
        #         ],
        #     ),
        # )
        # self.model.add_constraints(
        #     self.waterStorageTank.device_count[h]
        #     == self.device_count_cold_water[h]
        #     + self.waterStorageTank_device_heat[h]
        #     + self.waterStorageTank_device_gheat[h]
        #     for h in self.hourRange
        # )

        for output_type in self.output_types:
            self.model.add_constraints(
                self.__dict__[f"device_count_{output_type}"][h]
                <= self.volume * self.__dict__[f"ratio_{output_type}"]
                for h in self.hourRange
            )

            self.model.add_constraints(
                self.__dict__[f"device_count_{output_type}"][h]
                <= self.__dict__[f"{output_type}_flags"][h] * bigNumber
                for h in self.hourRange
            )

            self.model.add_constraints(
                self.__dict__[f"device_count_{output_type}"][h] >= 0
                for h in self.hourRange
            )

            self.model.add_constraints(
                self.__dict__[f"device_count_{output_type}"][h]
                >= self.volume * self.__dict__[f"ratio_{output_type}"]
                - (1 - self.__dict__[f"{output_type}_flags"][h]) * bigNumber
                for h in self.hourRange
            )
        #####################
        # self.add_lower_and_upper_bounds(
        #     self.__dict__[f"device_count_{output_type}"],
        #     self.elementwise_max(  # self.volume * self.ratio_cold_water - (1 - self.waterStorageTank_cool_flag[h]) * bigNumber
        #         self.elementwise_subtract(
        #             self.elementwise_multiply(
        #                 self.__dict__[f"ratio_{output_type}"], self.volume
        #             ),
        #             self.elementwise_multiply(
        #                 (
        #                     self.elementwise_add(
        #                         self.elementwise_multiply(
        #                             self.__dict__[f"{output_type}_flags"], -1
        #                         ),
        #                         1,
        #                     )
        #                 ),
        #                 bigNumber,
        #             ),
        #         ),
        #         0,
        #     ),
        #     self.elementwise_min(
        #         self.elementwise_multiply(
        #             self.waterStorageTank_cool_flag, bigNumber
        #         ),
        #         self.volume * self.ratio_cold_water,
        #     ),
        # )
        #####################

        # # (1)
        # self.model.add_constraints(
        #     self.device_count_cold_water[h] <= self.volume * self.ratio_cold_water
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.device_count_cold_water[h]
        #     <= self.waterStorageTank_cool_flag[h] * bigNumber
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.device_count_cold_water[h] >= 0 for h in self.hourRange
        # )

        # self.model.add_constraints(
        #     self.device_count_cold_water[h]
        #     >= self.volume * self.ratio_cold_water
        #     - (1 - self.waterStorageTank_cool_flag[h]) * bigNumber
        #     for h in self.hourRange
        # )

        # # (2)
        # self.model.add_constraints(
        #     self.waterStorageTank_device_heat[h] <= self.volume * self.ratio_warm_water
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.waterStorageTank_device_heat[h]
        #     <= self.waterStorageTank_heat_flag[h] * bigNumber
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.waterStorageTank_device_heat[h] >= 0 for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.waterStorageTank_device_heat[h]
        #     >= self.volume * self.ratio_warm_water
        #     - (1 - self.waterStorageTank_heat_flag[h]) * bigNumber
        #     for h in self.hourRange
        # )
        # # (3)
        # self.model.add_constraints(
        #     self.waterStorageTank_device_gheat[h] <= self.volume * self.ratio_hot_water
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.waterStorageTank_device_gheat[h]
        #     <= self.waterStorageTank_gheat_flag[h] * bigNumber
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.waterStorageTank_device_gheat[h] >= 0 for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.waterStorageTank_device_gheat[h]
        #     >= self.volume * self.ratio_hot_water
        #     - (1 - self.waterStorageTank_gheat_flag[h]) * bigNumber
        #     for h in self.hourRange
        # )
        # % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

        self.equations(
            reduce(
                self.elementwise_add,
                [
                    self.__dict__[f"{output_type}_flags"]
                    for output_type in self.output_types
                ],
            ),
            1,
        )
        # self.model.add_constraints(
        #     self.waterStorageTank_cool_flag[h]
        #     + self.waterStorageTank_heat_flag[h]
        #     + self.waterStorageTank_gheat_flag[h]
        #     == 1
        #     for h in self.hourRange
        # )  # % 三个方面进行核算。
        # （1） power_waterStorageTank_cool[h] == power_waterStorageTank[h] * waterStorageTank_cool_flag[h]
        # （2）power_waterStorageTank_heat[h] == power_waterStorageTank[h] * waterStorageTank_heat_flag[h]
        # （3）power_waterStorageTank_gheat[h] == power_waterStorageTank[h] * waterStorageTank_gheat_flag[h]
        # 上面的公式进行线性化后,用下面的公式替代

        for output_type in self.output_types:  # this is wrong.
            input_type = (
                output_type if output_type == "hot_water" else f"{output_type}_storage"
            )
            self.model.add_constraints(  # lower
                -bigNumber * self.__dict__[f"{output_type}_flags"][h]
                <= self.power_of_outputs[output_type][h]
                - self.power_of_inputs[input_type][h]
                for h in self.hourRange
            )
            self.model.add_constraints(  # upper
                self.power_of_outputs[output_type][h]
                - self.power_of_inputs[input_type][h]
                <= bigNumber * self.__dict__[f"{output_type}_flags"][h]
                for h in self.hourRange
            )
            self.model.add_constraints(  # lower
                self.waterStorageTank.power[h]
                - (1 - self.__dict__[f"{output_type}_flags"][h]) * bigNumber
                <= self.power_of_outputs[output_type][h]
                - self.power_of_inputs[input_type][h]
                for h in self.hourRange
            )
            self.model.add_constraints(  # upper
                self.power_of_outputs[output_type][h]
                - self.power_of_inputs[input_type][h]
                <= self.waterStorageTank.power[h]
                + (1 - self.__dict__[f"{output_type}_flags"][h]) * bigNumber
                for h in self.hourRange
            )
            ##########################

            # self.add_lower_and_upper_bounds(
            #     self.power_of_outputs[output_type],
            #     self.elementwise_max(
            #         self.elementwise_multiply(
            #             self.__dict__[f"{output_type}_flags"], -bigNumber
            #         ),
            #         self.elementwise_subtract(
            #             self.waterStorageTank.power,
            #             self.elementwise_multiply(
            #                 self.elementwise_add(
            #                     self.elementwise_multiply(
            #                         self.__dict__[f"{output_type}_flags"], -1
            #                     ),
            #                     1,
            #                 ),
            #                 bigNumber,
            #             ),
            #         ),
            #     ),
            #     self.elementwise_min(
            #         self.elementwise_multiply(
            #             self.__dict__[f"{output_type}_flags"], bigNumber
            #         ),
            #         self.elementwise_add(
            #             self.waterStorageTank.power,
            #             self.elementwise_multiply(
            #                 self.elementwise_add(
            #                     self.elementwise_multiply(
            #                         self.__dict__[f"{output_type}_flags"], -1
            #                     ),
            #                     1,
            #                 ),
            #                 bigNumber,
            #             ),
            #         ),
            #     ),
            # )
            ##########################
        # (1)
        # self.model.add_constraints(  # lower
        #     -bigNumber * self.waterStorageTank_cool_flag[h]
        #     <= self.power_waterStorageTank_cool[h]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(  # upper
        #     self.power_waterStorageTank_cool[h]
        #     <= bigNumber * self.waterStorageTank_cool_flag[h]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(  # lower
        #     self.waterStorageTank.power[h]
        #     - (1 - self.waterStorageTank_cool_flag[h]) * bigNumber
        #     <= self.power_waterStorageTank_cool[h]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(  # upper
        #     self.power_waterStorageTank_cool[h]
        #     <= self.waterStorageTank.power[h]
        #     + (1 - self.waterStorageTank_cool_flag[h]) * bigNumber
        #     for h in self.hourRange
        # )

        # # (2)
        # self.model.add_constraints(
        #     -bigNumber * self.waterStorageTank_heat_flag[h]
        #     <= self.power_waterStorageTank_heat[h]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_waterStorageTank_heat[h]
        #     <= bigNumber * self.waterStorageTank_heat_flag[h]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.waterStorageTank.power[h]
        #     - (1 - self.waterStorageTank_heat_flag[h]) * bigNumber
        #     <= self.power_waterStorageTank_heat[h]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_waterStorageTank_heat[h]
        #     <= self.waterStorageTank.power[h]
        #     + (1 - self.waterStorageTank_heat_flag[h]) * bigNumber
        #     for h in self.hourRange
        # )

        # # (3)
        # self.model.add_constraints(
        #     -bigNumber * self.waterStorageTank_gheat_flag[h]
        #     <= self.power_waterStorageTank_gheat[h]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_waterStorageTank_gheat[h]
        #     <= bigNumber * self.waterStorageTank_gheat_flag[h]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.waterStorageTank.power[h]
        #     - (1 - self.waterStorageTank_gheat_flag[h]) * bigNumber
        #     <= self.power_waterStorageTank_gheat[h]
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_waterStorageTank_gheat[h]
        #     <= self.waterStorageTank.power[h]
        #     + (1 - self.waterStorageTank_gheat_flag[h]) * bigNumber
        #     for h in self.hourRange
        # )
        self.model.add_constraint(
            self.annualized == self.volume * self.volume_price / 20
        )


# electricSteamGenerator?
# TODO: 修改为：电用蒸汽蒸汽发生器
class ElectricSteamGenerator(IntegratedEnergySystem):
    """
    电蒸汽发生器类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        # device_count_max: float,
        device_count_max: float,
        device_price: float,
        # device_price: float,
        device_price_solidHeatStorage: float,
        electricity_price: Union[np.ndarray, List],
        efficiency: float,
        device_name: str = "electricSteamGenerator",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (int): 表示地热蒸汽发生器的最大数量
            device_price (float): 表示地热蒸汽发生器的单价
            device_price_solidHeatStorage (float): 地热蒸汽发生器机组固态储热设备单价
            electricity_price (Union[np.ndarray, List]): 每小时电价
            efficiency (float): 效率参数
            device_name (str): 电蒸汽发生器机组名称，默认为"electricSteamGenerator"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # self.classSuffix += 1
        # self.num_hour = num_hour
        # self.device_count: ContinuousVarType = (
        #     self.model.continuous_var(
        #         name="device_count_{0}".format(self.classSuffix)
        #     )
        # )

        """
        电蒸汽发生器机组等效单位设备数 大于零的实数
        """
        self.power: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_{0}".format(self.classSuffix),
        )

        """
        电蒸汽发生器总功率
        """
        self.output_type = "steam"
        self.build_power_of_outputs([self.output_type])
        # self.power_of_outputs[self.output_type]: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_of_outputs[self.output_type]{0}".format(self.classSuffix),
        # )

        """
        电蒸汽发生器产生蒸汽功率
        """
        self.device_count_max = device_count_max
        self.device_count_max_solidHeatStorage = device_count_max * 6

        """
        电蒸汽发生器固体蓄热最大设备数=电蒸汽发生器最大设备数 * 6
        """
        self.device_price = device_price
        self.device_price_solidHeatStorage = device_price_solidHeatStorage
        self.electricity_price = electricity_price

        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="ElectricSteamGenerator_annualized_{0}".format(
        #         self.classSuffix
        #     )
        # )

        """
        电蒸汽发生器年化运维成本
        """
        self.efficiency = efficiency

        self.solidHeatStorage = EnergyStorageSystem(
            num_hour,
            model,
            self.device_count_max_solidHeatStorage,
            self.device_price_solidHeatStorage,
            device_price_powerConversionSystem=0,
            conversion_rate_max=2,
            efficiency=0.9,
            energy_init=1,
            stateOfCharge_min=0,
            stateOfCharge_max=1,
        )

        """
        电蒸汽发生器固态储热,由储能设备`EnergyStorageSystem`创建而来
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="electricity_cost_{0}".format(self.classSuffix)
        )

        """
        用电成本
        """
        # return val

    def constraints_register(self):
        super().constraints_register()

        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦每个时段的电蒸汽发生器的功率≦电蒸汽发生器设备
        3. 每个时段电蒸汽发生器产生蒸汽功率 = 每个时段电蒸汽发生器功率+每个时段储能系统中电蒸汽发生器固态储能设备功率,且大于等于0
        4. 用电成本=每个时段的功率 * 每个时段的电价
        5. 年化成本=电蒸汽发生器设备数 * 设备单价/15+电蒸汽发生器固态储能设备年化成本+用电成本

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        # self.hourRange = range(0, self.num_hour)
        self.solidHeatStorage.constraints_register()
        # self.model.add_constraint(self.device_count >= 0)
        # self.model.add_constraint(
        #     self.device_count
        #     <= self.device_count_max
        # )
        self.add_lower_and_upper_bounds(self.power, 0, self.device_count)
        # self.model.add_constraints(self.power[h] >= 0 for h in self.hourRange)

        # self.model.add_constraints(
        #     self.power[h] <= self.device_count for h in self.hourRange
        # )  # 与天气相关

        self.equations(
            self.power_of_outputs[self.output_type],
            self.elementwise_add(self.power, self.solidHeatStorage.power),
        )
        # self.model.add_constraints(
        #     self.power[h] + self.solidHeatStorage.power[h]
        #     == self.power_of_outputs[self.output_type][h]
        #     for h in self.hourRange
        # )  # troughPhotoThermal系统产生的highTemperature

        self.add_lower_bounds(self.power_of_outputs[self.output_type], 0)
        # self.model.add_constraints(
        #     0 <= self.power_of_outputs[self.output_type][h] for h in self.hourRange
        # )  # 约束能量不能倒流

        self.electricity_cost = self.sum_within_range(
            self.elementwise_multiply(self.power, self.electricity_price)
        )

        # this is simply wrong.
        # self.model.add_constraints(
        #     self.electricity_cost
        #     == self.power[h] * self.electricity_price[h]
        #     for h in self.hourRange
        # )

        self.model.add_constraint(
            self.annualized
            == self.device_count * self.device_price / 15
            + self.solidHeatStorage.annualized
            + self.electricity_cost
        )


# 适用于municipalSteam,municipalHotWater


# both input and output?
# "hot_water","steam"
class CitySupply(IntegratedEnergySystem):
    """市政能源类,适用于市政蒸汽、市政热水"""

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        running_price: Union[np.ndarray, List],
        efficiency: float,
        output_type: Union[Literal["hot_water"], Literal["steam"]],
        device_name: str = "city_supply",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        创建一个市政能源类

        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 市政能源设备机组最大装机量
            device_price (float): 设备单价
            running_price (Union[np.ndarray, List]): 每小时运维价格
            efficiency (float): 能源转换效率
            device_name (str): 市政能源设备机组名称,默认为"city_supply"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # # self.classSuffix += 1
        # self.num_hour = num_hour  # hours in a day
        # self.device_count: ContinuousVarType = self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        市政能源设备装机量 非负实数变量
        """
        self.output_type = output_type

        self.build_power_of_outputs([self.output_type])
        # self.power_of_outputs[self.output_type]: List[
        #     ContinuousVarType
        # ] = self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],
        #     name="power_of_outputs[self.output_type]{0}".format(self.classSuffix),
        # )
        """
        每小时市政能源热量实际消耗 实数变量列表
        """

        # input? this is how they count for price
        self.heat_consumed: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_consumed_{0}".format(self.classSuffix),
        )
        """
        每小时市政能源热量输入 实数变量列表
        """
        # self.device_count_max = device_count_max
        self.running_price = running_price
        # self.device_price = device_price

        self.efficiency = efficiency
        self.heat_cost: ContinuousVarType = self.model.continuous_var(
            name="heat_cost_{0}".format(self.classSuffix)
        )
        """
        市政能源消耗总费用 实数变量
        """
        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="citySupplied_annualized_{0}".format(self.classSuffix)
        # )
        """
        市政能源年运维费用 实数变量
        """
        # return val

    def constraints_register(self):
        super().constraints_register()

        """
        定义市政能源类内部约束条件：

        1. 机组最大装机量 >= 市政能源设备装机量 >= 0
        2. 市政能源设备装机量 >= 每小时市政能源热量消耗 >= 0
        3. 每小时市政能源热量消耗 <= 每小时市政能源热量输入 / 能源传输效率
        4. 市政能源消耗总费用 = sum(每小时市政能源热量输入 * 每小时市政能源价格)
        5. 市政能源年运维费用 = 市政能源设备装机量 * 设备单价 / 15 + 市政能源消耗总费用 * (365*24) / 一天小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        # self.hourRange = range(0, self.num_hour)
        # self.model.add_constraint(self.device_count >= 0)
        # self.model.add_constraint(self.device_count <= self.device_count_max)

        self.add_lower_and_upper_bounds(
            self.power_of_outputs[self.output_type], 0, self.device_count
        )

        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][h] >= 0 for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][h] <= self.device_count
        #     for h in self.hourRange
        # )

        self.equations(
            self.power_of_outputs[self.output_type],
            self.elementwise_divide(self.heat_consumed, self.efficiency),
        )

        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][h]
        #     == self.heat_consumed[h] / self.efficiency
        #     for h in self.hourRange
        # )

        self.heat_cost = self.sum_within_range(
            self.elementwise_add(self.heat_consumed, self.running_price)
        )
        # self.heat_cost = self.model.sum(
        #     self.heat_consumed[h] * self.running_price[h] for h in self.hourRange
        # )

        self.model.add_constraint(
            self.annualized
            == self.device_count * self.device_price / 15
            + self.heat_cost * (365 * 24) / self.num_hour
        )


# 电网？
# input: "electricity" <- this will not cost you money.
class GridNet(IntegratedEnergySystem):
    """
    电网类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        device_count_max: float,
        device_price: float,
        electricity_price: Union[np.ndarray, List],
        electricity_price_upload: float,
        device_name: str = "grid_net",
        device_count_min: int = 0,
        debug: bool = False,
    ):
        """
        新建一个电网类

        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 电网最大设备量
            device_price (float): 设备单价
            electricity_price (Union[np.ndarray, List]): 电力使用价格
            electricity_price_upload (float): 电力生产报酬
            device_name (str): 电网名称,默认为"grid_net"
        """
        # self.device_name = device_name

        super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
            debug=debug,
        )
        # print("DEVICE COUNT?", self.device_count)
        # breakpoint()
        # # self.classSuffix += 1
        # self.num_hour = num_hour
        # self.model = model
        # self.device_count: ContinuousVarType = self.model.continuous_var(
        #     name="device_count_{0}".format(self.classSuffix)
        # )
        """
        电网装机设备数 非负实数
        """

        # self.device_count_max = device_count_max
        self.electricity_price = electricity_price
        self.electricity_price_upload = electricity_price_upload

        # self.device_price = device_price

        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="electricity_cost_{0}".format(self.classSuffix)
        )
        """
        电网用电费用 非负实数
        """

        # self.annualized: ContinuousVarType = self.model.continuous_var(
        #     name="gridNet_annualized_{0}".format(self.classSuffix)
        # )
        """
        电网每年运维费用 非负实数
        """

        # can you not to connect anything as input?
        self.input_type = self.output_type = "electricity"

        # self.electricity_consumed = self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],
        #     lb=-bigNumber,  # lower bound
        #     name="electricity_consumed_{0}".format(self.classSuffix),
        # )  # power consumed?
        """
        电网逐小时下载电量 长度为`num_hour`的实数列表
        """
        self.build_power_of_inputs([self.input_type])
        self.build_power_of_outputs([self.output_type])

        # when input/upload is not zero, output is zero. download is zero.
        # when input/upload is zero, output is not zero, output equals to download.

        # self.power_output = self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],
        #     name="power_output_{0}".format(self.classSuffix),
        # )
        # """
        # 电网逐小时输出电量 长度为`num_hour`的非负实数列表
        # """
        # self.power_input = self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],
        #     name="power_input_{0}".format(self.classSuffix),
        # )
        """
        电网逐小时输入电量 长度为`num_hour`的非负实数列表
        """
        self.powerPeak = self.model.continuous_var(
            name="powerPeak_{0}".format(self.classSuffix)
        )
        """
        电网用电或者发电峰值 实数
        """
        self.baseCost = self.model.continuous_var(
            name="baseCost_{0}".format(self.classSuffix)
        )
        """
        电网基础费用 实数
        """
        self.directions = ["upload", "download"]
        # map to: ['input','output']
        for direction in self.directions:
            self.__dict__[f"electricity_{direction}_max"] = self.model.continuous_var(
                name=f"electricity_{direction}_max_{self.classSuffix}"
            )
            self.__dict__[f"electricity_{direction}"] = self.model.continuous_var_list(
                [i for i in range(0, num_hour)],
                lb=0,  # lower bound
                name=f"electricity_{direction}_{self.classSuffix}",
            )

        # self.equations(self.power_of_inputs[self.input_type], self.electricity_upload)
        # self.equations(
        #     self.power_of_outputs[self.output_type], self.electricity_download
        # )

        # self.power_output_max = self.model.continuous_var(
        #     name="power_output_max_{0}".format(self.classSuffix)
        # )
        """
        电网用电峰值 实数
        """
        # self.power_input_max = self.model.continuous_var(
        #     name="power_input_max_{0}".format(self.classSuffix)
        # )
        """
        电网发电峰值 实数
        """

        self.electricity_net_exchange = self.elementwise_subtract(
            self.power_of_outputs[self.output_type],
            self.power_of_inputs[self.input_type],
        )  # you need to pay this much.

        # self.electricity_net_exchange = self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],
        #     lb=0,
        #     ub=bigNumber,
        #     name=f"electricity_net_exchange_{self.classSuffix}",
        # )
        # return val
        self.io_directions = ["input", "output"]

    def constraints_register(self, powerPeak_predicted: float = 2000):
        super().constraints_register()

        """
        创建电网的约束条件到模型中

        1. 电网要么发电 要么用电 用电时发电量为0 发电时用电量为0 净用电量 = 用电量-发电量
        2. 电网最大设备数 >= 电网设备数 >= 0
        3. 每小时用电量小于电网设备数
        4. 每小时电网发电量小于电网设备数
        5. 电网一天基础消费 = min(max(用电或者发电峰值, 预估用电峰值) * 31, 电网设备数 * 22), 31是电价
        6. 电网一天总消费 = sum(每小时用电量 * 用电电价 + 每小时发电量 * 发电消费) + 电网基础消费
        7. 电网年运行成本 = 电网设备数量 * 设备单价 / 15 + 电网一天总消费 * (365*24) / 一天小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
            powerPeak_predicted (float): 预估用电峰值
        """
        # self.hourRange = range(0, self.num_hour)
        linearization = Linearization()
        # TODO: make sure this time we have power_input as positive number.

        # TODO: alter the definition of this gridnet, making it possible for upload and download at the same time.

        linearization.max_zeros(
            num_hour=self.num_hour,
            model=self.model,
            x=self.elementwise_multiply(self.electricity_net_exchange, -1),
            y=self.electricity_upload,
        )
        linearization.max_zeros(
            num_hour=self.num_hour,
            model=self.model,
            x=self.electricity_net_exchange,
            y=self.electricity_download,
        )

        # linearization.positive_negitive_constraints_register(
        #     self.num_hour,
        #     self.model,
        #     self.electricity_net_exchange,
        #     self.electricity_download,
        #     self.elementwise_multiply(self.electricity_upload, -1),
        # )
        # self.model.add_constraint(self.device_count >= 0)
        # self.model.add_constraint(self.device_count <= self.device_count_max)

        for direction, io_direction in zip(self.directions, self.io_directions):
            self.__dict__[f"electricity_{direction}_max"] = self.model.max(
                self.__dict__[f"power_of_{io_direction}s"][
                    self.__dict__[f"{io_direction}_type"]
                ]
            )
            self.add_upper_bounds(
                self.__dict__[f"power_of_{io_direction}s"][
                    self.__dict__[f"{io_direction}_type"]
                ],
                self.powerPeak,
            )
            self.add_upper_bounds(
                self.__dict__[f"power_of_{io_direction}s"][
                    self.__dict__[f"{io_direction}_type"]
                ],
                self.device_count,
            )
        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][h] <= self.device_count
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_inputs[self.input_type][h] <= self.device_count
        #     for h in self.hourRange
        # )

        # these are always true, not constraints.

        # self.model.add_constraints(
        #     self.power_of_outputs[self.output_type][h] <= self.powerPeak
        #     for h in self.hourRange
        # )
        # self.model.add_constraints(
        #     self.power_of_inputs[self.input_type][h] <= self.powerPeak
        #     for h in self.hourRange
        # )

        # self.power_output_max = self.model.max(self.power_output)
        # self.power_input_max = self.model.max(self.)
        self.powerPeak = self.model.max(
            self.__dict__[f"electricity_{direction}_max"]
            for direction in self.directions
        )

        self.baseCost = (
            self.min(
                self.max(self.powerPeak, powerPeak_predicted) * 31,
                self.device_count * 22,  # pre?
            )
            * 12
        )

        self.electricity_cost = self.baseCost + self.sum_within_range(
            self.elementwise_subtract(
                *[
                    self.elementwise_multiply(power, price)
                    for power, price in [
                        (
                            self.electricity_download,  # output
                            self.electricity_price,
                        ),
                        (
                            self.electricity_upload,  # input
                            self.electricity_price_upload,
                        ),
                    ]
                ]
            )
        )

        # self.electricity_cost = (
        #     self.model.sum(
        #         self.power_of_outputs[self.output_type][h] * self.electricity_price[h]
        #        - self.power_of_inputs[self.input_type][h] * self.electricity_price_upload
        #         for h in self.hourRange
        #     )
        #     + self.baseCost
        # )
        self.model.add_constraint(
            self.annualized
            == self.device_count * self.device_price / 15
            + self.electricity_cost * (365 * 24) / self.num_hour
        )
