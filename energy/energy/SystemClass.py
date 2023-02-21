import numpy as np
from config import *

class IGES(object):
    count = 0
    def __init__(self, name):
        self.name = name
        IGES.count += 1
        print('Define a set named:',name, ',set num is:', IGES.count)

# 柴油机
class Diesel(IGES):
    index = 0
    def __init__(self, num_h, mdl, **kwargs):
        IGES('diesel')
        Diesel.index += 1

        self.num_h      = num_h
        self.set_max    = kwargs.get('set_max',None)
        self.set_price  = kwargs.get('set_price',None)
        self.run_price  = kwargs.get('run_price',None)

        self.diesel_set = mdl.continuous_var(name='diesel_set{0}'.format(Diesel.index))
        self.p_diesel   = mdl.continuous_var_list(list(range(self.num_h)), name='p_diesel{0}'.format(Diesel.index))
        self.p_sum      = mdl.sum(self.p_diesel)
        self.nianhua    = mdl.continuous_var(name='diesel_nianhua{0}'.format(Diesel.index))

        self.cons_register(mdl)

    def cons_register(self, mdl):
        mdl.add_constraint(self.diesel_set <= self.set_max)
        mdl.add_constraint(self.diesel_set >= 0)
        mdl.add_constraints(self.p_diesel[i] <= self.diesel_set for i in range(self.num_h))
        mdl.add_constraint(self.nianhua == self.diesel_set * self.set_price / 15 + self.p_sum * self.run_price * 8760 / self.num_h)

    def total_cost(self, sol):
        return sol.get_value(self.diesel_set) * self.set_price

# 适用于光伏及平板式光热
class PV(IGES):
    index = 0
    def __init__(self, num_h, mdl, **kwargs):
        IGES('PV')
        PV.index += 1

        self.num_h     = num_h
        self.ha        = kwargs.get('ha',None)
        self.eff       = kwargs.get('eff',0.8)
        self.set_max   = kwargs.get('set_max',None)
        self.set_price = kwargs.get('set_price',None)

        self.pv_set  = mdl.continuous_var(name='pv_set{0}'.format(PV.index))
        self.p_pv    = mdl.continuous_var_list(list(range(num_h)), name='p_pv{0}'.format(PV.index))
        # 光照强度
        self.nianhua = mdl.continuous_var(name='pv_nianhua{0}'.format(PV.index))

        self.cons_register(mdl)

    def cons_register(self, mdl):
        mdl.add_constraint(self.pv_set <= self.set_max)
        mdl.add_constraint(self.pv_set >= 0)
        mdl.add_constraints(self.p_pv[i] <= self.pv_set * self.eff * self.ha[i] for i in range(self.num_h))
        mdl.add_constraint(self.nianhua == self.pv_set * self.set_price / 15)

    def total_cost(self, sol):
        return sol.get_value(self.pv_set) * self.set_price

