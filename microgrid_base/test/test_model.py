from common_fixtures import *

from typing import cast

try:
    from typing import Protocol
except:
    from typing_extensions import Protocol
from pyomo.environ import *

# may you hook arith methods to check expression (poly degree) on the way.

# render constraints as latex. use sigma notation.
EPS = 0.02


def check_solver_result(s_results):
    assert s_results, "no solver result."
    TC = s_results.solver.termination_condition
    SS = s_results.solver.status
    normalSSs = [SolverStatus.ok, SolverStatus.warning]
    normalTCs = [
        TerminationCondition.globallyOptimal,
        TerminationCondition.locallyOptimal,
        TerminationCondition.feasible,
        TerminationCondition.optimal,
        # TerminationCondition.maxTimeLimit,
    ]
    error_msg = []
    if TC not in normalTCs:
        error_msg.append(f"abnormal termination condition: {TC}")
    if SS not in normalSSs:
        error_msg.append(f"abnormal solver status: {TC}")
    if error_msg:
        raise Exception("\n".join(error_msg))


def test_convertMonthToDays():
    assert convertMonthToDays(1) == sum(month_days[:1])
    assert convertMonthToDays(2) == sum(month_days[:2])
    assert convertMonthToDays(11) == sum(month_days[:11])


import pytest


# BUG: BigM <= 1e+8
@pytest.mark.parametrize("v0_is_constant", [False, True])
@pytest.mark.parametrize(
    "v0_within, min_v0, max_v0, sense, result",
    [
        (Reals, -1, 10, minimize, -1),
        (Reals, -1, 10, maximize, 10),
        (NonNegativeReals, 1, 10, minimize, 0),
        (NonNegativeReals, 1, 10, maximize, 10),
    ],
)
@pytest.mark.parametrize("v1_init", [0, 1])
@pytest.mark.parametrize("v0_init", [3])
@pytest.mark.parametrize(
    "v1_within", [Boolean, pytest.param(NonNegativeReals, marks=pytest.mark.xfail)]
)
def test_BinVarMultiplySingle(
    model_wrapper: ModelWrapper,
    测试设备模型: 设备模型,
    v0_is_constant,
    v0_within,
    min_v0,
    max_v0,
    sense,
    result,
    v1_init,
    v0_init,
    v1_within,
):
    assert min_v0 <= max_v0
    if v0_is_constant:
        v0 = v0_init
    else:
        v0 = 测试设备模型.单变量(
            "v0", within=v0_within, initialize=v0_init, bounds=(min_v0, max_v0)
        )
    v1 = 测试设备模型.单变量("v1", within=v1_within, initialize=v1_init)
    v_result = 测试设备模型.BinVarMultiplySingle(v1, v0)
    model_wrapper.Objective(expr=v_result, sense=sense)
    with SolverFactory(Solver.cplex) as solver:  # type: ignore
        print(">>>SOLVING<<<")
        solver.options["timelimit"] = 5
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        check_solver_result(s_results)

        print(f"v0: {value(v0)}")
        print(f"v1: {value(v1)}")
        print(f"PROD: {value(v_result)}")
        print(f"EXPECTED: {result}")
        print(f"ACTUAL: {value(v0)*value(v1)}")
        if v0_is_constant:
            if sense == minimize:
                result = min(0, v0_init)
            elif sense == maximize:
                result = max(0, v0_init)
            else:
                assert False, f"Wrong sense: {sense}"
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
    with SolverFactory(Solver.cplex) as solver:  # type: ignore
        print(">>>SOLVING<<<")
        solver.options["timelimit"] = 5
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        check_solver_result(s_results)

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
    model_wrapper.Objective(expr=v0, sense=sense)
    with SolverFactory(Solver.cplex) as solver:  # type: ignore
        print(">>>SOLVING<<<")
        solver.options["timelimit"] = 5
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        check_solver_result(s_results)

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
    with SolverFactory(Solver.cplex) as solver:  # type: ignore
        print(">>>SOLVING<<<")
        solver.options["timelimit"] = 5
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        check_solver_result(s_results)

        assert abs(value(obj_expr) - y_expected) <= EPS


