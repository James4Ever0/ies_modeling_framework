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
        # def __init__(self, name: str, signature: List[str]):
        # self.__name__ = name
        # TODO: dynamically infer registry name
        # self.decorator_source = f"{self.__name__}.register"
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
    return solver_exec_script(Solver.cplex, ["-c", *script], logfile, timeout)


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


def load_cplex_sol_file(sol_file: str):
    with open(sol_file, "r") as f:
        file = f.read()

    # 'xml' is the parser used. For html files, which BeautifulSoup is typically used for, it would be 'html.parser'.
    soup = BeautifulSoup(file, "xml")
    data = {}
    for var in soup.find_all("variable"):
        name = var["name"]
        value = float(var["value"])
        data[name] = value
    return data


def feasopt(mw: ModelWrapper, mode: FeasoptMode, logfile: str):
    solved = False
    # TODO: logging
    with tempfile.TemporaryDirectory() as tmpdir:
        with chdir_context(tmpdir):
            with modelSolvedTestContext(mw.model) as check_solved:
                lp_path_abs = os.path.join(tmpdir, lp_path := "model.mps")
                # lp_path_abs = os.path.join(tmpdir, lp_path := "model.lp")
                sol_path_abs = os.path.join(tmpdir, sol_path := "solution.sol")
                exp_model = ExportedModel(mw.model, lp_path_abs)
                # _, smap_id = mw.model.write(lp_path)
                # smap = mw.model.solutions.symbol_map[smap_id]
                cplex_config = [
                    f"timelimit {FEASOPT_TIMELIMIT}"
                    if not ies_env.DETERMINISTIC_FAILSAFE
                    else f"dettimelimit {FEASOPT_TIMELIMIT*CPLEX_SEC_TO_TICK}",
                    f"feasopt mode {mode}",
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
                cplex_exec_script(
                    script, logfile, FEASOPT_TIMELIMIT + 10
                )  # we don't care about the exit code.
                if os.path.exists(sol_path):
                    # TODO: parse and assign value from solution
                    cplex_solution = load_cplex_sol_file(sol_path)
                    for v in mw.model.component_data_objects(ctype=Var):
                        varname = v.name
                        cplex_varname = exp_model.reverse_translation_table.get(
                            varname, None
                        )
                        val = cplex_solution.get(cplex_varname, None)
                        if val is not None:
                            v.set_value(val)
                    solved = check_solved()
        # breakpoint()
    return solved


@failsafe_methods.register
def feasopt_with_optimization(mw: ModelWrapper, logdir: str):
    logfile = os.path.join(logdir, "cplex_feasopt_with_optimization_failsafe.log")
    return feasopt(mw, FeasoptMode.optimal_minimum_sum_relaxation, logfile), logfile


@failsafe_methods.register
def feasopt_only(mw: ModelWrapper, logdir: str):
    logfile = os.path.join(logdir, "cplex_feasopt_only_failsafe.log")
    return feasopt(mw, FeasoptMode.minimum_sum_relaxation, logfile), logfile


IPOPT_MAX_ITERATION = 1000
IPOPT_TIMELIMIT = 30
IPOPT_ITERATION_KW = "Number of Iterations"
IPOPT_MAX_ITER_CONFIG_KW = "max_iter"
IPOPT_MAX_CPUTIME_CONFIG_KW = "max_cpu_time"
IPOPT_MAX_CPUTIME = 10
# you cannot use ipopt with constant objective.


@failsafe_methods.register
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
        3. ipopt
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
