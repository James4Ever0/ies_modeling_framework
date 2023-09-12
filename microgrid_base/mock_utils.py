"""
This library mocks algorithm response.

Hash input parameters for random seeds, if configured.
"""

from config import ies_env

THRESHOLD = ies_env.MOCK_DATA_THRESHOLD


def decreaseByOneThousand(number, threshold=10):
    assert number >= 0, f"invalid number: {repr(number)}"
    if number <= threshold:
        return number
    ret = number / 10
    # logger_print(number, ret)
    return decreaseByOneThousand(ret, threshold=threshold)


import pandas


def modifyIfIsDeviceCount(location, val):
    if "deviceCount" in location:
        return random.randint(1, 10)
    return val


def modifyValueIfNumber(location, val):
    # bool is subclass of int
    # if isinstance(val, Union[float, int]):
    if type(val) in [float, int]:
        if not pandas.isnull(val):
            if val != 0:
                positive = val > 0
                val_abs = abs(val)
                val_abs_modified = decreaseByOneThousand(val_abs, threshold=THRESHOLD)
                val_modified = (1 if positive else -1) * val_abs_modified
                val_modified = reduceNumberPrecisionByDecimalPoints(val_modified)
                return val_modified
    return val


def reduceNumberPrecisionByDecimalPoints(num, precision=3):
    factor = 10**precision
    reduced_num = int(num * factor) / factor
    return reduced_num


from pydantic_factories import ModelFactory
from log_utils import logger_print
from fastapi_datamodel_template import (
    单次计算结果,
    CalculationResult,
    ObjectiveResult,
    规划结果详情_翻译,
    规划方案概览_翻译,
    设备出力曲线,
    仿真结果,
    出力曲线,
    曲线,
    mDict,
)

from ies_optim import EnergyFlowGraph
import random
from pydantic import BaseModel
from solve_model import targetTypeAsTargetName
from json_utils import jsonApply
import hashlib


class 规划方案概览_翻译_工厂(ModelFactory):
    __model__ = 规划方案概览_翻译


class 规划结果详情_翻译_工厂(ModelFactory):
    __model__ = 规划结果详情_翻译


class 仿真结果工厂(ModelFactory):
    __model__ = 仿真结果


def generate_fake_output_data(input_data: EnergyFlowGraph):
    (
        firstMDict,
        curve_elemsize,
        curve_x_unit,
        mDictCount,
        planType,
    ) = get_fake_output_data_params(input_data)

    with deterministic_rng_context(input_data):
        resultList = []

        for _ in range(mDictCount):
            obj_r = ObjectiveResult(
                financialObjective=random.uniform(10, 1000),
                environmentalObjective=random.uniform(10, 1000),
            )
            prt = []
            ps = 规划方案概览_翻译_工厂.build()
            ps.planType = planType
            pdl = []
            srt = []

            for elem in firstMDict.nodes:
                if getattr(elem, "type") == "设备":
                    prepare_fake_calc_result_per_device(
                        curve_elemsize, curve_x_unit, prt, pdl, srt, elem
                    )

                    result = 单次计算结果(
                        objectiveResult=obj_r,
                        planningResultTable=prt,
                        planningSummary=ps,
                        performanceDataList=pdl,
                        simulationResultTable=srt,
                    )
                    resultList.append(result)

        cr = CalculationResult(
            resultList=resultList,
            residualEquipmentAnnualFactor=random.uniform(0, 5),
            success=True,
            error_log="",
        )

        # finally, pass to the number manipulation routines.
        processed_cr = jsonApply(cr.dict(), modifyValueIfNumber, modifyIfIsDeviceCount)
        pcr_obj = CalculationResult.parse_obj(processed_cr)
        return pcr_obj


