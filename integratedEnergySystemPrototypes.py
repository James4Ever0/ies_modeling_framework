from typing import List
from typing import Iterable, Union
import numpy as np
from docplex.mp.model import Model
from docplex.mp.solution import SolveSolution

from docplex.mp.vartype import (
    VarType,
    BinaryVarType,
    IntegerVarType,
    ContinuousVarType,
    # SemiContinuousVarType,
    # SemiIntegerVarType,
)


from config import (
    # localtime1,
    # run,
    # year,
    # node,
    # day_node,
    # debug,
    num_hour0,
    simulationTime,
    bigNumber,
    # intensityOfIllumination,
)


# we define some type of "special" type that can convert from and into any energy form, called "energy".


# another name for IES?
class IntegratedEnergySystem(object):
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
        classObject
        # className: str,
        # classIndex: int,
    ):
        """
        新建一个综合能源系统基类,设置设备名称,设备编号加一,打印设备名称和编号
        """
        # self.device_name = device_name
        IntegratedEnergySystem.device_index += 1
        classObject.index += 1
        self.hourRange = range(0, self.num_hour)
        self.className = classObject.__name__
        self.classIndex = classObject.index
        self.model = model
        self.num_hour = num_hour
        self.device_name = device_name
        self.device_count_max = device_count_max
        assert device_count_min >= 0
        assert device_count_max >= device_count_min
        self.device_count_min = device_count_min
        self.device_price = device_price
        self.classSuffix = f"{self.className}_{self.classIndex}"

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
        return IntegratedEnergySystem.device_index

    def build_power_of_inputs(self, energy_types: List[str]):
        for energy_type in energy_types:
            self.power_of_inputs.update(
                {
                    energy_type: self.model.continuous_var_list(
                        [i for i in range(0, self.num_hour)],
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
                        name=f"power_of_output_{energy_type}_{self.classSuffix}",
                    )
                }
            )

    def constraint_multiplexer(
        self, variables, values, index_range, constraint_function
    ):
        iterable = isinstance(values, List)

        for index in index_range:
            if iterable:
                value = values[index]
            else:
                value = values
            constraint_function(variables[index], value)

    def add_lower_bound(self, variable, lower_bound):
        self.model.add_constraint(lower_bound <= variable)  # 最大装机量

    def add_lower_bounds(self, variables, lower_bounds, index_range):
        self.constraint_multiplexer(
            variables, lower_bounds, index_range, self.add_lower_bound
        )

    def add_upper_bound(self, variable, upper_bound):
        self.model.add_constraint(upper_bound >= variable)  # 最大装机量

    def add_upper_bounds(self, variables, upper_bounds, index_range):
        self.constraint_multiplexer(
            variables, upper_bounds, index_range, self.add_upper_bound
        )

    def equation(self, variable, value):
        self.model.add_constraint(variable == value)

    def equations(self, variables, values, index_range):
        self.constraint_multiplexer(variables, values, index_range, self.equation)

    def add_lower_and_upper_bound(self, variable, lower_bound, upper_bound):
        self.add_lower_bound(variable, lower_bound)
        self.add_upper_bound(variable, upper_bound)

    def add_lower_and_upper_bounds(
        self, variable, lower_bounds, upper_bounds, index_range
    ):
        self.add_lower_bounds(variable, lower_bounds, index_range)
        self.add_upper_bounds(variable, upper_bounds, index_range)

    def constraints_register(self):
        self.add_lower_and_upper_bound(
            self.device_count, self.device_count_min, self.device_count_max
        )
        # self.model.add_constraint(self.device_count <= self.device_count_max)  # 最大装机量
        # self.model.add_constraint(self.device_count >= 0)
        # self.model.add_constraint(self.device_count_min<=self.device_count )

    def elementwise_operation(self, variables, values, operation_function):
        iterable = isinstance(values, List)
        results = []
        for index, variable in enumerate(variables):
            if iterable:
                value = values[index]
            else:
                value = values
            result = operation_function(variable, value)
            results.append(result)
        return results

    def divide(self, variable, value):
        return variable / value

    def multiply(self, variable, value):
        return variable * value

    def elementwise_divide(self, variables, values):
        return self.elementwise_operation(variables, values, self.divide)

    def elementwise_multiply(self, variables, values):
        return self.elementwise_operation(variables, values, self.multiply)

    def sum_within_range(self, variables, index_range):
        result = self.model.sum(variables[index] for index in index_range)
        return result


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
        intensityOfIllumination0: Union[np.ndarray, List],
        efficiency: float,  # efficiency
        device_name: str = "PhotoVoltaic",
        output_type: Union[
            Literal["electricity"], Literal["hot_water"]
        ] = "electricity",
        device_count_min=0,
    ):
        """
        新建一个光伏类

        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 光伏设备机组最大装机量
            device_price (float): 设备单价
            intensityOfIllumination0 (Union[np.ndarray, List]): 24小时光照强度
            efficiency (float): 设备运行效率
            device_name (str): 光伏机组名称,默认为"PhotoVoltaic"
        """
        # self.device_name = device_name
        # index += (
        #     1  # increase the index whenever another PhotoVoltaic system is created.
        # )
        # classObject=self.__class__

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
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
        self.intensityOfIllumination = intensityOfIllumination0
        self.efficiency = efficiency
        """
        每年消耗的运维成本 大于零的实数
        """
        return val

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

        self.add_upper_bound(
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


from typing import Literal


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
        device_count_min=0,
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
        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        # LiBrRefrigeration.index += 1
        # self.num_hour = num_hour

        # device count now.
        # self.device_count: ContinuousVarType =self.model.continuous_var(
        #     name="device_count{0}".format(LiBrRefrigeration.index)
        # )
        """
        溴化锂制冷机组等效单位设备数 大于零的实数
        """

        # self.power_of_inputs[self.input_type]: List[
        #     ContinuousVarType
        # ] =self.model.continuous_var_list(  # iterate through hours in a day?
        #     [i for i in range(0, self.num_hour)],
        #     name="inputs[self.input_type]{0}".format(LiBrRefrigeration.index),
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
        #     name="heat_LiBr{0}".format(LiBrRefrigeration.index),
        # )
        self.output_type = "cold_water"
        self.build_power_of_outputs([self.output_type])
        """
        初始化每个小时内溴化锂机组制冷量 大于零的实数 一共`num_hour`个变量
        """

        # self.device_count_max = device_count_max
        # self.device_price = device_price
        self.efficiency = efficiency
        # self.annualized: ContinuousVarType =self.model.continuous_var(
        #     name="LiBr_annualized{0}".format(LiBrRefrigeration.index)
        # )
        """
        每年消耗的运维成本 大于零的实数
        """
        return val

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
        run_price: int,
        device_name: str = "dieselEngine",
        device_count_min: int = 0,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 柴油发电机设备机组最大装机量
            device_price (float): 设备单价
            run_price (float): 运维价格
            device_name (str): 柴油发电机机组名称,默认为"DieselEngine"
        """
        # self.device_name = device_name
        #
        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        # DieselEngine.index += 1
        # self.num_hour = num_hour
        # self.device_count: ContinuousVarType =self.model.continuous_var(
        #     name="device_count{0}".format(DieselEngine.index)
        # )
        """
        柴油发电机机组等效单位设备数 大于零的实数
        """
        # self.power_of_outputs[self.output_type]: List[ContinuousVarType] =self.model.continuous_var_list(
        #     [i for i in range(0, self.num_hour)],  # keys, not values.
        #     name="self.power_of_outputs[self.output_type]{0}".format(DieselEngine.index),
        # )
        self.output_type = "electricity"
        self.build_power_of_inputs([self.output_type])
        """
        初始化每个小时内柴油发电机机组发电量 大于零的实数 一共`num_hour`个变量
        """
        # self.device_count_max = device_count_max
        # self.device_price = device_price
        self.run_price = run_price
        self.electricity_output_sum = self.sum_within_range(
            self.power_of_outputs[self.output_type], self.hourRange
        )
        """
        柴油发电机总发电量
        """
        # self.annualized: ContinuousVarType =self.model.continuous_var(
        #     name="dieselEngine_annualized{0}".format(DieselEngine.index)
        # )
        """
        每年消耗的运维成本 大于零的实数
        """
        return val

    def constraints_register(self):
        """
        定义机组内部约束

        1. 机组设备数大于等于0
        2. 机组设备总数不得大于最大装机量
        3. 每个小时内,设备发电量小于等于装机设备实际值
        4. 每年消耗的运维成本 = 机组等效单位设备数 * 单位设备价格/15+设备总发电量 * 设备运行价格 * 8760/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
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
            + self.electricity_output_sum * self.run_price * 8760 / self.num_hour,
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
        powerConversionSystem_price: float,
        conversion_rate_max: float,
        efficiency: float,
        energy_init: float,
        stateOfCharge_min: float,
        stateOfCharge_max: float,
        device_name: str = "energyStorageSystem",
        device_count_min: float = 0,
        input_type: str = "energy",
        output_type: str = "energy",
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 储能系统设备机组最大装机量
            device_price (float): 储能装置的购置价格。
            powerConversionSystem_price (float): 储能装置与电网之间的 PCS 转换价格。
            efficiency(float): 储能装置的充放能效率。
            conversion_rate_max (float): 储能装置的最大充放倍率。
            energy_init (float): 储能装置的初始能量。
            stateOfCharge_min (float): 储能装置的最小储能量百分比。
            stateOfCharge_max (float): 储能装置的最大储能量百分比。
            device_name (str): 储能系统机组名称,默认为"energyStorageSystem"
        """
        # self.device_name = device_name

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        # EnergyStorageSystem.index += 1

        # self.device_count: ContinuousVarType =self.model.continuous_var(
        #     name="device_count{0}".format(EnergyStorageSystem.index)
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
        self.powerConversionSystem_price = powerConversionSystem_price  # powerConversionSystem? power conversion system?
        # self.num_hour = num_hour
        self.powerConversionSystem_device_count: ContinuousVarType = (
            self.model.continuous_var(
                name=f"powerConversionSystem_device_count_{self.classSuffix}"
            )
        )  # powerConversionSystem
        """
        模型中的连续变量,表示 PCS 的容量。
        """
        self.charge_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(  # is charging?
            [i for i in range(0, num_hour)],
            name=f"charge_flag_{self.classSuffix}",
        )  # 充能
        """
        模型中的二元变量列表,长度为`num_hour`,表示每小时储能装置是否处于充能状态。
        """
        self.discharge_flag: List[BinaryVarType] = self.model.binary_var_list(
            [i for i in range(0, num_hour)],
            name=f"discharge_flag_{self.classSuffix}",
        )  # 放能
        """
        模型中的二元变量列表,长度为`num_hour`,表示每小时储能装置是否处于放能状态。
        """
        # 效率
        self.efficiency = efficiency
        self.conversion_rate_max = conversion_rate_max  # rate of change/charge?
        self.energy_init = energy_init
        self.stateOfCharge_min = stateOfCharge_min
        self.stateOfCharge_max = stateOfCharge_max
        # self.annualized: ContinuousVarType =self.model.continuous_var(
        #     name="energyStorageSystem_annualized{0}".format(EnergyStorageSystem.index)
        # )
        """
        每年消耗的运维成本 大于零的实数
        """
        return val

    def constraints_register(
        self, register_period_constraints: int = 1, day_node: int = 24
    ):
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

        self.add_lower_and_upper_bound(self.powerConversionSystem_device_count,self.device_count * self.conversion_rate_max)
        # self.model.add_constraint(
        #     self.device_count * self.conversion_rate_max
        #     >= self.powerConversionSystem_device_count  # satisfying the need of power conversion system? power per unit?
        # )
        self.model.add_constraint(self.powerConversionSystem_device_count >= 0)
        # 功率拆分
        self.model.add_constraints(
            self.power[i]
            == -self.power_of_inputs[self.input_type][i]
            + self.power_of_outputs[self.output_type][i]
            for i in self.hourRange
        )

        self.model.add_constraints(
            self.power_of_inputs[self.input_type][i] >= 0 for i in self.hourRange
        )
        self.model.add_constraints(
            self.power_of_inputs[self.input_type][i]
            <= self.charge_flag[i] * bigNumber  # smaller than infinity?
            for i in self.hourRange
        )
        self.model.add_constraints(
            self.power_of_inputs[self.input_type][i]
            <= self.powerConversionSystem_device_count
            for i in self.hourRange
        )

        self.model.add_constraints(
            self.power_of_outputs[self.output_type][i] >= 0 for i in self.hourRange
        )
        self.model.add_constraints(
            self.power_of_outputs[self.output_type][i]
            <= self.discharge_flag[i] * bigNumber
            for i in self.hourRange
        )
        self.model.add_constraints(
            self.power_of_outputs[self.output_type][i]
            <= self.powerConversionSystem_device_count
            for i in self.hourRange
        )

        self.model.add_constraints(
            self.charge_flag[i] + self.discharge_flag[i] == 1 for i in self.hourRange
        )

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

        self.model.add_constraints(
            self.energy[i] <= self.device_count * self.stateOfCharge_max
            for i in range(1, self.num_hour)
        )
        self.model.add_constraints(
            self.energy[i] >= self.device_count * self.stateOfCharge_min
            for i in range(1, self.num_hour)
        )
        self.model.add_constraint(
            self.annualized
            == (
                self.device_count * self.device_price
                + self.powerConversionSystem_device_count
                * self.powerConversionSystem_price
            )
            / 15
        )

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
            self.model.add_constraint(
                self.energy[0] == self.energy_init * self.device_count
            )
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
            solution.get_value(self.device_count) * self.device_price
            + solution.get_value(self.powerConversionSystem_device)
            * self.powerConversionSystem_price
        )


# 可变容量储能
# TODO: 水蓄能
class EnergyStorageSystemVariable(IntegratedEnergySystem):
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
        powerConversionSystem_price: float,
        conversion_rate_max: float,
        efficiency: float,
        energy_init: float,
        stateOfCharge_min: float,
        stateOfCharge_max: float,
        device_name: str = "energyStorageSystem_variable",
        input_type: str = "energy",
        output_type: str = "energy",
        device_count_min: int = 0,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            device_count_max (float): 储能系统设备机组最大装机量
            device_price (float): 储能装置的购置价格。
            powerConversionSystem_price (float): 储能装置与电网之间的 PCS 转换价格。
            efficiency(float): 储能装置的充放能效率。
            conversion_rate_max (float): 储能装置的最大充放倍率。
            energy_init (float): 储能装置的初始储能百分比。
            stateOfCharge_min (float): 储能装置的最小储能量百分比。
            stateOfCharge_max (float): 储能装置的最大储能量百分比。
            device_name (str): 可变容量储能系统机组名称,默认为"energyStorageSystem_variable"
        """
        # self.device_name = device_name

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        # EnergyStorageSystemVariable.index += 1
        self.input_type = input_type
        self.output_type = output_type

        # self.device_count: List[ContinuousVarType] =self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],
        #     name="energyStorageSystemVariable_device{0}".format(
        #         EnergyStorageSystemVariable.index
        #     ),
        # )
        """
        可变容量储能系统机组每小时等效单位设备数,长度为`num_hour`,大于零的实数列表
        """
        self.power: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, num_hour)],
            lb=-bigNumber,
            name=f"power_{self.classSuffix}",
        )
        """
        模型中的连续变量列表,长度为`num_hour`,表示每小时储能装置的充放能功率
        """
        # 充能功率
        self.build_power_of_inputs([self.input_type])
        self.build_power_of_outputs([self.output_type])
        # self.power_of_inputs[self.input_type]: List[ContinuousVarType] =self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],
        #     name="powerVariable_charge{0}".format(EnergyStorageSystemVariable.index),
        # )
        # """
        # 模型中的连续变量列表,长度为`num_hour`,表示每小时储能装置的充能功率
        # """
        # # 放能功率
        # self.power_of_outputs[self.output_type]: List[ContinuousVarType] =self.model.continuous_var_list(
        #     [i for i in range(0, num_hour)],
        #     name="powerVariable_discharge{0}".format(EnergyStorageSystemVariable.index),
        # )
        """
        模型中的连续变量列表,长度为`num_hour`,表示每小时储能装置的放能功率
        """
        # 能量
        self.energy: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name="energyStorageSystemVariable{0}".format(
                EnergyStorageSystemVariable.index
            ),
        )
        """
        模型中的连续变量列表,长度为`num_hour`,表示每小时储能装置的能量
        """
        self.device_count_max = device_count_max
        self.device_price = device_price
        self.powerConversionSystem_price = powerConversionSystem_price
        # self.num_hour = num_hour
        self.powerConversionSystem_device: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, num_hour)],
            name="powerConversionSystem_deviceVariable{0}".format(
                EnergyStorageSystemVariable.index
            ),
        )  # powerConversionSystem
        """
        模型中的连续变量,表示 PCS 的容量
        """
        # paradox? redundancy? both charge and discharge?
        self.charge_flag: List[BinaryVarType] = self.model.binary_var_list(
            [i for i in range(0, num_hour)],
            name="batteryEnergyStorageSystemVariable_charge_flag{0}".format(
                EnergyStorageSystemVariable.index
            ),
        )  # 充能
        """
        模型中的二元变量列表,长度为`num_h`,表示每小时储能装置是否处于充能状态。
        """
        self.discharge_flag: List[BinaryVarType] = self.model.binary_var_list(
            keys=[i for i in range(0, num_hour)],
            name="batteryEnergyStorageSystemVariable_discharge_flag{0}".format(
                EnergyStorageSystemVariable.index
            ),
        )  # 放能
        """
        模型中的二元变量列表,长度为`num_h`,表示每小时储能装置是否处于放能状态。
        """
        # 效率
        self.efficiency = efficiency
        self.conversion_rate_max = conversion_rate_max  # conversion rate? charge rate?
        self.energy_init = energy_init
        self.stateOfCharge_min = stateOfCharge_min
        self.stateOfCharge_max = stateOfCharge_max

    def constraints_register(
        self, model: Model, register_period_constraints=1, day_node=24
    ):
        """
        定义机组内部约束

        1. 机组设备数大于等于0
        2. 机组设备总数不得大于最大装机量
        3. 可变容量储能装置功率转化率约束:<br>储能系统设备 * 储能装置的最大倍率大于等于功率转化系统设备,且功率转化系统设备大于等于0
        4. 充能功率和放能功率之间的关系:<br>储能系统功率 = -充能功率+放能功率
        5. 充能功率约束:<br>充能功率大于等于0,小于等于功率转化系统设备,小于等于充能状态 * bigNumber
        6. 放能功率约束:<br>放能功率大于等于0,小于等于功率转化系统设备,小于等于放能状态 * bigNumber
        7. 充能功率和放能功率二选一
        8. 储能量守恒约束:<br>储能系统能量 = 上一时段储能量+(当前时段充能 * 效率-当前时段放能/效率) * simulationTime/3600
        9. 最大和最小储能量约束:<br>储能设备数 * 储能装置的最小储能量百分比≦储能系统能量≦储能设备数 * 储能装置的最大储能量百分比
        10. 两天之间充放能关系约束:<br>对于`range(day_node-1, num_hour, day_node)`区间每个数`i`，如果`register_period_constraints`参数为1,表示`energyStorageSystem[i] == energyStorageSystem[i - (day_node - 1)]`;如果`register_period_constraints`参数不为1,表示`energyStorageSystem[i] == energyStorageSystem[i - 1] + 充放能变化能量`


        Args:
            model (docplex.mp.model.Model): 求解模型实例
            register_period_constraints (int): 注册周期约束为1
            day_node (int): 一天时间节点为24
        """
        # bigNumber = 1e10
        self.hourRange = range(0, self.num_hour)
        self.model.add_constraints(
            self.device_count[i] <= self.device_count_max for i in self.hourRange
        )
        self.model.add_constraints(self.device_count[i] >= 0 for i in self.hourRange)
        self.model.add_constraints(
            self.device_count[i] * self.conversion_rate_max
            >= self.powerConversionSystem_device[i]
            for i in self.hourRange
        )
        self.model.add_constraints(
            self.powerConversionSystem_device[i] >= 0 for i in self.hourRange
        )
        # 功率拆分
        self.model.add_constraints(
            self.power[i]
            == -self.power_of_inputs[self.input_type][i]
            + self.power_of_outputs[self.output_type][i]
            for i in self.hourRange
        )

        self.model.add_constraints(
            self.power_of_inputs[self.input_type][i] >= 0 for i in self.hourRange
        )
        self.model.add_constraints(
            self.power_of_inputs[self.input_type][i] <= self.charge_flag[i] * bigNumber
            for i in self.hourRange
        )
        self.model.add_constraints(
            self.power_of_inputs[self.input_type][i]
            <= self.powerConversionSystem_device[i]
            for i in self.hourRange
        )

        self.model.add_constraints(
            self.power_of_outputs[self.output_type][i] >= 0 for i in self.hourRange
        )
        self.model.add_constraints(
            self.power_of_outputs[self.output_type][i]
            <= self.discharge_flag[i] * bigNumber
            for i in self.hourRange
        )
        self.model.add_constraints(
            self.power_of_outputs[self.output_type][i]
            <= self.powerConversionSystem_device[i]
            for i in self.hourRange
        )

        self.model.add_constraints(
            self.charge_flag[i] + self.discharge_flag[i] == 1 for i in self.hourRange
        )

        # seems this will discourage the simulation.
        # let's not make it zero.

        self.model.add_constraint(
            self.power_of_inputs[self.input_type][0]
            == self.power_of_inputs[self.input_type][1]
        )

        self.model.add_constraint(
            self.power_of_outputs[self.output_type][0]
            == self.power_of_outputs[self.output_type][1]
        )

        # should we not add these statements?

        # TODO: fix charge/discharge init value issues
        # we should set init charge/discharge value to 1
        for day in range(1, int(self.num_hour / day_node) + 1):
            self.model.add_constraints(
                self.energy[i]
                == self.energy[i - 1]
                + (
                    self.power_of_inputs[self.input_type][i] * self.efficiency
                    - self.power_of_outputs[self.output_type][i] / self.efficiency
                )
                * simulationTime
                / 3600
                for i in range(
                    1 + day_node * (day - 1), day_node * day
                )  # not starting from the zero day?
            )
        # TODO: figure out init (fixing init error)
        self.model.add_constraint(
            # self.model.add_constraints(
            self.energy[0]
            == self.energy_init * self.device_count[0]
            # for i in range(1, self.num_hour)
            # since it is init we should not iterate through all variables.
        )

        self.model.add_constraints(
            self.energy[i] <= self.device_count[i] * self.stateOfCharge_max
            for i in range(1, self.num_hour)
        )
        self.model.add_constraints(
            self.energy[i] >= self.device_count[i] * self.stateOfCharge_min
            for i in range(1, self.num_hour)
        )

        # 两天之间直接割裂,没有啥关系
        if register_period_constraints == 1:  # register??
            self.model.add_constraints(
                self.energy[i] == self.energy[i - (day_node - 1)]
                for i in range(day_node - 1, self.num_hour, day_node)
            )
        else:
            # 初始值
            # # TODO: figure out init
            # self.model.add_constraint(
            #     self.energy[0]
            #     == self.energy_init * self.device_count[0]
            #     # since it is init we should not iterate through all variables.
            # )
            # breakpoint()
            # not breaking here?
            # 两天之间的连接
            # TODO: 8760（一年）设置为num_hour时使用这个条件
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
        troughPhotoThermal_device_count_max: float,
        troughPhotoThermal_price: float,
        troughPhotoThermalSolidHeatStorage_price: float,  # (csgrgtxr是啥)
        intensityOfIllumination0: Union[np.ndarray, List],
        efficiency: float,
        device_name: str = "troughPhotoThermal",
        device_count_min: int = 0,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            troughPhotoThermal_device_count_max (float): 槽式光热设备机组最大装机量
            troughPhotoThermal_price (float): 槽式光热设备的购置价格。
            troughPhotoThermalSolidHeatStorage_price (float): 槽式光热储能设备价格
            intensityOfIllumination0 (Union[np.ndarray, List]): 24小时光照强度
            efficiency (float): 效率
            device_name (str): 槽式光热机组名称,默认为"troughPhotoThermal"
        """
        # self.device_name = device_name

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        TroughPhotoThermal.index += 1
        # self.num_hour = num_hour
        self.troughPhotoThermal_device: ContinuousVarType = self.model.continuous_var(
            name="troughPhotoThermal_device{0}".format(TroughPhotoThermal.index)
        )
        """
        槽式光热机组设备数 实数变量
        """
        self.power_troughPhotoThermal: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_troughPhotoThermal{0}".format(TroughPhotoThermal.index),
        )
        """
        槽式光热机组每小时产电功率 实数变量列表
        """
        self.power_troughPhotoThermal_steam: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_troughPhotoThermal_steam{0}".format(TroughPhotoThermal.index),
        )
        """
        槽式光热机组每小时产蒸汽功率 实数变量列表
        """
        self.troughPhotoThermal_device_count_max = troughPhotoThermal_device_max
        self.troughPhotoThermalSolidHeatStorage_device_count_max: float = (
            troughPhotoThermal_device_count_max * 6
        )
        """
        固态储热最大设备量 = 槽式光热机组最大装机量 * 6
        """
        self.troughPhotoThermal_price = troughPhotoThermal_price
        self.troughPhotoThermalSolidHeatStorage_price = (
            troughPhotoThermalSolidHeatStorage_price
        )
        self.intensityOfIllumination = (
            intensityOfIllumination0  # intensityOfIllumination
        )
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="troughPhotoThermal_annualized{0}".format(TroughPhotoThermal.index)
        )
        """
        槽式光热年运维成本
        """
        self.efficiency = efficiency

        self.troughPhotoThermalSolidHeatStorage_device = EnergyStorageSystem(
            num_hour,
            model,
            self.troughPhotoThermalSolidHeatStorage_device_max,
            self.troughPhotoThermalSolidHeatStorage_price,
            powerConversionSystem_price=100,
            conversion_rate_max=2,  # change?
            efficiency=0.9,
            energy_init=1,
            stateOfCharge_min=0,
            stateOfCharge_max=1,
        )
        """
        固态储热设备初始化为`EnergyStorageSystem`
        """

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
        self.hourRange = range(0, self.num_hour)
        self.troughPhotoThermalSolidHeatStorage_device.constraints_register(model)
        self.model.add_constraint(self.troughPhotoThermal_device >= 0)
        self.model.add_constraint(
            self.troughPhotoThermal_device <= self.troughPhotoThermal_device_max
        )
        self.model.add_constraints(
            self.power_troughPhotoThermal[h] >= 0 for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_troughPhotoThermal[h]
            <= self.troughPhotoThermal_device
            * self.intensityOfIllumination[h]
            * self.efficiency
            for h in self.hourRange
        )  # 与天气相关
        self.model.add_constraints(
            self.power_troughPhotoThermal[h]
            + self.troughPhotoThermalSolidHeatStorage_device.power[h]
            == self.power_troughPhotoThermal_steam[h]
            for h in self.hourRange
        )  # troughPhotoThermal系统产生的highTemperature
        self.model.add_constraints(
            0 <= self.power_troughPhotoThermal_steam[h] for h in self.hourRange
        )  # 约束能量不能倒流
        self.model.add_constraint(
            self.annualized
            == self.troughPhotoThermal_device * self.troughPhotoThermal_price / 15
            + self.troughPhotoThermalSolidHeatStorage_device.annualized
        )


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
        combinedHeatAndPower_num_max: float,
        combinedHeatAndPower_price: float,
        gas_price: Union[np.ndarray, List],
        combinedHeatAndPower_single_device: float,
        power_to_heat_ratio: float,  # drratio?
        device_name: str = "combinedHeatAndPower",
        device_count_min: int = 0,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            combinedHeatAndPower_num_max (float): 表示热电联产机组的最大等效设备数量
            combinedHeatAndPower_price (float): 表示热电联产等效设备的单价
            gas_price (Union[np.ndarray, List]): 表示燃气的单价
            combinedHeatAndPower_single_device (float): 表示每台热电联产设备的等效设备数量
            power_to_heat_ratio (float): 表示热电联产设备的电热比。
            device_name (str): 热电联产机组名称,默认为"combinedHeatAndPower"
        """
        # self.device_name = device_name

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        CombinedHeatAndPower.index += 1
        # self.num_hour = num_hour
        self.combinedHeatAndPower_device: ContinuousVarType = self.model.continuous_var(
            name="combinedHeatAndPower_device{0}".format(CombinedHeatAndPower.index)
        )
        """
        实数型,表示热电联产的等效设备数量
        """
        self.power_combinedHeatAndPower: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_combinedHeatAndPower{0}".format(CombinedHeatAndPower.index),
        )
        """
        实数型列表,表示热电联产在每个时段的发电量
        """
        self.heat_combinedHeatAndPower: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_combinedHeatAndPower{0}".format(CombinedHeatAndPower.index),
        )
        """
        实数型列表,表示热电联产在每个时段的供暖热水量
        """
        self.gas_combinedHeatAndPower: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="gas_combinedHeatAndPower{0}".format(CombinedHeatAndPower.index),
        )  # 时时耗气量? 时时是什么意思 实时？
        """
        实数型列表,表示热电联产在每个时段的耗气量
        """
        self.combinedHeatAndPower_price = combinedHeatAndPower_price
        self.gas_price = gas_price
        self.combinedHeatAndPower_open_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="combinedHeatAndPower_open_flag{0}".format(CombinedHeatAndPower.index),
        )
        """
        二元变量列表,表示热电联产在每个时段是否启动
        """
        self.wasteGasAndHeat_water_flag: BinaryVarType = self.model.binary_var(
            name="wasteGasAndHeat_water_flag{0}".format(CombinedHeatAndPower.index)
        )
        """
        二元变量,表示热电联产是否用于供暖热水
        """
        self.wasteGasAndHeat_steam_flag: BinaryVarType = self.model.binary_var(
            name="wasteGasAndHeat_steam_flag{0}".format(CombinedHeatAndPower.index)
        )
        """
        二元变量,表示热电联产是否用于供热蒸汽
        """
        # 机组数量
        self.combinedHeatAndPower_run_num: List[
            IntegerVarType
        ] = self.model.integer_var_list(
            [i for i in range(0, self.num_hour)],
            name="combinedHeatAndPower_run_num{0}".format(CombinedHeatAndPower.index),
        )
        """
        整数型列表,表示每个时段启动的热电联产等效设备数量
        """
        self.combinedHeatAndPower_num: IntegerVarType = self.model.integer_var(
            name="combinedHeatAndPower_num{0}".format(CombinedHeatAndPower.index)
        )
        """
        整数型,表示热电联产实际装机数量
        """
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="combinedHeatAndPower_annualized{0}".format(CombinedHeatAndPower.index)
        )
        """
        实数型,表示热电联产年化投资成本
        """
        self.gas_cost: ContinuousVarType = self.model.continuous_var(
            name="CombinedHeatAndPower_gas_cost{0}".format(CombinedHeatAndPower.index)
        )  # 燃气费用统计
        """
        实数型,表示总燃气费用
        """
        self.combinedHeatAndPower_num_max = combinedHeatAndPower_num_max
        self.combinedHeatAndPower_single_device = combinedHeatAndPower_single_device
        self.combinedHeatAndPower_limit_down_ratio = (
            0.2  # ? devices cannot be turned down more than 20% ? what is this?
        )
        """
        最低CHP机组开启比率 默认为0.2
        """

        self.power_to_heat_ratio = power_to_heat_ratio

        # arbitrary settings
        self.gasTurbineSystem_device = Exchanger(
            self.num_hour,
            model,
            self.combinedHeatAndPower_device * 0.5,
            device_price=300,
            k=0,
        )
        """
        燃气轮机热交换器，参数包括时间步数、数学模型实例、可用的设备数量、设备单价和换热系数等。
        """

        self.wasteGasAndHeat_water_device = Exchanger(
            self.num_hour,
            model,
            self.combinedHeatAndPower_device * 0.5,
            device_price=300,
            k=0,
        )

        """
        供暖热水热交换器，参数包括时间步数、数学模型实例、可用的设备数量、设备单价和换热系数等。
        """

        self.wasteGasAndHeat_steam_device = Exchanger(
            self.num_hour,
            model,
            self.combinedHeatAndPower_device * 0.5,
            device_price=300,
            k=0,
        )

        """
        供暖蒸汽热交换器，参数包括时间步数、数学模型实例、可用的设备数量、设备单价和换热系数等。
        """

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
        12. 根据二元决策变量wasteGasAndHeat_water_flag和一个大常数bigM来设定与余气余热系统的最大热交换能力。如果wasteGasAndHeat_water_flag为0,该约束就会失去作用。
        13. 根据二元决策变量wasteGasAndHeat_steam_flag和一个大常数bigM来设定蒸汽与余气余热系统的最大热交换能力。如果wasteGasAndHeat_steam_flag为0,该约束就会失去作用。
        14. GTS系统的最大热交换能力限制在所有时间段内热电联产机组额定热输出的50%
        15. 余气余热热水系统的最大换热量限制为所有时段热电联产机组额定热出力的50%
        16. 余气余热蒸汽系统的最大换热能力限制为所有时段热电联产机组额定热出力的50%
        17. 计算年总成本,包括运行CHP机组、GTS系统和余气余热系统的成本以及燃气成本。计算的依据是CHP机组的数量、其额定功率出力、CHP的单位成本、一年中的小时数等相关参数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """

        self.hourRange = range(0, self.num_hour)
        self.model.add_constraint(self.combinedHeatAndPower_num >= 0)
        self.model.add_constraint(
            self.combinedHeatAndPower_num <= self.combinedHeatAndPower_num_max
        )

        self.model.add_constraint(
            self.combinedHeatAndPower_device
            == self.combinedHeatAndPower_num * self.combinedHeatAndPower_single_device
        )
        self.model.add_constraints(
            self.combinedHeatAndPower_open_flag[h]
            * self.combinedHeatAndPower_single_device
            * self.combinedHeatAndPower_limit_down_ratio
            <= self.power_combinedHeatAndPower[h]
            for h in self.hourRange
        )
        # power_combinedHeatAndPower(1, h) <= combinedHeatAndPower_device * combinedHeatAndPower_open_flag(1, h) % combinedHeatAndPower功率限制, 采用线性化约束,有以下等效:
        self.model.add_constraints(
            self.power_combinedHeatAndPower[h] <= self.combinedHeatAndPower_device
            for h in self.hourRange
        )

        self.model.add_constraints(
            self.power_combinedHeatAndPower[h]
            <= self.combinedHeatAndPower_open_flag[h] * bigNumber
            for h in self.hourRange
        )
        # power_combinedHeatAndPower[h]>= 0
        # power_combinedHeatAndPower(1, h) >= combinedHeatAndPower_device - (1 - combinedHeatAndPower_open_flag[h]) * bigNumber
        self.model.add_constraints(
            self.combinedHeatAndPower_run_num[h]
            * self.combinedHeatAndPower_single_device
            >= self.power_combinedHeatAndPower[h]
            for h in self.hourRange
        )  # 确定CombinedHeatAndPower开启台数
        self.model.add_constraints(
            self.combinedHeatAndPower_run_num[h]
            * self.combinedHeatAndPower_single_device
            <= self.power_combinedHeatAndPower[h]
            + self.combinedHeatAndPower_single_device
            + 1
            for h in self.hourRange
        )  # 确定CombinedHeatAndPower开启台数
        self.model.add_constraints(
            0 <= self.combinedHeatAndPower_run_num[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.combinedHeatAndPower_run_num[h] <= self.combinedHeatAndPower_num
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_combinedHeatAndPower[h]
            * self.power_to_heat_ratio  # power * power_to_heat_coefficient = heat
            == self.heat_combinedHeatAndPower[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.gas_combinedHeatAndPower[h] == self.power_combinedHeatAndPower[h] / 3.5
            for h in self.hourRange
        )

        self.gas_cost = self.model.sum(
            self.gas_combinedHeatAndPower[h] * self.gas_price[h] for h in self.hourRange
        )  # 统计燃气费用
        #
        self.model.add_constraint(
            self.wasteGasAndHeat_water_flag + self.wasteGasAndHeat_steam_flag == 1
        )
        self.model.add_constraint(
            self.wasteGasAndHeat_water_device.exchanger_device
            <= self.wasteGasAndHeat_water_flag * bigNumber
        )
        self.model.add_constraint(
            self.wasteGasAndHeat_steam_device.exchanger_device
            <= self.wasteGasAndHeat_steam_flag * bigNumber
        )
        self.model.add_constraints(
            self.gasTurbineSystem_device.heat_exchange[h]
            <= self.heat_combinedHeatAndPower[h] * 0.5
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.wasteGasAndHeat_water_device.heat_exchange[h]
            <= self.heat_combinedHeatAndPower[h] * 0.5
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.wasteGasAndHeat_steam_device.heat_exchange[h]
            <= self.heat_combinedHeatAndPower[h] * 0.5
            for h in self.hourRange
        )

        self.model.add_constraint(
            self.annualized
            == self.combinedHeatAndPower_num
            * self.combinedHeatAndPower_single_device
            * self.combinedHeatAndPower_price
            / 15
            + self.gasTurbineSystem_device.annualized
            + self.wasteGasAndHeat_water_device.annualized
            + self.wasteGasAndHeat_steam_device.annualized
            + self.gas_cost * 8760 / self.num_hour
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
        gasBoiler_device_count_max: float,
        gasBoiler_price: float,
        gas_price: Union[np.ndarray, List],
        efficiency: float,
        device_name: str = "gasBoiler",
        device_count_min: int = 0,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            gasBoiler_device_count_max (float): 表示燃气锅炉的最大数量。
            gasBoiler_price (float): 表示燃气锅炉的单价。
            gas_price (Union[np.ndarray, List]): 表示燃气的单价。
            efficiency (float): 燃气锅炉的热效率
            device_name (str): 燃气锅炉机组名称,默认为"gasBoiler"
        """
        # self.device_name = device_name

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        GasBoiler.index += 1
        # self.num_hour = num_hour
        self.gasBoiler_device: ContinuousVarType = self.model.continuous_var(
            name="gasBoiler_device{0}".format(GasBoiler.index)
        )
        """
        燃气锅炉机组等效单位设备数 大于零的实数变量
        """
        self.heat_gasBoiler: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_gasBoiler{0}".format(GasBoiler.index),
        )
        """
        连续变量列表,表示燃气锅炉在每个时段的热功率
        """
        self.gas_gasBoiler: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="gas_gasBoiler{0}".format(GasBoiler.index),
        )  # 时时耗气量
        """
        连续变量列表,表示燃气锅炉在每个时段的燃气消耗量
        """
        self.gasBoiler_device_count_max = gasBoiler_device_max
        self.gasBoiler_price = gasBoiler_price
        self.gas_price = gas_price
        self.efficiency = efficiency
        self.gas_cost: ContinuousVarType = self.model.continuous_var(
            name="gasBoiler_gas_cost{0}".format(GasBoiler.index)
        )
        """
        连续变量,表示总燃气费用
        """
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="gasBoiler_annualized{0}".format(GasBoiler.index)
        )
        """
        连续变量,表示燃气锅炉的年化费用
        """

    def constraints_register(self):
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
        self.hourRange = range(0, self.num_hour)
        self.model.add_constraint(self.gasBoiler_device >= 0)
        self.model.add_constraint(self.gasBoiler_device <= self.gasBoiler_device_max)
        self.model.add_constraints(self.heat_gasBoiler[h] >= 0 for h in self.hourRange)
        self.model.add_constraints(
            self.heat_gasBoiler[h] <= self.gasBoiler_device for h in self.hourRange
        )  # 天燃气蒸汽锅炉
        self.model.add_constraints(
            self.gas_gasBoiler[h] == self.heat_gasBoiler[h] / (10 * self.efficiency)
            for h in self.hourRange
        )
        self.gas_cost = self.model.sum(
            self.gas_gasBoiler[h] * self.gas_price[h] for h in self.hourRange
        )
        self.model.add_constraint(
            self.annualized
            == self.gasBoiler_device * self.gasBoiler_price / 15
            + self.gas_cost * 8760 / self.num_hour
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
        electricBoiler_device_count_max: float,
        electricBoiler_price: float,
        electricity_price: Union[np.ndarray, List],
        efficiency: float,
        device_name: str = "electricBoiler",
        device_count_min: int = 0,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            electricBoiler_device_count_max (float): 表示电锅炉的最大数量。
            electricBoiler_price (float): 表示电锅炉的单价。
            electricity_price (Union[np.ndarray, List]): 表示电的单价。
            efficiency (float): 电锅炉的热效率
            device_name (str): 电锅炉机组名称,默认为"electricBoiler"
        """
        # self.device_name = device_name

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        ElectricBoiler.index += 1
        # self.num_hour = num_hour
        self.electricBoiler_device: ContinuousVarType = self.model.continuous_var(
            name="electricBoiler_device{0}".format(ElectricBoiler.index)
        )
        """
        电锅炉机组等效单位设备数 大于零的实数
        """
        self.heat_electricBoiler: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(  # h? heat?
            [i for i in range(0, self.num_hour)],
            name="heat_electricBoiler{0}".format(ElectricBoiler.index),
        )
        """
        连续变量列表,表示电锅炉在每个时段的热功率
        """
        self.electricity_electricBoiler: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_electricBoiler{0}".format(ElectricBoiler.index),
        )  # 时时耗气量
        """
        连续变量列表,表示电锅炉在每个时段的电消耗量
        """
        self.gas_device_count_max = electricBoiler_device_max
        self.electricBoiler_price = electricBoiler_price
        self.electricity_price = electricity_price
        self.efficiency = efficiency
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="electricity_cost{0}".format(ElectricBoiler.index)
        )
        """
        连续变量,表示总用电费用
        """
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="electricBoiler_annualized{0}".format(ElectricBoiler.index)
        )
        """
        连续变量,表示电锅炉的年化费用
        """

    def constraints_register(self):
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
        self.hourRange = range(0, self.num_hour)
        self.model.add_constraint(self.electricBoiler_device >= 0)
        self.model.add_constraint(self.electricBoiler_device <= self.gas_device_max)
        self.model.add_constraints(
            self.heat_electricBoiler[h] >= 0 for h in self.hourRange
        )
        self.model.add_constraints(
            self.heat_electricBoiler[h] <= self.electricBoiler_device
            for h in self.hourRange
        )  # 天燃气蒸汽锅炉
        self.model.add_constraints(
            self.electricity_electricBoiler[h]
            == self.heat_electricBoiler[h] / self.efficiency
            for h in self.hourRange
        )
        self.electricity_cost = self.model.sum(
            self.electricity_electricBoiler[h] * self.electricity_price[h]
            for h in self.hourRange
        )
        self.model.add_constraint(
            self.annualized
            == self.electricBoiler_device * self.electricBoiler_price / 15
            + self.electricity_cost * 8760 / self.num_hour
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
        device_name: str = "exchanger",
        device_count_min: int = 0,
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

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        # k 传热系数
        Exchanger.index += 1
        # self.num_hour = num_hour
        self.exchanger_device: ContinuousVarType = self.model.continuous_var(
            name="exchanger_device{0}".format(Exchanger.index)
        )
        """
        热交换器机组等效单位设备数 大于零的实数变量
        """
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="exchanger_annualized{0}".format(Exchanger.index)
        )
        """
        连续变量,表示热交换器的年化费用
        """
        self.device_price = device_price
        self.exchanger_device_count_max = device_max
        self.heat_exchange: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_exchanger{0}".format(Exchanger.index),
        )
        """
        连续变量列表,表示热交换器的每小时热交换量
        """

    def constraints_register(self):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦热交换器的热功率≦热交换器运行量
        3. 热交换器的总年化成本 == 热交换器设备数 * 设备价格/15

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        self.hourRange = range(0, self.num_hour)
        self.model.add_constraint(self.exchanger_device >= 0)
        self.model.add_constraint(self.exchanger_device <= self.exchanger_device_max)
        self.model.add_constraints(self.heat_exchange[h] >= 0 for h in self.hourRange)
        self.model.add_constraints(
            self.heat_exchange[h] <= self.exchanger_device for h in self.hourRange
        )  # 天燃气蒸汽锅炉
        self.model.add_constraint(
            self.annualized == self.exchanger_device * self.device_price / 15
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

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        # self.num_hour = num_hour
        AirHeatPump.index += 1
        self.electricity_price = electricity_price
        self.heatPump_device: ContinuousVarType = self.model.continuous_var(
            name="heatPump_device{0}".format(AirHeatPump.index)
        )
        """
        空气热泵机组等效单位设备数 大于零的实数
        """
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="AirHeatPumpower_annualized{0}".format(AirHeatPump.index)
        )
        """
        连续变量,表示空气热泵的年化费用
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="AirHeatPumpower_electricity_cost{0}".format(AirHeatPump.index)
        )
        """
        连续变量,表示空气热泵的电价成本
        """
        self.device_price = device_price
        self.device_count_max = device_max
        self.power_heatPump_cool: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_heatPump_cool{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示空气热泵在每个时段的制冷功率
        """
        self.cool_heatPump_out: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="cool_heatPump_out{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示空气热泵在每个时段的制冷出口温度
        """
        self.heatPump_cool_flag: List[BinaryVarType] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="heatPump_cool_flag{0}".format(AirHeatPump.index),
        )
        """
        二元变量列表,表示空气热泵在每个时段的制冷状态
        """

        self.power_heatPump_cooletStorage: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_heatPump_cooletStorage{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示空气热泵在每个时段的蓄冷功率
        """
        self.cooletStorage_heatPump_out: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="cooletStorage_heatPump_out{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示空气热泵在每个时段的蓄冷出口温度
        """

        self.heatPump_cooletStorage_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="heatPump_cooletStorage_flag{0}".format(AirHeatPump.index),
        )
        """
        二元变量列表,表示空气热泵在每个时段的蓄冷状态
        """
        self.power_heatPump_heat: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_heatPump_heat{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示空气热泵在每个时段的制热功率
        """
        self.heat_heatPump_out: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_heatPump_out{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示空气热泵在每个时段的制热出口温度
        """
        self.heatPump_heat_flag: List[BinaryVarType] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="heatPump_heat_flag{0}".format(AirHeatPump.index),
        )
        """
        二元变量列表,表示空气热泵在每个时段的制热状态
        """
        self.power_heatPump_heatStorage: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_heatPump_heatStorage{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示空气热泵在每个时段的蓄热功率
        """
        self.heatStorage_heatPump_out: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heatStorage_heatPump_out{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示空气热泵在每个时段的蓄热出口温度
        """
        # TODO: 可以调节工作模式 热水温度较高时储存热量 （是否应当作为设备连接约束条件？）
        self.heatPump_heatStorage_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="heatPump_heatStorage_flag{0}".format(AirHeatPump.index),
        )
        """
        二元变量列表,表示空气热泵在每个时段的蓄热状态
        """
        self.electricity_heatPump: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_heatPump{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示空气热泵在每个时段的用电量
        """
        self.power_heatPump: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_heatPump{0}".format(AirHeatPump.index),
        )
        """
        连续变量列表,表示空气热泵在每个时段的总功率
        """

        # TODO: unclear meaning of "cooletStorage" and "heatStorage"
        self.coefficientOfPerformance_heatPump_cool = 3  # 表示该组件制冷时的性能系数
        self.coefficientOfPerformance_heatPump_cooletStorage = 3  # 表示该组件蓄冷时的性能系数
        self.coefficientOfPerformance_heatPump_heat = 3  # 表示该组件供热时的性能系数
        self.coefficientOfPerformance_heatPump_heatStorage = 3  # 表示该组件蓄热时的性能系数

    def constraints_register(self):
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
        10. 空气热泵的总年化成本 = 空气热泵设备数 * 设备价格/15+用电成本 * 8760/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        self.hourRange = range(0, self.num_hour)
        self.model.add_constraint(0 <= self.heatPump_device)
        self.model.add_constraint(self.heatPump_device <= self.device_max)

        self.model.add_constraints(
            0 <= self.power_heatPump_cool[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_heatPump_cool[h]
            <= self.cool_heatPump_out[h] * self.heatPump_device / 100
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_heatPump_cool[h] <= bigNumber * self.heatPump_cool_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            0 <= self.power_heatPump_cooletStorage[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_heatPump_cooletStorage[h]
            <= self.cooletStorage_heatPump_out[h] * self.heatPump_device / 100
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_heatPump_cooletStorage[h]
            <= bigNumber * self.heatPump_cooletStorage_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            0 <= self.power_heatPump_heat[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_heatPump_heat[h]
            <= self.heat_heatPump_out[h] * self.heatPump_device / 100
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_heatPump_heat[h] <= bigNumber * self.heatPump_heat_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            0 <= self.power_heatPump_heatStorage[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_heatPump_heatStorage[h]
            <= self.heatStorage_heatPump_out[h] * self.heatPump_device / 100
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_heatPump_heatStorage[h]
            <= bigNumber * self.heatPump_heatStorage_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            self.heatPump_cool_flag[h]
            + self.heatPump_cooletStorage_flag[h]
            + self.heatPump_heat_flag[h]
            + self.heatPump_heatStorage_flag[h]
            == 1
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.electricity_heatPump[h]
            # are you sure you want to subscribe?
            == self.power_heatPump_cool[h]
            / self.coefficientOfPerformance_heatPump_cool  # [h]
            + self.power_heatPump_cooletStorage[h]
            / self.coefficientOfPerformance_heatPump_cooletStorage  # [h]
            + self.power_heatPump_heat[h]
            / self.coefficientOfPerformance_heatPump_heat  # [h]
            + self.power_heatPump_heatStorage[h]
            / self.coefficientOfPerformance_heatPump_heatStorage  # [h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_heatPump[h]
            == self.power_heatPump_cool[h]
            + self.power_heatPump_cooletStorage[h]
            + self.power_heatPump_heat[h]
            + self.power_heatPump_heatStorage[h]
            for h in self.hourRange
        )

        self.electricity_cost = self.model.sum(
            self.electricity_heatPump[h] * self.electricity_price[h]
            for h in self.hourRange
        )
        # 年化
        self.model.add_constraint(
            self.annualized
            == self.heatPump_device * self.device_price / 15
            + self.electricity_cost * 8760 / self.num_hour
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

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        # 不同工况下热冷效率
        # case_ratio 不同工况下制热量/制冷量的比值
        # self.num_hour = num_hour
        WaterHeatPump.index += 1
        self.electricity_price = electricity_price
        self.waterSourceHeatPumps_device: ContinuousVarType = self.model.continuous_var(
            name="waterSourceHeatPumps_device{0}".format(WaterHeatPump.index)
        )
        """
        水源热泵机组等效单位设备数 大于零的实数
        """
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="WaterHeatPumpower_annualized{0}".format(WaterHeatPump.index)
        )
        """
        连续变量,表示水源热泵的年化费用
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="WaterHeatPumpower_electricity_sum{0}".format(WaterHeatPump.index)
        )
        """
        连续变量,表示水源热泵的用电成本
        """
        self.device_price = device_price
        self.device_count_max = device_max
        self.case_ratio = case_ratio

        self.power_waterSourceHeatPumps_cool: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterSourceHeatPumps_cool{0}".format(WaterHeatPump.index),
        )
        """
        连续变量列表,表示每个时刻水源热泵制冷功率
        """

        self.waterSourceHeatPumps_cool_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterSourceHeatPumps_cool_flag{0}".format(WaterHeatPump.index),
        )
        """
        二元变量列表,表示每个时刻水源热泵制冷状态
        """

        self.power_waterSourceHeatPumps_cooletStorage: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterSourceHeatPumps_cooletStorage{0}".format(
                WaterHeatPump.index
            ),
        )
        """
        连续变量列表,表示每个时刻水源热泵蓄冷功率
        """
        self.waterSourceHeatPumps_cooletStorage_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterSourceHeatPumps_cooletStorage_flag{0}".format(
                WaterHeatPump.index
            ),
        )
        """
        二元变量列表,表示每个时刻水源热泵蓄冷状态
        """
        self.power_waterSourceHeatPumps_heat: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterSourceHeatPumps_heat{0}".format(WaterHeatPump.index),
        )
        """
        连续变量列表,表示每个时刻水源热泵制热功率
        """
        self.waterSourceHeatPumps_heat_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterSourceHeatPumps_heat_flag{0}".format(WaterHeatPump.index),
        )
        """
        二元变量列表,表示每个时刻水源热泵制热状态
        """
        self.power_waterSourceHeatPumps_heatStorage: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterSourceHeatPumps_heatStorage{0}".format(
                WaterHeatPump.index
            ),
        )
        """
        连续变量列表,表示每个时刻水源热泵蓄热功率
        """
        self.waterSourceHeatPumps_heatStorage_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterSourceHeatPumps_heatStorage_flag{0}".format(WaterHeatPump.index),
        )
        """
        二元变量列表,表示每个时刻水源热泵蓄热状态
        """
        self.electricity_waterSourceHeatPumps: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_waterSourceHeatPumps{0}".format(WaterHeatPump.index),
        )
        """
        连续变量列表,表示每个时刻水源热泵用电量
        """
        self.power_waterSourceHeatPumps: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterSourceHeatPumps{0}".format(WaterHeatPump.index),
        )
        """
        连续变量列表,表示每个时刻水源热泵总功率
        """
        self.coefficientOfPerformance_waterSourceHeatPumps_cool = 5  # 制冷性能系数
        self.coefficientOfPerformance_waterSourceHeatPumps_cooletStorage = 5  # 蓄冷性能系数
        self.coefficientOfPerformance_waterSourceHeatPumps_heat = 5  # 制热性能系数
        self.coefficientOfPerformance_waterSourceHeatPumps_heatStorage = 5  # 蓄热性能系数

    def constraints_register(self):
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
        10. 水源热泵的总年化成本 = 水源热泵设备数 * 设备价格/15+用电成本 * 8760/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        self.hourRange = range(0, self.num_hour)
        self.model.add_constraint(0 <= self.waterSourceHeatPumps_device)
        self.model.add_constraint(self.waterSourceHeatPumps_device <= self.device_max)

        self.model.add_constraints(
            0 <= self.power_waterSourceHeatPumps_cool[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterSourceHeatPumps_cool[h]
            <= self.waterSourceHeatPumps_device * self.case_ratio[0]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterSourceHeatPumps_cool[h]
            <= bigNumber * self.waterSourceHeatPumps_cool_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            0 <= self.power_waterSourceHeatPumps_cooletStorage[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterSourceHeatPumps_cooletStorage[h]
            <= self.waterSourceHeatPumps_device * self.case_ratio[1]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterSourceHeatPumps_cooletStorage[h]
            <= bigNumber * self.waterSourceHeatPumps_cooletStorage_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            0 <= self.power_waterSourceHeatPumps_heat[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterSourceHeatPumps_heat[h]
            <= self.waterSourceHeatPumps_device * self.case_ratio[2]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterSourceHeatPumps_heat[h]
            <= bigNumber * self.waterSourceHeatPumps_heat_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            0 <= self.power_waterSourceHeatPumps_heatStorage[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterSourceHeatPumps_heatStorage[h]
            <= self.waterSourceHeatPumps_device * self.case_ratio[3]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterSourceHeatPumps_heatStorage[h]
            <= bigNumber * self.waterSourceHeatPumps_heatStorage_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            self.waterSourceHeatPumps_cool_flag[h]
            + self.waterSourceHeatPumps_cooletStorage_flag[h]
            + self.waterSourceHeatPumps_heat_flag[h]
            + self.waterSourceHeatPumps_heatStorage_flag[h]
            == 1
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.electricity_waterSourceHeatPumps[h]
            == self.power_waterSourceHeatPumps_cool[h]
            / self.coefficientOfPerformance_waterSourceHeatPumps_cool
            + self.power_waterSourceHeatPumps_cooletStorage[h]
            / self.coefficientOfPerformance_waterSourceHeatPumps_cooletStorage
            + self.power_waterSourceHeatPumps_heat[h]
            / self.coefficientOfPerformance_waterSourceHeatPumps_heat
            + self.power_waterSourceHeatPumps_heatStorage[h]
            / self.coefficientOfPerformance_waterSourceHeatPumps_heatStorage
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterSourceHeatPumps[h]
            == self.power_waterSourceHeatPumps_cool[h]
            + self.power_waterSourceHeatPumps_cooletStorage[h]
            + self.power_waterSourceHeatPumps_heat[h]
            + self.power_waterSourceHeatPumps_heatStorage[h]
            for h in self.hourRange
        )

        self.electricity_cost = self.model.sum(
            self.electricity_waterSourceHeatPumps[h] * self.electricity_price[h]
            for h in self.hourRange
        )
        # 年化
        self.model.add_constraint(
            self.annualized
            == self.waterSourceHeatPumps_device * self.device_price / 15
            + self.electricity_cost * 8760 / self.num_hour
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

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        # self.num_hour = num_hour
        WaterCoolingSpiral.index += 1
        self.electricity_price = electricity_price
        self.waterCoolingSpiralMachine_device: ContinuousVarType = (
            self.model.continuous_var(
                name="waterCoolingSpiralMachine_device{0}".format(
                    WaterCoolingSpiral.index
                )
            )
        )
        """
        水冷螺旋机机组等效单位设备数 大于零的实数
        """
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="waterCoolingSpiral_annualized{0}".format(WaterCoolingSpiral.index)
        )
        """
        连续变量,表示水冷螺旋机的年化费用
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="waterCoolingSpiral_electricity_sum{0}".format(
                WaterCoolingSpiral.index
            )
        )
        """
        连续变量,表示水冷螺旋机的用电成本
        """
        self.device_price = device_price
        self.device_count_max = device_max
        self.case_ratio = case_ratio
        self.power_waterCoolingSpiralMachine_cool: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterCoolingSpiralMachine_cool{0}".format(
                WaterCoolingSpiral.index
            ),
        )
        """
        连续变量列表,表示水冷螺旋机的制冷功率
        """
        self.waterCoolingSpiralMachine_cool_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterCoolingSpiralMachine_cool_flag{0}".format(
                WaterCoolingSpiral.index
            ),
        )
        """
        二元变量列表,表示水冷螺旋机的散热状态
        """

        self.power_waterCoolingSpiralMachine_cooletStorage: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterCoolingSpiralMachine_cooletStorage{0}".format(
                WaterCoolingSpiral.index
            ),
        )
        """
        连续变量列表,表示水冷螺旋机的蓄冷功率
        """

        self.waterCoolingSpiralMachine_cooletStorage_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterCoolingSpiralMachine_cooletStorage_flag{0}".format(
                WaterCoolingSpiral.index
            ),
        )
        """
        二元变量列表,表示水冷螺旋机的蓄冷状态
        """

        self.electricity_waterCoolingSpiralMachine: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_waterCoolingSpiralMachine{0}".format(
                WaterCoolingSpiral.index
            ),
        )
        """
        连续变量列表,表示水冷螺旋机的用电量
        """
        self.power_waterCoolingSpiralMachine: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterCoolingSpiralMachine{0}".format(WaterCoolingSpiral.index),
        )
        """
        连续变量列表,表示水冷螺旋机的功率
        """
        self.coefficientOfPerformance_waterCoolingSpiralMachine_cool = 5
        self.coefficientOfPerformance_waterCoolingSpiralMachine_cooletStorage = 5

    def constraints_register(self):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦水冷螺旋机的制冷功率≦水冷螺旋机设备数 * (况1)制冷情况下水冷螺旋机利用率<br>0≦水冷螺旋机的制冷功率≦水冷螺旋机制冷状态 * bigNumber
        3. 0≦水冷螺旋机的蓄冷功率≦水冷螺旋机设备数 * (况2)蓄冷情况下水冷螺旋机利用率<br>0≦水冷螺旋机的蓄冷功率≦水冷螺旋机蓄冷状态 * bigNumber
        4. 制冷状态+蓄冷状态=1
        5. 水冷螺旋机用电量 = 设备制冷功率/制冷性能系数+设备蓄冷功率/蓄冷性能系数
        6. 热泵总功率 = 制冷功率+蓄冷功率
        7. 用电成本 = 每个时刻(设备用电量 * 电价)的总和
        8. 水冷螺旋机的总年化成本 = 水源热泵设备数 * 设备价格/15+用电成本 * 8760/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        self.hourRange = range(0, self.num_hour)
        self.model.add_constraint(0 <= self.waterCoolingSpiralMachine_device)
        self.model.add_constraint(
            self.waterCoolingSpiralMachine_device <= self.device_max
        )

        self.model.add_constraints(
            0 <= self.power_waterCoolingSpiralMachine_cool[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterCoolingSpiralMachine_cool[h]
            <= self.waterCoolingSpiralMachine_device * self.case_ratio[0]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterCoolingSpiralMachine_cool[h]
            <= bigNumber * self.waterCoolingSpiralMachine_cool_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            0 <= self.power_waterCoolingSpiralMachine_cooletStorage[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterCoolingSpiralMachine_cooletStorage[h]
            <= self.waterCoolingSpiralMachine_device * self.case_ratio[1]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterCoolingSpiralMachine_cooletStorage[h]
            <= bigNumber * self.waterCoolingSpiralMachine_cooletStorage_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            self.waterCoolingSpiralMachine_cool_flag[h]
            + self.waterCoolingSpiralMachine_cooletStorage_flag[h]
            == 1
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.electricity_waterCoolingSpiralMachine[h]
            == self.power_waterCoolingSpiralMachine_cool[h]
            / self.coefficientOfPerformance_waterCoolingSpiralMachine_cool
            + self.power_waterCoolingSpiralMachine_cooletStorage[h]
            / self.coefficientOfPerformance_waterCoolingSpiralMachine_cooletStorage
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterCoolingSpiralMachine[h]
            == self.power_waterCoolingSpiralMachine_cool[h]
            + self.power_waterCoolingSpiralMachine_cooletStorage[h]
            for h in self.hourRange
        )

        self.electricity_cost = self.model.sum(
            self.electricity_waterCoolingSpiralMachine[h] * self.electricity_price[h]
            for h in self.hourRange
        )
        # 年化
        self.model.add_constraint(
            self.annualized
            == self.waterCoolingSpiralMachine_device * self.device_price / 15
            + self.electricity_cost * 8760 / self.num_hour
        )


# 双工况机组
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

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        # self.num_hour = num_hour
        DoubleWorkingConditionUnit.index += 1
        self.electricity_price = electricity_price
        self.doubleWorkingConditionUnit_device: ContinuousVarType = (
            self.model.continuous_var(
                name="doubleWorkingConditionUnit_device{0}".format(
                    DoubleWorkingConditionUnit.index
                )
            )
        )
        """
        双工况机组等效单位设备数 大于零的实数
        """
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="DoubleWorkingConditionUnit_annualized{0}".format(
                DoubleWorkingConditionUnit.index
            )
        )
        """
        连续变量,表示双工况机组的年化费用
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="DoubleWorkingConditionUnit_electricity_sum{0}".format(
                DoubleWorkingConditionUnit.index
            )
        )
        """
        连续变量,表示双工况机组的用电成本
        """
        self.device_price = device_price
        self.device_count_max = device_max
        self.case_ratio = case_ratio
        self.power_doubleWorkingConditionUnit_cool: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_doubleWorkingConditionUnit_cool{0}".format(
                DoubleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示双工况机组的制冷功率
        """

        self.doubleWorkingConditionUnit_cool_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="doubleWorkingConditionUnit_cool_flag{0}".format(
                DoubleWorkingConditionUnit.index
            ),
        )
        """
        二元变量列表,表示双工况机组的制冷状态
        """

        self.power_doubleWorkingConditionUnit_ice: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_doubleWorkingConditionUnit_ice{0}".format(
                DoubleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示双工况机组的制冰功率
        """

        self.doubleWorkingConditionUnit_ice_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="doubleWorkingConditionUnit_ice_flag{0}".format(
                DoubleWorkingConditionUnit.index
            ),
        )
        """
        二元变量列表,表示双工况机组的制冰状态
        """

        self.electricity_doubleWorkingConditionUnit: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_doubleWorkingConditionUnit{0}".format(
                DoubleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示双工况机组的用电量
        """
        self.power_doubleWorkingConditionUnit: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_doubleWorkingConditionUnit{0}".format(
                DoubleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示双工况机组的功率
        """
        self.coefficientOfPerformance_doubleWorkingConditionUnit_cool = 5
        self.coefficientOfPerformance_doubleWorkingConditionUnit_ice = 5

    # 三工况机组

    def constraints_register(self):
        """
        定义机组内部约束

        1. 0≦机组设备数≦最大设备量
        2. 0≦双工况机组的制冷功率≦双工况机组设备数 *  (况1)制冷情况下双工况机组利用率<br>0≦双工况机组的制冷功率≦双工况机组制冷状态 * bigNumber
        3. 0≦双工况机组的制冰功率≦双工况机组设备数 *  (况2)制冰情况下双工况机组利用率<br>0≦双工况机组的制冰功率≦双工况机组制冰状态 * bigNumber
        4. 制冷状态+制冰状态=1
        5. 双工况机组用电量 = 设备制冷功率/制冷性能系数+设备制冰功率/制冰性能系数
        6. 热泵总功率 = 制冷功率+制冰功率
        7. 用电成本 = 每个时刻(设备用电量 * 电价)的总和
        8. 双工况机组的总年化成本 = 双工况机组设备数 * 设备价格/15+用电成本 * 8760/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        self.hourRange = range(0, self.num_hour)
        self.model.add_constraint(0 <= self.doubleWorkingConditionUnit_device)
        self.model.add_constraint(
            self.doubleWorkingConditionUnit_device <= self.device_max
        )

        self.model.add_constraints(
            0 <= self.power_doubleWorkingConditionUnit_cool[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_doubleWorkingConditionUnit_cool[h]
            <= self.doubleWorkingConditionUnit_device * self.case_ratio[0]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_doubleWorkingConditionUnit_cool[h]
            <= bigNumber * self.doubleWorkingConditionUnit_cool_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            0 <= self.power_doubleWorkingConditionUnit_ice[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_doubleWorkingConditionUnit_ice[h]
            <= self.doubleWorkingConditionUnit_device * self.case_ratio[1]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_doubleWorkingConditionUnit_ice[h]
            <= bigNumber * self.doubleWorkingConditionUnit_ice_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            self.doubleWorkingConditionUnit_cool_flag[h]
            + self.doubleWorkingConditionUnit_ice_flag[h]
            == 1
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.electricity_doubleWorkingConditionUnit[h]
            == self.power_doubleWorkingConditionUnit_cool[h]
            / self.coefficientOfPerformance_doubleWorkingConditionUnit_cool
            + self.power_doubleWorkingConditionUnit_ice[h]
            / self.coefficientOfPerformance_doubleWorkingConditionUnit_ice
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_doubleWorkingConditionUnit[h]
            == self.power_doubleWorkingConditionUnit_cool[h]
            + self.power_doubleWorkingConditionUnit_ice[h]
            for h in self.hourRange
        )

        self.electricity_cost = self.model.sum(
            self.electricity_doubleWorkingConditionUnit[h] * self.electricity_price[h]
            for h in self.hourRange
        )
        # 年化
        self.model.add_constraint(
            self.annualized
            == self.doubleWorkingConditionUnit_device * self.device_price / 15
            + self.electricity_cost * 8760 / self.num_hour
        )


# TODO: 冷水机组效率与带载情况有关 考虑分段拟合
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

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        # self.num_hour = num_hour

        TripleWorkingConditionUnit.index += 1
        self.electricity_price = electricity_price
        self.tripleWorkingConditionUnit_device: ContinuousVarType = (
            self.model.continuous_var(
                name="tripleWorkingConditionUnit_device{0}".format(
                    TripleWorkingConditionUnit.index
                )
            )
        )
        """
        三工况机组等效单位设备数 大于零的实数
        """
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="TripleWorkingConditionUnit_annualized{0}".format(
                TripleWorkingConditionUnit.index
            )
        )
        """
        连续变量,表示三工况机组的年化费用
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="TripleWorkingConditionUnit_electricity_sum{0}".format(
                TripleWorkingConditionUnit.index
            )
        )
        """
        连续变量,表示三工况机组的用电成本
        """
        self.device_price = device_price
        self.device_count_max = device_max
        self.case_ratio = case_ratio
        self.power_tripleWorkingConditionUnit_cool: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_tripleWorkingConditionUnit_cool{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示三工况机组的制冷功率
        """

        self.tripleWorkingConditionUnit_cool_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="tripleWorkingConditionUnit_cool_flag{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        二元变量列表,表示三工况机组的制冷状态
        """

        self.power_tripleWorkingConditionUnit_ice: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_tripleWorkingConditionUnit_ice{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示三工况机组的制冰功率
        """

        self.tripleWorkingConditionUnit_ice_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="tripleWorkingConditionUnit_ice_flag{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        二元变量列表,表示三工况机组的制冰状态
        """

        self.power_tripleWorkingConditionUnit_heat: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_tripleWorkingConditionUnit_heat{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示三工况机组的制热功率
        """

        self.tripleWorkingConditionUnit_heat_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="tripleWorkingConditionUnit_heat_flag{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        二元变量列表,表示三工况机组的制热状态
        """

        self.electricity_tripleWorkingConditionUnit: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_tripleWorkingConditionUnit{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示三工况机组的用电量
        """
        self.power_tripleWorkingConditionUnit: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_tripleWorkingConditionUnit{0}".format(
                TripleWorkingConditionUnit.index
            ),
        )
        """
        连续变量列表,表示三工况机组的功率
        """
        self.coefficientOfPerformance_tripleWorkingConditionUnit_cool = 5
        self.coefficientOfPerformance_tripleWorkingConditionUnit_ice = 4
        self.coefficientOfPerformance_tripleWorkingConditionUnit_heat = 5

    def constraints_register(self):
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
        9. 三工况机组的总年化成本 = 三工况机组设备数 * 设备价格/15+用电成本 * 8760/小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        self.hourRange = range(0, self.num_hour)
        self.model.add_constraint(0 <= self.tripleWorkingConditionUnit_device)
        self.model.add_constraint(
            self.tripleWorkingConditionUnit_device <= self.device_max
        )

        self.model.add_constraints(
            0 <= self.power_tripleWorkingConditionUnit_cool[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_tripleWorkingConditionUnit_cool[h]
            <= self.tripleWorkingConditionUnit_device * self.case_ratio[0]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_tripleWorkingConditionUnit_cool[h]
            <= bigNumber * self.tripleWorkingConditionUnit_cool_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            0 <= self.power_tripleWorkingConditionUnit_ice[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_tripleWorkingConditionUnit_ice[h]
            <= self.tripleWorkingConditionUnit_device * self.case_ratio[1]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_tripleWorkingConditionUnit_ice[h]
            <= bigNumber * self.tripleWorkingConditionUnit_ice_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            0 <= self.power_tripleWorkingConditionUnit_heat[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_tripleWorkingConditionUnit_heat[h]
            <= self.tripleWorkingConditionUnit_device * self.case_ratio[2]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_tripleWorkingConditionUnit_heat[h]
            <= bigNumber * self.tripleWorkingConditionUnit_heat_flag[h]
            for h in self.hourRange
        )

        self.model.add_constraints(
            self.tripleWorkingConditionUnit_cool_flag[h]
            + self.tripleWorkingConditionUnit_ice_flag[h]
            + self.tripleWorkingConditionUnit_heat_flag[h]
            == 1
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.electricity_tripleWorkingConditionUnit[h]
            == self.power_tripleWorkingConditionUnit_cool[h]
            / self.coefficientOfPerformance_tripleWorkingConditionUnit_cool
            + self.power_tripleWorkingConditionUnit_ice[h]
            / self.coefficientOfPerformance_tripleWorkingConditionUnit_ice
            + self.power_tripleWorkingConditionUnit_heat[h]
            / self.coefficientOfPerformance_tripleWorkingConditionUnit_heat
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_tripleWorkingConditionUnit[h]
            == self.power_tripleWorkingConditionUnit_cool[h]
            + self.power_tripleWorkingConditionUnit_ice[h]
            + self.power_tripleWorkingConditionUnit_heat[h]
            for h in self.hourRange
        )

        self.electricity_cost = self.model.sum(
            self.electricity_tripleWorkingConditionUnit[h] * self.electricity_price[h]
            for h in self.hourRange
        )
        # 年化
        self.model.add_constraint(
            self.annualized
            == self.tripleWorkingConditionUnit_device * self.device_price / 15
            + self.electricity_cost * 8760 / self.num_hour
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

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        # self.num_hour = num_hour
        GeothermalHeatPump.index += 1
        self.electricity_price = electricity_price
        self.groundSourceHeatPump_device: ContinuousVarType = self.model.continuous_var(
            name="groundSourceHeatPump_device{0}".format(GeothermalHeatPump.index)
        )
        """
        地源热泵机组设备数量
        """
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="GeothermalHeatPumpower_annualized{0}".format(GeothermalHeatPump.index)
        )
        """
        地源热泵机组年运维成本
        """
        self.electricity_cost: ContinuousVarType = self.model.continuous_var(
            name="GeothermalHeatPumpower_electricity_sum{0}".format(
                GeothermalHeatPump.index
            )
        )
        """
        地源热泵每小时耗电费用
        """
        self.device_price = device_price
        self.device_count_max = device_max

        self.electricity_groundSourceHeatPump: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="electricity_groundSourceHeatPump{0}".format(GeothermalHeatPump.index),
        )
        """
        地源热泵每小时耗电量
        """
        self.power_groundSourceHeatPump: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_groundSourceHeatPump{0}".format(GeothermalHeatPump.index),
        )
        """
        地源热泵每小时输出功率
        """
        self.coefficientOfPerformance_groundSourceHeatPump = 5
        """
        地源热泵设备运行效率参数 默认为5
        """

    def constraints_register(self):
        """
        定义地源热泵机组约束条件:

        1. 0 <= 机组设备数量 <= 最大装机量
        2. 0 <= 每小时输出功率 <= 机组设备数量
        3. 每小时耗电量 = 每小时输出功率 / 运行效率参数
        4. 机组一天用电费用 = sum(每小时耗电量 * 该小时用电价格)
        5. 机组年运维成本 = 机组设备数量 * 设备价格 / 15 + 机组一天用电费用 * 8760 / 一天小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        self.hourRange = range(0, self.num_hour)

        self.model.add_constraint(0 <= self.groundSourceHeatPump_device)
        self.model.add_constraint(self.groundSourceHeatPump_device <= self.device_max)

        self.model.add_constraints(
            0 <= self.power_groundSourceHeatPump[h] for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_groundSourceHeatPump[h] <= self.groundSourceHeatPump_device
            for h in self.hourRange
        )

        self.model.add_constraints(
            self.electricity_groundSourceHeatPump[h]
            == self.power_groundSourceHeatPump[h]
            / self.coefficientOfPerformance_groundSourceHeatPump
            for h in self.hourRange
        )
        self.electricity_cost = self.model.sum(
            self.electricity_groundSourceHeatPump[h] * self.electricity_price[h]
            for h in self.hourRange
        )
        # 年化
        self.model.add_constraint(
            self.annualized
            == self.groundSourceHeatPump_device * self.device_price / 15
            + self.electricity_cost * 8760 / self.num_hour
        )


# 水蓄能,可蓄highTemperature,可以蓄低温
# waterStorageTank,可变容量的储能体
class WaterEnergyStorage(IntegratedEnergySystem):
    """
    水蓄能类
    """

    # index=0
    def __init__(
        self,
        num_hour: int,
        model: Model,
        waterStorageTank_Volume_max: float,  # V?
        volume_price: float,
        powerConversionSystem_price: float,
        conversion_rate_max: float,
        efficiency: float,
        energy_init: float,
        stateOfCharge_min: float,
        stateOfCharge_max: float,
        ratio_cool: float,
        ratio_heat: float,
        ratio_gheat: float,  # gheat? 工作热量？ geothermal heat?
        device_name: str = "water_energy_storage",
        device_count_min: int = 0,
    ):
        """
        创建一个水蓄能类

        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            waterStorageTank_Volume_max (float): 单个水罐的最大体积
            volume_price (float): 单位体积储水费用
            powerConversionSystem_price (float): 电力转换系统设备价格
            conversion_rate_max (float): 最大充放能倍率
            efficiency (float): 水罐储水效率参数
            energy_init (float): 储能装置的初始能量
            stateOfCharge_min (float): 最小储能量
            stateOfCharge_max (float): 最大储能量
            ratio_cool (float): 蓄冷模式下水蓄能罐单位体积的蓄冷效率
            ratio_heat (float): 蓄热模式下水蓄能罐单位体积的蓄热效率
            ratio_gheat (float): 地源热泵模式下水蓄能罐单位体积的蓄热效率
            device_name (str): 水蓄能机组名称,默认为"water_energy_storage",
        """
        # self.device_name = device_name

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        # self.num_hour = num_hour
        self.model = model
        # 对于水蓄能,优化的变量为水罐的体积
        self.waterStorageTank = EnergyStorageSystemVariable(
            num_hour,
            model,
            bigNumber,
            0,
            powerConversionSystem_price,
            conversion_rate_max,
            efficiency,
            energy_init,
            stateOfCharge_min,
            stateOfCharge_max,
        )
        """
        水蓄能罐,由可变储能设备`EnergyStorageSystemVariable`创建而来
        """
        self.index = EnergyStorageSystemVariable.index
        self.waterStorageTank_device_cool: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterStorageTank_device_cool{0}".format(self.index),
        )
        """
        每小时水蓄能在蓄冷模式下的储水量
        """
        self.waterStorageTank_device_heat: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterStorageTank_device_heat{0}".format(self.index),
        )
        """
        每小时水蓄能在蓄热模式下的储水量
        """
        self.waterStorageTank_device_gheat: List[  # generate?
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterStorageTank_device_gheat{0}".format(self.index),
        )
        """
        每小时水蓄能在地源热泵模式下的储水量
        """
        self.volume_price = volume_price
        self.waterStorageTank_Volume_max = waterStorageTank_Volume_max
        self.waterStorageTank_Volume: ContinuousVarType = self.model.continuous_var(
            name="waterStorageTank_V{0}".format(self.index)
        )
        """
        水蓄能机组总体积
        """
        self.waterStorageTank_cool_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterStorageTank_cool_flag{0}".format(self.index),
        )
        """
        每小时水蓄能设备是否处在蓄冷状态下
        """
        self.waterStorageTank_heat_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterStorageTank_heat_flag{0}".format(self.index),
        )
        """
        每小时水蓄能设备是否处在蓄热状态下
        """
        self.waterStorageTank_gheat_flag: List[
            BinaryVarType
        ] = self.model.binary_var_list(
            [i for i in range(0, self.num_hour)],
            name="waterStorageTank_gheat_flag{0}".format(self.index),
        )
        """
        每小时水蓄能设备是否处在高温热水状态下
        """
        self.ratio_cool = ratio_cool
        self.ratio_heat = ratio_heat
        self.ratio_gheat = ratio_gheat  # 蓄能效率 高温水
        self.power_waterStorageTank_cool: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterStorageTank_cool{0}".format(self.index),
        )
        """
        每小时水蓄能设备储能功率 蓄冷状态下
        """
        self.power_waterStorageTank_heat: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterStorageTank_heat{0}".format(self.index),
        )
        """
        每小时水蓄能设备储能功率 蓄热状态下
        """
        self.power_waterStorageTank_gheat: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_waterStorageTank_gheat{0}".format(self.index),  # gheat?
        )
        """
        每小时水蓄能设备储能功率 高温热水状态下
        """
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="power_waterStorageTank_annualized{0}".format(self.index)
        )
        """
        水蓄能设备年运维费用
        """

    def constraints_register(
        self, model: Model, register_period_constraints: int, day_node: int
    ):
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
        self.hourRange = range(0, self.num_hour)
        self.waterStorageTank.constraints_register(
            model, register_period_constraints, day_node
        )
        # waterStorageTank_device[h] == waterStorageTank_cool_flag[h] * waterStorageTank_Volume * ratio_cool + waterStorageTank_heat_flag[h] * waterStorageTank_Volume * ratio_heat + waterStorageTank_gheat_flag[
        #   h] * waterStorageTank_Volume * ratio_gheat
        # 用下面的式子进行线性化
        self.model.add_constraint(
            self.waterStorageTank_Volume <= self.waterStorageTank_Volume_max
        )
        self.model.add_constraint(self.waterStorageTank_Volume >= 0)
        self.model.add_constraints(
            self.waterStorageTank.device_count[h]
            == self.waterStorageTank_device_cool[h]
            + self.waterStorageTank_device_heat[h]
            + self.waterStorageTank_device_gheat[h]
            for h in self.hourRange
        )
        # (1)
        self.model.add_constraints(
            self.waterStorageTank_device_cool[h]
            <= self.waterStorageTank_Volume * self.ratio_cool
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.waterStorageTank_device_cool[h]
            <= self.waterStorageTank_cool_flag[h] * bigNumber
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.waterStorageTank_device_cool[h] >= 0 for h in self.hourRange
        )
        self.model.add_constraints(
            self.waterStorageTank_device_cool[h]
            >= self.waterStorageTank_Volume * self.ratio_cool
            - (1 - self.waterStorageTank_cool_flag[h]) * bigNumber
            for h in self.hourRange
        )
        # (2)
        self.model.add_constraints(
            self.waterStorageTank_device_heat[h]
            <= self.waterStorageTank_Volume * self.ratio_heat
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.waterStorageTank_device_heat[h]
            <= self.waterStorageTank_heat_flag[h] * bigNumber
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.waterStorageTank_device_heat[h] >= 0 for h in self.hourRange
        )
        self.model.add_constraints(
            self.waterStorageTank_device_heat[h]
            >= self.waterStorageTank_Volume * self.ratio_heat
            - (1 - self.waterStorageTank_heat_flag[h]) * bigNumber
            for h in self.hourRange
        )
        # (3)
        self.model.add_constraints(
            self.waterStorageTank_device_gheat[h]
            <= self.waterStorageTank_Volume * self.ratio_gheat
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.waterStorageTank_device_gheat[h]
            <= self.waterStorageTank_gheat_flag[h] * bigNumber
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.waterStorageTank_device_gheat[h] >= 0 for h in self.hourRange
        )
        self.model.add_constraints(
            self.waterStorageTank_device_gheat[h]
            >= self.waterStorageTank_Volume * self.ratio_gheat
            - (1 - self.waterStorageTank_gheat_flag[h]) * bigNumber
            for h in self.hourRange
        )
        # % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
        self.model.add_constraints(
            self.waterStorageTank_cool_flag[h]
            + self.waterStorageTank_heat_flag[h]
            + self.waterStorageTank_gheat_flag[h]
            == 1
            for h in self.hourRange
        )  # % 三个方面进行核算。
        # （1） power_waterStorageTank_cool[h] == power_waterStorageTank[h] * waterStorageTank_cool_flag[h]
        # （2）power_waterStorageTank_heat[h] == power_waterStorageTank[h] * waterStorageTank_heat_flag[h]
        # （3）power_waterStorageTank_gheat[h] == power_waterStorageTank[h] * waterStorageTank_gheat_flag[h]
        # 上面的公式进行线性化后,用下面的公式替代
        # (1)

        self.model.add_constraints(
            -bigNumber * self.waterStorageTank_cool_flag[h]
            <= self.power_waterStorageTank_cool[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterStorageTank_cool[h]
            <= bigNumber * self.waterStorageTank_cool_flag[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.waterStorageTank.power[h]
            - (1 - self.waterStorageTank_cool_flag[h]) * bigNumber
            <= self.power_waterStorageTank_cool[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterStorageTank_cool[h]
            <= self.waterStorageTank.power[h]
            + (1 - self.waterStorageTank_cool_flag[h]) * bigNumber
            for h in self.hourRange
        )
        # (2)
        self.model.add_constraints(
            -bigNumber * self.waterStorageTank_heat_flag[h]
            <= self.power_waterStorageTank_heat[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterStorageTank_heat[h]
            <= bigNumber * self.waterStorageTank_heat_flag[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.waterStorageTank.power[h]
            - (1 - self.waterStorageTank_heat_flag[h]) * bigNumber
            <= self.power_waterStorageTank_heat[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterStorageTank_heat[h]
            <= self.waterStorageTank.power[h]
            + (1 - self.waterStorageTank_heat_flag[h]) * bigNumber
            for h in self.hourRange
        )
        # (3)
        self.model.add_constraints(
            -bigNumber * self.waterStorageTank_gheat_flag[h]
            <= self.power_waterStorageTank_gheat[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterStorageTank_gheat[h]
            <= bigNumber * self.waterStorageTank_gheat_flag[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.waterStorageTank.power[h]
            - (1 - self.waterStorageTank_gheat_flag[h]) * bigNumber
            <= self.power_waterStorageTank_gheat[h]
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_waterStorageTank_gheat[h]
            <= self.waterStorageTank.power[h]
            + (1 - self.waterStorageTank_gheat_flag[h]) * bigNumber
            for h in self.hourRange
        )
        self.model.add_constraint(
            self.annualized == self.waterStorageTank_Volume * self.volume_price / 20
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
        electricSteamGenerator_device_count_max: float,
        electricSteamGenerator_price: float,
        electricSteamGeneratorSolidHeatStorage_price: float,
        electricity_price: Union[np.ndarray, List],
        efficiency: float,
        device_name: str = "electricSteamGenerator",
        device_count_min: int = 0,
    ):
        """
        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            electricSteamGenerator_device_count_max (int): 表示地热蒸汽发生器的最大数量
            electricSteamGenerator_price (float): 表示地热蒸汽发生器的单价
            electricSteamGeneratorSolidHeatStorage_price (float): 地热蒸汽发生器机组固态储热设备单价
            electricity_price (Union[np.ndarray, List]): 每小时电价
            efficiency (float): 效率参数
            device_name (str): 电蒸汽发生器机组名称，默认为"electricSteamGenerator"
        """
        # self.device_name = device_name

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        ElectricSteamGenerator.index += 1
        # self.num_hour = num_hour
        self.electricSteamGenerator_device: ContinuousVarType = (
            self.model.continuous_var(
                name="electricSteamGenerator_device{0}".format(
                    ElectricSteamGenerator.index
                )
            )
        )

        """
        电蒸汽发生器机组等效单位设备数 大于零的实数
        """
        self.power_electricSteamGenerator: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_electricSteamGenerator{0}".format(ElectricSteamGenerator.index),
        )

        """
        电蒸汽发生器总功率
        """
        self.power_electricSteamGenerator_steam: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="power_electricSteamGenerator_steam{0}".format(
                TroughPhotoThermal.index
            ),
        )

        """
        电蒸汽发生器产生蒸汽功率
        """
        self.electricSteamGenerator_device_count_max = electricSteamGenerator_device_max
        self.electricSteamGeneratorSolidHeatStorage_device_count_max = (
            electricSteamGenerator_device_count_max * 6
        )

        """
        电蒸汽发生器固体蓄热最大设备数=电蒸汽发生器最大设备数 * 6
        """
        self.electricSteamGenerator_price = electricSteamGenerator_price
        self.electricSteamGeneratorSolidHeatStorage_price = (
            electricSteamGeneratorSolidHeatStorage_price
        )
        self.electricity_price = electricity_price

        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="ElectricSteamGenerator_annualized{0}".format(
                ElectricSteamGenerator.index
            )
        )

        """
        电蒸汽发生器年化运维成本
        """
        self.efficiency = efficiency

        self.electricSteamGeneratorSolidHeatStorage_device = EnergyStorageSystem(
            num_hour,
            model,
            self.electricSteamGeneratorSolidHeatStorage_device_max,
            self.electricSteamGeneratorSolidHeatStorage_price,
            powerConversionSystem_price=0,
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
            name="electricSteamGenerator_electricity_cost{0}".format(
                ElectricSteamGenerator.index
            )
        )

        """
        用电成本
        """

    def constraints_register(self):
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
        self.hourRange = range(0, self.num_hour)
        self.electricSteamGeneratorSolidHeatStorage_device.constraints_register(model)
        self.model.add_constraint(self.electricSteamGenerator_device >= 0)
        self.model.add_constraint(
            self.electricSteamGenerator_device <= self.electricSteamGenerator_device_max
        )
        self.model.add_constraints(
            self.power_electricSteamGenerator[h] >= 0 for h in self.hourRange
        )
        self.model.add_constraints(
            self.power_electricSteamGenerator[h] <= self.electricSteamGenerator_device
            for h in self.hourRange
        )  # 与天气相关
        self.model.add_constraints(
            self.power_electricSteamGenerator[h]
            + self.electricSteamGeneratorSolidHeatStorage_device.power[h]
            == self.power_electricSteamGenerator_steam[h]
            for h in self.hourRange
        )  # troughPhotoThermal系统产生的highTemperature
        self.model.add_constraints(
            0 <= self.power_electricSteamGenerator_steam[h] for h in self.hourRange
        )  # 约束能量不能倒流
        self.model.add_constraints(
            self.electricity_cost
            == self.power_electricSteamGenerator[h] * self.electricity_price[h]
            for h in self.hourRange
        )
        self.model.add_constraint(
            self.annualized
            == self.electricSteamGenerator_device
            * self.electricSteamGenerator_price
            / 15
            + self.electricSteamGeneratorSolidHeatStorage_device.annualized
            + self.electricity_cost
        )


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
        Linearization.index += 1  # 要增加变量
        self.model = model
        self.b_positive: List[BinaryVarType] = self.model.binary_var_list(
            [i for i in hourRange],
            name="b_positive_absolute{0}".format(Linear_absolute.index),
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
            name="b_negitive_absolute{0}".format(Linear_absolute.index),
        )
        """
        一个二进制变量列表,长度为`len(hourRange)`
        
        对于`b_negitive`和`x_negitive`,有:
        `b_negitive[i]` == 1`时,`x_negitive[i] >= 0`
        `b_negitive[i]` == 0`时,`x_negitive[i] == 0`
        """
        self.x_positive: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in hourRange],
            name="x_positive_absolute{0}".format(Linear_absolute.index),
        )
        """
        一个实数变量列表,长度为`len(hourRange)`
        
        对于区间`hourRange`的每个数`i`,`x_positive[i]`是非负数,`x_positive[i]`和`x_negitive[i]`中必须有一个为0,另外一个大于0
        """
        self.x_negitive: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in hourRange],
            name="x_negitive_absolute{0}".format(Linear_absolute.index),
        )
        """
        一个实数变量列表,长度为`len(hourRange)`
        
        对于区间`hourRange`的每个数`i`,`x_negitive[i]`是非负数,`x_positive[i]`和`x_negitive[i]`中必须有一个为0,另外一个大于0
        """
        self.absolute_x: List[ContinuousVarType] = self.model.continuous_var_list(
            [i for i in hourRange], name="absolute_x{0}".format(Linear_absolute.index)
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


# 适用于municipalSteam,municipalHotWater
class CitySupply(IntegratedEnergySystem):
    """市政能源类,适用于市政蒸汽、市政热水"""

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        citySupplied_device_count_max: float,
        device_price: float,
        run_price: Union[np.ndarray, List],
        efficiency: float,
        device_name: str = "city_supply",
        device_count_min: int = 0,
    ):
        """
        创建一个市政能源类

        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            citySupplied_device_count_max (float): 市政能源设备机组最大装机量
            device_price (float): 设备单价
            run_price (Union[np.ndarray, List]): 每小时运维价格
            efficiency (float): 能源转换效率
            device_name (str): 市政能源设备机组名称,默认为"city_supply"
        """
        # self.device_name = device_name

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        CitySupply.index += 1
        # self.num_hour = num_hour  # hours in a day
        self.citySupplied_device: ContinuousVarType = self.model.continuous_var(
            name="citySupplied_device{0}".format(CitySupply.index)
        )
        """
        市政能源设备装机量 非负实数变量
        """
        self.heat_citySupplied: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_citySupplied{0}".format(CitySupply.index),
        )
        """
        每小时市政能源热量实际消耗 实数变量列表
        """
        self.heat_citySupplied_from: List[
            ContinuousVarType
        ] = self.model.continuous_var_list(
            [i for i in range(0, self.num_hour)],
            name="heat_citySupplied_from{0}".format(CitySupply.index),
        )
        """
        每小时市政能源热量输入 实数变量列表
        """
        self.citySupplied_device_count_max = citySupplied_device_max
        self.run_price = run_price
        self.device_price = device_price

        self.efficiency = efficiency
        self.citySupplied_cost: ContinuousVarType = self.model.continuous_var(
            name="citySupplied_cost{0}".format(CitySupply.index)
        )
        """
        市政能源消耗总费用 实数变量
        """
        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="citySupplied_annualized{0}".format(CitySupply.index)
        )
        """
        市政能源年运维费用 实数变量
        """

    def constraints_register(self):
        """
        定义市政能源类内部约束条件：

        1. 机组最大装机量 >= 市政能源设备装机量 >= 0
        2. 市政能源设备装机量 >= 每小时市政能源热量消耗 >= 0
        3. 每小时市政能源热量消耗 <= 每小时市政能源热量输入 / 能源传输效率
        4. 市政能源消耗总费用 = sum(每小时市政能源热量输入 * 每小时市政能源价格)
        5. 市政能源年运维费用 = 市政能源设备装机量 * 设备单价 / 15 + 市政能源消耗总费用 * 8760 / 一天小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
        """
        self.hourRange = range(0, self.num_hour)
        self.model.add_constraint(self.citySupplied_device >= 0)
        self.model.add_constraint(
            self.citySupplied_device <= self.citySupplied_device_max
        )
        self.model.add_constraints(
            self.heat_citySupplied[h] >= 0 for h in self.hourRange
        )
        self.model.add_constraints(
            self.heat_citySupplied[h] <= self.citySupplied_device
            for h in self.hourRange
        )
        self.model.add_constraints(
            self.heat_citySupplied[h]
            == self.heat_citySupplied_from[h] / self.efficiency
            for h in self.hourRange
        )
        self.citySupplied_cost = self.model.sum(
            self.heat_citySupplied_from[h] * self.run_price[h] for h in self.hourRange
        )
        self.model.add_constraint(
            self.annualized
            == self.citySupplied_device * self.device_price / 15
            + self.citySupplied_cost * 8760 / self.num_hour
        )


