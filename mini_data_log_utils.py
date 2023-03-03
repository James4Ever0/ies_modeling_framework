from typing import List
from docplex.mp.model import Model
from integratedEnergySystemPrototypes import IntegratedEnergySystem, check_conflict



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
        import os, shutil
        save_directory = f"{simulation_name}_figures"
        if os.path.isdir(save_directory):
            shutil.rmtree(save_directory)

        for system in systems:
            system_name = system.device_name
            system_data_name_list = dir(system)
            for system_data_name in system_data_name_list:
                system_data = system.__dict__.get(system_data_name, None)
                for port_direction in ['input','output']:
                    if system_data_name == f"power_of_{port_direction}s" and type(system_data) == dict:
                        for key,value in system_data.items():
                            if type(value) == list:
                                plotSingle(value,title_content=f"{system_name}_{system_data_name}_{key}",save_directory=save_directory)
                if type(system_data) == list:
                    # then we plot this!
                    plotSingle(
                        system_data,
                        title_content=f"{system_name}_{system_data_name}",
                        save_directory=save_directory,
                    )
        print("TOTAL ANNUAL:", objective.solution_value)
        # breakpoint()
        # 1007399999.999996 if charge[0] == discharge[0] == 0
        # 992227727.2532595 if no init constrains on charge/discharge


def check_solve_and_log(systems: List[IntegratedEnergySystem], model: Model, simulation_name: str):
    # before all the fuzz...
    has_conflict = check_conflict(model)  # no conflict?

    if has_conflict:
        print("MODEL HAS CONFLICT.")
        breakpoint()
    
    # non-convex quadratic constraint?
    # please show me!
    has_quad_cons = False
    print()
    print("#"*30)
    for quadratic_constraint in model.iter_quadratic_constraints():
        print("QUAD CONS?",quadratic_constraint)
        if not has_quad_cons:
            has_quad_cons=True
    print("#"*30)
    print()
    if has_quad_cons:
        raise Exception("You have quadratic constraints in model.")
    
    solve_and_log(systems,model,simulation_name)