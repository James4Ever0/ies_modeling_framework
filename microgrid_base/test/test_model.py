from pytest import fixture
import sys

sys.path.append("../")

from typing import cast

try:
    from typing import Protocol
except:
    from typing_extensions import Protocol
from ies_optim import ModelWrapper
from ies_optim import 计算参数
from pyomo.environ import *

# may you hook arith methods to check expression (poly degree) on the way.

# render constraints as latex. use sigma notation.


@fixture()
# @fixture(scope="session")
def model_wrapper():
    mw = ModelWrapper()
    yield mw
    # cleanup this!
    # del mw.model
    del mw
    # return mw


EPS = 0.03

# class mObject:
#     a = 1
#     b = 2
#     @staticmethod
#     def method():
#         return "method return value"

# @fixture()
# def teardown_fixture():
#     yield mObject()
#     print("TEARDOWN FIXTURE")

# # @fixture == @fixture()

# @fixture()
# def t2f(teardown_fixture):
#     print(teardown_fixture)
#     print("VAL A?", teardown_fixture.a)
#     print("VAL B?", teardown_fixture.b)
#     print("VAL METHOD?", teardown_fixture.method())
#     print("_____EXIT T2F_____")
#     yield teardown_fixture
#     # return teardown_fixture
#     print("TEARDOWN T2F")

# def test_teardown(t2f: mObject):
#     print(t2f)
#     print("VAL A?", t2f.a)
#     print("VAL B?", t2f.b)
#     print("VAL METHOD?", t2f.method())


from ies_optim import 柴油信息


@fixture(scope="session")
def 测试柴油信息():

    return 柴油信息(设备名称="柴油1", Price=(10, "元/L"), 热值=(10, "MJ/L"), CO2=(10, "kg/L"))


from ies_optim import 柴油发电信息


@fixture(scope="session")
def 测试柴油发电信息():

    return 柴油发电信息(
        生产厂商="柴油发电1",
        设备型号="柴油发电1",
        设备名称="柴油发电1",
        RatedPower=20,
        PowerDeltaLimit=1,
        PowerStartupLimit=1,
        CostPerMachine=100,
        CostPerYearPerMachine=100,
        VariationalCostPerWork=100,
        Life=20,
        BuildCostPerMachine=10,
        BuildBaseCost=10,
        DieselToPower_Load=[[2, 10], [3, 50], [1, 100]],
        DeviceCount=1,
        MaxDeviceCount=2,
        MinDeviceCount=1,
    )


from ies_optim import 柴油发电模型, 柴油发电ID


@fixture()
def 测试柴油发电ID():
    devID = 柴油发电ID(ID=0, 燃料接口=1, 电接口=2)
    return devID


@fixture()
def 测试柴油发电模型(
    测试柴油发电信息: 柴油发电信息, model_wrapper: ModelWrapper, 测试计算参数: 计算参数, 测试柴油发电ID: 柴油发电ID
):
    mDieselEngineModel = 柴油发电模型(
        PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, 设备ID=测试柴油发电ID, 设备信息=测试柴油发电信息
    )
    return mDieselEngineModel


@fixture(scope="session")
def 测试计算参数():
    import numpy as np

    a = abs(np.random.random((24,))).tolist()
    # a = abs(np.random.random((8760,))).tolist()

    return 计算参数(
        计算目标="经济",
        # 计算目标="经济_环保",
        # 计算目标="环保",
        计算步长="小时",
        典型日=True,
        典型日代表的日期=[1],
        # 典型日=False,
        计算类型="仿真模拟",
        # 计算类型="设计规划",
        风速=a,
        光照=a,
        气温=a,
        年利率=0.1,
    )


# def test_init():
#     print("hello test")


def test_convertMonthToDays():
    from ies_optim import convertMonthToDays, month_days

    assert convertMonthToDays(1) == sum(month_days[:1])
    assert convertMonthToDays(2) == sum(month_days[:2])
    assert convertMonthToDays(11) == sum(month_days[:11])


