from log_utils import logger_print

每小时秒数 = 3600
每天小时数 = 24
每年天数 = 365
秒级仿真小时数 = 2
两小时秒数 = 每小时秒数 * 秒级仿真小时数
每年小时数 = 每天小时数 * 每年天数
每年月数 = 12

from enum import auto
from strenum import StrEnum

class Solver(StrEnum):
    cplex = auto()
    gurobi = auto()
    ipopt = auto()
    cbc = auto()
    scip = auto()
    # params: https://www.scipopt.org/doc/html/PARAMETERS.php
    # TODO: set all failsafe methods into find first solution and return
    """change minuc -> optimize"""
    glpk = auto()


"""
cbc repl keywords explained: (from chatgpt)

Sure, here's an explanation of all the CBC REPL keywords:

Double parameters:
- `dualB(ound)` - dual bound value for the problem
- `dualT(olerance)` - dual feasibility tolerance
- `primalT(olerance)` - primal feasibility tolerance
- `primalW(eight)` - weight for primal infeasibility in the objective
- `psi` - objective function weight
- `zeroT(olerance)` - zero tolerance for problem constraints

Branch and Cut double parameters:
- `allow(ableGap)` - allowable gap between the best integer feasible solution and the best bound
- `cuto(ff)` - cutoff bound for the problem
- `inc(rement)` - increment in the objective function value when the solver is unable to find a better feasible solution
- `integerT(olerance)` - tolerance for considering a variable to be integer
- `preT(olerance)` - tolerance for problem constraints before presolve
- `pumpC(utoff)` - cutoff value for the feasibility pump heuristic
- `ratio(Gap)` - relative gap tolerance for the problem
- `sec(onds)` - maximum time allowed for solving the problem in seconds

Integer parameters:
- `force(Solution)` - force a solution to be found within a certain number of iterations
- `idiot(Crash)` - enable/disable idiot crash mode
- `maxF(actor)` - maximum factorization size allowed
- `maxIt(erations)` - maximum number of iterations allowed
- `output(Format)` - output format for the solution
- `randomS(eed)` - seed for the random number generator
- `slog(Level)` - logging level for the solver
- `slogger_print(Crash)` - enable/disable sprint crash mode

Branch and Cut integer parameters:
- `cutD(epth)` - maximum depth to explore when generating cutting planes
- `cutL(ength)` - maximum number of non-zero coefficients in a generated cutting plane
- `depth(MiniBab)` - maximum depth for the tree search
- `hot(StartMaxIts)` - maximum number of iterations to perform during a hot start
- `log(Level)` - logging level for the branch and cut solver
- `maxN(odes)` - maximum number of nodes to explore during the tree search
- `maxSaved(Solutions)` - maximum number of solutions to save during the search
- `maxSo(lutions)` - maximum number of solutions to find before stopping the search
- `passC(uts)` - enable/disable passing cuts from parent to child nodes during the tree search
- `passF(easibilityPump)` - enable/disable passing information from the feasibility pump heuristic from parent to child nodes during the tree search
- `passT(reeCuts)` - enable/disable passing tree cuts from parent to child nodes during the tree search
- `pumpT(une)` - tuning parameter for the feasibility pump heuristic
- `randomC(bcSeed)` - seed for the random number generator used by the branch and cut solver
- `slow(cutpasses)` - number of passes to make when generating cutting planes
- `strat(egy)` - strategy for selecting variables to branch on
- `strong(Branching)` - enable/disable strong branching
- `trust(PseudoCosts)` - trust level for the pseudo-costs of variables

Keyword parameters:
- `allC(ommands)` - display all available commands
- `chol(esky)` - enable/disable the use of Cholesky factorization
- `crash` - enable/disable crash mode
- `cross(over)` - enable/disable crossover during tree search
- `direction` - direction of the optimization
- `error(sAllowed)` - number of allowed errors during execution
- `fact(orization)` - factorization method to use
- `keepN(ames)` - enable/disable keeping original variable names in the output
- `mess(ages)` - enable/disable display of messages during execution
- `perturb(ation)` - perturbation amount to use
- `presolve` - enable/disable presolve
- `printi(ngOptions)` - display printing options
- `scal(ing)` - enable/disable scaling of the problem
- `timeM(ode)` - display timing information

Branch and Cut keyword parameters:
- `clique(Cuts)` - enable/disable the generation of clique cuts
- `combine(Solutions)` - enable/disable the combination of solutions during tree search
- `combine2(Solutions)` - enable/disable the combination of solutions during tree search
- `constraint(fromCutoff)` - constraint to add when a cutoff bound is reached
- `cost(Strategy)` - cost strategy to use
- `cplex(Use)` - use CPLEX for linear programming
- `cuts(OnOff)` - enable/disable all cuts
- `Dins` - enable/disable DINS heuristic
- `DivingS(ome)` - enable/disable diving heuristic
- `DivingC(oefficient)` - diving coefficient to use
- `DivingF(ractional)` - enable/disable diving on fractional variables
- `DivingG(uided)` - enable/disable guided diving heuristic
- `DivingL(ineSearch)` - enable/disable line search for diving heuristic
- `DivingP(seudoCost)` - enable/disable pseudo-cost diving heuristic
- `DivingV(ectorLength)` - diving vector length to use
- `dw(Heuristic)` - enable/disable DW heuristic
- `feas(ibilityPump)` - enable/disable feasibility pump heuristic
- `flow(CoverCuts)` - enable/disable the generation of flow cover cuts
- `GMI(Cuts)` - enable/disable the generation of Gomory mixed integer cuts
- `gomory(Cuts)` - enable/disable the generation of Gomory cuts
- `greedy(Heuristic)` - enable/disable greedy heuristic
- `heur(isticsOnOff)` - enable/disable all heuristics
- `knapsack(Cuts)` - enable/disable the generation of knapsack cuts
- `lagomory(Cuts)` - enable/disable the generation of Lagrangean relaxation Gomory cuts
- `latwomir(Cuts)` - enable/disable the generation of Lattimore-Foland cuts
- `lift(AndProjectCuts)` - enable/disable the generation of lift-and-project cuts
- `local(TreeSearch)` - enable/disable local search during tree search
- `mixed(IntegerRoundingCuts)` - enable/disable mixed integer rounding cuts
- `node(Strategy)` - node selection strategy to use
- `PrepN(ames)` - enable/disable preserving original variable names in the output
- `pivotAndC(omplement)` - enable/disable pivot-and-complement heuristic
- `pivotAndF(ix)` - enable/disable pivot-and-fix heuristic
- `preprocess` - enable/disable preprocessing
- `probing(Cuts)` - enable/disable the generation of probing cuts
- `proximity(Search)` - enable/disable proximity search
- `randomi(zedRounding)` - enable/disable randomized rounding heuristic
- `reduce(AndSplitCuts)` - enable/disable the generation of reduce-and-split cuts
- `reduce2(AndSplitCuts)` - enable/disable the generation of reduce-and-split cuts
- `residual(CapacityCuts)` - enable/disable the generation of residual capacity cuts
- `Rens` - enable/disable RENS heuristic
- `Rins` - enable/disable RINS heuristic
- `round(ingHeuristic)` - enable/disable rounding heuristic
- `sosO(ptions)` - SOS option to use
- `sosP(rioritize)` - SOS prioritization method to use
- `two(MirCuts)` - enable/disable the generation of two-MIR cuts
- `Vnd(VariableNeighborhoodSearch)` - enable/disable variable neighborhood search heuristic
- `zero(HalfCuts)` - enable/disable the generation of zero-half cuts

Actions or string parameters:
- `allS(lack)` - display all slack variables
- `barr(ier)` - enable/disable barrier method
- `basisI(n)` - load an initial basis from a file
- `basisO(ut)` - write the final basis to a file
- `directory` - set the directory for input/output files
- `dualS(implex)` - enable/disable dual simplex method
- `either(Simplex)` - enable/disable either simplex method
- `end` - end the current execution
- `exit` - exit the CBC REPL
- `export` - export the problem to a file
- `gsolu(tion)` - enable/disable display of best feasible solution found so far
- `guess` - enable/disable intelligent guess for initial solution
- `help` - display help information
- `import` - import a problem from a file
- `initialS(olve)` - solve the problem using the initial values of the decision
- `max(imize)` - set the optimization direction to maximize (default)
- `min(imize)` - set the optimization direction to minimize
- `para(metrics)` - display the parameters used by the solver
- `primalS(implex)` - enable/disable primal simplex method
- `printM(ask)` - enable/disable printing of the solution progress
- `quit` - exit the CBC REPL
- `restoreS(olution)` - restore a saved solution
- `saveS(olution)` - save the current solution
- `solu(tion)` - display the current solution
- `stat(istics)` - display the solver statistics
- `stop` - stop the current execution

Branch and Cut actions:
- `branch(AndCut)` - branch on a variable and generate cutting planes
- `doH(euristic)` - perform a heuristic search
- `mips(tart)` - start solving the problem using the MIP solver
- `nextB(estSolution)` - display the next best solution found so far
- `prio(rityIn)` - set the priority of a variable or constraint
- `solv(e)` - solve the problem

"""