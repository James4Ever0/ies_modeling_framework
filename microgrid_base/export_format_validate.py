from typing import List

from pydantic import BaseModel, validator
from ies_optim import 柴油模型

class 柴油仿真结果(BaseModel):
    元件名称: str

    柴油消耗费用: str
    
    @staticmethod
    def export(model:柴油模型):
        return 柴油仿真结果()


class 电负荷仿真结果(BaseModel):
    元件名称: str

    电负荷: str


class 光伏发电仿真结果(BaseModel):
    元件名称: str

    设备型号: str

    设备台数: int
    """
    单位: one
    """

    设备维护费用: float
    """
    单位: 万元
    """

    产电量: str


class 风力发电仿真结果(BaseModel):
    元件名称: str

    设备型号: str

    设备台数: int
    """
    单位: one
    """

    设备维护费用: float
    """
    单位: 万元
    """

    产电量: str


class 柴油发电仿真结果(BaseModel):
    元件名称: str

    设备型号: str

    设备台数: int
    """
    单位: one
    """

    设备维护费用: float
    """
    单位: 万元
    """

    产电量: str

    柴油消耗量: str

    平均效率_平均COP: float
    """
    单位: one
    """


class 锂电池仿真结果(BaseModel):
    元件名称: str

    设备型号: str

    设备台数: int
    """
    单位: one
    """

    设备维护费用: float
    """
    单位: 万元
    """

    平均效率_平均COP: float
    """
    单位: one
    """


class 变压器仿真结果(BaseModel):
    元件名称: str

    设备型号: str

    设备台数: int
    """
    单位: one
    """

    设备维护费用: float
    """
    单位: 万元
    """

    平均效率_平均COP: float
    """
    单位: one
    """


class 变流器仿真结果(BaseModel):
    元件名称: str

    设备型号: str

    设备台数: int
    """
    单位: one
    """

    设备维护费用: float
    """
    单位: 万元
    """

    平均效率_平均COP: float
    """
    单位: one
    """


class 双向变流器仿真结果(BaseModel):
    元件名称: str

    设备型号: str

    设备台数: int
    """
    单位: one
    """

    设备维护费用: float
    """
    单位: 万元
    """

    平均效率_平均COP: float
    """
    单位: one
    """


class 传输线仿真结果(BaseModel):
    元件名称: str

    设备型号: str

    设备台数: int
    """
    单位: one
    """

    设备维护费用: float
    """
    单位: 万元
    """

    平均效率_平均COP: float
    """
    单位: one
    """


class 光伏发电出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    发电功率: List[float]
    """
    单位: kW
    """


class 风力发电出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    发电功率: List[float]
    """
    单位: kW
    """


class 柴油发电出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    发电功率: List[float]
    """
    单位: kW
    """


class 锂电池出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    充电功率: List[float]
    """
    单位: kW
    """

    放电功率: List[float]
    """
    单位: kW
    """

    荷电容量: List[float]
    """
    单位: kWh
    """

    荷电状态: List[float]
    """
    单位: percent <- one
    """

    @validator("荷电状态")
    def standard_unit_to_custom_荷电状态(cls, v):
        return [e / 0.01 for e in v]


class 变压器出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    转换功率: List[float]
    """
    单位: kW
    """


class 变流器出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    转换功率: List[float]
    """
    单位: kW
    """


class 双向变流器出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    转换功率: List[float]
    """
    单位: kW
    """
