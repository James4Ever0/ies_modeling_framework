import numpy


load_format = {"workday": [0, 1, 2, 3, 4], "hoilday": [5, 6]}
load_format1 = {"workday": [1, 2, 3, 4, 5], "hoilday": [0, 6]}

lfs = [load_format, load_format1]

# assert day in range(7)

# 温度聚类 -> 9 sets -> avg wind/solar

# shape: 1x365
# 春季是3月到5月，夏季是6月到8月，秋季是9月到11月，冬季是12月到2月
# 平年的2月是28天，闰年2月是29天。
# 4月、6月、9月、11月各是30天。
# 1月、3月、5月、7月、8月、10月、12月各是31天。
month_days = [31] * 12
month_days[1] = 28
month_days[4 - 1] = month_days[6 - 1] = month_days[9 - 1] = month_days[11 - 1] = 30

mdr = numpy.cumsum(month_days)
print(mdr)

spring_days = [d for d in range(mdr[2], mdr[5])]
summer_days = [d for d in range(mdr[5], mdr[8])]
autumn_days = [d for d in range(mdr[8], mdr[11])]
winter_days = [
    d for d in range(365) if d not in spring_days + summer_days + autumn_days
]


# {day_index: {"main": main_category, ""}}

# append by keys.
# {data_key: [index, ...]}

for lf in lfs:
    wd, hd = set(lf["workday"]), set(lf["hoilday"])
    assert wd.intersection(hd) == set()
    assert wd.union(hd) == set(range(7))