# if use timeout as solver option, usually not so good.
# you will not get accurate results.


@pytest.mark.parametrize("diesel_rate, fee_rate_per_hour", [(1, 2), (3, 6)])
@pytest.mark.parametrize("sense", [minimize, maximize])
def test_柴油(
    model_wrapper: ModelWrapper, 测试柴油模型: 柴油模型, diesel_rate, fee_rate_per_hour, sense
):
    测试柴油模型.constraints_register()
    测试柴油模型.RangeConstraintMulti(
        测试柴油模型.燃料接口, expression=lambda x: x == diesel_rate
    )  # unit: m^3
    obj_expr = 测试柴油模型.燃料接口[0]
    model_wrapper.Objective(expr=obj_expr, sense=sense)
    with SolverFactory(Solver.cplex) as solver:  # type: ignore
        print(">>>SOLVING<<<")
        solver.options["timelimit"] = 5
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        check_solver_result(s_results)

        val_fee = value(测试柴油模型.总成本年化 / 1000) / 8760
        assert abs(val_fee - fee_rate_per_hour) < EPS


@pytest.mark.timeout(30)  # pip3 install pytest-timeout
@pytest.mark.parametrize(
    "power_output, expected_val, expected_diesel, adcr_expected",
    [
        (10, 10, -(3 * 2 + 1 * 3) / 5 * 0.001 * 10, (3 * 2 + 1 * 3) / 5 * 0.001),
        (20, 20, -(3 * 2 + 1 * 3) / 5 * 0.001 * 20, (3 * 2 + 1 * 3) / 5 * 0.001),
    ],
)
def test_柴油发电(
    model_wrapper: ModelWrapper,
    测试柴油发电模型: 柴油发电模型,
    power_output,
    expected_val,
    expected_diesel,
    adcr_expected,
):
    测试柴油发电模型.燃料热值 = 1
    测试柴油发电模型.constraints_register()
    测试柴油发电模型.RangeConstraintMulti(测试柴油发电模型.电输出, expression=lambda x: x == power_output)
    assert (测试柴油发电模型.averageDieselConsumptionRate - adcr_expected) < EPS
    assert 测试柴油发电模型.averageLoadRate == 0.8
    obj_expr = 测试柴油发电模型.总成本年化
    print("年化:", obj_expr)
    model_wrapper.Objective(expr=obj_expr, sense=minimize)
    with SolverFactory(Solver.cplex) as solver:  # type: ignore
        print(">>>SOLVING<<<")
        solver.options["timelimit"] = 5
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        check_solver_result(s_results)

        print("ELECTRICITY:", value(测试柴油发电模型.电输出[0]), expected_val)
        print("DIESEL:", value(测试柴油发电模型.柴油输入[0]), expected_diesel)
        assert abs(value(测试柴油发电模型.电输出[0]) - expected_val) <= EPS
        assert abs(value(测试柴油发电模型.柴油输入[0]) - expected_diesel) <= 0.0015
        # breakpoint()


def test_电价模型():
    mydata = dict(PriceList=[1] * 12)
    myInfo = 电负荷信息.parse_obj(
        dict(
            设备名称="Any",
            EnergyConsumption=[1, 2, 3],
            MaxEnergyConsumption=4,
            PriceModel=mydata,
        )
    )
    myPriceModel = 分月电价.parse_obj(mydata)
    print(myInfo)
    # breakpoint()
    assert myPriceModel == myInfo.PriceModel


@pytest.mark.parametrize(
    "day_index, expected_month",
    [
        (1, 0),
        pytest.param(365, 11, marks=pytest.mark.xfail),
        (364, 11),
        (363, 11),
        (333, 10),
    ],
)
def test_DayToMonth(day_index, expected_month):
    month_index = convertDaysToMonth(day_index)
    assert month_index == expected_month


