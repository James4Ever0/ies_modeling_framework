# find all combinations of conjugate loads

import random

rng = lambda: random.randint(0,1)
arr_size = 8760
subject_count = 5
subjects = {i: [rng() for _ in range(arr_size)] for i in range(subject_count)}
from frozendict import frozendict
total_combs = set()
for arr_i in range(arr_size):
    comb = {i:subjects[i][arr_i] for i in range(subject_count)}
    comb = frozendict(comb)
    total_combs.add(comb)

print(total_combs)
print(len(total_combs)) # 32