from log_utils import logger_print

from config import ies_env
from contextlib import contextmanager
from log_utils import logger_traceback
from ies_optim import *
from enum import auto, IntEnum
from debug_utils import ExportedModel, modelSolvedTestContext
import random
import tempfile


# we need a configurable context manager which suppress exception.
@contextmanager
def failsafe_suppress_exception(hint="failsafe suppressed exception:"):
    try:
        yield
    except Exception as e:
        if not ies_env.FAILSAFE:
            raise e
        else:
            logger_traceback(hint, stacklevel=5)


import inspect


class MethodRegistry(list):
    """
    A registry of methods, used to register methods with given signature.
    """

    def __init__(self, signature: List[str]):
        self.signature = signature
        self.names = set()
        super().__init__()

    def check_signature(self, obj):
        obj_sig = inspect.signature(obj)
        obj_keys = list(obj_sig.parameters.keys())
        assert (
            obj_keys == self.signature
        ), "Signature mismatch: (registered signature: {}, given signature: {})".format(
            self.signature, obj_keys
        )
        return True

    def add(self, obj):
        name = obj.__name__
        if name not in self.names:
            if self.check_signature(obj):
                self.names.add(name)
                self.append(obj)

    def register(self, obj):
        self.add(obj)
        return obj


failsafe_methods = MethodRegistry(signature=["mw", "logdir"])


def quote(s: str, q='"'):
    return q + s + q


from pyomo.common.tee import TeeStream
from pyomo.common.log import LogStream
import datetime


class FileLogger:
    def __init__(self, fname: str):
        self.fname = fname
        self.handle = open(fname, "a+")
        self.handle.write(datetime.datetime.now().isoformat().center(70, "=") + "\n")
        # self.handle = open(fname, "w+")

    def log(self, level, message):
        logger_print(message)
        self.handle.write(message + "\n")

    def __del__(self):
        self.handle.close()
        del self.fname
        del self.handle


import subprocess


def solver_exec_script(solver: Solver, script: List[str], logfile: str, timeout: float):
    check_script_is_not_empty(script)
    cmd = [solver, *script]
    flogger = FileLogger(logfile)
    logger_print("running solver:", cmd)
    return_code = -1

    try:
        with failsafe_suppress_exception():
            ostreams = [LogStream(level=None, logger=flogger), sys.stdout]
            # cmd = " ".join([e if " " not in e else quote(e) for e in cmd ])
            # return_code = os.system(cmd)

            with TeeStream(*ostreams) as t:
                cp = subprocess.run(
                    cmd,
                    timeout=timeout,
                    stdout=t.STDOUT,
                    stderr=t.STDERR,
                    universal_newlines=True,
                )
                return_code = cp.returncode
            # cmd = f"{Solver.cplex} -c {' '.join([quote(e) for e in script])}"
            # return_code = os.system(cmd)
        return return_code
    finally:
        del flogger


def cplex_exec_script(script: List[str], logfile: str, timeout: float):
    check_script_is_not_empty(script)
    return solver_exec_script(Solver.cplex, ["-c", *script], logfile, timeout)

def check_script_is_not_empty(script):
    assert len(script)>0, "no script to execute"

def scip_exec_script(script: List[str], logfile: str, timeout: float):
    check_script_is_not_empty(script)
    args = []
    for s in script:
        args.append("-c")
        args.append(s)
    return  solver_exec_script(Solver.scip, args, logfile, timeout)

SCIP_NOT_SOLVED_KW="no solution available" 
SCIP_SOLVED_KW = "objective value"
def check_scip_if_solved(first_two_lines:list[str]):
    _c = "\n".join(first_two_lines)
    if SCIP_SOLVED_KW in _c:
        return True
    elif SCIP_NOT_SOLVED_KW in _c:
        return False
    else:
        raise Exception(f"Unknown scip solution conditon. Is it a scip solution file?\nFirst two lines:\n{_c}")
import re
REGEX_FIND_NON_BLANK_SEGMENTS = re.compile(r"[^ \t]+")
TWO = 2
def parse_scip_solution_content(content:str):
    lines = content.strip().split("\n")
    first_two_lines = lines[:TWO]
    solution_lines = lines[TWO:]
    solved = check_scip_if_solved(first_two_lines)
    solution = {}
    if solved:
        for line in solution_lines:
            line = line.strip()
            if len(line)>0:
                candidates = REGEX_FIND_NON_BLANK_SEGMENTS.findall(line)
                if len(candidates)>=TWO:
                    try:
                        varname, value_str = candidates[:TWO]
                        varname = varname.strip()
                        if len(varname)>0:
                            value = float(value_str)
                            solution[varname] = value
                    except TypeError:
                        pass
                    except Exception as e:
                        raise e
    return solution

@contextmanager
def chdir_context(dirpath: str):
    cwd = os.getcwd()
    os.chdir(dirpath)
    try:
        yield
    finally:
        os.chdir(cwd)


