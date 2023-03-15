from pydantic import BaseModel
from pyomo.environ import *
from dataclasses import dataclass
import uuid

model = ConcreteModel()


@dataclass
class 环境:
    温度: float  # (°C)
    空气比湿度: float  # (kg/kg)
    太阳辐射强度: float  # (W/m2)
    土壤平均温度: float  # (°C)
    距地面10m处东向风速: float  # (m/s)
    距地面50m处东向风速: float  # (m/s)
    距地面10m处北向风谏: float  # (m/s)
    距地面50m处北向风速: float  # (m/s)


import datetime


@dataclass
class 模拟参数:
    开始时间: datetime.datetime
    结束时间: datetime.datetime
    步长: float # 单位：分钟

    @property
    def 仿真时长(self):
        """
        返回单位: 天
        """
        return (self.结束时间 - self.开始时间).days # int


@dataclass
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

        self.设备配置台数 = 设备配置台数 if 设备配置台数 is not None else Var(domain=NonNegativeIntegers)

        self.输入功率 = {}
        self.输出功率 = {}
        self.输入类型列表 = 输入类型列表
        self.输出类型列表 = 输出类型列表
        self.建立输入功率(输入类型列表)
        self.建立输出功率(输出类型列表)

    def 建立输入功率(self, input_types):
        for input_type in input_types:
            self.输入功率[input_type] = VarList()
            self.model.add_component(
                f"{self.uuid}_输入功率_{input_type}", self.输入功率[input_type]
            )

    def 建立输出功率(self, output_types):
        for output_type in output_types:
            self.输出功率[output_type] = VarList()
            self.model.add_component(
                f"{self.uuid}_输出功率_{output_type}", self.输出功率[output_type]
            )


class 光伏(设备):
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备额定运行参数: dict = {},  # if any
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam
        输出类型列表:list=["电"],
        输入类型列表:list=[]
    ):
        super().__init__(
            model=model,
            生产厂商=生产厂商,
            生产型号=生产型号,
            设备额定运行参数=设备额定运行参数,
            设备运行约束=设备运行约束,
            设备经济性参数=设备经济性参数,
            设备工况=设备工况,
            输出类型列表=输出类型列表,  # add this later.
            输入类型列表=输入类型列表,
        )
        ## 设置设备额定运行参数 ##
        self.单个光伏板面积 = self.设备额定运行参数["单个光伏板面积"]
        """单位：(m²)"""
        self.光电转换效率 = self.设备额定运行参数["光电转换效率"]
        """单位：(%)"""
        self.功率因数 = self.设备额定运行参数["功率因数"]
        """0<x<1"""

        ## 设置设备运行约束 ##
        self.最大发电功率 = self.设备运行约束["最大发电功率"]
        """单位：(kW)"""

        ## 设备经济性参数 ##
        self.采购成本 = self.设备经济性参数["采购成本"]
        """单位：(万元/台)"""
        self.固定维护成本 = self.设备经济性参数["固定维护成本"]
        """单位：(万元/年)"""
        self.可变维护成本 = self.设备经济性参数["可变维护成本"]/10000
        """单位：(万元/kWh) <- (元/kWh)"""
        self.设计寿命 = self.设备经济性参数["设计寿命"]
        """单位：(年)"""

    def add_constraints(self):
        光照强度 = self.环境.太阳辐射强度
        Constraint(
            self.输出功率["电"]
            <= self.设备配置台数 * self.光电转换效率 * 光照强度 * self.单个光伏板面积 * self.功率因数
        )
        Constraint(expr=self.输出功率["电"] <= self.最大发电功率 * self.功率因数)
    
    def add_economic_constraints(self):
        
        self.成本 = (
            self.可变维护成本 * sum(self.输出功率["电"]) * self.模拟参数.步长/60
            + self.固定维护成本 * self.模拟参数.仿真时长
            + self.采购成本 * self.设备配置台数
        )