from ies_optim import 设备模型


@fixture
def 测试设备模型(model_wrapper: ModelWrapper, 测试计算参数: 计算参数):
    mDeviceModel = 设备模型(PD={}, mw=model_wrapper, 计算参数实例=测试计算参数, ID=1)
    yield mDeviceModel


# from collections import namedtuple
import pytest

# BUG: BigM <= 1e+8
@pytest.mark.parametrize(
    "v0_within, v0_init, v1_within, v1_init, result, min_v0, max_v0, sense",
    [
        (Reals, 3, Boolean, 0, 10, -1, 10, maximize),
        (Reals, 3, Boolean, 0, -1, -1, 10, minimize),
        (Reals, 3, Boolean, 1, 10, -1, 10, maximize),
        (Reals, 3, Boolean, 1, -1, -1, 10, minimize),  # error: assert 10 <= 0.01
        (NonNegativeReals, 3, Boolean, 0, 10, 1, 10, maximize),
        (NonNegativeReals, 3, Boolean, 0, 0, 1, 10, minimize),
        (NonNegativeReals, 3, Boolean, 1, 10, 1, 10, maximize),
        (NonNegativeReals, 3, Boolean, 1, 0, 1, 10, minimize),
        pytest.param(
            NonNegativeReals,
            3,
            NonNegativeReals,
            0,
            -1,
            -1,
            10,
            maximize,
            marks=pytest.mark.xfail,
        ),
    ],
)
def test_BinVarMultiplySingle(
    model_wrapper: ModelWrapper,
    # 测试计算参数: 计算参数,
    测试设备模型: 设备模型,
    v0_within,
    v0_init,
    v1_within,
    v1_init,
    result,
    max_v0,
    min_v0,
    sense,
):
    assert min_v0 <= max_v0
    v0 = 测试设备模型.单变量("v0", within=v0_within, initialize=v0_init, bounds=(min_v0, max_v0))

    v1 = 测试设备模型.单变量("v1", within=v1_within, initialize=v1_init)
    v_result = 测试设备模型.BinVarMultiplySingle(v1, v0)
    # obj_expr = v1
    obj_expr = v_result
    # if sense == maximize:
    #     obj_expr = -obj_expr
    # OBJ = model_wrapper.Objective(expr=obj_expr, sense=minimize)
    OBJ = model_wrapper.Objective(expr=obj_expr, sense=sense)

    with SolverFactory("cplex") as solver:
        print(">>>SOLVING<<<")
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        print(f"v0: {value(v0)}")
        print(f"v1: {value(v1)}")
        print(f"PROD: {value(v_result)}")
        print(f"EXPECTED: {result}")
        print(f"ACTUAL: {value(v0)*value(v1)}")
        assert abs(value(v_result) - result) <= EPS


@pytest.mark.parametrize(
    "v0_min, v0_max, v1_min, v1_max, sense, expected, param",
    [
        (1, 5, 2, 4, minimize, 2, 0),
        (1, 5, 2, 4, maximize, 20, 0),
        (-1, 3, -2, 4, minimize, -10, -2),
        (-1, 3, -2, 4, maximize, 8, -2),
    ],
)
def test_VarMultiplySingle(
    model_wrapper: ModelWrapper,
    测试设备模型: 设备模型,
    v0_min,
    v0_max,
    v1_min,
    v1_max,
    sense,
    expected,
    param,
):
    v0 = 测试设备模型.变量列表("v0", bounds=(v0_min, v0_max))
    v0_dict = dict(var=v0, max=v0_max, min=v0_min)

    v1 = 测试设备模型.变量列表("v1", bounds=(v1_min, v1_max))
    v1_dict = dict(var=v1, max=v1_max, min=v1_min)

    v0_v1 = 测试设备模型.Multiply(v0_dict, v1_dict, "v0_v1")
    obj_expr = v0_v1[0] + param * (v0[0] + v1[0])
    model_wrapper.Objective(expr=obj_expr, sense=sense)

    with SolverFactory("cplex") as solver:
        print(">>>SOLVING<<<")
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        assert abs(value(obj_expr) - expected) <= EPS