# 电网？
class GridNet(IntegratedEnergySystem):
    """
    电网类
    """

    index = 0

    def __init__(
        self,
        num_hour: int,
        model: Model,
        gridNet_device_count_max: float,
        device_price: float,
        electricity_price_from: Union[np.ndarray, List],
        electricity_price_to: float,
        device_name: str = "grid_net",
        device_count_min: int = 0,
    ):
        """
        新建一个电网类

        Args:
            num_hour (int): 一天的小时数
            model (docplex.mp.model.Model): 求解模型实例
            gridnet_device_count_max (float): 电网最大设备量
            device_price (float): 设备单价
            electricity_price_from (Union[np.ndarray, List]): 电力使用价格
            electricity_price_to (float): 电力生产报酬
            device_name (str): 电网名称,默认为"grid_net"
        """
        # self.device_name = device_name

        val = super().__init__(
            model=model,
            num_hour=num_hour,
            device_name=device_name,
            device_count_max=device_count_max,
            device_count_min=device_count_min,
            device_price=device_price,
            classObject=self.__class__,
        )
        GridNet.index += 1
        # self.num_hour = num_hour
        self.model = model
        self.gridNet_device: ContinuousVarType = self.model.continuous_var(
            name="gridNet_device{0}".format(GridNet.index)
        )
        """
        电网装机设备数 非负实数
        """

        self.gridNet_device_count_max = gridNet_device_max
        self.electricity_price_from = electricity_price_from
        self.electricity_price_to = electricity_price_to

        self.device_price = device_price

        self.gridNet_cost: ContinuousVarType = self.model.continuous_var(
            name="gridNet_cost{0}".format(GridNet.index)
        )
        """
        电网用电费用 非负实数
        """

        self.annualized: ContinuousVarType = self.model.continuous_var(
            name="gridNet_annualized{0}".format(GridNet.index)
        )
        """
        电网每年运维费用 非负实数
        """

        self.total_power = self.model.continuous_var_list(
            [i for i in range(0, num_hour0)],
            lb=-bigNumber,  # lower bound
            name="total_power {0}".format(GridNet.index),
        )
        """
        电网逐小时净用电量 长度为`num_hour0`的实数列表 大于零时电网耗电 小于零时电网发电
        """

        self.powerFrom = self.model.continuous_var_list(
            [i for i in range(0, num_hour0)], name="powerFrom{0}".format(GridNet.index)
        )
        """
        电网逐小时用电量 长度为`num_hour0`的非负实数列表
        """
        self.powerTo = self.model.continuous_var_list(
            [i for i in range(0, num_hour0)], name="powerTo {0}".format(GridNet.index)
        )
        """
        电网逐小时发电量 长度为`num_hour0`的非负实数列表
        """
        self.powerPeak = self.model.continuous_var(
            name="powerPeak{0}".format(GridNet.index)
        )
        """
        电网用电或者发电峰值 实数
        """
        self.baseCost = self.model.continuous_var(
            name="baseCost{0}".format(GridNet.index)
        )
        """
        电网基础费用 实数
        """
        self.powerFrom_max = self.model.continuous_var(
            name="powerFrom_max{0}".format(GridNet.index)
        )
        """
        电网用电峰值 实数
        """
        self.powerTo_max = self.model.continuous_var(
            name="powerTo_max{0}".format(GridNet.index)
        )
        """
        电网发电峰值 实数
        """

    def constraints_register(self, powerPeak_pre: float = 2000):
        """
        创建电网的约束条件到模型中

        1. 电网要么发电 要么用电 用电时发电量为0 发电时用电量为0 净用电量 = 用电量-发电量
        2. 电网最大设备数 >= 电网设备数 >= 0
        3. 每小时用电量小于电网设备数
        4. 每小时电网发电量小于电网设备数
        5. 电网一天基础消费 = min(max(用电或者发电峰值, 预估用电峰值) * 31, 电网设备数 * 22), 31是电价
        6. 电网一天总消费 = sum(每小时用电量 * 用电电价 + 每小时发电量 * 发电消费) + 电网基础消费
        7. 电网年运行成本 = 电网设备数量 * 设备单价 / 15 + 电网一天总消费 * 8760 / 一天小时数

        Args:
            model (docplex.mp.model.Model): 求解模型实例
            powerPeak_pre (float): 预估用电峰值
        """
        self.hourRange = range(0, self.num_hour)
        linearization = Linearization()
        linearization.positive_negitive_constraints_register(
            self.num_hour, model, self.total_power, self.powerFrom, self.powerTo
        )
        self.model.add_constraint(self.gridNet_device >= 0)
        self.model.add_constraint(self.gridNet_device <= self.gridNet_device_max)
        self.model.add_constraints(
            self.powerFrom[h] <= self.gridNet_device for h in self.hourRange
        )
        self.model.add_constraints(
            self.powerTo[h] <= self.gridNet_device for h in self.hourRange
        )

        # these are always true, not constraints.
        self.model.add_constraints(
            self.powerFrom[h] <= self.powerPeak for h in self.hourRange
        )
        self.model.add_constraints(
            self.powerTo[h] <= self.powerPeak for h in self.hourRange
        )
        self.powerFrom_max = model.max(self.powerFrom)
        self.powerTo_max = model.max(self.powerFrom)
        self.powerPeak = model.max(self.powerFrom_max, self.powerTo_max)

        self.baseCost = (
            model.min(
                model.max([self.powerPeak, powerPeak_pre]) * 31,
                self.gridNet_device * 22,  # pre?
            )
            * 12
        )

        self.gridNet_cost = (
            self.model.sum(
                self.powerFrom[h] * self.electricity_price_from[h]
                + self.powerTo[h] * self.electricity_price_to
                for h in self.hourRange
            )
            + self.baseCost
        )
        self.model.add_constraint(
            self.annualized
            == self.gridNet_device * self.device_price / 15
            + self.gridNet_cost * 8760 / self.num_hour
        )


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
        Linearization.index += 1
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
        Linearization.index += 1
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
        Linearization.index += 1
        model.add_constraints(var_bin[i] >= 0 for i in hourRangeback)
        model.add_constraints(
            var_bin[i] >= var[i - 1] - (1 - bin0[i]) * bigNumber for i in hourRangeback
        )
        model.add_constraints(var_bin[i] <= var[i - 1] for i in hourRangeback)
        model.add_constraints(
            var_bin[i] <= bin0[i] * bigNumber for i in hourRangeback
        )

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
        Linearization.index += 1
        y_flag = model.binary_var_list(
            [i for i in range(0, num_hour)],
            name="y_flag{0}".format(Linearization.index),
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
        model.add_constraints(
            y[h] <= y_flag[h] * bigNumber for h in range(0, num_hour)
        )
        # 当y_flag[h] == 0, y[h] 小于等于 0 (此时y[h] == 0)
        # 当y_flag[h] == 1, y[h] 小于等于 bigNumber
        model.add_constraints(
            x[h] <= y_flag[h] * bigNumber for h in range(0, num_hour)
        )
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
        Linearization.index += 1
        add_y = model.continuous_var_list(
            [i for i in range(0, num_hour)], name="add_y{0}".format(Linearization.index)
        )
        model.add_constraints(
            add_y[h] == x1[h] + x2[h] for h in range(0, num_hour)
        )
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
        Linearization.index += 1
        # bigNumber = 1e10
        positive_flag = model.binary_var_list(
            [i for i in range(0, num_hour)],
            name="Linearization_positive_flag{0}".format(Linearization.index),
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
