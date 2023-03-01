from typing import List
from docplex.mp.model import Model
from integratedEnergySystemPrototypes import IntegratedEnergySystem



from docplex.mp.conflict_refiner import ConflictRefiner


def check_conflict(model:Model):
    refiner = ConflictRefiner()  # 先实例化ConflictRefiner类
    res = refiner.refine_conflict(model)  # 将模型导入该类,调用方法
    res.display()  # 显示冲突约束

def solve_and_log(
    systems: List[IntegratedEnergySystem], model: Model, simulation_name: str
):
    systems_annualized = [system.annualized for system in systems]

    import functools

    objective = functools.reduce(lambda a, b: a + b, systems_annualized)

    model.minimize(objective)

    # 1000秒以内解出 否则放弃
    model.set_time_limit(time_limit=1000)

    from typing import Union
    from docplex.mp.solution import SolveSolution

    # 模型求解返回值 可为空
    solution_run1: Union[None, SolveSolution] = model.solve(
        log_output=True
    )  # output some solution.

    from data_visualize_utils import (
        printDecisionVariablesFromSolution,
        printIntegratedEnergySystemDeviceCounts,
        plotSingle,
    )

    if solution_run1 == None:
        print("UNABLE TO SOLVE")
    else:
        printDecisionVariablesFromSolution(model)
        printIntegratedEnergySystemDeviceCounts(systems)

        # collect all types of lists.

        for system in systems:
            system_name = system.device_name
            system_data_name_list = dir(system)
            for system_data_name in system_data_name_list:
                system_data = system.__dict__.get(system_data_name, None)
                if type(system_data) == list:
                    # then we plot this!
                    plotSingle(
                        system_data,
                        title_content=f"{system_name}_{system_data_name}",
                        save_directory=f"{simulation_name}_figures",
                    )
        print("TOTAL ANNUAL:", objective.solution_value)
        # breakpoint()
        # 1007399999.999996 if charge[0] == discharge[0] == 0
        # 992227727.2532595 if no init constrains on charge/discharge
