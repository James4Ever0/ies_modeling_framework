from integratedEnergySystemPrototypes import EnergySystemUtils, Model

model = Model('test_model')

var  =   model.continuous_var(name='var')

target_value = 10 # 10>5, but we set 5 as lower bound, to check if this issue happens.

# set 15 as upper bound.
lower_bound, upper_bound=15,5

util = EnergySystemUtils(model,num_hour=1)

util.add_lower_and_upper_bounds([var],lower_bound, upper_bound)

util.equation(var,target_value)

# check for conflicts?

from mini_data_log_utils import check_conflict

check_conflict(model)