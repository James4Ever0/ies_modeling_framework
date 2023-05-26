load_format = {"workday": [0,1,2,3], "hoilday": [6,7]}
load_format1 = {"workday": [2,3,4], "hoilday": [5,6]}

lfs = [load_format, load_format1]

assert day in range(7)

for lf in lfs:
    wd, hd = lf['workday'], lf['hoilday']
    assert set(wd).intersection(set(hd)) == set()
    assert 