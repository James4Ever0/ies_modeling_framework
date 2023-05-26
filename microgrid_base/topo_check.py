# the main code for computing.
# currently just compute microgrid
# three computation modes:

# 8760 hours of data
# several days of data to compute a year

# 7200 seconds. simulation

# device parameters would be the same.

# load and environment might change.

# so for every device the will change.

# iterate through all device-port pairs, then retrieve attributes from another dict.

from pydantic import BaseModel
from typing import List

# string, digits, tables.
# you can dump and load from json.


class 光伏发电ID(BaseModel):
    电接口: int
    """
    类型: 供电端输出
    """


class 光伏发电数据(BaseModel):  # 发电设备
    生产厂商: str

    设备型号: str

    光伏板面积: float
    """
    单位: m2
    """

    电电转换效率: float
    """
    单位: percent
    """

    最大发电功率: float
    """
    单位: kWp
    """

    发电爬坡率: float
    """
    单位: percent/s
    """

    采购成本: float
    """
    单位: 万元/kWp
    """

    固定维护成本: float
    """
    单位: 万元/(kWp*年)
    """

    可变维护成本: float
    """
    单位: 元/kWh
    """

    设计寿命: float
    """
    单位: 年
    """

    建设费用系数: float
    """
    单位: 万元/kWp
    """

    建设费用基数: float
    """
    单位: 万元
    """

    最大安装面积: float
    """
    单位: m2
    """

    最小安装面积: float
    """
    单位: m2
    """


class 风力发电ID(BaseModel):
    电接口: int
    """
    类型: 供电端输出
    """


class 风力发电数据(BaseModel):  # 发电设备
    生产厂商: str

    设备型号: str

    额定功率: float
    """
    单位: kWp
    """

    额定风速: float
    """
    单位: m/s
    """

    切入风速: float
    """
    单位: m/s
    """

    切出风速: float
    """
    单位: m/s
    """

    发电爬坡率: float
    """
    单位: percent/s
    """

    采购成本: float
    """
    单位: 万元/kWp
    """

    固定维护成本: float
    """
    单位: 万元/(kWp*年)
    """

    可变维护成本: float
    """
    单位: 元/kWh
    """

    设计寿命: float
    """
    单位: 年
    """

    建设费用系数: float
    """
    单位: 万元/kWp
    """

    建设费用基数: float
    """
    单位: 万元
    """

    最大安装台数: float
    """
    单位: 台
    """

    最小安装台数: float
    """
    单位: 台
    """


class 柴油发电ID(BaseModel):
    电接口: int
    """
    类型: 供电端输出
    """
    燃料接口: int
    """
    类型: 柴油输入
    """


class 柴油发电数据(BaseModel):  # 发电设备
    生产厂商: str

    设备型号: str

    额定功率: float
    """
    单位: kW
    """

    发电爬坡率: float
    """
    单位: percent/s
    """

    启动功率百分比: float
    """
    单位: percent
    """

    采购成本: float
    """
    单位: 万元/台
    """

    固定维护成本: float
    """
    单位: 万元/(台*年)
    """

    可变维护成本: float
    """
    单位: 元/kWh
    """

    设计寿命: float
    """
    单位: 年
    """

    建设费用系数: float
    """
    单位: 万元/台
    """

    建设费用基数: float
    """
    单位: 万元
    """

    最大安装台数: float
    """
    单位: 台
    """

    最小安装台数: float
    """
    单位: 台
    """

    燃油消耗率_负载率: List[List[float]]
    """
    燃油消耗率 单位: L/kWh
    负载率 单位: percent
    """


class 锂电池ID(BaseModel):
    电接口: int
    """
    类型: 电储能端输入输出
    """


