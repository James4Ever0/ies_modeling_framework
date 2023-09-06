# virtually run interdependent tasks, generate the execution sequence

from pyomo.environ import *


def resolv_task_deps(task_tree: list[dict], solver_name: str = "cplex"):
    model = ConcreteModel()
    lateinit_constraints = []
    tasknames = set()
    depnames = set()
    for elem in task_tree:
        name = elem.get("name")
        deps = elem.get("deps", [])
        deps = set(deps)
        if name not in tasknames:
            tasknames.add(name)
        else:
            raise Exception(f"Redefinition of task <{name}> dependencies: {repr(deps)}")
        setattr(model, name, Var(domain=Integers))
        for dep in deps:
            depnames.add(dep)
            lateinit_constraints.append((name, dep))
    if not depnames.issubset(tasknames):
        raise Exception("Have unmet dependencies: %s" % depnames.difference(tasknames))
    for index, (name, dep) in enumerate(lateinit_constraints):
        setattr(
            model,
            f"constraint_{index}",
            Constraint(expr=getattr(model, name) <= getattr(model, dep) - 1),
        )

    model.obj = Objective(expr=0, sense=minimize)
    solver = SolverFactory(solver_name)
    ret = solver.solve(model, tee=True)
    normalTCs = [
        TerminationCondition.globallyOptimal,
        TerminationCondition.locallyOptimal,
        TerminationCondition.feasible,
        TerminationCondition.optimal,
    ]
    if (TC := ret.solver.termination_condition) not in normalTCs:
        raise Exception(
            "Dependency resolution failed.\nSolver termination condition: " + TC
        )
    else:
        priority_map = {}

        for tn in tasknames:
            task_priority = value(getattr(model, tn))
            priority_map[tn] = task_priority
            print(f"{tn}:\t{task_priority}")
        return priority_map


def get_task_seq(task_tree: list[dict], solver_name: str = "cplex"):
    pm = resolv_task_deps(task_tree, solver_name)
    if isinstance(pm, dict) and pm != {}:
        seq = list(pm.items())
        seq.sort(key=lambda x: -x[1])
        seq = [x[0] for x in seq]
        print(f"Task exec sequence: {', '.join(seq)}")
        return seq


if __name__ == "__main__":
    task_tree = [
        {"name": "task1", "deps": ["task2", "task3"]},
        {"name": "task2", "deps": ["task4"]},
        {"name": "task4"},
        {"name": "task3"},
    ]
    # task_tree += [ # circular dependency. you might want to use translation tools to identify issue.
    #     {"name": "task5", "deps": ["task6"]},
    #     {"name": "task6", "deps": ["task7"]},
    #     {"name": "task7", "deps": ["task5"]},
    # ]
    seq = get_task_seq(task_tree)
# this verification shall be performed before our worker ever starts up.
