# test if failsafe mechanism is working.
import os

os.environ["FAILSAFE"] = "True"

from common_fixtures import *

# import pytest

if not os.path.exists(failsafe_logdir := "failsafe_solver_logs"):
    os.mkdir(failsafe_logdir)
failsafe_logdir = os.path.abspath(failsafe_logdir)

import json

# import pickle


import copy


def get_infeasible_mw():
    input_params = copy.deepcopy(infeasible_input)
    efg = EnergyFlowGraph.parse_obj(input_params)
    mDictList = efg.dict()["mDictList"]
    calcParamList = mDictListToCalcParamList(mDictList)
    firstParam_graphparam = calcParamList[0][2]

    典型日 = firstParam_graphparam["典型日"]
    计算步长 = firstParam_graphparam["计算步长"]
    计算类型 = firstParam_graphparam["计算类型"]
    calcTarget = 计算目标 = firstParam_graphparam["计算目标"]
    mw = ModelWrapper()
    ret = getCalcStruct(mw, calcParamList, 典型日, 计算步长, 计算类型)
    obj_expr = ret.calcTargetLUT[calcTarget]
    sense = minimize
    OBJ = mw.Objective(expr=obj_expr, sense=sense)
    return mw


infeasible_model_input_path = "sample_data/input_abnormal.json"
# infeasible_pickle = "sample_data/infeasible_abnormal.pickle"
# if os.path.exists(infeasible_pickle):
#     with open(infeasible_pickle, 'rb') as f:
#         infeasible_model= pickle.load(f)
# else:
with open(infeasible_model_input_path, "r") as f:
    infeasible_input = json.load(f)
infeasible_mw = get_infeasible_mw()
infeasible_mw.model.write("infeasible_model.lp")

# infeasible_model = infeasible_mw.model
# with open(infeasible_pickle, 'wb') as f:
#     pickle.dump(infeasible_model, f)

# @pytest.fixture
# def infeasible_modelwrapper():
#     return infeasible_mw
#     # mw = ModelWrapper()
#     # mw.model = infeasible_model
#     # # mw.model = infeasible_mw.model.clone() # taking eternal.
#     # return mw


# sometimes these will stuck
# but i think ipopt may always stuck.
params = [
    [feasopt_with_optimization,"feasopt_with_optimization"],
    [feasopt_only,"feasopt_only"],
    [ipopt_no_presolve, "ipopt_no_presolve"],
    [random_value_assignment, "random_value_assignment"],
]
# @pytest.mark.parametrize("failsafe_method, method_name",params)
# def test_failsafe_method(infeasible_modelwrapper,failsafe_method, method_name):
#     _test_failsafe_method(infeasible_modelwrapper, failsafe_method, method_name)


def _test_failsafe_method(infeasible_modelwrapper, failsafe_method, method_name):
    solved, logfile = failsafe_method(infeasible_modelwrapper, failsafe_logdir)
    # breakpoint()
    if not solved:
        print(f"failsafe method <{method_name}> has failed.")
    else:
        print(f"failsafe method <{method_name}> has succeeded.")
    return solved, logfile


if __name__ == "__main__":
    report = []
    for failsafe_method, method_name in params:
        print("running:", method_name)
        r, l = _test_failsafe_method(infeasible_mw, failsafe_method, method_name)
        report.append((method_name, r, os.path.exists(l)))

    for n, r, l_exists in report:
        print(f"{n}:\t{r}\t(logfile exists? {l_exists})")