class FeasoptMode(IntEnum):
    """
    CPLEX> set feasopt mode <mode>
        0 = find minimum-sum relaxation
        1 = find optimal minimum-sum relaxation
        2 = find minimum number of relaxations
        3 = find optimal relaxation with minimum number of relaxations
        4 = find minimum quadratic-sum relaxation
        5 = find optimal minimum quadratic-sum relaxation
    """

    minimum_sum_relaxation = (
        0  # do not use 'auto' here because that will make it into 1
    )
    optimal_minimum_sum_relaxation = auto()
    minimum_number_of_relaxations = auto()
    optimal_relaxation_with_minimum_number_of_relaxations = auto()
    minimum_quadratic_sum_relaxation = auto()
    optimal_minimum_quadratic_sum_relaxation = auto()


FEASOPT_TIMELIMIT = 30
CPLEX_SEC_TO_TICK = 290
from bs4 import BeautifulSoup

def load_scip_sol_file(sol_file:str):
    return solution_loader(sol_file, parse_scip_solution_content)

def parse_cplex_solution_content(content):
    
    # 'xml' is the parser used. For html files, which BeautifulSoup is typically used for, it would be 'html.parser'.
    soup = BeautifulSoup(content, "xml")
    data = {}
    for var in soup.find_all("variable"):
        name = var["name"]
        value = float(var["value"])
        data[name] = value
    return data

def solution_loader(sol_file:str, parser):
    
    with open(sol_file, "r") as f:
        content = f.read()
        data = parser(content)
        return data

def load_cplex_sol_file(sol_file: str):
    return solution_loader(sol_file, parse_cplex_solution_content)

def invoke_solver_with_custom_config_and_solution_parser(mw: ModelWrapper, logfile:str, timelimit:int, script_generator, script_executor, solution_parser):
    solved = False
    # TODO: logging
    with tempfile.TemporaryDirectory() as tmpdir:
        with chdir_context(tmpdir):
            with modelSolvedTestContext(mw.model) as check_solved:
                # lp_path_abs = os.path.join(tmpdir, lp_path := "model.mps")
                lp_path_abs = os.path.join(tmpdir, lp_path := "model.lp")
                sol_path = "solution.sol"
                exp_model = ExportedModel(mw.model, lp_path_abs)

                script = script_generator(lp_path, sol_path)

                script_executor(
                    script, logfile, timelimit
                )
                if os.path.exists(sol_path):
                    # TODO: parse and assign value from solution
                    solution = solution_parser(sol_path)
                    for v in mw.model.component_data_objects(ctype=Var):
                        varname = v.name
                        trans_varname = exp_model.reverse_translation_table.get(
                            varname, None
                        )
                        val = solution.get(trans_varname, None)
                        if val is not None:
                            v.set_value(val)
                    solved = check_solved()
                # breakpoint()
    return solved

def feasopt_script_generator(lp_path:str, sol_path:str, mode:FeasoptMode, solutionCount:int):
    cplex_config = [
        f"timelimit {FEASOPT_TIMELIMIT}"
        if not ies_env.DETERMINISTIC_FAILSAFE
        else f"dettimelimit {FEASOPT_TIMELIMIT*CPLEX_SEC_TO_TICK}",
        f"feasopt mode {mode}",
        f"mip limits solutions {solutionCount}",
    ]
    if ies_env.DETERMINISTIC_FAILSAFE:
        cplex_config.append(f"randomseed {ies_env.ANSWER_TO_THE_UNIVERSE}")
    script = [
        f"read {lp_path}",
        *[f"set {c}" for c in cplex_config],
        "feasopt all",  # dettime: 8816 ticks for 30s timelimit
        f"write {sol_path}",
        "quit",
    ]
    return script

from functools import partial
def feasopt(mw: ModelWrapper, mode: FeasoptMode, logfile: str, solutionCount:int=1):
    solved = invoke_solver_with_custom_config_and_solution_parser(mw, logfile, FEASOPT_TIMELIMIT + 10, partial(feasopt_script_generator, mode=mode, solutionCount=solutionCount), cplex_exec_script,load_cplex_sol_file)
    return solved

@failsafe_methods.register
def feasopt_with_optimization(mw: ModelWrapper, logdir: str):
    logfile = os.path.join(logdir, "cplex_feasopt_with_optimization_failsafe.log")
    return feasopt(mw, FeasoptMode.optimal_minimum_sum_relaxation, logfile), logfile


@failsafe_methods.register
def feasopt_only(mw: ModelWrapper, logdir: str):
    logfile = os.path.join(logdir, "cplex_feasopt_only_failsafe.log")
    return feasopt(mw, FeasoptMode.minimum_sum_relaxation, logfile), logfile

def scip_minuc_script_generator(lp_path:str, sol_path:str, solutionCount:int = 1):
    scip_config = [
                    f"limits time {FEASOPT_TIMELIMIT}",
                    f"limits solutions {solutionCount}",
                    f"limits maxsol {solutionCount}",
    ]
    if ies_env.DETERMINISTIC_FAILSAFE:
        scip_config.append(f"random lpseed {ies_env.ANSWER_TO_THE_UNIVERSE}")
        scip_config.append(f"random permutationseed {ies_env.ANSWER_TO_THE_UNIVERSE}")
        scip_config.append(f"random randomseedshift {ies_env.ANSWER_TO_THE_UNIVERSE}")
    script = [
        f"read {lp_path}",
        *[f"set {c}" for c in scip_config],
        "change minuc",
        "optimize",
        f"write solution {sol_path}",
        "quit",
    ]
    return script