# 储能系统基类
class ESS(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES('ess')
        ESS.index += 1
        self.num_h      = num_h
        self.set_max    = kwargs.get('set_max',None)
        self.ess_price  = kwargs.get('set_price',None)
        self.pcs_price  = kwargs.get('pcs_price',None)

        self.c_rate_max = kwargs.get('c_rate_max',2)
        self.eff        = kwargs.get('eff',0.9)
        self.ess_init   = kwargs.get('ess_init',1)
        self.soc_min    = kwargs.get('soc_min',0)
        self.soc_max    = kwargs.get('soc_max',1)

        self.ess_set   = mdl.continuous_var(name='ess_set{0}'.format(ESS.index))
        self.p_ess     = mdl.continuous_var_list(list(range(num_h)), lb=-BIGM, name='p_ess{0}'.format(ESS.index))
        # 充电功率
        self.p_ess_ch  = mdl.continuous_var_list(list(range(num_h)), name='p_ess_ch{0}'.format(ESS.index))
        # 放电功率
        self.p_ess_dis = mdl.continuous_var_list(list(range(num_h)), name='p_ess_dis{0}'.format(ESS.index))
        # 能量
        self.ess       = mdl.continuous_var_list(list(range(num_h)), name='ess{0}'.format(ESS.index))
        self.pcs_set   = mdl.continuous_var(name='pcs_set{0}'.format(ESS.index))  # pcs
        self.ch_flag   = mdl.binary_var_list(list(range(num_h)), name='bess_ch_flag{0}'.format(ESS.index))  # 充电
        self.dis_flag  = mdl.binary_var_list(list(range(num_h)), name='bess_dis_flag{0}'.format(ESS.index))  # 放电
        # 效率
        self.nianhua    = mdl.continuous_var(name='ess_nianhua{0}'.format(ESS.index))

        self.cons_register(mdl)

    def cons_register(self, mdl, period=1, day_node=24):
        bigM = 1e10
        irange = range(self.num_h)
        mdl.add_constraint(self.ess_set <= self.set_max)
        mdl.add_constraint(self.ess_set >= 0)
        mdl.add_constraint(self.ess_set * self.c_rate_max >= self.pcs_set)
        mdl.add_constraint(self.pcs_set >= 0)
        # 功率拆分
        mdl.add_constraints(self.p_ess[i] == -self.p_ess_ch[i] + self.p_ess_dis[i] for i in irange)

        mdl.add_constraints(self.p_ess_ch[i] >= 0 for i in irange)
        mdl.add_constraints(self.p_ess_ch[i] <= self.ch_flag[i] * bigM for i in irange)
        mdl.add_constraints(self.p_ess_ch[i] <= self.pcs_set for i in irange)

        mdl.add_constraints(self.p_ess_dis[i] >= 0 for i in irange)
        mdl.add_constraints(self.p_ess_dis[i] <= self.dis_flag[i] * bigM for i in irange)
        mdl.add_constraints(self.p_ess_dis[i] <= self.pcs_set for i in irange)

        mdl.add_constraints(self.ch_flag[i] + self.dis_flag[i] == 1 for i in irange)
        # 节点必须是24的倍数
        # day_node=24
        for day in range(1, int(self.num_h / day_node) + 1):
            mdl.add_constraints(self.ess[i] == self.ess[i - 1] + ( self.p_ess_ch[i] * self.eff - self.p_ess_dis[i] / self.eff) * SIMULATIONT / 3600 for i in range(1 + day_node * (day - 1), day_node * day))

        mdl.add_constraints(self.ess[i] <= self.ess_set * self.soc_max for i in range(1, self.num_h))
        mdl.add_constraints(self.ess[i] >= self.ess_set * self.soc_min for i in range(1, self.num_h))
        mdl.add_constraint(self.nianhua == (self.ess_set * self.ess_price + self.pcs_set * self.pcs_price) / 15)

        # 两天之间直接割裂，没有啥关系
        if period == 1:
            mdl.add_constraints(self.ess[i] == self.ess[i - (day_node - 1)] for i in range(day_node - 1, self.num_h, day_node))
        else:
            # 初始值
            mdl.add_constraint(self.ess[0] == self.ess_init * self.ess_set)
            # 两天之间的连接
            mdl.add_constraints(self.ess[i] == self.ess[i - 1] + (self.p_ess_ch[i] * self.eff - self.p_ess_dis[i] / self.eff) * SIMULATIONT / 3600   for i in range(day_node, self.num_h, day_node))

    def total_cost(self, sol):
        return sol.get_value(self.ess_set) * self.ess_price + sol.get_value(self.pcs_set) * self.pcs_price

#
class Csgr(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES('csgr')
        Csgr.index += 1

        self.num_h      = num_h
        self.set_max    = kwargs.get('set_max',None)
        self.gtxr_max   = kwargs.get('set_max * 6',None)
        self.set_price  = kwargs.get('set_price',None)
        self.gtxr_price = kwargs.get('gtxr_price',None)
        self.ha         = kwargs.get('ha',None)  # 光照强度
        self.eff        = kwargs.get('eff',0.8)

        self.csgr_set     = mdl.continuous_var(name='csgr_set{0}'.format(Csgr.index))
        self.p_csgr       = mdl.continuous_var_list(list(range(num_h)), name='p_csgr{0}'.format(Csgr.index))
        self.p_csgr_steam = mdl.continuous_var_list(list(range(num_h)), name='p_csgr_steam{0}'.format(Csgr.index))
        self.nianhua      = mdl.continuous_var(name='csgr_nianhua{0}'.format(Csgr.index))

        self.csgrgtxr_set = ESS(num_h, mdl, set_max=self.gtxr_max, set_price=self.gtxr_price, pcs_price=100)

        self.cons_register(mdl)

    def cons_register(self, mdl):
        # self.csgrgtxr_set.cons_register(mdl)
        hrange = range(self.num_h)
        mdl.add_constraint(self.csgr_set >= 0)
        mdl.add_constraint(self.csgr_set <= self.set_max)
        mdl.add_constraints(self.p_csgr[h] >= 0 for h in hrange)
        mdl.add_constraints(self.p_csgr[h] <= self.csgr_set * self.ha[h] * self.eff for h in hrange)  # 与天气相关
        mdl.add_constraints(self.p_csgr[h] + self.csgrgtxr_set.p_ess[h] == self.p_csgr_steam[h] for h in hrange)  # 槽式光热系统产生的高温
        mdl.add_constraints(0 <= self.p_csgr_steam[h] for h in hrange)  # 约束能量不能倒流
        mdl.add_constraint(self.nianhua == self.csgr_set * self.set_price / 15 + self.csgrgtxr_set.nianhua)

#
class Dyzqfsq(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES("dyzqfsq")
        Dyzqfsq.index += 1

        self.num_h      = num_h
        self.set_max    = kwargs.get('set_max',None)
        self.gtxr_max   = kwargs.get('set_max * 6',None)
        self.set_price  = kwargs.get('set_price',None)
        self.gtxr_price = kwargs.get('gtxr_price',None)
        self.ele_price  = kwargs.get('ele_price',None)
        self.eff        = kwargs.get('eff',0.9)

        self.dyzqfsq_set     = mdl.continuous_var(name='dyzqfsq_set{0}'.format(Dyzqfsq.index))
        self.p_dyzqfsq       = mdl.continuous_var_list(list(range(num_h)), name='p_dyzqfsq{0}'.format(Dyzqfsq.index))
        self.p_dyzqfsq_steam = mdl.continuous_var_list(list(range(num_h)),name='p_dyzqfsq_steam{0}'.format(Csgr.index))
        self.nianhua         = mdl.continuous_var(name='Dyzqfsq_nianhua{0}'.format(Dyzqfsq.index))
        self.ele_cost        = mdl.continuous_var(name='dyzqfsq_ele_cost{0}'.format(Dyzqfsq.index))

        self.dyzqfsqgtxr_set = ESS(num_h, mdl, set_max=self.gtxr_max, set_price=self.gtxr_price, pcs_price=0)

        self.cons_register(mdl)


    def cons_register(self, mdl):
        # self.dyzqfsqgtxr_set.cons_register(mdl)
        hrange = range(self.num_h)
        mdl.add_constraint(self.dyzqfsq_set >= 0)
        mdl.add_constraint(self.dyzqfsq_set <= self.set_max)
        mdl.add_constraints(self.p_dyzqfsq[h] >= 0 for h in hrange)
        mdl.add_constraints(self.p_dyzqfsq[h] <= self.dyzqfsq_set for h in hrange)  # 与天气相关
        mdl.add_constraints(self.p_dyzqfsq[h] + self.dyzqfsqgtxr_set.p_ess[h] == self.p_dyzqfsq_steam[h] for h in hrange)  # 槽式光热系统产生的高温
        mdl.add_constraints(0 <= self.p_dyzqfsq_steam[h] for h in hrange)  # 约束能量不能倒流
        mdl.add_constraints(self.ele_cost == self.p_dyzqfsq[h] * self.ele_price[h] for h in hrange)
        mdl.add_constraint(self.nianhua == self.dyzqfsq_set * self.set_price / 15 + self.dyzqfsqgtxr_set.nianhua + self.ele_cost)

class Exchanger(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES("exchanger")
        # k 传热系数
        Exchanger.index += 1

        self.num_h        = num_h
        self.set_price    = kwargs.get('set_price',None)
        self.exch_set_max = kwargs.get('set_max',None)

        self.exch_set = mdl.continuous_var(name='exchanger_set{0}'.format(Exchanger.index))
        self.nianhua  = mdl.continuous_var(name='exchanger_nianhua{0}'.format(Exchanger.index))
        self.h_exch   = mdl.continuous_var_list(list(range(num_h)), name='h_exchanger{0}'.format(Exchanger.index))

    def cons_register(self, mdl):
        hrange = range(self.num_h)
        mdl.add_constraint(self.exch_set >= 0)
        mdl.add_constraint(self.exch_set <= self.exch_set_max)
        mdl.add_constraints(self.h_exch[h] >= 0 for h in hrange)
        mdl.add_constraints(self.h_exch[h] <= self.exch_set for h in hrange)  # 天然气蒸汽锅炉
        mdl.add_constraint(self.nianhua == self.exch_set * self.set_price / 15)

# CHP设备
class CHP(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES('chp')
        CHP.index += 1

        self.num_h          = num_h
        self.chp_price      = kwargs.get('chp_price',None)
        self.gas_price      = kwargs.get('gas_price',None)
        self.chp_num_max    = kwargs.get('chp_num_max',None)
        self.chp_single_set = kwargs.get('chp_single_set',None)
        self.drratio        = kwargs.get('drratio',None)
        self.chp_down_ratio = 0.2

        self.chp_set        = mdl.continuous_var(name='chp_set{0}'.format(CHP.index))
        self.p_chp          = mdl.continuous_var_list(list(range(num_h)), name='p_chp{0}'.format(CHP.index))
        self.h_chp          = mdl.continuous_var_list(list(range(num_h)), name='h_chp{0}'.format(CHP.index))
        self.gas_chp        = mdl.continuous_var_list(list(range(num_h)), name='gas_chp{0}'.format(CHP.index))  # 时时耗气量
        self.chp_open_flag  = mdl.binary_var_list(list(range(num_h)),name='chp_open_flag{0}'.format(CHP.index))
        self.yqyrwater_flag = mdl.binary_var(name='yqyrwater_flag{0}'.format(CHP.index))
        self.yqyrsteam_flag = mdl.binary_var(name='yqyrsteam_flag{0}'.format(CHP.index))
        # 机组数量
        self.chp_run_num    = mdl.integer_var_list(list(range(num_h)),name='chp_run_num{0}'.format(CHP.index))
        self.chp_num        = mdl.integer_var(name='chp_num{0}'.format(CHP.index))
        self.nianhua        = mdl.continuous_var(name='chp_nianhua{0}'.format(CHP.index))
        self.gas_cost       = mdl.continuous_var(name='CHP_gas_cost{0}'.format(CHP.index))  # 燃气费用统计

        self.gts_set       = Exchanger(self.num_h, mdl, set_max=self.chp_set * 0.5, set_price=300)
        self.yqyrwater_set = Exchanger(self.num_h, mdl, set_max=self.chp_set * 0.5, set_price=300)
        self.yqyrsteam_set = Exchanger(self.num_h, mdl, set_max=self.chp_set * 0.5, set_price=300)

        self.cons_register(mdl)

    def cons_register(self, mdl):
        hrange = range(self.num_h)
        mdl.add_constraint(self.chp_num >= 0)
        mdl.add_constraint(self.chp_num <= self.chp_num_max)
        mdl.add_constraint(self.chp_set == self.chp_num * self.chp_single_set)
        mdl.add_constraints(self.chp_open_flag[h] * self.chp_single_set * self.chp_down_ratio <= self.p_chp[h] for h in hrange)
        # p_chp(1, h) <= chp_set * chp_open_flag(1, h) % chp功率限制, 采用线性化约束，有以下等效：
        mdl.add_constraints(self.p_chp[h] <= self.chp_set for h in hrange)
        mdl.add_constraints(self.p_chp[h] <= self.chp_open_flag[h] * BIGM for h in hrange)
        mdl.add_constraints(self.chp_run_num[h] * self.chp_single_set >= self.p_chp[h] for h in hrange)  # 确定CHP开启台数
        mdl.add_constraints( self.chp_run_num[h] * self.chp_single_set <= self.p_chp[h] + self.chp_single_set + 1 for h in hrange)  # 确定CHP开启台数
        mdl.add_constraints(0 <= self.chp_run_num[h] for h in hrange)
        mdl.add_constraints(self.chp_run_num[h] <= self.chp_num for h in hrange)
        mdl.add_constraints(self.p_chp[h] * self.drratio == self.h_chp[h] for h in hrange)
        mdl.add_constraints(self.gas_chp[h] == self.p_chp[h] / 3.5 for h in hrange)

        self.gas_cost = mdl.sum(self.gas_chp[h] * self.gas_price[h] for h in hrange)  # 统计燃气费用
        mdl.add_constraint(self.yqyrwater_flag + self.yqyrsteam_flag == 1)
        mdl.add_constraint(self.yqyrwater_set.exch_set <= self.yqyrwater_flag * BIGM)
        mdl.add_constraint(self.yqyrsteam_set.exch_set <= self.yqyrsteam_flag * BIGM)
        mdl.add_constraints(self.gts_set.h_exch[h] <= self.h_chp[h] * 0.5 for h in hrange)
        mdl.add_constraints(self.yqyrwater_set.h_exch[h] <= self.h_chp[h] * 0.5 for h in hrange)
        mdl.add_constraints(self.yqyrsteam_set.h_exch[h] <= self.h_chp[h] * 0.5 for h in hrange)

        mdl.add_constraint(self.nianhua == self.chp_num * self.chp_single_set * self.chp_price / 15 + self.gts_set.nianhua + self.yqyrwater_set.nianhua + self.yqyrsteam_set.nianhua + self.gas_cost * 8760 / self.num_h)

# 燃气锅炉：蒸汽，热水
class Gasgl(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES("gasgl")
        Gasgl.index += 1

        self.num_h       = num_h
        self.set_max     = kwargs.get('set_max',None)
        self.gasgl_price = kwargs.get('gasgl_price',None)
        self.gas_price   = kwargs.get('gas_price',None)
        self.eff         = kwargs.get('eff',0.9)

        self.gasgl_set = mdl.continuous_var(name='gasgl_set{0}'.format(Gasgl.index))
        self.h_gasgl   = mdl.continuous_var_list(list(range(num_h)),name='h_gasgl{0}'.format(Gasgl.index))
        self.gas_gasgl = mdl.continuous_var_list(list(range(num_h)),name='gas_gasgl{0}'.format(Gasgl.index))  # 时时耗气量

        self.gas_cost  = mdl.continuous_var(name='gasgl_gas_cost{0}'.format(Gasgl.index))
        self.nianhua   = mdl.continuous_var(name='gasgl_nianhua{0}'.format(Gasgl.index))

        self.cons_register(mdl)

    def cons_register(self, mdl):
        hrange = range(self.num_h)
        mdl.add_constraint(self.gasgl_set >= 0)
        mdl.add_constraint(self.gasgl_set <= self.set_max)
        mdl.add_constraints(self.h_gasgl[h] >= 0 for h in hrange)
        mdl.add_constraints(self.h_gasgl[h] <= self.gasgl_set for h in hrange)  # 天然气蒸汽锅炉
        mdl.add_constraints(self.gas_gasgl[h] == self.h_gasgl[h] / (10 * self.eff) for h in hrange)
        self.gas_cost = mdl.sum(self.gas_gasgl[h] * self.gas_price[h] for h in hrange)
        mdl.add_constraint(self.nianhua == self.gasgl_set * self.gasgl_price / 15 + self.gas_cost * 8760 / self.num_h)

# 适用于市政蒸汽，市政热水
class CitySupply(IGES):
    index = 0

    def __init__(self, num_h, mdl,**kwargs):
        IGES("city_supply")
        CitySupply.index += 1

        self.num_h     = num_h
        self.set_max   = kwargs.get('set_max',None)
        self.run_price = kwargs.get('run_price',None)
        self.set_price = kwargs.get('set_price',None)
        self.eff       = kwargs.get('eff',0.9)

        self.citysupply_set    = mdl.continuous_var(name='citysupply_set{0}'.format(CitySupply.index))
        self.h_citysupply      = mdl.continuous_var_list(list(range(num_h)), name='h_citysupply{0}'.format(CitySupply.index))
        self.h_citysupply_from = mdl.continuous_var_list(list(range(num_h)),name='h_citysupply_from{0}'.format(CitySupply.index))
        self.citysupply_cost   = mdl.continuous_var(name='citysupply_cost{0}'.format(CitySupply.index))
        self.nianhua           = mdl.continuous_var(name='citysupply_nianhua{0}'.format(CitySupply.index))

        self.cons_register(mdl)

    def cons_register(self, mdl):
        hrange = range(self.num_h)
        mdl.add_constraint(self.citysupply_set >= 0)
        mdl.add_constraint(self.citysupply_set <= self.set_max)
        mdl.add_constraints(self.h_citysupply[h] >= 0 for h in hrange)
        mdl.add_constraints(self.h_citysupply[h] <= self.citysupply_set for h in hrange)
        mdl.add_constraints(self.h_citysupply[h] == self.h_citysupply_from[h] / self.eff for h in hrange)
        self.citysupply_cost = mdl.sum(self.h_citysupply_from[h] * self.run_price[h] for h in hrange)
        mdl.add_constraint(self.nianhua == self.citysupply_set * self.set_price / 15 + self.citysupply_cost * 8760 / self.num_h)

# 溴化锂
class LiBrRefrigeration(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES('LiBrRefrigeration')
        LiBrRefrigeration.index += 1
        self.num_h = num_h
        self.set_max   = kwargs.get('set_max',None)
        self.set_price = kwargs.get('set_price',None)
        self.eff       = kwargs.get('eff',0.9)

        self.xhl_set    = mdl.continuous_var(name='xhl_set{0}'.format(LiBrRefrigeration.index))
        self.h_xhl_from = mdl.continuous_var_list(list(range(num_h)),name='h_xhl_from{0}'.format(LiBrRefrigeration.index))
        self.c_xhl      = mdl.continuous_var_list(list(range(num_h)),name='h_xhl{0}'.format(LiBrRefrigeration.index))
        self.nianhua    = mdl.continuous_var(name='xhl_nianhua{0}'.format(LiBrRefrigeration.index))

        self.cons_register(mdl)

    def cons_register(self, mdl):
        hrange = range(self.num_h)
        mdl.add_constraint(self.xhl_set >= 0)
        mdl.add_constraint(self.xhl_set <= self.set_max)
        mdl.add_constraints(self.h_xhl_from[h] >= 0 for h in hrange)
        mdl.add_constraints(self.h_xhl_from[h] <= self.xhl_set for h in hrange)
        mdl.add_constraints(self.c_xhl[h] == self.h_xhl_from[h] / self.eff for h in hrange)
        mdl.add_constraint(self.nianhua == self.xhl_set * self.set_price / 15)

# 电锅炉
class Dgl(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES('dgl')
        Dgl.index += 1

        self.num_h       = num_h
        self.gas_set_max = kwargs.get('set_max',None)
        self.dgl_price   = kwargs.get('dgl_price',None)
        self.ele_price   = kwargs.get('ele_price',None)
        self.eff         = kwargs.get('eff',0.9)

        self.dgl_set  = mdl.continuous_var(name='dgl_set{0}'.format(Dgl.index))
        self.h_dgl    = mdl.continuous_var_list(list(range(num_h)), name='h_dgl{0}'.format(Dgl.index))
        self.ele_dgl  = mdl.continuous_var_list(list(range(num_h)),name='ele_dgl{0}'.format(Dgl.index))  # 时时耗气量
        self.ele_cost = mdl.continuous_var(name='ele_cost{0}'.format(Dgl.index))
        self.nianhua  = mdl.continuous_var(name='dgl_nianhua{0}'.format(Dgl.index))

        self.cons_register(mdl)

    def cons_register(self, mdl):
        hrange = range(self.num_h)
        mdl.add_constraint(self.dgl_set >= 0)
        mdl.add_constraint(self.dgl_set <= self.gas_set_max)
        mdl.add_constraints(self.h_dgl[h] >= 0 for h in hrange)
        mdl.add_constraints(self.h_dgl[h] <= self.dgl_set for h in hrange)  # 天然气蒸汽锅炉
        mdl.add_constraints(self.ele_dgl[h] == self.h_dgl[h] / self.eff for h in hrange)
        self.ele_cost = mdl.sum(self.ele_dgl[h] * self.ele_price[h] for h in hrange)
        mdl.add_constraint(self.nianhua == self.dgl_set * self.dgl_price / 15 + self.ele_cost * 8760 / self.num_h)


# 可变容量储能
class ESSVariable(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES('ess_variable')
        ESSVariable.index += 1
        self.num_h       = num_h
        self.set_max   = kwargs.get('set_max',None)
        self.ess_price = kwargs.get('ess_price',None)
        self.pcs_price = kwargs.get('pcs_price',None)
        # 效率
        self.c_rate_max = kwargs.get('c_rate_max',2)
        self.eff        = kwargs.get('eff',0.9)
        self.ess_init   = kwargs.get('ess_init',1)
        self.soc_min    = kwargs.get('soc_min',0)
        self.soc_max    = kwargs.get('soc_max',1)

        self.ess_set   = mdl.continuous_var_list(list(range(num_h)),name='essVariable_set{0}'.format(ESSVariable.index))
        self.p_ess     = mdl.continuous_var_list(list(range(num_h)), lb=-BIGM,name='p_essVariable{0}'.format(ESSVariable.index))
        # 充电功率
        self.p_ess_ch  = mdl.continuous_var_list(list(range(num_h)),name='p_essVariable_ch{0}'.format(ESSVariable.index))
        # 放电功率
        self.p_ess_dis = mdl.continuous_var_list(list(range(num_h)),name='p_essVariable_dis{0}'.format(ESSVariable.index))
        # 能量
        self.ess       = mdl.continuous_var_list(list(range(num_h)),name='essVariable{0}'.format(ESSVariable.index))
        self.pcs_set   = mdl.continuous_var_list(list(range(num_h)),name='pcs_setVariable{0}'.format(ESSVariable.index))  # pcs
        self.ch_flag   = mdl.binary_var_list(list(range(num_h)),name='bessVariable_ch_flag{0}'.format(ESSVariable.index))  # 充电
        self.dis_flag  = mdl.binary_var_list(list(range(num_h)),name='bessVariable_dis_flag{0}'.format(ESSVariable.index))  # 放电
        self.cons_register(mdl)

    def cons_register(self, mdl, period=1, day_node=24):
        bigM = 1e10
        irange = range(self.num_h)
        mdl.add_constraints(self.ess_set[i] <= self.set_max for i in irange)
        mdl.add_constraints(self.ess_set[i] >= 0 for i in irange)
        mdl.add_constraints(self.ess_set[i] * self.c_rate_max >= self.pcs_set[i] for i in irange)
        mdl.add_constraints(self.pcs_set[i] >= 0 for i in irange)
        # 功率拆分
        mdl.add_constraints(self.p_ess[i] == -self.p_ess_ch[i] + self.p_ess_dis[i] for i in irange)

        mdl.add_constraints(self.p_ess_ch[i] >= 0 for i in irange)
        mdl.add_constraints(self.p_ess_ch[i] <= self.ch_flag[i] * bigM for i in irange)
        mdl.add_constraints(self.p_ess_ch[i] <= self.pcs_set[i] for i in irange)

        mdl.add_constraints(self.p_ess_dis[i] >= 0 for i in irange)
        mdl.add_constraints(self.p_ess_dis[i] <= self.dis_flag[i] * bigM for i in irange)
        mdl.add_constraints(self.p_ess_dis[i] <= self.pcs_set[i] for i in irange)

        mdl.add_constraints(self.ch_flag[i] + self.dis_flag[i] == 1 for i in irange)
        for day in range(1, int(self.num_h / day_node) + 1):
            mdl.add_constraints(self.ess[i] == self.ess[i - 1] + (self.p_ess_ch[i] * self.eff - self.p_ess_dis[i] / self.eff) *  SIMULATIONT / 3600
                                for i in range(1 + day_node * (day - 1), day_node * day))
        mdl.add_constraints(self.ess[0] == self.ess_init * self.ess_set[i] for i in range(1, self.num_h))

        mdl.add_constraints(self.ess[i] <= self.ess_set[i] * self.soc_max for i in range(1, self.num_h))
        mdl.add_constraints(self.ess[i] >= self.ess_set[i] * self.soc_min for i in range(1, self.num_h))

        # 两天之间直接割裂，没有啥关系
        if period == 1:
            mdl.add_constraints(
                self.ess[i] == self.ess[i - (day_node - 1)] for i in range(day_node - 1, self.num_h, day_node))
        else:
            # 初始值
            mdl.add_constraint(self.ess[0] == self.ess_init * self.ess_set)
            # 两天之间的连接
            mdl.add_constraints(self.ess[i] == self.ess[i - 1] + (self.p_ess_ch[i] * self.eff - self.p_ess_dis[i] / self.eff) * SIMULATIONT / 3600
                                                        for i in range(day_node, self.num_h, day_node))

# 水蓄能罐，可变容量的储能体
class WaterEnergyStorage(IGES):
    # index=0
    def __init__(self, num_h, mdl, **kwargs):
        IGES('water_energy_storage')
        self.num_h   = num_h
        self.set_max = kwargs.get('set_max',None)
        self.v_price = kwargs.get('v_price',None)
        pcs_price    = kwargs.get('pcs_price',None)
        c_rate_max   = kwargs.get('c_rate_max',0.5)

        self.ratio_cool  = kwargs.get('ratio_cool',10)
        self.ratio_heat  = kwargs.get('ratio_heat',10)
        self.ratio_gheat = kwargs.get('ratio_gheat',20)

        # 对于水蓄能，优化的变量为水罐的体积
        self.sx = ESSVariable(num_h, mdl, set_max=self.set_max,ess_price=0,pcs_price=pcs_price,c_rate_max=c_rate_max)
        self.index = ESSVariable.index

        self.sx_set_cool  = mdl.continuous_var_list(list(range(num_h)),name='sx_set_cool{0}'.format(self.index))
        self.sx_set_heat  = mdl.continuous_var_list(list(range(num_h)),name='sx_set_heat{0}'.format(self.index))
        self.sx_set_gheat = mdl.continuous_var_list(list(range(num_h)),name='sx_set_gheat{0}'.format(self.index))

        self.sx_V          = mdl.continuous_var(name='sx_V{0}'.format(self.index))
        self.sx_cool_flag  = mdl.binary_var_list(list(range(num_h)),name='sx_cool_flag{0}'.format(self.index))
        self.sx_heat_flag  = mdl.binary_var_list(list(range(num_h)),name='sx_heat_flag{0}'.format(self.index))
        self.sx_gheat_flag = mdl.binary_var_list(list(range(num_h)),name='sx_gheat_flag{0}'.format(self.index))

        self.p_sx_cool  = mdl.continuous_var_list(list(range(num_h)),name='p_sx_cool{0}'.format(self.index))
        self.p_sx_heat  = mdl.continuous_var_list(list(range(num_h)),name='p_sx_heat{0}'.format(self.index))
        self.p_sx_gheat = mdl.continuous_var_list(list(range(num_h)),name='p_sx_gheat{0}'.format(self.index))
        self.nianhua    = mdl.continuous_var(name='p_sx_nianhua{0}'.format(self.index))
        self.cons_regester(mdl)

    def cons_regester(self, mdl, period=1, day_node=24):
        bigM = 1e10
        hrange = range(self.num_h)
        # self.sx.cons_register(mdl, period, day_node)
        # sx_set[h] == sx_cool_flag[h] * sx_V * ratio_cool + sx_heat_flag[h] * sx_V * ratio_heat + sx_gheat_flag[
        #   h] * sx_V * ratio_gheat
        # 用下面的式子进行线性化
        mdl.add_constraint(self.sx_V <= self.set_max)
        mdl.add_constraint(self.sx_V >= 0)
        mdl.add_constraints(self.sx.ess_set[h] == self.sx_set_cool[h] + self.sx_set_heat[h] + self.sx_set_gheat[h] for h in hrange)
        # (1)
        mdl.add_constraints(self.sx_set_cool[h] <= self.sx_V * self.ratio_cool for h in hrange)
        mdl.add_constraints(self.sx_set_cool[h] <= self.sx_cool_flag[h] * bigM for h in hrange)
        mdl.add_constraints(self.sx_set_cool[h] >= 0 for h in hrange)
        mdl.add_constraints(self.sx_set_cool[h] >= self.sx_V * self.ratio_cool - (1 - self.sx_cool_flag[h]) * bigM for h in hrange)
        # (2)
        mdl.add_constraints(self.sx_set_heat[h] <= self.sx_V * self.ratio_heat for h in hrange)
        mdl.add_constraints(self.sx_set_heat[h] <= self.sx_heat_flag[h] * bigM for h in hrange)
        mdl.add_constraints(self.sx_set_heat[h] >= 0 for h in hrange)
        mdl.add_constraints(self.sx_set_heat[h] >= self.sx_V * self.ratio_heat - (1 - self.sx_heat_flag[h]) * bigM for h in hrange)
        # (3)
        mdl.add_constraints(self.sx_set_gheat[h] <= self.sx_V * self.ratio_gheat for h in hrange)
        mdl.add_constraints(self.sx_set_gheat[h] <= self.sx_gheat_flag[h] * bigM for h in hrange)
        mdl.add_constraints(self.sx_set_gheat[h] >= 0 for h in hrange)
        mdl.add_constraints(self.sx_set_gheat[h] >= self.sx_V * self.ratio_gheat - (1 - self.sx_gheat_flag[h]) * bigM for h in hrange)
        # % %
        mdl.add_constraints(self.sx_cool_flag[h] + self.sx_heat_flag[h] + self.sx_gheat_flag[h] == 1 for h in hrange)  # % 三个方面进行核算。
        # （1） p_sx_cool[h] == p_sx[h] * sx_cool_flag[h]
        # （2）p_sx_heat[h] == p_sx[h] * sx_heat_flag[h]
        # （3）p_sx_gheat[h] == p_sx[h] * sx_gheat_flag[h]
        # 上面的公式进行线性化后，用下面的公式替代
        # (1)
        mdl.add_constraints(-bigM * self.sx_cool_flag[h] <= self.p_sx_cool[h] for h in hrange)
        mdl.add_constraints(self.p_sx_cool[h] <= bigM * self.sx_cool_flag[h] for h in hrange)
        mdl.add_constraints(self.sx.p_ess[h] - (1 - self.sx_cool_flag[h]) * bigM <= self.p_sx_cool[h] for h in hrange)
        mdl.add_constraints(self.p_sx_cool[h] <= self.sx.p_ess[h] + (1 - self.sx_cool_flag[h]) * bigM for h in hrange)
        # (2)
        mdl.add_constraints(-bigM * self.sx_heat_flag[h] <= self.p_sx_heat[h] for h in hrange)
        mdl.add_constraints(self.p_sx_heat[h] <= bigM * self.sx_heat_flag[h] for h in hrange)
        mdl.add_constraints(self.sx.p_ess[h] - (1 - self.sx_heat_flag[h]) * bigM <= self.p_sx_heat[h] for h in hrange)
        mdl.add_constraints(self.p_sx_heat[h] <= self.sx.p_ess[h] + (1 - self.sx_heat_flag[h]) * bigM for h in hrange)
        # (3)
        mdl.add_constraints(-bigM * self.sx_gheat_flag[h] <= self.p_sx_gheat[h] for h in hrange)
        mdl.add_constraints(self.p_sx_gheat[h] <= bigM * self.sx_gheat_flag[h] for h in hrange)
        mdl.add_constraints(self.sx.p_ess[h] - (1 - self.sx_gheat_flag[h]) * bigM <= self.p_sx_gheat[h] for h in hrange)
        mdl.add_constraints(self.p_sx_gheat[h] <= self.sx.p_ess[h] + (1 - self.sx_gheat_flag[h]) * bigM for h in hrange)
        mdl.add_constraint(self.nianhua == self.sx_V * self.v_price / 20)

# 水源热泵
class WaterHeatPump(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES('water_heat_pump')
        # case_ratio 不同工况下制热量/制冷量的比值
        WaterHeatPump.index += 1

        self.num_h      = num_h
        self.set_max    = kwargs.get('set_max',None)
        self.set_price  = kwargs.get('set_price',None)
        self.ele_price  = kwargs.get('ele_price',None)
        self.case_ratio = kwargs.get('case_ratio',np.ones(4))
        self.cop_sy_cool  = 5
        self.cop_sy_xcool = 5
        self.cop_sy_heat  = 5
        self.cop_sy_xheat = 5

        self.sy_set   = mdl.continuous_var(name='sy_set{0}'.format(WaterHeatPump.index))
        self.nianhua  = mdl.continuous_var(name='WaterHeatPump_nianhua{0}'.format(WaterHeatPump.index))
        self.ele_cost = mdl.continuous_var(name='WaterHeatPump_ele_sum{0}'.format(WaterHeatPump.index))

        self.p_sy_cool     = mdl.continuous_var_list(list(range(num_h)),name='p_sy_cool{0}'.format(WaterHeatPump.index))
        self.sy_cool_flag  = mdl.binary_var_list(list(range(num_h)),name='sy_cool_flag{0}'.format(WaterHeatPump.index))
        self.p_sy_xcool    = mdl.continuous_var_list(list(range(num_h)),name='p_sy_xcool{0}'.format(WaterHeatPump.index))
        self.sy_xcool_flag = mdl.binary_var_list(list(range(num_h)),name='sy_xcool_flag{0}'.format(WaterHeatPump.index))
        self.p_sy_heat     = mdl.continuous_var_list(list(range(num_h)),name='p_sy_heat{0}'.format(WaterHeatPump.index))
        self.sy_heat_flag  = mdl.binary_var_list(list(range(num_h)),name='sy_heat_flag{0}'.format(WaterHeatPump.index))
        self.p_sy_xheat    = mdl.continuous_var_list(list(range(num_h)),name='p_sy_xheat{0}'.format(WaterHeatPump.index))

        self.sy_xheat_flag = mdl.binary_var_list(list(range(num_h)),name='sy_xheat_flag{0}'.format(WaterHeatPump.index))
        self.ele_sy        = mdl.continuous_var_list(list(range(num_h)),name='ele_sy{0}'.format(WaterHeatPump.index))
        self.p_sy          = mdl.continuous_var_list(list(range(num_h)),name='p_sy{0}'.format(WaterHeatPump.index))

        self.cons_register(mdl)

    def cons_register(self, mdl):

        hrange = range(self.num_h)
        mdl.add_constraint(0 <= self.sy_set)
        mdl.add_constraint(self.sy_set <= self.set_max)

        mdl.add_constraints(0 <= self.p_sy_cool[h] for h in hrange)
        mdl.add_constraints(self.p_sy_cool[h] <= self.sy_set * self.case_ratio[0] for h in hrange)
        mdl.add_constraints(self.p_sy_cool[h] <= BIGM * self.sy_cool_flag[h] for h in hrange)

        mdl.add_constraints(0 <= self.p_sy_xcool[h] for h in hrange)
        mdl.add_constraints(self.p_sy_xcool[h] <= self.sy_set * self.case_ratio[1] for h in hrange)
        mdl.add_constraints(self.p_sy_xcool[h] <= BIGM * self.sy_xcool_flag[h] for h in hrange)

        mdl.add_constraints(0 <= self.p_sy_heat[h] for h in hrange)
        mdl.add_constraints(self.p_sy_heat[h] <= self.sy_set * self.case_ratio[2] for h in hrange)
        mdl.add_constraints(self.p_sy_heat[h] <= BIGM * self.sy_heat_flag[h] for h in hrange)

        mdl.add_constraints(0 <= self.p_sy_xheat[h] for h in hrange)
        mdl.add_constraints(self.p_sy_xheat[h] <= self.sy_set * self.case_ratio[3] for h in hrange)
        mdl.add_constraints(self.p_sy_xheat[h] <= BIGM * self.sy_xheat_flag[h] for h in hrange)

        mdl.add_constraints(self.sy_cool_flag[h] + self.sy_xcool_flag[h] + self.sy_heat_flag[h] + self.sy_xheat_flag[h] == 1 for h in hrange)
        mdl.add_constraints(self.ele_sy[h] == self.p_sy_cool[h] / self.cop_sy_cool + self.p_sy_xcool[h] / self.cop_sy_xcool + \
                                                self.p_sy_heat[h] / self.cop_sy_heat + self.p_sy_xheat[h] / self.cop_sy_xheat for h in hrange)
        mdl.add_constraints(self.p_sy[h] == self.p_sy_cool[h] + self.p_sy_xcool[h] + self.p_sy_heat[h] + self.p_sy_xheat[h] for h in hrange)

        self.ele_cost = mdl.sum(self.ele_sy[h] * self.ele_price[h] for h in hrange)
        # 年化
        mdl.add_constraint(self.nianhua == self.sy_set * self.set_price / 15 + self.ele_cost * 8760 / self.num_h)

# 水冷螺杆机
class WaterCooledScrew(IGES):
    index = 0

    def __init__(self, num_h, mdl,**kwargs):
        IGES('water_cooled_screw')

        WaterCooledScrew.index += 1

        self.num_h      = num_h
        self.set_price  = kwargs.get('set_price',None)
        self.ele_price  = kwargs.get('ele_price',None)
        self.set_max    = kwargs.get('set_max',None)
        self.case_ratio = kwargs.get('case_ratio',np.array([1, 0.8]))

        self.cop_slj_cool  = 5
        self.cop_slj_xcool = 5

        self.slj_set        = mdl.continuous_var(name='slj_set{0}'.format(WaterCooledScrew.index))
        self.nianhua        = mdl.continuous_var(name='WaterCooledScrew_nianhua{0}'.format(WaterCooledScrew.index))
        self.ele_cost       = mdl.continuous_var(name='WaterCooledScrew_ele_sum{0}'.format(WaterCooledScrew.index))

        self.p_slj_cool     = mdl.continuous_var_list(list(range(num_h)),name='p_slj_cool{0}'.format(WaterCooledScrew.index))
        self.slj_cool_flag  = mdl.binary_var_list(list(range(num_h)),name='slj_cool_flag{0}'.format(WaterCooledScrew.index))
        self.p_slj_xcool    = mdl.continuous_var_list(list(range(num_h)),name='p_slj_xcool{0}'.format(WaterCooledScrew.index))
        self.slj_xcool_flag = mdl.binary_var_list(list(range(num_h)),name='slj_xcool_flag{0}'.format(WaterCooledScrew.index))
        self.ele_slj        = mdl.continuous_var_list(list(range(num_h)),name='ele_slj{0}'.format(WaterCooledScrew.index))
        self.p_slj          = mdl.continuous_var_list(list(range(num_h)),name='p_slj{0}'.format(WaterCooledScrew.index))

        self.cons_register(mdl)

    def cons_register(self, mdl):
        hrange = range(self.num_h)
        mdl.add_constraint(0 <= self.slj_set)
        mdl.add_constraint(self.slj_set <= self.set_max)

        mdl.add_constraints(0 <= self.p_slj_cool[h] for h in hrange)
        mdl.add_constraints(self.p_slj_cool[h] <= self.slj_set * self.case_ratio[0] for h in hrange)
        mdl.add_constraints(self.p_slj_cool[h] <= BIGM * self.slj_cool_flag[h] for h in hrange)

        mdl.add_constraints(0 <= self.p_slj_xcool[h] for h in hrange)
        mdl.add_constraints(self.p_slj_xcool[h] <= self.slj_set * self.case_ratio[1] for h in hrange)
        mdl.add_constraints(self.p_slj_xcool[h] <= BIGM * self.slj_xcool_flag[h] for h in hrange)

        mdl.add_constraints(self.slj_cool_flag[h] + self.slj_xcool_flag[h] == 1 for h in hrange)
        mdl.add_constraints(self.ele_slj[h] == self.p_slj_cool[h] / self.cop_slj_cool + self.p_slj_xcool[h] / self.cop_slj_xcool for h in hrange)
        mdl.add_constraints(self.p_slj[h] == self.p_slj_cool[h] + self.p_slj_xcool[h] for h in hrange)

        self.ele_cost = mdl.sum(self.ele_slj[h] * self.ele_price[h] for h in hrange)
        # 年化
        mdl.add_constraint(self.nianhua == self.slj_set * self.set_price / 15 + self.ele_cost * 8760 / self.num_h)


class ThreeGK(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES('threegk')
        ThreeGK.index += 1

        self.num_h = num_h
        self.set_max    = kwargs.get('set_max',None)
        self.set_price  = kwargs.get('set_price',None)
        self.ele_price  = kwargs.get('ele_price',None)
        self.case_ratio = kwargs.get('case_ratio',[1, 0.8, 0.8])

        self.cop_threegk_cool = 5
        self.cop_threegk_ice  = 4
        self.cop_threegk_heat = 5

        self.threegk_set = mdl.continuous_var(name='threegk_set{0}'.format(ThreeGK.index))
        self.nianhua     = mdl.continuous_var(name='ThreeGK_nianhua{0}'.format(ThreeGK.index))
        self.ele_cost    = mdl.continuous_var(name='ThreeGK_ele_sum{0}'.format(ThreeGK.index))

        self.p_threegk_cool    = mdl.continuous_var_list(list(range(num_h)),name='p_threegk_cool{0}'.format(ThreeGK.index))
        self.threegk_cool_flag = mdl.binary_var_list(list(range(num_h)),name='threegk_cool_flag{0}'.format(ThreeGK.index))
        self.p_threegk_ice     = mdl.continuous_var_list(list(range(num_h)),name='p_threegk_ice{0}'.format(ThreeGK.index))
        self.threegk_ice_flag  = mdl.binary_var_list(list(range(num_h)),name='threegk_ice_flag{0}'.format(ThreeGK.index))
        self.p_threegk_heat    = mdl.continuous_var_list(list(range(num_h)),name='p_threegk_heat{0}'.format(ThreeGK.index))
        self.threegk_heat_flag = mdl.binary_var_list(list(range(num_h)),name='threegk_heat_flag{0}'.format(ThreeGK.index))
        self.ele_threegk       = mdl.continuous_var_list(list(range(num_h)),name='ele_threegk{0}'.format(ThreeGK.index))
        self.p_threegk         = mdl.continuous_var_list(list(range(num_h)),name='p_threegk{0}'.format(ThreeGK.index))

        self.cons_register(mdl)

    def cons_register(self, mdl):
        hrange = range(self.num_h)
        mdl.add_constraint(0 <= self.threegk_set)
        mdl.add_constraint(self.threegk_set <= self.set_max)

        mdl.add_constraints(0 <= self.p_threegk_cool[h] for h in hrange)
        mdl.add_constraints(self.p_threegk_cool[h] <= self.threegk_set * self.case_ratio[0] for h in hrange)
        mdl.add_constraints(self.p_threegk_cool[h] <= BIGM * self.threegk_cool_flag[h] for h in hrange)

        mdl.add_constraints(0 <= self.p_threegk_ice[h] for h in hrange)
        mdl.add_constraints(self.p_threegk_ice[h] <= self.threegk_set * self.case_ratio[1] for h in hrange)
        mdl.add_constraints(self.p_threegk_ice[h] <= BIGM * self.threegk_ice_flag[h] for h in hrange)

        mdl.add_constraints(0 <= self.p_threegk_heat[h] for h in hrange)
        mdl.add_constraints(self.p_threegk_heat[h] <= self.threegk_set * self.case_ratio[2] for h in hrange)
        mdl.add_constraints(self.p_threegk_heat[h] <= BIGM * self.threegk_heat_flag[h] for h in hrange)

        mdl.add_constraints(self.threegk_cool_flag[h] + self.threegk_ice_flag[h] + self.threegk_heat_flag[h] == 1 for h in hrange)
        mdl.add_constraints(self.ele_threegk[h] == self.p_threegk_cool[h] / self.cop_threegk_cool + self.p_threegk_ice[h] / self.cop_threegk_ice + self.p_threegk_heat[h] / self.cop_threegk_heat for h in hrange)
        mdl.add_constraints(self.p_threegk[h] == self.p_threegk_cool[h] + self.p_threegk_ice[h] + self.p_threegk_heat[h] for h in hrange)

        self.ele_cost = mdl.sum(self.ele_threegk[h] * self.ele_price[h] for h in hrange)
        # 年化
        mdl.add_constraint(self.nianhua == self.threegk_set * self.set_price / 15 + self.ele_cost * 8760 / self.num_h)

# 双工况机组
class DoubleGK(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES('doublegk')

        DoubleGK.index += 1

        self.num_h      = num_h
        self.set_max    = kwargs.get('set_max',None)
        self.ele_price  = kwargs.get('ele_price',None)
        self.set_price  = kwargs.get('set_price',None)
        self.case_ratio = kwargs.get('case_ratio', [1, 0.8])

        self.cop_doublegk_cool = 5
        self.cop_doublegk_ice = 5

        self.doublegk_set       = mdl.continuous_var(name='doublegk_set{0}'.format(DoubleGK.index))
        self.nianhua            = mdl.continuous_var(name='DoubleGK_nianhua{0}'.format(DoubleGK.index))
        self.ele_cost           = mdl.continuous_var(name='DoubleGK_ele_sum{0}'.format(DoubleGK.index))
        self.p_doublegk_cool    = mdl.continuous_var_list(list(range(num_h)),name='p_doublegk_cool{0}'.format(DoubleGK.index))
        self.doublegk_cool_flag = mdl.binary_var_list(list(range(num_h)),name='doublegk_cool_flag{0}'.format(DoubleGK.index))
        self.p_doublegk_ice     = mdl.continuous_var_list(list(range(num_h)),name='p_doublegk_ice{0}'.format(DoubleGK.index))
        self.doublegk_ice_flag  = mdl.binary_var_list(list(range(num_h)),name='doublegk_ice_flag{0}'.format(DoubleGK.index))
        self.ele_doublegk       = mdl.continuous_var_list(list(range(num_h)),name='ele_doublegk{0}'.format(DoubleGK.index))
        self.p_doublegk         = mdl.continuous_var_list(list(range(num_h)),name='p_doublegk{0}'.format(DoubleGK.index))

        self.cons_register(mdl)

    # 三工况机组
    def cons_register(self, mdl):
        hrange = range(self.num_h)
        mdl.add_constraint(0 <= self.doublegk_set)
        mdl.add_constraint(self.doublegk_set <= self.set_max)

        mdl.add_constraints(0 <= self.p_doublegk_cool[h] for h in hrange)
        mdl.add_constraints(self.p_doublegk_cool[h] <= self.doublegk_set * self.case_ratio[0] for h in hrange)
        mdl.add_constraints(self.p_doublegk_cool[h] <= BIGM * self.doublegk_cool_flag[h] for h in hrange)

        mdl.add_constraints(0 <= self.p_doublegk_ice[h] for h in hrange)
        mdl.add_constraints(self.p_doublegk_ice[h] <= self.doublegk_set * self.case_ratio[1] for h in hrange)
        mdl.add_constraints(self.p_doublegk_ice[h] <= BIGM * self.doublegk_ice_flag[h] for h in hrange)

        mdl.add_constraints(self.doublegk_cool_flag[h] + self.doublegk_ice_flag[h] == 1 for h in hrange)
        mdl.add_constraints(self.ele_doublegk[h] == self.p_doublegk_cool[h] / self.cop_doublegk_cool + self.p_doublegk_ice[h] / self.cop_doublegk_ice for h in hrange)
        mdl.add_constraints(self.p_doublegk[h] == self.p_doublegk_cool[h] + self.p_doublegk_ice[h] for h in hrange)

        self.ele_cost = mdl.sum(self.ele_doublegk[h] * self.ele_price[h] for h in hrange)
        # 年化
        mdl.add_constraint(self.nianhua == self.doublegk_set * self.set_price / 15 + self.ele_cost * 8760 / self.num_h)


class GeothermalHeatPump(IGES):
    index = 0

    def __init__(self, num_h, mdl, **kwargs):
        IGES('geothermal_heat_pump')

        GeothermalHeatPump.index += 1

        self.num_h = num_h
        self.set_max   = kwargs.get('set_max',None)
        self.set_price = kwargs.get('set_price',None)
        self.ele_price = kwargs.get('ele_price',None)
        self.cop_dire = 5

        self.dire_set = mdl.continuous_var(name='dire_set{0}'.format(GeothermalHeatPump.index))
        self.nianhua  = mdl.continuous_var(name='GeothermalHeatPump_nianhua{0}'.format(GeothermalHeatPump.index))
        self.ele_cost = mdl.continuous_var(name='GeothermalHeatPump_ele_sum{0}'.format(GeothermalHeatPump.index))

        self.ele_dire = mdl.continuous_var_list(list(range(num_h)),name='ele_dire{0}'.format(GeothermalHeatPump.index))
        self.p_dire   = mdl.continuous_var_list(list(range(num_h)), name='p_dire{0}'.format(GeothermalHeatPump.index))

        self.cons_register(mdl)


    def cons_register(self, mdl):
        hrange = range(self.num_h)

        mdl.add_constraint(0 <= self.dire_set)
        mdl.add_constraint(self.dire_set <= self.set_max)

        mdl.add_constraints(0 <= self.p_dire[h] for h in hrange)
        mdl.add_constraints(self.p_dire[h] <= self.dire_set for h in hrange)

        mdl.add_constraints(self.ele_dire[h] == self.p_dire[h] / self.cop_dire for h in hrange)
        self.ele_cost = mdl.sum(self.ele_dire[h] * self.ele_price[h] for h in hrange)
        # 年化
        mdl.add_constraint(self.nianhua == self.dire_set * self.set_price / 15 + self.ele_cost * 8760 / self.num_h)


class Linearization(object):
    bigM0 = 1e10
    index = 0
    def product_var_bin(self, mdl, var_bin, var, bin):
        Linearization.inxex += 1
        mdl.add_constraint(var_bin >= 0)
        mdl.add_constraint(var_bin >= var - (1 - bin) * self.bigM0)
        mdl.add_constraint(var_bin <= var)
        mdl.add_constraint(var_bin <= bin * self.bigM0)

    def product_var_bins(self, mdl, var_bin, var, bin0, irange):
        Linearization.inxex += 1
        mdl.add_constraints(var_bin[i] >= 0 for i in irange)
        mdl.add_constraints(var_bin[i] >= var[i] - (1 - bin0[i]) * self.bigM0 for i in irange)
        mdl.add_constraints(var_bin[i] <= var[i] for i in irange)
        mdl.add_constraints(var_bin[i] <= bin0[i] * self.bigM0 for i in irange)

    def product_var_back_bins(self, mdl, var_bin, var, bin0, irangeback):
        Linearization.inxex += 1
        mdl.add_constraints(var_bin[i] >= 0 for i in irangeback)
        mdl.add_constraints(var_bin[i] >= var[i - 1] - (1 - bin0[i]) * self.bigM0 for i in irangeback)
        mdl.add_constraints(var_bin[i] <= var[i - 1] for i in irangeback)
        mdl.add_constraints(var_bin[i] <= bin0[i] * self.bigM0 for i in irangeback)

    def max_zeros(self, num_h, mdl, x, y):
        Linearization.index += 1
        y_flag = mdl.binary_var_list([i for i in range(0, num_h)], name='y_flag{0}'.format(Linearization.index))
        mdl.add_constraints(y[h] <= x[h] + (1 - y_flag[h]) * BIGM for h in range(0, num_h))
        mdl.add_constraints(y[h] >= x[h] - (1 - y_flag[h]) * BIGM for h in range(0, num_h))
        mdl.add_constraints(y[h] <= y_flag[h] * BIGM for h in range(0, num_h))
        mdl.add_constraints(x[h] <= y_flag[h] * BIGM for h in range(0, num_h))
        mdl.add_constraints(y[h] >= 0 for h in range(0, num_h))

    def add(self, num_h, mdl, x1, x2):
        Linearization.index += 1
        add_y = mdl.continuous_var_list([i for i in range(0, num_h)], name='add_y{0}'.format(Linearization.index))
        mdl.add_constraints(add_y[h] == x1[h] + x2[h] for h in range(0, num_h))
        return add_y

    def posi_neg_cons_regester(self, num_h, mdl, x, xposi, xneg):
        Linearization.index += 1
        bigM = 1e10
        posi_flag = mdl.binary_var_list([i for i in range(0, num_h)],
                                         name='Linearization_posi_flag{0}'.format(Linearization.index))
        mdl.add_constraints(x[h] == xposi[h] - xneg[h] for h in range(0, num_h))
        mdl.add_constraints(xposi[h] >= 0 for h in range(0, num_h))
        mdl.add_constraints(xneg[h] >= 0 for h in range(0, num_h))
        mdl.add_constraints(xposi[h] <= bigM * posi_flag[h] for h in range(0, num_h))
        mdl.add_constraints(xneg[h] <= bigM * (1 - posi_flag[h]) for h in range(0, num_h))



class GridNet(IGES):
    index = 0

    def __init__(self, num_h, mdl,**kwargs):
        IGES('grid_net')
        GridNet.index += 1

        self.num_h          = num_h
        self.mdl            = mdl
        self.set_max        = kwargs.get('set_max',None)
        self.set_price      = kwargs.get('set_price',None)
        self.ele_price_from = kwargs.get('ele_price',None)
        self.ele_price_to   = kwargs.get('ele_price_to',None)

        self.gridnet_set  = mdl.continuous_var(name='gridnet_set{0}'.format(GridNet.index))
        self.gridnet_cost = mdl.continuous_var(name='gridnet_cost{0}'.format(GridNet.index))
        self.nianhua      = mdl.continuous_var(name='gridnet_nianhua{0}'.format(GridNet.index))

        self.total_power   = mdl.continuous_var_list(list(range(num_h)), lb=BIGM,name='total_power {0}'.format(GridNet.index))
        self.powerfrom     = mdl.continuous_var_list(list(range(num_h)),name='powerfrom{0}'.format(GridNet.index))
        self.powerto       = mdl.continuous_var_list(list(range(num_h)), name='powerto {0}'.format(GridNet.index))
        self.powerpeak     = mdl.continuous_var(name='powerpeak{0}'.format(GridNet.index))
        self.basecost      = mdl.continuous_var(name='basecost{0}'.format(GridNet.index))
        self.powerfrom_max = mdl.continuous_var(name='powerfrom_max{0}'.format(GridNet.index))
        self.powerto_max   = mdl.continuous_var(name='powerto_max{0}'.format(GridNet.index))

        self.cons_register(mdl)

    def cons_register(self, mdl, powerpeak_pre=2000):

        lin = Linearization()
        lin.posi_neg_cons_regester(self.num_h, mdl, self.total_power, self.powerfrom, self.powerto)
        hrange = range(self.num_h)
        mdl.add_constraint(self.gridnet_set >= 0)
        mdl.add_constraint(self.gridnet_set <= self.set_max)
        mdl.add_constraints(self.powerfrom[h] <= self.gridnet_set for h in hrange)
        mdl.add_constraints(self.powerto[h] <= self.gridnet_set for h in hrange)

        mdl.add_constraints(self.powerfrom[h] <= self.powerpeak for h in hrange)
        mdl.add_constraints(self.powerto[h] <= self.powerpeak for h in hrange)
        self.powerfrom_max = mdl.max(self.powerfrom)
        self.powerto_max   = mdl.max(self.powerfrom)
        self.powerpeak     = mdl.max(self.powerfrom_max, self.powerto_max)
        self.basecost      = mdl.min(mdl.max([self.powerpeak, powerpeak_pre]) * 31, self.gridnet_set * 22) * 12

        self.gridnet_cost = mdl.sum(self.powerfrom[h] * self.ele_price_from[h] + self.powerto[h] * self.ele_price_to for h in hrange) + self.basecost
        mdl.add_constraint(self.nianhua == self.gridnet_set * self.set_price / 15 + self.gridnet_cost * 8760 / self.num_h)

