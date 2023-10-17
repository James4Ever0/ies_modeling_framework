Pwire_arr = [1,20,100]
GivenMaxPower = 20
ind = -1
dis = -1
for _ind, val in enumerate(Pwire_arr):
    _dis = val - GivenMaxPower
    if _dis >= 0:
        if dis < 0 or dis > _dis:
            dis = _dis
            ind = _ind
print(ind,dis)