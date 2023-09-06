# virtually run interdependent tasks, generate the execution sequence

task_tree = [
    {"name": "task1", "deps": ["task2", "task3"]},
    {"name": "task2", "deps": ["task4"]},
    {"name": "task4"},
    {"name": "task3"},
]

from pyomo.environ import *


def get_task_deps(task_tree: list[dict], solver_name: str = "cplex"):
    model = ConcreteModel()
    lateinit_constraints = []
    tasknames = set()
    depnames = set()
    for elem in task_tree:
        name = elem.get("name")
        tasknames.add(name)
        setattr(model, name, Var(domain=NonNegativeIntegers))
        deps = elem.get("deps", [])
        for dep in deps:
            depnames.add(deps)
            lateinit_constraints.append((name, dep))
    if not depnames.issubset(tasknames):
        raise Exception("Have unmet dependencies: %s" % depnames.difference(tasknames))
    for index, (name, dep) in enumerate(lateinit_constraints):
        setattr(
            model,
            f"constraint_{index}",
            Constraint(expr=getattr(model, name) <= getattr(model, dep)),
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
        for tn in tasknames:
            print(f"{tn}:\t{value(getattr(model, tn))}")
