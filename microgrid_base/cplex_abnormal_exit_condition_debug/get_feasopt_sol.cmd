cplex -c "read converted.mps" "set timelimit 30" "feasopt all" "write feasopt.sol" "quit" 
@REM cannot use 'xml' as output solution file name
@REM cplex -c "read converted.mps" "set feasopt mode 1" "feasopt all" "write feasopt.sol" "quit"
@REM Please specify what to relax (constraints, variables, or all):
@REM no need for "quit"
@REM Present value for relaxation measure: 0 (default is 0)
@REM  0 = find minimum-sum relaxation
@REM  1 = find optimal minimum-sum relaxation
@REM  2 = find minimum number of relaxations
@REM  3 = find optimal relaxation with minimum number of relaxations
@REM  4 = find minimum quadratic-sum relaxation
@REM  5 = find optimal minimum quadratic-sum relaxation