class 锂电池数据(BaseModel):  # 储能设备
    生产厂商: str

    设备型号: str

    额定容量: float
    """
    单位: kWh
    """

    电池充放电倍率: float
    """
    单位: 1/hour
    """

    充能效率: float
    """
    单位: percent
    """

    放能效率: float
    """
    单位: percent
    """

    存储衰减: float
    """
    单位: percent/hour
    """

    生命周期总放电量: float
    """
    单位: kWh
    """

    电池换芯周期: float
    """
    单位: 年
    """

    采购成本: float
    """
    单位: 万元/kWh
    """

    固定维护成本: float
    """
    单位: 万元/(kWh*年)
    """

    可变维护成本: float
    """
    单位: 元/kWh
    """

    设计寿命: float
    """
    单位: 年
    """

    建设费用系数: float
    """
    单位: 万元/kWh
    """

    建设费用基数: float
    """
    单位: 万元
    """

    最大安装台数: float
    """
    单位: 台
    """

    最小安装台数: float
    """
    单位: 台
    """


class 变压器ID(BaseModel):
    电输入: int
    """
    类型: 电母线输入
    """
    电输出: int
    """
    类型: 变压器输出
    """


class 变压器数据(BaseModel):  # 配电传输
    生产厂商: str

    设备型号: str

    效率: float
    """
    单位: percent
    """

    变压器容量: float
    """
    单位: kW
    """

    采购成本: float
    """
    单位: 万元/kW
    """

    固定维护成本: float
    """
    单位: 万元/(kW*年)
    """

    可变维护成本: float
    """
    单位: 元/kWh
    """

    设计寿命: float
    """
    单位: 年
    """

    建设费用系数: float
    """
    单位: 万元/kW
    """

    建设费用基数: float
    """
    单位: 万元
    """

    最大安装台数: float
    """
    单位: 台
    """

    最小安装台数: float
    """
    单位: 台
    """


class 变流器ID(BaseModel):
    电输出: int
    """
    类型: 电母线输出
    """
    电输入: int
    """
    类型: 变流器输入
    """


class 变流器数据(BaseModel):  # 配电传输
    生产厂商: str

    设备型号: str

    额定功率: float
    """
    单位: kW
    """

    效率: float
    """
    单位: percent
    """

    采购成本: float
    """
    单位: 万元/kW
    """

    固定维护成本: float
    """
    单位: 万元/(kW*年)
    """

    可变维护成本: float
    """
    单位: 元/kWh
    """

    设计寿命: float
    """
    单位: 年
    """

    建设费用系数: float
    """
    单位: 万元/kW
    """

    建设费用基数: float
    """
    单位: 万元
    """

    最大安装台数: float
    """
    单位: 台
    """

    最小安装台数: float
    """
    单位: 台
    """


class 双向变流器ID(BaseModel):
    储能端: int
    """
    类型: 双向变流器储能端输入输出
    """
    线路端: int
    """
    类型: 双向变流器线路端输入输出
    """


class 双向变流器数据(BaseModel):  # 配电传输
    生产厂商: str

    设备型号: str

    额定功率: float
    """
    单位: kW
    """

    效率: float
    """
    单位: percent
    """

    采购成本: float
    """
    单位: 万元/kW
    """

    固定维护成本: float
    """
    单位: 万元/(kW*年)
    """

    可变维护成本: float
    """
    单位: 元/kWh
    """

    设计寿命: float
    """
    单位: 年
    """

    建设费用系数: float
    """
    单位: 万元/kW
    """

    建设费用基数: float
    """
    单位: 万元
    """

    最大安装台数: float
    """
    单位: 台
    """

    最小安装台数: float
    """
    单位: 台
    """


class 传输线ID(BaseModel):
    电输入: int
    """
    类型: 电母线输入
    """
    电输出: int
    """
    类型: 电母线输出
    """


class 传输线数据(BaseModel):  # 配电传输
    生产厂商: str

    设备型号: str

    能量衰减系数: float
    """
    单位: kW/km
    """

    采购成本: float
    """
    单位: 万元/km
    """

    维护成本: float
    """
    单位: 万元/(km*年)
    """

    设计寿命: float
    """
    单位: 年
    """

    建设费用系数: float
    """
    单位: 万元/km
    """

    建设费用基数: float
    """
    单位: 万元
    """

    长度: float
    """
    单位: km
    """