@pytest.mark.parametrize(
    "v0_min, v0_max, sense, expected_v0, expected_v1_b_pos, expected_v1_x_pos, expected_v1_b_neg, expected_v1_x_neg, expected_v1_x_abs",
    [
        (-1, 5, maximize, 5, 1, 5, 0, 0, 5),
        (-1, 5, minimize, -1, 0, 0, 1, 1, 1),
        (-2, 5, minimize, -2, 0, 0, 1, 2, 2),
    ],
)
def test_单表达式生成指示变量(
    model_wrapper: ModelWrapper,
    测试设备模型: 设备模型,
    v0_min,
    v0_max,
    sense,
    expected_v0,
    expected_v1_b_pos,
    expected_v1_x_pos,
    expected_v1_b_neg,
    expected_v1_x_neg,
    expected_v1_x_abs,
):
    v0 = 测试设备模型.单变量("v0", bounds=(v0_min, v0_max))
    v1 = 测试设备模型.单表达式生成指示变量("v1", v0)
    # v1 = 测试设备模型.单表达式生成指示变量("v1", v0+0)
    obj_expr = v0
    model_wrapper.Objective(expr=obj_expr, sense=sense)

    with SolverFactory("cplex") as solver:
        print(">>>SOLVING<<<")
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        assert abs(expected_v0 - value(v0)) <= EPS
        assert abs(expected_v1_b_pos - value(v1.b_pos)) <= EPS
        assert abs(expected_v1_x_neg - value(v1.x_neg)) <= EPS
        assert abs(expected_v1_b_neg - value(v1.b_neg)) <= EPS
        assert abs(expected_v1_x_pos - value(v1.x_pos)) <= EPS
        assert abs(expected_v1_x_abs - value(v1.x_abs)) <= EPS


import numpy as np


@pytest.mark.parametrize(
    "x_init, y_expected, sense",
    [
        (0, 2, minimize),
        (0, 2, maximize),
        (0.3, 2.3, minimize),
        (0.3, 2.3, maximize),
        (0 - 1, 2, minimize),  # BUG: y = 0 if x is out of bound
        (0 - 1, 2, maximize),
        (0 + 3, 4, minimize),
        (0 + 3, 4, maximize),
    ],
)
def test_Piecewise(
    model_wrapper: ModelWrapper, 测试设备模型: 设备模型, x_init, y_expected, sense
):
    x = [测试设备模型.单变量("x", initialize=x_init, bounds=(x_init, x_init))]
    y = [测试设备模型.单变量("y")]
    x_vals = np.linspace(0, 2, 2)
    y_vals = x_vals + 2
    测试设备模型.Piecewise(x, y, x_vals.tolist(), y_vals.tolist(), range_list=[0])
    obj_expr = y[0]
    model_wrapper.Objective(expr=obj_expr, sense=sense)

    with SolverFactory("cplex") as solver:
        print(">>>SOLVING<<<")
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        assert abs(value(obj_expr) - y_expected) <= EPS


@pytest.mark.parametrize("power_output, expected_val, expected_diesel", [(10, 10,...)])
def test_柴油发电(
    model_wrapper: ModelWrapper, 测试柴油发电模型: 柴油发电模型, power_output, expected_val, expected_diesel
):
    测试柴油发电模型.燃料热值 = 1
    测试柴油发电模型.constraints_register()
    测试柴油发电模型.RangeConstraintMulti(测试柴油发电模型.电输出, expression=lambda x: x == power_output)
    obj_expr = 测试柴油发电模型.总成本年化
    print("年化:", obj_expr)
    model_wrapper.Objective(obj_expr, sense=minimize)

    with SolverFactory("cplex") as solver:
        print(">>>SOLVING<<<")
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        assert abs(value(测试柴油发电模型.原电输出[0]) - expected_val) <= EPS


def test_柴油(model_wrapper: ModelWrapper):
    ...
