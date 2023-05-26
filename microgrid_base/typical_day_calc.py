load_format = {"workday": [0,1,2,3,4], "hoilday": [5,6]}
load_format1 = {"workday": [1,2,3,4,5], "hoilday": [0,6]}

lfs = [load_format, load_format1]

# assert day in range(7)

# 温度聚类 -> 9 sets -> avg wind/solar

# shape: 1x365
# 春季是3月到5月，夏季是6月到8月，秋季是9月到11月，冬季是12月到2月
# 平年的2月是28天，闰年2月是29天。
# 4月、6月、9月、11月各是30天。
# 1月、3月、5月、7月、8月、10月、12月各是31天。
month_days = [0]*12
4月、6月、9月、11月=30 

{day_index: {"main": main_category, ""}}

# append by keys.
# {data_key: [index, ...]}

for lf in lfs:
    wd, hd = set(lf['workday']), set(lf['hoilday'])
    assert wd.intersection(hd) == set()
    assert wd.union(hd) == set(range(7))