def prepare_fake_calc_result_per_device(
    curve_elemsize, curve_x_unit, prt, pdl, srt, elem
):
    subtype = getattr(elem, "subtype")
    param = getattr(elem, "param")
    设备名称, 生产厂商, 设备型号 = (
        getattr(param, "设备名称", "未知"),
        getattr(param, "生产厂商", "未知"),
        getattr(param, "设备型号", "未知"),
    )
    px = [f"{i}{curve_x_unit}" for i in range(curve_elemsize)]
    py = [random.uniform(-10, 10) for _ in range(curve_elemsize)]
    pcurve = 曲线(x=px, y=py)
    abbr = "功率"
    pl = [出力曲线(name=f"{subtype}{abbr}曲线", abbr=abbr, data=pcurve)]
    pr = 规划结果详情_翻译_工厂.build()
    pr.deviceName = 设备名称
    pr.deviceModel = 设备型号
    pd = 设备出力曲线(name=设备名称, plot_list=pl)
    sr = 仿真结果工厂.build()
    sr.name = 设备名称
    sr.type = 设备型号
    prt.append(pr)
    pdl.append(pd)
    srt.append(sr)


from contextlib import contextmanager
import os


def restore_randomness():
    trng_seed = lambda: os.urandom(ies_env.ANSWER_TO_THE_UNIVERSE)
    random.seed(trng_seed())
    规划方案概览_翻译_工厂.seed_random(trng_seed())
    规划结果详情_翻译_工厂.seed_random(trng_seed())
    仿真结果工厂.seed_random(trng_seed())


@contextmanager
def deterministic_rng_context(input_data: BaseModel):
    if ies_env.DETERMINISTIC_MOCK:
        input_hash = get_datamodel_hash(input_data)
        random.seed(input_hash)
        规划方案概览_翻译_工厂.seed_random(input_hash)
        规划结果详情_翻译_工厂.seed_random(input_hash)
        仿真结果工厂.seed_random(input_hash)
    try:
        yield
    finally:
        if ies_env.DETERMINISTIC_MOCK:
            restore_randomness()


def get_datamodel_hash(input_data: BaseModel):
    input_bytes = input_data.json().encode("utf-8")
    input_hash = hashlib.sha1(input_bytes).digest()
    return input_hash


def get_fake_output_data_params(input_data: EnergyFlowGraph):
    firstMDict: mDict = input_data.mDictList[0]
    calcTarget = firstMDict.graph.计算目标
    calcStepSize = firstMDict.graph.计算步长

    curve_elemsize, curve_x_unit = get_fake_data_curve_params(calcStepSize)

    mDictCount = get_fake_data_mdict_count(calcTarget)

    planType = targetTypeAsTargetName(calcTarget)
    return firstMDict, curve_elemsize, curve_x_unit, mDictCount, planType


def get_fake_data_mdict_count(calcTarget):
    if calcTarget == "经济_环保":
        mDictCount = 9
    elif calcTarget in ["经济", "环保"]:
        mDictCount = 1
    else:
        raise Exception("Unknown calculation target: %s" % calcTarget)
    return mDictCount


def get_fake_data_curve_params(calcStepSize):
    if calcStepSize == "小时":
        curve_elemsize = 8760
        curve_x_unit = "时"
    elif calcStepSize == "秒":
        curve_elemsize = 7200
        curve_x_unit = "秒"
    else:
        raise Exception("Unknown calculation step size: %s" % calcStepSize)
    return curve_elemsize, curve_x_unit


def determinism_assertation(deterministic, hash1, hash2):
    expr = lambda a, b: a == b if deterministic else a != b
    error_msg = (
        f"Non-deterministic when configured as deterministic: {hash1} != {hash2}"
        if deterministic
        else f"Deterministic when configured as non-deterministic: {hash1} == {hash2}"
    )
    assert expr(hash1, hash2), error_msg
    logger_print(f"Passed {'' if deterministic else 'non-'}determinism check.")


if __name__ == "__main__":
    # test the util.
    def test_determinism(input_data: EnergyFlowGraph, deterministic: bool):
        ies_env.DETERMINISTIC_MOCK = deterministic

        fake_output_data1 = generate_fake_output_data(input_data)
        fake_output_data2 = generate_fake_output_data(input_data)

        hash1 = get_datamodel_hash(fake_output_data1)
        hash2 = get_datamodel_hash(fake_output_data2)

        determinism_assertation(deterministic, hash1, hash2)

    mock_input = "mock_data_energy_flow_graph.json"
    input_data = EnergyFlowGraph.parse_file(mock_input)

    for det in [True, False]:
        test_determinism(input_data, det)
