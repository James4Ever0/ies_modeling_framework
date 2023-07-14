from typing import List


def check_if_executable(statement, environment) -> bool:
    return is_executable


def execute_statement(statement, environment):
    return environment


def functional_executor(statement_array: List, environment=...):
    IES = []
    LES = []
    for statement in statement_array:
        TLES = []  # create it along the way.

        # stage 1
        if check_if_executable(statement, environment):
            environment = execute_statement(statement, environment)
            IES.append(statement)

        else:
            TLES.append(statement)

        # stage 2
        while True:
            late_removal_indexes = []
            for index, elem in enumerate(LES.copy()):
                if check_if_executable(elem, environment):
                    environment = execute_statement(elem, environment)
                    IES.append(elem)

                    late_removal_indexes.append(index)
            if len(late_removal_indexes) == 0:
                break
            LES = [e for i, e in enumerate(LES) if i not in late_removal_indexes]

        # stage 3
        for elem in TLES:
            if check_if_executable(elem, environment):
                environment = execute_statement(elem, environment)
                IES.append(elem)

            else:
                LES.append(elem)
    # usually, LES == []
    return IES, LES
