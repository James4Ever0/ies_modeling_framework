from typing import List

from pyomo.environ import value
from pydantic import BaseModel, validator

from ies_optim import *
import statistics
from pyomo.core.base.var import IndexedVar


def sumVarList(varList: IndexedVar):
    return sum(varList.values())


def addListElem(*args):
    vals = []
    for elem_zip in zip(*args):
        vals.append(sum(elem_zip))
    return vals


def ReLU(val):
    if type(val) not in [int, float]:
        val = value(val)
    if val > 0:
        return val
    else:
        return 0


############
# 仿真结果 #
############


class 柴油仿真结果(BaseModel):
    元件名称: str

    ## UNIQ PARAMS ##
    柴油消耗费用: float
    """
    单位: 万元
    """

    @staticmethod
    def export(model: 柴油模型, timeParam: float):

        return 柴油仿真结果(
            元件名称=model.设备信息.设备名称,
            柴油消耗费用=((value(model.总成本年化)) * timeParam),
        )


class 电负荷仿真结果(BaseModel):
    元件名称: str

    ## UNIQ PARAMS ##
    电负荷: float
    """
    单位: kWh
    """

    @staticmethod
    def export(model: 电负荷模型, timeParam: float):

        return 电负荷仿真结果(
            元件名称=model.设备信息.设备名称,
            电负荷=((statistics.mean(model.设备信息.EnergyConsumption)) * timeParam),
        )


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

    ## UNIQ PARAMS ##
    产电量: float
    """
    单位: kWh
    """

    @staticmethod
    def export(model: 光伏发电模型, timeParam: float):

        return 光伏发电仿真结果(
            元件名称=model.设备信息.设备名称,
            设备型号=model.设备信息.设备型号,
            设备台数=value(model.DeviceCount),
            设备维护费用=((value(model.年化率 * model.总固定维护成本 + model.总可变维护成本年化)) * timeParam),
            产电量=((statistics.mean([value(e) for e in model.电接口.values()])) * timeParam),
        )


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

    ## UNIQ PARAMS ##
    产电量: float
    """
    单位: kWh
    """

    @staticmethod
    def export(model: 风力发电模型, timeParam: float):

        return 风力发电仿真结果(
            元件名称=model.设备信息.设备名称,
            设备型号=model.设备信息.设备型号,
            设备台数=value(model.DeviceCount),
            设备维护费用=((value(model.年化率 * model.总固定维护成本 + model.总可变维护成本年化)) * timeParam),
            产电量=((statistics.mean([value(e) for e in model.电接口.values()])) * timeParam),
        )


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

    ## UNIQ PARAMS ##
    产电量: float
    """
    单位: kWh
    """

    柴油消耗量: float
    """
    单位: L <- m3
    """

    @validator("柴油消耗量")
    def standard_unit_to_custom_柴油消耗量(cls, v):
        return v / 0.0010000000000000002

    平均效率_平均COP: float
    """
    单位: one
    """

    @staticmethod
    def export(model: 柴油发电模型, timeParam: float):

        return 柴油发电仿真结果(
            元件名称=model.设备信息.设备名称,
            设备型号=model.设备信息.设备型号,
            设备台数=value(model.DeviceCount),
            设备维护费用=((value(model.年化率 * model.总固定维护成本 + model.总可变维护成本年化)) * timeParam),
            产电量=((statistics.mean([value(e) for e in model.电接口.values()])) * timeParam),
            柴油消耗量=(
                (statistics.mean([value(e) for e in model.燃料接口.values()])) * timeParam
            ),
            平均效率_平均COP=(
                ((statistics.mean([value(e) for e in model.电接口.values()])) * timeParam)
            )
            / (
                model.燃料热值
                * (
                    (
                        (statistics.mean([value(e) for e in model.燃料接口.values()]))
                        * timeParam
                    )
                )
                + 1e-10
            ),
        )


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

    ## UNIQ PARAMS ##
    平均效率_平均COP: float
    """
    单位: one
    """

    @staticmethod
    def export(model: 锂电池模型, timeParam: float):

        return 锂电池仿真结果(
            元件名称=model.设备信息.设备名称,
            设备型号=model.设备信息.设备型号,
            设备台数=value(model.DeviceCount),
            设备维护费用=((value(model.年化率 * model.总固定维护成本 + model.总可变维护成本年化)) * timeParam),
            平均效率_平均COP=ReLU(
                (
                    ((statistics.mean([ReLU(e) for e in model.电接口])) * timeParam)
                    - (model.InitSOC * model.TotalCapacity)
                )
                / (
                    -(((statistics.mean([-ReLU(-e) for e in model.电接口])) * timeParam))
                    + 1e-10
                )
            ),
        )


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

    ## UNIQ PARAMS ##
    平均效率_平均COP: float
    """
    单位: one
    """

    @staticmethod
    def export(model: 变压器模型, timeParam: float):

        return 变压器仿真结果(
            元件名称=model.设备信息.设备名称,
            设备型号=model.设备信息.设备型号,
            设备台数=value(model.DeviceCount),
            设备维护费用=((value(model.年化率 * model.总固定维护成本 + model.总可变维护成本年化)) * timeParam),
            平均效率_平均COP=-(statistics.mean([value(e) for e in model.电输入.values()]))
            / (statistics.mean([value(e) for e in model.电输出.values()]) + 1e-10),
        )


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

    ## UNIQ PARAMS ##
    平均效率_平均COP: float
    """
    单位: one
    """

    @staticmethod
    def export(model: 变流器模型, timeParam: float):

        return 变流器仿真结果(
            元件名称=model.设备信息.设备名称,
            设备型号=model.设备信息.设备型号,
            设备台数=value(model.DeviceCount),
            设备维护费用=((value(model.年化率 * model.总固定维护成本 + model.总可变维护成本年化)) * timeParam),
            平均效率_平均COP=-(statistics.mean([value(e) for e in model.电输入.values()]))
            / (statistics.mean([value(e) for e in model.电输出.values()]) + 1e-10),
        )


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

    ## UNIQ PARAMS ##
    平均效率_平均COP: float
    """
    单位: one
    """

    @staticmethod
    def export(model: 双向变流器模型, timeParam: float):

        return 双向变流器仿真结果(
            元件名称=model.设备信息.设备名称,
            设备型号=model.设备信息.设备型号,
            设备台数=value(model.DeviceCount),
            设备维护费用=((value(model.年化率 * model.总固定维护成本 + model.总可变维护成本年化)) * timeParam),
            平均效率_平均COP=value(
                (
                    (sumVarList(model.储能端_.x_pos) / sumVarList(model.线路端_.x_neg))
                    * sumVarList(model.储能端_.b_pos)
                )
                + (
                    (sumVarList(model.线路端_.x_pos) / sumVarList(model.储能端_.x_neg))
                    * sumVarList(model.线路端_.b_pos)
                )
            )
            / model.计算参数.迭代步数,
        )


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

    ## UNIQ PARAMS ##
    平均效率_平均COP: float
    """
    单位: one
    """

    @staticmethod
    def export(model: 传输线模型, timeParam: float):

        return 传输线仿真结果(
            元件名称=model.设备信息.设备名称,
            设备型号=model.设备信息.设备型号,
            设备台数=value(model.DeviceCount),
            设备维护费用=((value(model.年化率 * model.总固定维护成本 + model.总可变维护成本年化)) * timeParam),
            平均效率_平均COP=-(statistics.mean([value(e) for e in model.电输入.values()]))
            / (statistics.mean([value(e) for e in model.电输出.values()]) + 1e-10),
        )