@pytest.mark.parametrize(
    "hour_index, expected_price, power",
    [
        (2, 4 * 0.0001 * 1, 4),
        (24 * 40, 4 * 0.0001 * 2, 4),
        (24 * 30 * 2 + 10, 4 * 0.0001 * 3, 4),
        pytest.param(8760, 4 * 0.0001 * 12, 4, marks=pytest.mark.xfail),
        (8779, 4 * 0.0001 * 12, 4),
    ],
)
def test_分月电价(hour_index, expected_price, power):
    myPriceModel = 分月电价(PriceList=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
    mprice = myPriceModel.getFee(power, time_in_day=hour_index)
    assert abs(mprice - expected_price) == 0


@pytest.mark.parametrize("illumination, output", [(1, 9.8), (0.5, 4.9), (2, 9.8)])
def test_光伏发电(model_wrapper: ModelWrapper, 测试光伏发电模型: 光伏发电模型, illumination, output):
    illumination_array = [illumination] * 24

    测试光伏发电模型.计算参数.光照 = illumination_array
    测试光伏发电模型.constraints_register()
    model_wrapper.Objective(expr=测试光伏发电模型.电接口[0] + 测试光伏发电模型.电接口[2], sense=maximize)
    with SolverFactory(Solver.cplex) as solver:  # type: ignore
        print(">>>SOLVING<<<")
        solver.options["timelimit"] = 5
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        check_solver_result(s_results)

        devCount = value(测试光伏发电模型.DeviceCount)
        assert abs(value(测试光伏发电模型.电接口[0]) - output * devCount) < EPS
        assert abs(value(测试光伏发电模型.电接口[2]) - output * devCount) < EPS


@pytest.mark.parametrize(
    "windspeed, output",
    [
        (5, 0),
        (10, 0),
        (20, 100 * ((10 / 90) ** 3)),
        (50, 100 * (((50 - 10) / 90) ** 3)),
        (100, 100),
        (150, 100),
        (200, 100),
        (210, 0),
    ],
)
def test_风力发电(model_wrapper: ModelWrapper, 测试风力发电模型: 风力发电模型, windspeed, output):
    windspeed_array = [windspeed] * 24
    # override the windspeed.
    测试风力发电模型.计算参数.风速 = windspeed_array
    测试风力发电模型.constraints_register()
    model_wrapper.Objective(expr=测试风力发电模型.电接口[0] + 测试风力发电模型.电接口[2], sense=maximize)
    with SolverFactory(Solver.cplex) as solver:  # type: ignore
        print(">>>SOLVING<<<")
        solver.options["timelimit"] = 5
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        check_solver_result(s_results)

        devCount = 测试风力发电模型.设备信息.DeviceCount
        assert abs(value(测试风力发电模型.DeviceCount) - devCount) < EPS
        if 测试风力发电模型.设备信息.machineType == "标幺值":
            output = 测试风力发电模型.设备信息.RatedPower * 0.5
        assert abs(value(测试风力发电模型.单台发电功率[0]) - output) < EPS
        assert abs(value(测试风力发电模型.单台发电功率[2]) - output) < EPS
        assert abs(value(测试风力发电模型.电接口[0]) - output * devCount) < EPS
        assert abs(value(测试风力发电模型.电接口[2]) - output * devCount) < EPS


@pytest.mark.parametrize("_input, output", [(100, 98), (200, 196)])
@pytest.mark.parametrize("direction", [False, True])
@pytest.mark.parametrize("sense", [minimize, maximize])
def test_双向变流器(
    model_wrapper: ModelWrapper, 测试双向变流器模型: 双向变流器模型, _input, output, direction, sense
):
    测试双向变流器模型.constraints_register()
    if direction:
        测试双向变流器模型.RangeConstraintMulti(测试双向变流器模型.储能端, expression=lambda x: x == -_input)
    else:
        测试双向变流器模型.RangeConstraintMulti(测试双向变流器模型.线路端, expression=lambda x: x == -_input)
    model_wrapper.Objective(expr=测试双向变流器模型.总成本年化, sense=sense)
    with SolverFactory(Solver.cplex) as solver:  # type: ignore
        print(">>>SOLVING<<<")
        solver.options["timelimit"] = 5
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        check_solver_result(s_results)

        if direction:
            assert abs(value(测试双向变流器模型.线路端[0]) - output) < EPS
            assert abs(value(测试双向变流器模型.线路端[2]) - output) < EPS
        else:
            assert abs(value(测试双向变流器模型.储能端[0]) - output) < EPS
            assert abs(value(测试双向变流器模型.储能端[2]) - output) < EPS


@pytest.mark.parametrize(
    "_input, output",
    [(100, 100 - 1.377), (200, 200 - 1.377), (1, 0), (1.377, 0), (1.378, 0.001)],
)
@pytest.mark.parametrize("sense", [minimize, maximize])
def test_传输线(model_wrapper: ModelWrapper, 测试传输线模型: 传输线模型, _input, output, sense):
    测试传输线模型.constraints_register()
    测试传输线模型.RangeConstraintMulti(测试传输线模型.电输入, expression=lambda x: x == -_input)
    model_wrapper.Objective(expr=测试传输线模型.SumRange(测试传输线模型.电输出), sense=sense)
    with SolverFactory(Solver.cplex) as solver:  # type: ignore
        print(">>>SOLVING<<<")
        solver.options["timelimit"] = 5
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        check_solver_result(s_results)

        assert abs(value(测试传输线模型.电输出[0]) - output) < EPS
        assert abs(value(测试传输线模型.电输出[2]) - output) < EPS

        assert abs(-value(测试传输线模型.电输入[0]) - _input) < EPS
        assert abs(-value(测试传输线模型.电输入[2]) - _input) < EPS


from runtime_override_stepwise import iterate_till_keyword, overwrite_func


@pytest.mark.parametrize("device_count, total_decay_rate", [(500 / 20, 500 * 0.1)])
@pytest.mark.parametrize("sense", [minimize, maximize])
def test_锂电池(
    model_wrapper: ModelWrapper, 测试锂电池模型: 锂电池模型, device_count, total_decay_rate, sense
):
    测试锂电池模型.constraints_register()

    def verify_constraints(i):
        delta_capacity = value(
            测试锂电池模型.CurrentTotalCapacity[i] * (1 - 测试锂电池模型.sigma * 测试锂电池模型.计算参数.deltaT)
            - 测试锂电池模型.CurrentTotalCapacity[i + 1]
        )
        assert (
            abs(delta_capacity - value(测试锂电池模型.原电接口.x[i] * 测试锂电池模型.计算参数.deltaT)) < EPS
        )

    model_wrapper.Objective(expr=测试锂电池模型.总成本年化, sense=sense)
    with SolverFactory(Solver.cplex) as solver:  # type: ignore
        print(">>>SOLVING<<<")
        solver.options["timelimit"] = 5
        s_results = solver.solve(model_wrapper.model, tee=True)
        print("SOLVER RESULTS?")
        print(s_results)
        check_solver_result(s_results)

        assert abs(value(测试锂电池模型.DeviceCount)) == device_count

        init_capacity = (
            value(测试锂电池模型.DeviceCount) * 测试锂电池模型.InitSOC * 测试锂电池模型.RatedCapacity
        )

        assert abs(value(测试锂电池模型.CurrentTotalCapacity[0]) - init_capacity) < EPS
        for i in range(5):
            verify_constraints(i)

        if (
            last_capacity := value(
                测试锂电池模型.CurrentTotalCapacity[len(测试锂电池模型.计算参数.风速) - 1]
            )
            < 0
        ):
            assert abs(last_capacity) <= EPS