@failsafe_methods.register
def scip_minuc(mw:ModelWrapper, logdir:str):
    logfile = os.path.join(logdir, "scip_minuc.log")
    solved = invoke_solver_with_custom_config_and_solution_parser(mw, logfile, FEASOPT_TIMELIMIT + 30, scip_minuc_script_generator, scip_exec_script,load_scip_sol_file)
    return solved, logfile

IPOPT_MAX_ITERATION = 1000
IPOPT_TIMELIMIT = 30
IPOPT_ITERATION_KW = "Number of Iterations"
IPOPT_MAX_ITER_CONFIG_KW = "max_iter"
IPOPT_MAX_CPUTIME_CONFIG_KW = "max_cpu_time"
IPOPT_MAX_CPUTIME = 10
# you cannot use ipopt with constant objective.


# @failsafe_methods.register
# don't register it. deprecated.
def ipopt_no_presolve(mw: ModelWrapper, logdir: str):
    solved = False
    logfile = os.path.join(logdir, "ipopt_failsafe.log")
    with SolverFactory(Solver.ipopt) as solver:
        with modelSolvedTestContext(mw.model) as check_solved:
            solver.options[IPOPT_MAX_ITER_CONFIG_KW] = IPOPT_MAX_ITERATION
            solver.options[IPOPT_MAX_CPUTIME_CONFIG_KW] = IPOPT_MAX_CPUTIME
            if ies_env.DETERMINISTIC_FAILSAFE:
                # we pass initial values of variables as random seeds. don't have cli configuration.
                ...
            solved = ipopt_solve(mw, logfile, solver, check_solved)
            if not solved:
                # parse the logfile and rerun the task.
                adjusted_max_iter = 0
                if os.path.exists(logfile):
                    with open(logfile, "r") as f:
                        content = f.read()
                        content_lines = content.split("\n")
                        for line in content_lines:
                            if IPOPT_ITERATION_KW in line:
                                iteration = re.search(r"\d+", line).group()
                                logger_print("IPOPT FAILED AT ITERATION: ", iteration)
                                adjusted_max_iter = int(iteration) - 1
                                break
                if adjusted_max_iter > 0:
                    solver.options[IPOPT_MAX_ITER_CONFIG_KW] = adjusted_max_iter
                    os.remove(logfile)
                    solved = ipopt_solve(mw, logfile, solver, check_solved)
                else:
                    logger_print(
                        "FAILED TO GET ITERATION COUNT FROM FAILED IPOPT SESSION"
                    )
            # breakpoint()
    return solved, logfile


def ipopt_solve(mw, logfile, solver, check_solved):
    solved = False
    with failsafe_suppress_exception():
        solver.solve(mw.model, tee=True, logfile=logfile, timelimit=IPOPT_TIMELIMIT)
        solved = check_solved()
    return solved


@failsafe_methods.register
def random_value_assignment(mw: ModelWrapper, logdir: str):
    rng = lambda: random.uniform(-100, 100)
    for v in mw.model.component_data_objects(ctype=Var):
        v.set_value(rng(), skip_validation=True) # suppress W1001
        # ref: https://pyomo.readthedocs.io/en/stable/errors.html#W1001
    return (
        True,
        "",
    )  # instead of None, to prevent unwanted behavior when checking existance


# for m in [
#     feasopt_with_optimization,
#     feasopt_only,
#     ipopt_no_presolve,
#     random_value_assignment,
# ]:
#     failsafe_methods.add(m)


def solve_failsafe(mw: ModelWrapper, logdir: str):
    """
    Steps (fail and continue):
        1. feasopt & objective optimization
        2. feasopt only
        3. scip minuc
        4. random value assignment
    """
    solved = False
    report = []
    for method in failsafe_methods:
        try:
            name = method.__name__
            logger_print(f"trying failsafe method: {name}")
            solved, logfile = method(mw, logdir)

            if solved:
                logger_print(f"solved with {name}")
                if os.path.exists(logfile):
                    logger_print(f"logfile write to: {logfile}")
                else:
                    logger_print(f"logfile not found at: {logfile}")
                break  # you may not break just because of the 'solved' flag but also the existance of the logfile.
            else:
                logger_print(f"failed to solve with {name}")
            report.append((name, solved, os.path.exists(logfile)))
        except:
            report.append((name, False, False))
            logger_traceback()

    for n, r, l_exists in report:
        logger_print(f"{n}:\t{r}\t(logfile exists? {l_exists})")
    return solved


if __name__ == "__main__":
    ies_env.FAILSAFE = True
    with failsafe_suppress_exception():
        raise Exception("Exc")
    # it will reach and raise Exc2
    ies_env.FAILSAFE = False
    with failsafe_suppress_exception():
        raise Exception("Exc2")
