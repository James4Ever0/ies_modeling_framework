# from pydantic import BaseModel
# is the BaseModel needed?
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
    步长: float  # 单位：分钟

    @property
    def 仿真时长(self):
        """
        返回单位: 天
        """
        return (self.结束时间 - self.开始时间).days  # int


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