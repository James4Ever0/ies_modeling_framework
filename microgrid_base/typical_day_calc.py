load_format = {"workday": [0,1,2,3,4], "hoilday": [5,6]}
load_format1 = {"workday": [1,2,3,4,5], "hoilday": [0,6]}

lfs = [load_format, load_format1]

# assert day in range(7)

# 温度聚类 -> 9 sets -> avg wind/solar

# shape: 1x365

for lf in lfs:
    wd, hd = set(lf['workday']), set(lf['hoilday'])
    assert wd.intersection(hd) == set()
    assert wd.union(hd) == set(range(7))