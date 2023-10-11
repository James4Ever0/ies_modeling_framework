# demo on how to solve a miniatured ies system with cplex, swipl (clpqr) or something else.

# you can use constant objective in cplex or 'once/1' in prolog to check if model is solveable.

# bonus: in cplex you can use feasopt to relax port status constraints and diagnose the cause, while in swipl you can only transform it yourself to minimize the violation.

# in real model you should relax the adder constraints

# this check is after the isomorphism check. it will not eliminate multiple energy type sets of adders

# since miniature system is hard to build, and not directly related to underlying model, let's just skip it.
# we only build time sliced systems at this time, since this is related to the actual model, easier for investigation.

fpath = "isomorphic_topo_status.pkl"

# 1. miniature system check (skipped)
#   cplex

# 2. time sliced system check
#   cplex

# 3. build and solve the model
#   cplex

# if the final solution has failed, we will perform feasopt to check which case is unsatisfiable, which case is missing and which case does not exist in existing state set.

# to ensure solveability, we elimitate the initial soc limit of lithium battery model. 
# for some model, only output port ranges will be acquired, like load, PV, lithium battery and diesel generator
# for models like grid, diesel, we make sure any state is valid for them 

# steps:

# 1. filter state frame list
#     if state frame has load port at input state, iteratively try to make one load running at maximum rate
#     if w/o any load port at input state, just enforce the directions (minimum positive/maximum negative value)
#     eliminate impossible states

# 2. check on remained state frame list
#     check if all loads has maximum state, exit if not
#     check with 2 sets of verifiers again, exit if not passed verification

# 3. collect result
#     emit final possible state frames

import pickle

with open(fpath, "rb") as f:
    data = pickle.load(f)

print("data:", data)

# from pyomo.environ import *

# solver = SolverFactory('cplex')

# for state_frame in state_frame_list:
#     ...
