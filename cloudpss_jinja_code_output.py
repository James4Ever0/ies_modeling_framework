# from pydantic import BaseModel
# is the BaseModel needed?
from pyomo.environ import *

from pydantic import BaseModel
import uuid
import numpy as np
import math

model = ConcreteModel()


class 环境(BaseModel):  # shall be array. not just numbers.
    
    _温度: np.ndarray
    """单位：(°C)
    """
    
    _空气比湿度: np.ndarray
    """单位：(kg/kg)
    """
    
    _太阳辐射强度: np.ndarray
    """单位：(W/m2)
    """
    
    _土壤平均温度: np.ndarray
    """单位：(°C)
    """
    
    _距地面10m处东向风速: np.ndarray
    """单位：(m/s)
    """
    
    _距地面50m处东向风速: np.ndarray
    """单位：(m/s)
    """
    
    _距地面10m处北向风速: np.ndarray
    """单位：(m/s)
    """
    
    _距地面50m处北向风速: np.ndarray
    """单位：(m/s)
    """
    
    
    @property
    def 温度(self):
        """
        单位：(kelvin) <- (degree_Celsius)
        """
        return self._温度 + 274.15
    
    @property
    def 空气比湿度(self):
        """
        单位：(dimensionless)
        """
        return self._空气比湿度
    
    @property
    def 太阳辐射强度(self):
        """
        单位：(kilowatt / m2) <- (watt / m2)
        """
        return self._太阳辐射强度 * 0.001
    
    @property
    def 土壤平均温度(self):
        """
        单位：(kelvin) <- (degree_Celsius)
        """
        return self._土壤平均温度 + 274.15
    
    @property
    def 距地面10m处东向风速(self):
        """
        单位：(kilometer / 年) <- (meter / second)
        """
        return self._距地面10m处东向风速 * 31557.600000000002
    
    @property
    def 距地面50m处东向风速(self):
        """
        单位：(kilometer / 年) <- (meter / second)
        """
        return self._距地面50m处东向风速 * 31557.600000000002
    
    @property
    def 距地面10m处北向风速(self):
        """
        单位：(kilometer / 年) <- (meter / second)
        """
        return self._距地面10m处北向风速 * 31557.600000000002
    
    @property
    def 距地面50m处北向风速(self):
        """
        单位：(kilometer / 年) <- (meter / second)
        """
        return self._距地面50m处北向风速 * 31557.600000000002
    

import datetime



class 模拟参数(BaseModel):
    开始时间: datetime.datetime
    结束时间: datetime.datetime
    _步长: float
    """
    单位：分钟
    """

    @property
    def 步长(self):
        """
        单位: 年
        """
        return self._步长 * 1.901285268841737e-06

    @property
    def _仿真时长(self):
        """
        单位: 天
        """
        return (self.结束时间 - self.开始时间).days

    @property
    def 仿真时长(self):
        """
        单位: 年
        """
        return self._仿真时长 * 0.0027378507871321013

    @property
    def 仿真步数(self):
        """
        总仿真步数
        """
        return math.floor(self.仿真时长 / self.步长)


