from pydantic import BaseModel
from pyomo.environ import *

model = ConcreteModel()


class 设备:
    def __init__(
        self,
        model,
        生产厂商: str,
        生产型号: str,
        设备额定运行参数: dict = {},
        设备运行约束: dict = {},  # if any
        设备经济性参数: dict = {},  #  if any
        设备工况: dict = {},  # OperateParam (vue)
    ):
        self.model = model
        self.生产厂商 = 生产厂商
        self.生产型号 = 生产型号
        self.设备额定运行参数 = 设备额定运行参数
        self.设备运行约束 = 设备运行约束
        self.设备经济性参数 = 设备经济性参数
        self.设备工况 = 设备工况


class 光伏(设备):
    def __init__(self, model):
        self.model = model

    def 设备额定运行参数(
        self,
        model,
        光伏板面积: float,
        光电转换效率: float,
        功率因数: float,
        输出功率: float,
        最大输出功率: float,
        光照强度: float,
    ):
        self.model = model
        self.光伏板面积 = 光伏板面积
        self.光电转换效率 = 光电转换效率
        self.功率因数 = 功率因数
        self.光照强度 = 光照强度
        self.最大输出功率 = 最大输出功率

        self.输出功率 = min(光电转换效率 * 光照强度 * 光伏板面积, 最大输出功率) * 功率因数

    class 设备运行约束(BaseModel):
        最大发电功率: float  # (kW)

    class 设备经济性参数(BaseModel):
        采购成本: float  # (万元/台)
        固定维护成本: float  #  (万元/年)
        可变维护成本: float  #  (元/kWh)
        设计寿命: float  # (年)
