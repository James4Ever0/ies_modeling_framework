# ref: https://zhuanlan.zhihu.com/p/403532735
# 导入库
from docplex.mp.model import Model
from docplex.mp.model_reader import ModelReader

# import signal
# just raise signal.SIGINT in another thread. requires higher python version.
# from collections import defaultdict
# import os
# import sys
# sys_platform = sys.platform

# # no process called "cplex"
# if sys_platform == 'win32':
#     import wmi
#     import pythoncom

#     def kill_cplex():
#         for p in wmi.WMI().Win32_Process(Name="cplex.exe"):
#             print('killing process:', p)
#             p.Terminate(Result=1)
# elif sys_platform in ['darwin', 'linux']:
#     def kill_cplex():
#         os.system("pkill cplex")
# else:
#     raise Exception("unsupported platform: %s" % sys_platform)
# # just kill cplex when possible

import threading
import time
import cplex


def kill_cplex_after_duration(duration: int):
    def run():
        # pythoncom.CoInitialize()
        print(f"will kill cplex after {duration} secs.")
        time.sleep(duration)
        print("calling kill_cplex")
        # cplex._internal._procedual.refineconflictext
        # which uses "cplex._internal._procedual.SigIntHandler"
        # "cplex._internal._pycplex.CPXXrefineconflictext" is taking forever.
        # consider override that.
        # only works on higher python versions.
        # signal.raise_signal(signal.SIGINT)
        # kill_cplex()
        pycplex = cplex._internal._pycplex
        # that's what you called "intervention"
        getattr(pycplex, "set_py_terminator", getattr(pycplex, "setpyterminate"))()
        print("exit kill_cplex")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()


import traceback

MAXTIME = 5
# must install compatible "cplex" python package on selevted versions.
# turns out that we need to install other python versions (<3.7, >3.4) which supported by cplex 12.8

# install cplex (), docplex, pandas

api = "cplex"
# api = "docplex"

error = "infeasible"
# error = "unbounded"
# no hint for unbounded variables?

# cplex没有提供直接读取string的接口，不得不进行个文件暂存操作
# temp_input_file_name = "no_bound.lp"
# temp_input_file_name = "temp.lp" # later we will give it our unbounded model
temp_input_file_name = "exported.mps" # feasible?
# temp_input_file_name = "E:\\works\\jubilant-adventure2\\microgrid_base\\logs\\pyomo_2023_08_08_17_15_44_141633+08_00\\model.lp"
mdl: Model = ModelReader.read(temp_input_file_name, model_name="InfeasibelLP")
print("model loaded successfully from: %s" % temp_input_file_name)

import sys
mdl.cplex.set_error_stream(sys.stderr)
mdl.cplex.set_log_stream(sys.stderr)
mdl.cplex.set_results_stream(sys.stderr)
mdl.cplex.set_warning_stream(sys.stderr)
# 清除临时文件
# if os.path.exists(temp_input_file_name):
#     os.remove(temp_input_file_name)
from docplex.mp.conflict_refiner import ConflictRefiner, ConflictRefinerResult

# import cplex
# as long as 'cplex' executable is in PATH we are good.
# from func_timeout import func_timeout


# import pdb
def check_conflict(model) -> bool:
    has_conflict = False
    output_table = None
    try:
        refiner = ConflictRefiner()  # 先实例化ConflictRefiner类
        kill_cplex_after_duration(MAXTIME)
        # pdb.set_trace() # for py3.6
        res: ConflictRefinerResult = refiner.refine_conflict(model)
        # res: ConflictRefinerResult = func_timeout(
        #     MAXTIME,
        #     refiner.refine_conflict,
        #     args=(model,),
        #     kwargs=dict(log_output=True),
        # )  # 将模型导入该类,调用方法
        # not (self) writable.
        # sys.stdin.write("\n")

        number_of_conflicts = res.number_of_conflicts
        print("conflict count:", number_of_conflicts)  # taking too long.
        has_conflict = number_of_conflicts != 0
        if has_conflict:
            # print(dir(res))
            # breakpoint()
            output_table = res.as_output_table()
            # res.display()  # 显示冲突约束
        del res
        del refiner
    except:
        traceback.print_exc()
        print("conflict check failed")
        has_conflict = True
        output_table = None
    return has_conflict, output_table


if error == "infeasible":
    if api == "cplex":
        # 获取cplex.Cplex()类对象
        c = mdl.cplex
        # 进行冲突检测
        # print(dir(c.conflict))
        # breakpoint()
        all_constraints = c.conflict.all_constraints()
        kill_cplex_after_duration(MAXTIME)
        c.conflict.refine(
            all_constraints,
        )
        # func_timeout(MAXTIME, c.conflict.refine, args=(all_constraints,))
        # 输出检测信息，再重新读入并在控制台中输出
        # 需要吐槽的是Cplex并不支持以IOSteam为对象输入输出，因此不得不反复建立临时文件
        output_fname = "conflict.txt"
        c.conflict.write(output_fname)
        print("conflict written to:", output_fname)
        # with open(output_fname, "r") as f:
        #     print(f.read())
    elif api == "docplex":
        has_conflict, output_table = check_conflict(mdl)
        if output_table is not None:
            output_table.to_csv("output_table.csv")
    else:
        raise Exception("unknown api for model error '%s': %s" % (error, api))
# elif error == "unbounded":
#     if api == "cplex":
#         c = mdl.cplex
#         # print(dir(c))
#         # sol = mdl.solve(
#         # log_output=True
#         # )  # output some solution.
#         # breakpoint()
#         # c.solve()
#         # c.presolve()
#         # print(dir(sol))
#         # raty =c.DualFarkas()
#         # # ray = c.solution.advanced.get_ray() # no solution exists!
#         # print("RAY?", ray)
#     else:
#         raise Exception("unknown api for error '%s': %s" % (error, api))
else:
    raise Exception("unknown error: %s" % error)
