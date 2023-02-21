import numpy as np
from docplex.mp.model import Model

from config import *
from InitParam import ResourceGet
from SystemClass import *
from DeviceGroup import DeviceGroup


if __name__=='__main__':

    RG = ResourceGet('./old/jinan_changqing-hour.dat', NUMH)
    ha0              = RG.ha
    ele_price0       = RG.ele_price
    gas_price0       = RG.gas_price
    cityrs_price0    = RG.cityrs_price
    citysteam_price0 = RG.citysteam

    power_load = RG.power_load
    cool_load  = RG.cool_load
    heat_load  = RG.heat_load
    steam_load = RG.steam_load

    MDL = Model(name='buses')

    DG = DeviceGroup(NUMH, MDL,RG)

    iges_set = [DG.diesel,DG.pv,DG.bess,DG.csgr,DG.dyzqfsq,DG.chp,DG.gasgl,DG.qs_exchanger,DG.zq_xhl,DG.pbgr,
                DG.xbxr,DG.szrs,DG.rsdgl,DG.gasgl_rs,DG.sx,DG.shizheng,DG.rs_xhl,DG.ss_exchanger,
                DG.rb,DG.sy,DG.slj,DG.sangk,DG.doublegk,DG.dire,DG.bx,DG.xbxl,DG.lowxbxr,DG.gridnet]

    obj = iges_set[0].nianhua
    for ii in range(1, len(iges_set)):
        obj = obj + iges_set[ii].nianhua

    MDL.minimize(obj)
    MDL.print_information()

    MDL.set_time_limit(1000)

    sol_run1 = MDL.solve(log_output=True)
    # print('abs2 value:')
    # print(sol_run1.get_value(abs1.abs_x[1]))
    print(sol_run1.solve_details)

    ii = 0
    print('obj:{0}'.format(ii), sol_run1.get_value(obj))
    ii += 1
    print('obj:{0}'.format(ii), sol_run1.get_value(iges_set[ii].pv_set))
    ii += 1
    print('obj:{0}'.format(ii), sol_run1.get_value(iges_set[ii].ess_set))
    ii += 1
    print('obj:{0}'.format(ii), sol_run1.get_value(iges_set[ii].csgr_set))
    ii += 1
    print('obj:{0}'.format(ii), sol_run1.get_value(iges_set[ii].dyzqfsq_set))
    ii += 1
    print('obj:{0}'.format(ii), sol_run1.get_value(iges_set[ii].chp_set))
    ii += 1
    print('obj:{0}'.format(ii), sol_run1.get_value(iges_set[ii].gasgl_set))
    ii += 1
    print('obj:{0}'.format(ii), sol_run1.get_value(iges_set[ii].exch_set))
    ii += 1
    print('obj:{0}'.format(ii), sol_run1.get_value(iges_set[ii].xhl_set))
    ii += 1
    print('obj:{0}'.format(ii), sol_run1.get_value(iges_set[ii].pv_set))
    ii += 1
    print('obj:{0}'.format(ii), sol_run1.get_value(iges_set[ii].ess_set))
    ii += 1

    for v in MDL.iter_integer_vars():
        print(v, " = ", v.solution_value)