class 设备:
    def __init__(
        self,
        model: ConcreteModel,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        self.model = model
        self.uuid = str(uuid.uuid4())
        self.生产厂商 = 生产厂商
        self.生产型号 = 生产型号
        self.设备额定运行参数 = 设备额定运行参数
        self.设备运行约束 = 设备运行约束
        self.设备经济性参数 = 设备经济性参数
        self.设备工况 = 设备工况

        self.环境 = environ
        self.模拟参数 = simulation_params

        self.设备配置台数 = Param(initialize=设备配置台数) if type(设备配置台数) is int else Var(domain=NonNegativeIntegers)
        self.model.add_component(f"{self.uuid}_设备配置台数", self.设备配置台数)
        

        self.输入功率 = {}
        self.输出功率 = {}
        self.输入类型列表 = 输入类型列表
        self.输出类型列表 = 输出类型列表
        self.建立输入功率(输入类型列表)
        self.建立输出功率(输出类型列表)

        self.variable_indices = [i for i in range(self.environ.仿真步数)]

    def 建立输入功率(self, input_types):
        for input_type in input_types:
            self.输入功率[input_type] = VarList(self.variable_indices)
            self.model.add_component(
                f"{self.uuid}_输入功率_{input_type}", self.输入功率[input_type]
            )

    def 建立输出功率(self, output_types):
        for output_type in output_types:
            self.输出功率[output_type] = VarList(self.variable_indices)
            self.model.add_component(
                f"{self.uuid}_输出功率_{output_type}", self.输出功率[output_type]
            )


class 光伏(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.单个光伏板面积 = self.设备额定运行参数["单个光伏板面积"]
        """单位：(m2) [设备额定运行参数]"""
        self.光电转换效率 = self.设备额定运行参数["光电转换效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大发电功率 = self.设备运行约束["最大发电功率"]
        """单位：(kilowatt) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 风机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定容量 = self.设备额定运行参数["额定容量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.额定风速 = self.设备额定运行参数["额定风速"] * 31557.600000000002
        """单位：(kilometer / 年) <- (meter / second) [设备额定运行参数]"""
        self.切出风速 = self.设备额定运行参数["切出风速"] * 31557.600000000002
        """单位：(kilometer / 年) <- (meter / second) [设备额定运行参数]"""
        self.切入风速 = self.设备额定运行参数["切入风速"] * 31557.600000000002
        """单位：(kilometer / 年) <- (meter / second) [设备额定运行参数]"""
        self.塔筒高度 = self.设备额定运行参数["塔筒高度"] * 0.001
        """单位：(kilometer) <- (meter) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 燃气轮机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定发电功率 = self.设备额定运行参数["额定发电功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.发电效率 = self.设备额定运行参数["发电效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.制热效率 = self.设备额定运行参数["制热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大烟气出口温度 = self.设备运行约束["最大烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小烟气出口温度 = self.设备运行约束["最小烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 燃气内燃机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定发电功率 = self.设备额定运行参数["额定发电功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.发电效率 = self.设备额定运行参数["发电效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.制热效率 = self.设备额定运行参数["制热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.循环水流量 = self.设备额定运行参数["循环水流量"] * 8766.0
        """单位：(metric_ton / 年) <- (metric_ton / hour) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大热水出口温度 = self.设备运行约束["最大热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水出口温度 = self.设备运行约束["最小热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水进口温度 = self.设备运行约束["最大热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水进口温度 = self.设备运行约束["最小热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大烟气出口温度 = self.设备运行约束["最大烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小烟气出口温度 = self.设备运行约束["最小烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 蒸汽轮机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        
        
        ## 设置设备运行约束 ##
        
        self.最大蒸汽进口温度 = self.设备运行约束["最大蒸汽进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小蒸汽进口温度 = self.设备运行约束["最小蒸汽进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大发电量 = self.设备运行约束["最大发电量"]
        """单位：(kilowatt) [设备运行约束]"""
        self.最小发电量 = self.设备运行约束["最小发电量"]
        """单位：(kilowatt) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 热泵(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定制热量 = self.设备额定运行参数["额定制热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.额定能效比COP = self.设备额定运行参数["额定能效比COP"]
        """设备额定运行参数"""
        self.额定制冷量 = self.设备额定运行参数["额定制冷量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制冷能效比COP = self.设备额定运行参数["制冷能效比COP"]
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大热水出口温度 = self.设备运行约束["最大热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水出口温度 = self.设备运行约束["最小热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水进口温度 = self.设备运行约束["最大热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水进口温度 = self.设备运行约束["最小热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大冷水出口温度 = self.设备运行约束["最大冷水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷水出口温度 = self.设备运行约束["最小冷水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大冷水进口温度 = self.设备运行约束["最大冷水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷水进口温度 = self.设备运行约束["最小冷水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大工作电压 = self.设备运行约束["最大工作电压"]
        """单位：(volt) [设备运行约束]"""
        self.最小工作电压 = self.设备运行约束["最小工作电压"]
        """单位：(volt) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 燃气热水锅炉(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.燃气锅炉类型 = self.设备额定运行参数["燃气锅炉类型"]
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制热效率 = self.设备额定运行参数["制热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大热水出口温度 = self.设备运行约束["最大热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水出口温度 = self.设备运行约束["最小热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水进口温度 = self.设备运行约束["最大热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水进口温度 = self.设备运行约束["最小热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 燃气蒸汽锅炉(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.燃气锅炉类型 = self.设备额定运行参数["燃气锅炉类型"]
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制热效率 = self.设备额定运行参数["制热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大蒸汽出口温度 = self.设备运行约束["最大蒸汽出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小蒸汽出口温度 = self.设备运行约束["最小蒸汽出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 余热热水锅炉(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.燃气锅炉类型 = self.设备额定运行参数["燃气锅炉类型"]
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.换热效率 = self.设备额定运行参数["换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大烟气出口温度 = self.设备运行约束["最大烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小烟气出口温度 = self.设备运行约束["最小烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大烟气进口温度 = self.设备运行约束["最大烟气进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小烟气进口温度 = self.设备运行约束["最小烟气进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水出口温度 = self.设备运行约束["最大热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水出口温度 = self.设备运行约束["最小热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水进口温度 = self.设备运行约束["最大热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水进口温度 = self.设备运行约束["最小热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 余热蒸汽锅炉_单压(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.燃气锅炉类型 = self.设备额定运行参数["燃气锅炉类型"]
        """设备额定运行参数"""
        self.压力等级 = self.设备额定运行参数["压力等级"]
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.换热效率 = self.设备额定运行参数["换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大烟气出口温度 = self.设备运行约束["最大烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小烟气出口温度 = self.设备运行约束["最小烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大烟气进口温度 = self.设备运行约束["最大烟气进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小烟气进口温度 = self.设备运行约束["最小烟气进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大蒸汽出口温度 = self.设备运行约束["最大蒸汽出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小蒸汽出口温度 = self.设备运行约束["最小蒸汽出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 余热蒸汽锅炉_双压(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.燃气锅炉类型 = self.设备额定运行参数["燃气锅炉类型"]
        """设备额定运行参数"""
        self.压力等级 = self.设备额定运行参数["压力等级"]
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.换热效率 = self.设备额定运行参数["换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大烟气出口温度 = self.设备运行约束["最大烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小烟气出口温度 = self.设备运行约束["最小烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大烟气进口温度 = self.设备运行约束["最大烟气进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小烟气进口温度 = self.设备运行约束["最小烟气进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大次高压蒸汽出口温度 = self.设备运行约束["最大次高压蒸汽出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小次高压蒸汽出口温度 = self.设备运行约束["最小次高压蒸汽出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大高压蒸汽出口温度 = self.设备运行约束["最大高压蒸汽出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小高压蒸汽出口温度 = self.设备运行约束["最小高压蒸汽出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 热管式太阳能集热器(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.单个集热器面积 = self.设备额定运行参数["单个集热器面积"]
        """单位：(m2) [设备额定运行参数]"""
        self.集热效率 = self.设备额定运行参数["集热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大热水出口温度 = self.设备运行约束["最大热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水出口温度 = self.设备运行约束["最小热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水进口温度 = self.设备运行约束["最大热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水进口温度 = self.设备运行约束["最小热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 电压缩制冷机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定制冷量 = self.设备额定运行参数["额定制冷量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制冷能效比COP = self.设备额定运行参数["制冷能效比COP"]
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大冷水出口温度 = self.设备运行约束["最大冷水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷水出口温度 = self.设备运行约束["最小冷水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大冷水进口温度 = self.设备运行约束["最大冷水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷水进口温度 = self.设备运行约束["最小冷水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 热水吸收式制冷机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.热源流体类型 = self.设备额定运行参数["热源流体类型"]
        """设备额定运行参数"""
        self.制冷状态额定制冷量 = self.设备额定运行参数["制冷状态额定制冷量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制冷状态时冷热比 = self.设备额定运行参数["制冷状态时冷热比"]
        """设备额定运行参数"""
        self.制热状态额定制热量 = self.设备额定运行参数["制热状态额定制热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制热状态时换热效率 = self.设备额定运行参数["制热状态时换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.用电功率 = self.设备额定运行参数["用电功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大热源出口温度 = self.设备运行约束["最大热源出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热源出口温度 = self.设备运行约束["最小热源出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热源进口温度 = self.设备运行约束["最大热源进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热源进口温度 = self.设备运行约束["最小热源进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大冷水出口温度 = self.设备运行约束["最大冷水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷水出口温度 = self.设备运行约束["最小冷水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大冷水进口温度 = self.设备运行约束["最大冷水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷水进口温度 = self.设备运行约束["最小冷水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水出口温度 = self.设备运行约束["最大热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水出口温度 = self.设备运行约束["最小热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水进口温度 = self.设备运行约束["最大热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水进口温度 = self.设备运行约束["最小热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大工作电压 = self.设备运行约束["最大工作电压"]
        """单位：(volt) [设备运行约束]"""
        self.最小工作电压 = self.设备运行约束["最小工作电压"]
        """单位：(volt) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 烟气吸收式制冷机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.热源流体类型 = self.设备额定运行参数["热源流体类型"]
        """设备额定运行参数"""
        self.制冷状态额定制冷量 = self.设备额定运行参数["制冷状态额定制冷量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制冷状态时冷热比 = self.设备额定运行参数["制冷状态时冷热比"]
        """设备额定运行参数"""
        self.制热状态额定制热量 = self.设备额定运行参数["制热状态额定制热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制热状态时换热效率 = self.设备额定运行参数["制热状态时换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.用电功率 = self.设备额定运行参数["用电功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大烟气出口温度 = self.设备运行约束["最大烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小烟气出口温度 = self.设备运行约束["最小烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大烟气进口温度 = self.设备运行约束["最大烟气进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小烟气进口温度 = self.设备运行约束["最小烟气进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大冷水出口温度 = self.设备运行约束["最大冷水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷水出口温度 = self.设备运行约束["最小冷水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大冷水进口温度 = self.设备运行约束["最大冷水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷水进口温度 = self.设备运行约束["最小冷水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水出口温度 = self.设备运行约束["最大热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水出口温度 = self.设备运行约束["最小热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水进口温度 = self.设备运行约束["最大热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水进口温度 = self.设备运行约束["最小热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大工作电压 = self.设备运行约束["最大工作电压"]
        """单位：(volt) [设备运行约束]"""
        self.最小工作电压 = self.设备运行约束["最小工作电压"]
        """单位：(volt) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 蒸汽吸收式制冷机(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.热源流体类型 = self.设备额定运行参数["热源流体类型"]
        """设备额定运行参数"""
        self.制冷状态额定制冷量 = self.设备额定运行参数["制冷状态额定制冷量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制冷状态时冷热比 = self.设备额定运行参数["制冷状态时冷热比"]
        """设备额定运行参数"""
        self.制热状态额定制热量 = self.设备额定运行参数["制热状态额定制热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制热状态时换热效率 = self.设备额定运行参数["制热状态时换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.用电功率 = self.设备额定运行参数["用电功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大蒸汽进口温度 = self.设备运行约束["最大蒸汽进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小蒸汽进口温度 = self.设备运行约束["最小蒸汽进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大冷水出口温度 = self.设备运行约束["最大冷水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷水出口温度 = self.设备运行约束["最小冷水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大冷水进口温度 = self.设备运行约束["最大冷水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷水进口温度 = self.设备运行约束["最小冷水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水出口温度 = self.设备运行约束["最大热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水出口温度 = self.设备运行约束["最小热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水进口温度 = self.设备运行约束["最大热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水进口温度 = self.设备运行约束["最小热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大工作电压 = self.设备运行约束["最大工作电压"]
        """单位：(volt) [设备运行约束]"""
        self.最小工作电压 = self.设备运行约束["最小工作电压"]
        """单位：(volt) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 蓄冰空调(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定放冷功率 = self.设备额定运行参数["额定放冷功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.额定蓄冷功率 = self.设备额定运行参数["额定蓄冷功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.放冷效率 = self.设备额定运行参数["放冷效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.蓄冷效率 = self.设备额定运行参数["蓄冷效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大冷水出口温度 = self.设备运行约束["最大冷水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大冷水进口温度 = self.设备运行约束["最大冷水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷水出口温度 = self.设备运行约束["最小冷水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷水进口温度 = self.设备运行约束["最小冷水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.蓄冰空调最大容量 = self.设备运行约束["蓄冰空调最大容量"]
        """单位：(kilowatt_hour) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 蓄热电锅炉(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.蓄热效率 = self.设备额定运行参数["蓄热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.额定放热功率 = self.设备额定运行参数["额定放热功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.额定蓄热功率 = self.设备额定运行参数["额定蓄热功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.放热效率 = self.设备额定运行参数["放热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.蓄热电锅炉最大容量 = self.设备运行约束["蓄热电锅炉最大容量"]
        """单位：(kilowatt_hour) [设备运行约束]"""
        self.最大热水出口温度 = self.设备运行约束["最大热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水进口温度 = self.设备运行约束["最大热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水出口温度 = self.设备运行约束["最小热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水进口温度 = self.设备运行约束["最小热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 蓄电池(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.充电效率 = self.设备额定运行参数["充电效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.放电效率 = self.设备额定运行参数["放电效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.额定充电功率 = self.设备额定运行参数["额定充电功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.额定放电功率 = self.设备额定运行参数["额定放电功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.电池最大容量 = self.设备运行约束["电池最大容量"]
        """单位：(kilowatt_hour) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 变压器(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.副边侧额定电压有效值 = self.设备额定运行参数["副边侧额定电压有效值"]
        """单位：(volt) [设备额定运行参数]"""
        self.励磁电导 = self.设备额定运行参数["励磁电导"]
        """单位：(p_u_) [设备额定运行参数]"""
        self.励磁电纳 = self.设备额定运行参数["励磁电纳"]
        """单位：(p_u_) [设备额定运行参数]"""
        self.原边侧额定电压有效值 = self.设备额定运行参数["原边侧额定电压有效值"] * 1000.0
        """单位：(volt) <- (kilovolt) [设备额定运行参数]"""
        self.变压器非标准变比 = self.设备额定运行参数["变压器非标准变比"]
        """单位：(p_u_) [设备额定运行参数]"""
        self.短路电抗 = self.设备额定运行参数["短路电抗"]
        """单位：(p_u_) [设备额定运行参数]"""
        self.短路电阻 = self.设备额定运行参数["短路电阻"]
        """单位：(p_u_) [设备额定运行参数]"""
        self.额定容量 = self.设备额定运行参数["额定容量"] * 1000.0
        """单位：(kilowatt) <- (megavolt_ampere) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大非标准变比 = self.设备运行约束["最大非标准变比"]
        """单位：(p_u_) [设备运行约束]"""
        self.最小非标准变比 = self.设备运行约束["最小非标准变比"]
        """单位：(p_u_) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 传输线(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.单位长度正序电抗 = self.设备额定运行参数["单位长度正序电抗"]
        """单位：(p_u_ / kilometer) [设备额定运行参数]"""
        self.单位长度正序电纳 = self.设备额定运行参数["单位长度正序电纳"]
        """单位：(p_u_ / kilometer) [设备额定运行参数]"""
        self.单位长度正序电阻 = self.设备额定运行参数["单位长度正序电阻"]
        """单位：(p_u_ / kilometer) [设备额定运行参数]"""
        self.额定电压 = self.设备额定运行参数["额定电压"] * 1000.0
        """单位：(volt) <- (kilovolt) [设备额定运行参数]"""
        self.额定频率 = self.设备额定运行参数["额定频率"]
        """单位：(hertz) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / kilometer) [设备经济性参数]"""
        self.维护成本 = self.设备经济性参数["维护成本"] * 0.0001
        """单位：(万元 / kilometer / 年) <- (元 / kilometer / 年) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 电容器(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定容量 = self.设备额定运行参数["额定容量"] * 1000.0
        """单位：(kilowatt) <- (megavolt_ampere) [设备额定运行参数]"""
        self.额定电压有效值 = self.设备额定运行参数["额定电压有效值"]
        """单位：(hertz) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 离心泵(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.工作特性曲线系数A = self.设备额定运行参数["工作特性曲线系数A"]
        """设备额定运行参数"""
        self.工作特性曲线系数B = self.设备额定运行参数["工作特性曲线系数B"]
        """设备额定运行参数"""
        self.工作特性曲线系数C = self.设备额定运行参数["工作特性曲线系数C"]
        """设备额定运行参数"""
        self.泵效率 = self.设备额定运行参数["泵效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最低进口压力 = self.设备运行约束["最低进口压力"]
        """单位：(megapascal) [设备运行约束]"""
        self.最大进口压力 = self.设备运行约束["最大进口压力"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 换热器(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.热流体类型 = self.设备额定运行参数["热流体类型"]
        """设备额定运行参数"""
        self.额定热负荷 = self.设备额定运行参数["额定热负荷"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.换热效率 = self.设备额定运行参数["换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大热流体出口温度 = self.设备运行约束["最大热流体出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热流体出口温度 = self.设备运行约束["最小热流体出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热流体进口温度 = self.设备运行约束["最大热流体进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热流体进口温度 = self.设备运行约束["最小热流体进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大冷流体出口温度 = self.设备运行约束["最大冷流体出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷流体出口温度 = self.设备运行约束["最小冷流体出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大冷流体进口温度 = self.设备运行约束["最大冷流体进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小冷流体进口温度 = self.设备运行约束["最小冷流体进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元 / 台) [设备经济性参数]"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元 / 年) [设备经济性参数]"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"] * 0.0001
        """单位：(万元 / kilowatt_hour) <- (元 / kilowatt_hour) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 管道(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.管道内径 = self.设备额定运行参数["管道内径"] * 1e-06
        """单位：(kilometer) <- (millimeter) [设备额定运行参数]"""
        self.管道壁厚 = self.设备额定运行参数["管道壁厚"] * 1e-06
        """单位：(kilometer) <- (millimeter) [设备额定运行参数]"""
        self.管道总传热系数 = self.设备额定运行参数["管道总传热系数"]
        """单位：(watt / kelvin / meter) [设备额定运行参数]"""
        self.管道粗糙度 = self.设备额定运行参数["管道粗糙度"] * 1e-06
        """单位：(kilometer) <- (millimeter) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        self.管道设计压力 = self.设备运行约束["管道设计压力"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        self.采购成本 = self.设备经济性参数["采购成本"] * 0.1
        """单位：(万元 / kilometer) <- (元 / meter) [设备经济性参数]"""
        self.维护成本 = self.设备经济性参数["维护成本"] * 0.1
        """单位：(万元 / kilometer / 年) <- (元 / meter / 年) [设备经济性参数]"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年) [设备经济性参数]"""
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 光伏_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.光伏板面积 = self.设备额定运行参数["光伏板面积"]
        """单位：(m2) [设备额定运行参数]"""
        self.光电转换效率 = self.设备额定运行参数["光电转换效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.功率因数 = self.设备额定运行参数["功率因数"]
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大发电功功率 = self.设备运行约束["最大发电功功率"]
        """单位：(kilowatt) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 风机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定发电量 = self.设备额定运行参数["额定发电量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.额定风速 = self.设备额定运行参数["额定风速"] * 31557.600000000002
        """单位：(kilometer / 年) <- (meter / second) [设备额定运行参数]"""
        self.切出风速 = self.设备额定运行参数["切出风速"] * 31557.600000000002
        """单位：(kilometer / 年) <- (meter / second) [设备额定运行参数]"""
        self.切入风速 = self.设备额定运行参数["切入风速"] * 31557.600000000002
        """单位：(kilometer / 年) <- (meter / second) [设备额定运行参数]"""
        self.轮毂高度 = self.设备额定运行参数["轮毂高度"] * 0.001
        """单位：(kilometer) <- (meter) [设备额定运行参数]"""
        self.功率因数 = self.设备额定运行参数["功率因数"]
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 燃气轮机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.局部压降系数  = self.设备额定运行参数["局部压降系数 "] * 1.00413490930961e-18
        """单位：(megapascal * 年 ** 2 / m3 ** 2) <- (kilopascal * second ** 2 / m3 ** 2) [设备额定运行参数]"""
        self.功率因数 = self.设备额定运行参数["功率因数"]
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        self.最小供水温度  = self.设备运行约束["最小供水温度 "] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大供水温度  = self.设备运行约束["最大供水温度 "] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 燃气内燃机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定发电功率 = self.设备额定运行参数["额定发电功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.发电效率 = self.设备额定运行参数["发电效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.制热效率 = self.设备额定运行参数["制热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.循环水流量 = self.设备额定运行参数["循环水流量"] * 8766.0
        """单位：(metric_ton / 年) <- (metric_ton / hour) [设备额定运行参数]"""
        self.功率因数 = self.设备额定运行参数["功率因数"]
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大热水出口温度 = self.设备运行约束["最大热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水出口温度 = self.设备运行约束["最小热水出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大热水进口温度 = self.设备运行约束["最大热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小热水进口温度 = self.设备运行约束["最小热水进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大烟气出口温度 = self.设备运行约束["最大烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小烟气出口温度 = self.设备运行约束["最小烟气出口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 蒸汽轮机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定蒸汽进口温度 = self.设备额定运行参数["额定蒸汽进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备额定运行参数]"""
        self.蒸汽流量 = self.设备额定运行参数["蒸汽流量"] * 8766.0
        """单位：(metric_ton / 年) <- (metric_ton / hour) [设备额定运行参数]"""
        self.发电效率 = self.设备额定运行参数["发电效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.功率因数 = self.设备额定运行参数["功率因数"]
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        self.最大蒸汽进口温度 = self.设备运行约束["最大蒸汽进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最小蒸汽进口温度 = self.设备运行约束["最小蒸汽进口温度"] + 274.15
        """单位：(kelvin) <- (degree_Celsius) [设备运行约束]"""
        self.最大发电量 = self.设备运行约束["最大发电量"]
        """单位：(kilowatt) [设备运行约束]"""
        self.最小发电量 = self.设备运行约束["最小发电量"]
        """单位：(kilowatt) [设备运行约束]"""
        self.机组最大承压 = self.设备运行约束["机组最大承压"]
        """单位：(megapascal) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 热泵_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定制热量 = self.设备额定运行参数["额定制热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.额定能效比COP = self.设备额定运行参数["额定能效比COP"]
        """设备额定运行参数"""
        self.额定制冷量 = self.设备额定运行参数["额定制冷量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制冷能效比COP = self.设备额定运行参数["制冷能效比COP"]
        """设备额定运行参数"""
        self.功率因数 = self.设备额定运行参数["功率因数"]
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 燃气热水锅炉_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.燃气锅炉类型 = self.设备额定运行参数["燃气锅炉类型"]
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制热效率 = self.设备额定运行参数["制热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 燃气蒸汽锅炉_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.燃气锅炉类型 = self.设备额定运行参数["燃气锅炉类型"]
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制热效率 = self.设备额定运行参数["制热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 余热热水锅炉_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.燃气锅炉类型 = self.设备额定运行参数["燃气锅炉类型"]
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.换热效率 = self.设备额定运行参数["换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 余热蒸汽锅炉_单压_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.燃气锅炉类型 = self.设备额定运行参数["燃气锅炉类型"]
        """设备额定运行参数"""
        self.压力等级 = self.设备额定运行参数["压力等级"]
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.换热效率 = self.设备额定运行参数["换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 余热蒸汽锅炉_双压_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.燃气锅炉类型 = self.设备额定运行参数["燃气锅炉类型"]
        """设备额定运行参数"""
        self.压力等级 = self.设备额定运行参数["压力等级"]
        """设备额定运行参数"""
        self.额定供热量 = self.设备额定运行参数["额定供热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.换热效率 = self.设备额定运行参数["换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 热管式太阳能集热器_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.局部压降系数 = self.设备额定运行参数["局部压降系数"] * 1.00413490930961e-18
        """单位：(megapascal * 年 ** 2 / m3 ** 2) <- (kilopascal * second ** 2 / m3 ** 2) [设备额定运行参数]"""
        self.集热器面积 = self.设备额定运行参数["集热器面积"]
        """单位：(m2) [设备额定运行参数]"""
        self.集热效率 = self.设备额定运行参数["集热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 电压缩制冷机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定制冷量 = self.设备额定运行参数["额定制冷量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制冷能效比COP = self.设备额定运行参数["制冷能效比COP"]
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 热水吸收式制冷机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.热源流体类型 = self.设备额定运行参数["热源流体类型"]
        """设备额定运行参数"""
        self.制冷状态额定制冷量 = self.设备额定运行参数["制冷状态额定制冷量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制冷状态时冷热比 = self.设备额定运行参数["制冷状态时冷热比"]
        """设备额定运行参数"""
        self.制热状态额定制热量 = self.设备额定运行参数["制热状态额定制热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制热状态时换热效率 = self.设备额定运行参数["制热状态时换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.用电功率 = self.设备额定运行参数["用电功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 烟气吸收式制冷机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.热源流体类型 = self.设备额定运行参数["热源流体类型"]
        """设备额定运行参数"""
        self.制冷状态额定制冷量 = self.设备额定运行参数["制冷状态额定制冷量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制冷状态时冷热比 = self.设备额定运行参数["制冷状态时冷热比"]
        """设备额定运行参数"""
        self.制热状态额定制热量 = self.设备额定运行参数["制热状态额定制热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制热状态时换热效率 = self.设备额定运行参数["制热状态时换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.用电功率 = self.设备额定运行参数["用电功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 蒸汽吸收式制冷机_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.热源流体类型 = self.设备额定运行参数["热源流体类型"]
        """设备额定运行参数"""
        self.制冷状态额定制冷量 = self.设备额定运行参数["制冷状态额定制冷量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制冷状态时冷热比 = self.设备额定运行参数["制冷状态时冷热比"]
        """设备额定运行参数"""
        self.制热状态额定制热量 = self.设备额定运行参数["制热状态额定制热量"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.制热状态时换热效率 = self.设备额定运行参数["制热状态时换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.用电功率 = self.设备额定运行参数["用电功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 蓄冰空调_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定放冷功率 = self.设备额定运行参数["额定放冷功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.额定蓄冷功率 = self.设备额定运行参数["额定蓄冷功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.放冷效率 = self.设备额定运行参数["放冷效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.蓄冷效率 = self.设备额定运行参数["蓄冷效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.功率因数 = self.设备额定运行参数["功率因数"]
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 蓄热电锅炉_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.蓄热效率 = self.设备额定运行参数["蓄热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.额定放热功率 = self.设备额定运行参数["额定放热功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.额定蓄热功率 = self.设备额定运行参数["额定蓄热功率"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.放热效率 = self.设备额定运行参数["放热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 蓄电池_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.充电效率 = self.设备额定运行参数["充电效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.放电效率 = self.设备额定运行参数["放电效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        self.功率因数 = self.设备额定运行参数["功率因数"]
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        self.电池最大容量 = self.设备运行约束["电池最大容量"]
        """单位：(kilowatt_hour) [设备运行约束]"""
        self.最大充电功率 = self.设备运行约束["最大充电功率"]
        """单位：(kilowatt) [设备运行约束]"""
        self.最大放电功率 = self.设备运行约束["最大放电功率"]
        """单位：(kilowatt) [设备运行约束]"""
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 储水罐_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.入口侧局部压降系数 = self.设备额定运行参数["入口侧局部压降系数"] * 1.00413490930961e-18
        """单位：(megapascal * 年 ** 2 / m3 ** 2) <- (kilopascal * second ** 2 / m3 ** 2) [设备额定运行参数]"""
        self.出口侧局部压降系数 = self.设备额定运行参数["出口侧局部压降系数"] * 1.00413490930961e-18
        """单位：(megapascal * 年 ** 2 / m3 ** 2) <- (kilopascal * second ** 2 / m3 ** 2) [设备额定运行参数]"""
        self.罐底面积 = self.设备额定运行参数["罐底面积"]
        """单位：(m2) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 变压器_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.变压器非标准变比 = self.设备额定运行参数["变压器非标准变比"]
        """单位：(p_u_) [设备额定运行参数]"""
        self.一次侧短路电抗 = self.设备额定运行参数["一次侧短路电抗"]
        """单位：(ohm) [设备额定运行参数]"""
        self.一次侧短路电阻 = self.设备额定运行参数["一次侧短路电阻"]
        """单位：(ohm) [设备额定运行参数]"""
        self.额定容量 = self.设备额定运行参数["额定容量"] * 1000.0
        """单位：(kilowatt) <- (megavolt_ampere) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 传输线_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.单位长度电抗 = self.设备额定运行参数["单位长度电抗"]
        """单位：(ohm / kilometer) [设备额定运行参数]"""
        self.单位长度容抗 = self.设备额定运行参数["单位长度容抗"] * 1000000.0
        """单位：(kilometer * ohm) <- (kilometer * megaohm) [设备额定运行参数]"""
        self.单位长度电阻 = self.设备额定运行参数["单位长度电阻"]
        """单位：(ohm / kilometer) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 电容器_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定容量 = self.设备额定运行参数["额定容量"] * 1000.0
        """单位：(kilowatt) <- (megavolt_ampere) [设备额定运行参数]"""
        self.额定电压有效值 = self.设备额定运行参数["额定电压有效值"]
        """单位：(hertz) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 模块化多电平变流器_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定电压 = self.设备额定运行参数["额定电压"] * 1000.0
        """单位：(volt) <- (kilovolt) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 离心泵_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.额定转速  = self.设备额定运行参数["额定转速 "] * 0.10471975511965977
        """单位：(hertz) <- (revolutions_per_minute) [设备额定运行参数]"""
        self.最大工作转速 = self.设备额定运行参数["最大工作转速"]
        """设备额定运行参数"""
        self.最小工作转速 = self.设备额定运行参数["最小工作转速"]
        """设备额定运行参数"""
        self.功率因数 = self.设备额定运行参数["功率因数"]
        """设备额定运行参数"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 换热器_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.热流体类型 = self.设备额定运行参数["热流体类型"]
        """设备额定运行参数"""
        self.额定热负荷 = self.设备额定运行参数["额定热负荷"]
        """单位：(kilowatt) [设备额定运行参数]"""
        self.换热效率 = self.设备额定运行参数["换热效率"] * 0.01
        """单位：(one) <- (percent) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


class 管道_建模仿真(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备配置台数: int,
        environ: 环境,
        simulation_params: 模拟参数,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam 挡位
        输出类型列表: list = [],
        输入类型列表: list = [],
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备配置台数=设备配置台数,
            environ=environ,
            simulation_params=simulation_params,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        
        ## 设置设备额定运行参数 ##
        
        self.管道内径 = self.设备额定运行参数["管道内径"] * 1e-06
        """单位：(kilometer) <- (millimeter) [设备额定运行参数]"""
        self.管道壁厚 = self.设备额定运行参数["管道壁厚"] * 1e-06
        """单位：(kilometer) <- (millimeter) [设备额定运行参数]"""
        self.管道总传热系数 = self.设备额定运行参数["管道总传热系数"]
        """单位：(watt / kelvin / meter) [设备额定运行参数]"""
        self.管道粗糙度 = self.设备额定运行参数["管道粗糙度"] * 1e-06
        """单位：(kilometer) <- (millimeter) [设备额定运行参数]"""
        
        
        ## 设置设备运行约束 ##
        
        
        
        ## 设置设备经济性参数 ##
        
        
        
        ## 设置设备工况 ##
        
        
        

    def add_constraints(self):
        ...

    def add_economic_constraints(self):
        ...


