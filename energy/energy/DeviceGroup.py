from SystemClass import *
import numpy as np

class DeviceGroup(object):

    def __init__(self,numh,mdl,RG):
        self.NUMH = numh
        self.MDL  = mdl
        self.ha = RG.ha
        self.gas_price    = RG.gas_price
        self.ele_price    = RG.ele_price
        self.cityrs_price = RG.cityrs_price
        self.steam_load   = RG.steam_load
        self.cool_load    = RG.cool_load
        self.heat_load    = RG.heat_load
        self.power_load   = RG.power_load

        self.generate_init() ## 初始化设备
        self.generate_steam()  ## 高温蒸汽
        self.generate_hot_water() ##  高温热水
        self.generate_heating_cooling() ##设备制热制冷
        self.generate_electric_quantity()# 电量平衡

    def generate_init(self):
        self.diesel = Diesel(self.NUMH, self.MDL, set_max=320, set_price=750, run_price=2)  # 柴油机
        self.pv     = PV(self.NUMH, self.MDL, set_max=5000, set_price=4500, ha=self.ha)  # 光伏
        self.bess   = ESS(self.NUMH, self.MDL, set_max=20000, set_price=1800,pcs_price=250)

        self.csgr     = Csgr(self.NUMH, self.MDL, set_max=5000, set_price=2000, gtxr_price=1000, ha=self.ha)  # 高温蒸汽 + ESS
        self.dyzqfsq  = Dyzqfsq(self.NUMH, self.MDL, set_max=20000, set_price=200, gtxr_price=200,ele_price=self.ele_price)
        self.chp      = CHP(self.NUMH, self.MDL, chp_num_max=5, chp_price=2000, gas_price=self.gas_price, chp_single_set=2000, drratio=1.2)
        self.gasgl    = Gasgl(self.NUMH, self.MDL, set_max=5000, gasgl_price=200, gas_price=self.gas_price)
        self.shizheng = CitySupply(self.NUMH, self.MDL, set_max=5000, set_price=3000, run_price=0.3 * np.ones(NUMH))

        self.qs_exchanger = Exchanger(self.NUMH, self.MDL, set_max=20000, set_price=400)
        self.qs_exchanger.cons_register(self.MDL)
        self.zq_xhl = LiBrRefrigeration(self.NUMH, self.MDL, set_max=10000, set_price=1000)

        self.pbgr     = PV(self.NUMH, self.MDL, set_max=10000, set_price=500, ha=self.ha)  # 平板光热
        self.xbxr     = ESS(self.NUMH, self.MDL, set_max=10000, set_price=350, pcs_price=0,c_rate_max=0.5)
        self.szrs     = CitySupply(self.NUMH, self.MDL, set_max=10000, set_price=3000, run_price=self.cityrs_price)
        self.rsdgl    = Dgl(self.NUMH, self.MDL, set_max=10000, dgl_price=200, ele_price=self.ele_price)
        self.gasgl_rs = Gasgl(self.NUMH, self.MDL, set_max=20000, gasgl_price=200, gas_price=self.gas_price)
        self.sx       = WaterEnergyStorage(self.NUMH, self.MDL, set_max=10000, v_price=300, pcs_price=1)

        self.rs_xhl = LiBrRefrigeration(self.NUMH, self.MDL, set_max=10000, set_price=1000)
        self.ss_exchanger = Exchanger(self.NUMH, self.MDL, set_max=20000, set_price=400)
        self.ss_exchanger.cons_register(self.MDL)

        self.rb       = WaterHeatPump(self.NUMH, self.MDL, set_max=20000, set_price=1000, ele_price=self.ele_price)
        self.sy       = WaterHeatPump(self.NUMH, self.MDL, set_max=2000, set_price=3000, ele_price=self.ele_price)
        self.slj      = WaterCooledScrew(self.NUMH, self.MDL, set_max=2000, set_price=1000, ele_price=self.ele_price)
        self.sangk    = ThreeGK(self.NUMH, self.MDL, set_max=20000, set_price=1000, ele_price=self.ele_price)
        self.doublegk = DoubleGK(self.NUMH, self.MDL, set_max=20000, set_price=1000,ele_price=self.ele_price)
        self.dire     = GeothermalHeatPump(self.NUMH, self.MDL, set_max=20000, set_price=40000,ele_price=self.ele_price)

        self.bx      = ESS(self.NUMH, self.MDL, set_max=20000, set_price=300, pcs_price=1, c_rate_max=0.5)
        self.xbxl    = ESS(self.NUMH, self.MDL, set_max=20000, set_price=500, pcs_price=1, c_rate_max=0.5)
        self.lowxbxr = ESS(self.NUMH, self.MDL, set_max=20000, set_price=300, pcs_price=1, c_rate_max=0.5)

        self.gridnet = GridNet(self.NUMH, self.MDL, set_max=200000, set_price=0, ele_price=self.ele_price, ele_price_to=0.35)

    def generate_steam(self):

        p_steam_sum = self.MDL.continuous_var_list(list(range(self.NUMH)), name='p_steam_sum')
        self.MDL.add_constraints(p_steam_sum[h] == self.shizheng.h_citysupply[h] + self.chp.yqyrsteam_set.h_exch[h] + self.csgr.p_csgr_steam[h] +
                                                    self.dyzqfsq.p_dyzqfsq_steam[h] + self.gasgl.h_gasgl[h] for h in range(self.NUMH))

        p_steam_used_product = self.MDL.continuous_var_list(list(range(self.NUMH)),name='p_steam_used_product')
        p_steam_used_heatcool = self.MDL.continuous_var_list(list(range(self.NUMH)),name='p_steam_used_heatcool')
        # 高温蒸汽去处
        self.MDL.add_constraints(p_steam_sum[h] >= self.steam_load[h] + p_steam_used_heatcool[h] for h in range(0, self.NUMH))

        self.MDL.add_constraints(p_steam_used_heatcool[h] >=  self.qs_exchanger.h_exch[h] +  self.zq_xhl.h_xhl_from[h] for h in range(self.NUMH))

    def generate_hot_water(self):

        # 高温热水合计
        p_gws_sum = self.MDL.continuous_var_list(list(range(self.NUMH)), name='p_gws_sum')
        self.MDL.add_constraints(p_gws_sum[h] == self.chp.gts_set.h_exch[h] + self.chp.yqyrwater_set.h_exch[h] + self.pbgr.p_pv[h] + self.xbxr.p_ess[h] +
               self.szrs.h_citysupply[h] + self.gasgl.h_gasgl[h] + self.rsdgl.h_dgl[h] + self.sx.p_sx_gheat[h] for h in range(self.NUMH))

        # 高温热水去向
        self.MDL.add_constraints(p_gws_sum[h] >=  self.rs_xhl.h_xhl_from[h] +  self.ss_exchanger.h_exch[h] for h in range(self.NUMH))
        self.MDL.add_constraints(p_gws_sum[h] >= 0 for h in range(self.NUMH))

    def generate_heating_cooling(self):
        # p_rb[h]*rb_flag[h]+p_sx[h]*sx_flag[h]+p_slj[h]*sy_flag[h]+p_xhl[h]+p_slj[h]+p_bx[h]==cool_load[h]%冷量需求
        # p_rb[h]*(1-rb_flag[h])+p_sx[h]*(1-sx_flag[h])+p_sy[h]*(1-sy_flag[h])+p_gas[h]+p_dire[h]==heat_load[h]%热量需求
        # 采用线性化技巧，处理为下面的约束.基于每种设备要么制热,要么制冷。
        # 供冷：风冷热泵 地源热泵 蓄能水罐 热水溴化锂机组 蒸汽溴化锂机组 相变蓄冷
        # 供热：风冷热泵 地源热泵 蓄能水罐 地热 水水换热器传热
        # rb = AirHeatPump(num_h0, mdl1, set_max=10000, set_price=1000, ele_price=ele_price0)
        # rb.cons_register(mdl1)

        p_xcool = self.MDL.continuous_var_list(list(range(self.NUMH)), name='p_xcool')
        p_xheat = self.MDL.continuous_var_list(list(range(self.NUMH)), name='p_xheat')
        p_xice  = self.MDL.continuous_var_list(list(range(self.NUMH)), name='p_xice')
        # p_rb_cool[h]+p_xcool[h]+p_sy_cool[h]+p_zqxhl[h]+p_rsxhl[h]+p_slj_cool[h]+p_ice[h]+p_sangk_cool[h]+p_doublegk_cool[h]==cool_load[h]%冷量需求

        self.MDL.add_constraints(self.rb.p_sy_cool[h] + p_xcool[h] + self.sy.p_sy_cool[h] + self.zq_xhl.c_xhl[h] + self.rs_xhl.c_xhl[h]
                                    + self.slj.p_slj_cool[h] + p_xice[h] + self.sangk.p_threegk_cool[h] + self.doublegk.p_doublegk_cool[h] == self.cool_load[h] for h in range(self.NUMH))
        # p_rb_heat[h]+p_xheat[h]+p_sy_heat[h]+p_gas_heat[h]+p_ss_heat[h]+p_dire[h]+p_sangk_heat[h]==heat_load[h]%热量需求
        self.MDL.add_constraints(self.rb.p_sy_heat[h] + p_xheat[h] + self.sy.p_sy_heat[h] + self.qs_exchanger.h_exch[h] +self.ss_exchanger.h_exch[h] +
                                    self.sangk.p_threegk_heat[h] + self.dire.p_dire[h] == self.heat_load[h] for h in range(self.NUMH))
        # 冰蓄冷逻辑组合
        self.MDL.add_constraints(self.sangk.p_threegk_ice[h] + self.doublegk.p_doublegk_ice[h] + self.bx.p_ess[h] == p_xice[h] for h in range(self.NUMH))

        lin = Linearization()
        lin.max_zeros(self.NUMH, self.MDL, p_xice, self.bx.p_ess)
        # 蓄冷逻辑组合
        self.MDL.add_constraints(self.rb.p_sy_xcool[h] + self.sy.p_sy_xcool[h] + self.slj.p_slj_xcool[h] + self.sx.p_sx_cool[h] + self.xbxl.p_ess[h] == p_xcool[h] for h in range(self.NUMH))
        lin.max_zeros(self.NUMH, self.MDL, p_xcool, lin.add(self.NUMH, self.MDL, self.sx.p_sx_cool, self.xbxl.p_ess))
        # 蓄热逻辑组合
        self.MDL.add_constraints(self.rb.p_sy_xheat[h] + self.sy.p_sy_xheat[h] + self.sx.p_sx_heat[h] + self.lowxbxr.p_ess[h] == p_xheat[h] for h in range(self.NUMH))
        lin.max_zeros(self.NUMH, self.MDL, p_xheat, lin.add(self.NUMH, self.MDL, self.sx.p_sx_heat, self.lowxbxr.p_ess))

    def generate_electric_quantity(self):
        # ele_dire[h] + ele_slj[h] + ele_rb[h] - p_bess[h] - p_pv[h] + ele_sy[h] + power_load[h] - p_chp[h] - p_chaifa[h] + \
        # p_dyzqfsq[h] + p_dgl[h] + ele_sangk[h] + ele_doublegk[h] == total_power[h]
        # 市政电力电流是双向的，其余市政是单向的。
        self.MDL.add_constraints(self.dire.ele_dire[h] + self.slj.ele_slj[h] + self.rb.ele_sy[h] - self.bess.p_ess[h] - self.pv.p_pv[h] + self.sy.ele_sy[h] + self.power_load[h] -
                                 self.chp.p_chp[h] - self.diesel.p_diesel[h] + self.dyzqfsq.p_dyzqfsq[h] + self.rsdgl.ele_dgl[h] + self.sangk.ele_threegk[h] + self.doublegk.ele_doublegk[h] ==
                                 self.gridnet.total_power[h] for h in range(self.NUMH))