################
# 设备出力曲线 #
################


class 光伏发电出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    ## UNIQ PARAMS ##
    发电功率: List[float]
    """
    单位: kW
    """

    @staticmethod
    def export(model: 光伏发电模型, timeParam: float):

        return 光伏发电出力曲线(
            时间=list(range(model.计算参数.迭代步数)),
            元件名称=model.设备信息.设备名称,
            发电功率=[value(e) for e in model.电接口.values()],
        )


class 风力发电出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    ## UNIQ PARAMS ##
    发电功率: List[float]
    """
    单位: kW
    """

    @staticmethod
    def export(model: 风力发电模型, timeParam: float):

        return 风力发电出力曲线(
            时间=list(range(model.计算参数.迭代步数)),
            元件名称=model.设备信息.设备名称,
            发电功率=[value(e) for e in model.电接口.values()],
        )


class 柴油发电出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    ## UNIQ PARAMS ##
    发电功率: List[float]
    """
    单位: kW
    """

    @staticmethod
    def export(model: 柴油发电模型, timeParam: float):

        return 柴油发电出力曲线(
            时间=list(range(model.计算参数.迭代步数)),
            元件名称=model.设备信息.设备名称,
            发电功率=[value(e) for e in model.电接口.values()],
        )


class 锂电池出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    ## UNIQ PARAMS ##
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

    @staticmethod
    def export(model: 锂电池模型, timeParam: float):

        return 锂电池出力曲线(
            时间=list(range(model.计算参数.迭代步数)),
            元件名称=model.设备信息.设备名称,
            充电功率=[-ReLU(-e) for e in model.电接口],
            放电功率=[ReLU(e) for e in model.电接口],
            荷电容量=[
                value(e + model.MinTotalCapacity)
                for e in model.CurrentTotalActualCapacity.values()
            ],
            荷电状态=[
                value((e + model.MinTotalCapacity) / model.TotalCapacity)
                for e in model.CurrentTotalActualCapacity.values()
            ],
        )


class 变压器出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    ## UNIQ PARAMS ##
    转换功率: List[float]
    """
    单位: kW
    """

    @staticmethod
    def export(model: 变压器模型, timeParam: float):

        return 变压器出力曲线(
            时间=list(range(model.计算参数.迭代步数)),
            元件名称=model.设备信息.设备名称,
            转换功率=[value(e) for e in model.电输出.values()],
        )


class 变流器出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    ## UNIQ PARAMS ##
    转换功率: List[float]
    """
    单位: kW
    """

    @staticmethod
    def export(model: 变流器模型, timeParam: float):

        return 变流器出力曲线(
            时间=list(range(model.计算参数.迭代步数)),
            元件名称=model.设备信息.设备名称,
            转换功率=[value(e) for e in model.电输出.values()],
        )


class 双向变流器出力曲线(BaseModel):
    元件名称: str

    时间: List[int]
    """
    单位: one
    """

    ## UNIQ PARAMS ##
    转换功率: List[float]
    """
    单位: kW
    """

    @staticmethod
    def export(model: 双向变流器模型, timeParam: float):

        return 双向变流器出力曲线(
            时间=list(range(model.计算参数.迭代步数)),
            元件名称=model.设备信息.设备名称,
            转换功率=addListElem(
                [value(e) for e in model.储能端_.x_pos.values()],
                [value(e) for e in model.线路端_.x_pos.values()],
            ),
        )
