import sys

assert sys.version_info >= (3, 6) and sys.version_info < (3, 7),  f"Python version mismatch!\nExpected: >= 3.6, < 3.7\nActual: {sys.version.split()[0]}"

import argparse
# would you like not to modify print statements here?
# cause we might not have anything to do with logging in "docplex" environment
from docplex.mp.model import Model
from docplex.mp.model_reader import ModelReader
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
from docplex.mp.conflict_refiner import ConflictRefiner, ConflictRefinerResult
import traceback

            
def check_conflict(model, maxtime:float) -> bool:
    has_conflict = False
    output_table = None
    try:
        refiner = ConflictRefiner()  # 先实例化ConflictRefiner类
        kill_cplex_after_duration(maxtime)
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


def conflict_refiner(model_path: str, output: str, config: str, timeout: float):
    assert timeout > 0, f"invalid timeout: {timeout}"
    mdl: Model = ModelReader.read(model_path, model_name="InfeasibelLP")
    print("model loaded successfully from: %s" % model_path)
    if config == "docplex":
        _, output_table = check_conflict(mdl, timeout)
        if output_table is not None:
            output_table.to_csv(output)
        else:
            print('no conflict was found.')
    elif config == "cplex":
        # 获取cplex.Cplex()类对象
        c = mdl.cplex
        # 进行冲突检测
        # print(dir(c.conflict))
        # breakpoint()
        all_constraints = c.conflict.all_constraints()
        kill_cplex_after_duration(timeout)
        c.conflict.refine(
            all_constraints,
        )
        # func_timeout(MAXTIME, c.conflict.refine, args=(all_constraints,))
        # 输出检测信息，再重新读入并在控制台中输出
        # 需要吐槽的是Cplex并不支持以IOSteam为对象输入输出，因此不得不反复建立临时文件
        c.conflict.write(output)
        print("conflict written to:", output)
    else:
        raise Exception("unknown config: %s" % config)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-m", "--model_path", type=str, required=True, help="'.lp' model file path"
    )
    argparser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="conflict analysis output file path",
    )
    argparser.add_argument(
        "-c",
        "--config",
        type=str,
        required=True,
        help="conflict resolution method, can be one of ['cplex', 'docplex']",
    )
    argparser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=5,
        help="timeout in seconds, default is 5 seconds",
    )
    arguments = argparser.parse_args()
    conflict_refiner(
        arguments.model_path, arguments.output, arguments.config, arguments.timeout
    )
