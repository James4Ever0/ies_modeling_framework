var __spreadArray=(this&&this.__spreadArray)||function(to,from,pack) {
    if(pack||arguments.length===2) for(var i=0,l=from.length,ar; i<l; i++) {
        if(ar||!(i in from)) {
            if(!ar) ar=Array.prototype.slice.call(from,0,i);
            ar[i]=from[i];
        }
    }
    return to.concat(ar||Array.prototype.slice.call(from));
};
// import MessageBus from '@/Utils/message/message-bus';
var excelMap={
    fuels: {
        燃料类型: 'fuelType',
        计量单位: 'calculatingUnit',
        '热值（MJ/计量单位)': 'calorificFuel',
        '价格(元/计量单位)': 'priceFuel',
        CO2排放系数: 'PollutantDischargeFactor.pollutionCO2',
        NOx排放系数: 'PollutantDischargeFactor.pollutionNOX',
        SO2排放系数: 'PollutantDischargeFactor.pollutionSO2',
        灰尘排放系数: 'PollutantDischargeFactor.dust'
    },
    常数电价: {
        类型: 'name',
        '电价(元/kWh)': {
            route: 'purchasePriceModel.params',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return [data[0].value[0]];
            }
        }
    },
    分时电价: {
        类型: 'name',
        时间: {
            route: 'purchasePriceModel.params',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return __spreadArray([],Array(data[0].value.length),true).map(function(x,index) {return index;});
            }
        },
        '分时电价(元/kwh)': {
            route: 'purchasePriceModel.params',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return data[0].value;
            }
        }
    },
    阶梯电价: {
        类型: 'name',
        '容量下限(kwh)': {
            route: 'purchasePriceModel.params',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return data.map(function(x) {return x.quantity;});
            }
        },
        '阶梯电价(元/kwh)': {
            route: 'purchasePriceModel.params',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return data.map(function(x) {return x.value[0];});
            }
        }
    },
    '分时+阶梯': {
        类型: 'name',
        '阶段(kwh)': {
            route: 'purchasePriceModel.params',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return __spreadArray([],Array(24),true).map(function(x,index) {return "".concat(index,"h");});
            }
        }
    },
    '热-按热量计价': {
        模型名称: 'name',
        计价方式: 'purchasePriceModel.pricingMethod',
        '价格（元/kWh）': 'purchasePriceModel.price'
    },
    '热-按用量计价': {
        模型名称: 'name',
        计价方式: 'purchasePriceModel.pricingMethod',
        '价格（元/t）': 'purchasePriceModel.price'
    },
    '热-按采暖面积计价': {
        模型名称: 'name',
        计价方式: 'purchasePriceModel.pricingMethod',
        '价格（元/㎡）': 'purchasePriceModel.price'
    },
    '冷-按热量计价': {
        模型名称: 'name',
        计价方式: 'purchasePriceModel.pricingMethod',
        '价格（元/kWh）': 'purchasePriceModel.price'
    },
    '冷-按用量计价': {
        模型名称: 'name',
        计价方式: 'purchasePriceModel.pricingMethod',
        '价格（元/t）': 'purchasePriceModel.price'
    },
    '冷-按供冷面积计价': {
        模型名称: 'name',
        计价方式: 'purchasePriceModel.pricingMethod',
        '价格（元/㎡）': 'purchasePriceModel.price'
    },
    光伏: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '单个光伏板面积(m²)': 'ratedParam.singlePanelArea',
        '光电转换效率(%)': 'ratedParam.photoelectricConversionEfficiency',
        '最大发电功率(kW)': 'operationalConstraints.maxPowerGenerating',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    风机: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定容量(kW)': 'ratedParam.ratedPowerGenerating',
        '额定风速(m/s)': 'ratedParam.ratedWindSpeed',
        '切出风速(m/s)': 'ratedParam.cutoutWindSpeed',
        '切入风速(m/s)': 'ratedParam.cutinWindSpeed',
        '塔筒高度(m)': 'ratedParam.towerHeight',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    燃气轮机: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定发电功率(kW)': 'ratedParam.powerGenerating',
        '发电效率(%)': 'ratedParam.generatingEfficiency',
        '制热效率(%)': 'ratedParam.heatingEfficiency',
        '最大烟气出口温度(℃)': 'operationalConstraints.maxExhaustOutletTemp',
        '最小烟气出口温度(℃)': 'operationalConstraints.miniExhaustOutletTemp',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    燃气内燃机: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定发电功率(kW)': 'ratedParam.powerGenerating',
        '发电效率(%)': 'ratedParam.generatingEfficiency',
        '制热效率(%)': 'ratedParam.heatingEfficiency',
        '循环水流量(t/h)': 'ratedParam.waterMassFlowrate',
        '最大热水出口温度(℃)': 'operationalConstraints.maxHeatWaterOutletTemp',
        '最小热水出口温度(℃)': 'operationalConstraints.miniHeatWaterOutletTemp',
        '最大热水进口温度(℃)': 'operationalConstraints.maxHeatWaterInletTemp',
        '最小热水进口温度(℃)': 'operationalConstraints.miniHeatWaterInletTemp',
        '最大烟气出口温度(℃)': 'operationalConstraints.maxExhaustOutletTemp',
        '最小烟气出口温度(℃)': 'operationalConstraints.miniExhaustOutletTemp',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    蒸汽轮机: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '最大蒸汽进口温度(℃)': 'operationalConstraints.maxSteamInletTemp',
        '最小蒸汽进口温度(℃)': 'operationalConstraints.miniSteamInletTemp',
        '最大发电量(kW)': 'operationalConstraints.maxPowerGenerating',
        '最小发电量(kW)': 'operationalConstraints.miniPowerGenerating',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    热泵: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定制热量(kW)': 'ratedParam.ratedHeatSupply',
        额定能效比COP: 'ratedParam.heatingCOP',
        '额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷能效比COP: 'ratedParam.coolingCOP',
        '最大热水出口温度(℃)': 'operationalConstraints.maxHeatWaterOutletTemp',
        '最小热水出口温度(℃)': 'operationalConstraints.miniHeatWaterOutletTemp',
        '最大热水进口温度(℃)': 'operationalConstraints.maxHeatWaterInletTemp',
        '最小热水进口温度(℃)': 'operationalConstraints.miniHeatWaterInletTemp',
        '最大冷水出口温度(℃)': 'operationalConstraints.maxColdWaterOutletTemp',
        '最小冷水出口温度(℃)': 'operationalConstraints.miniColdWaterOutletTemp',
        '最大冷水进口温度(℃)': 'operationalConstraints.maxColdWaterInletTemp',
        '最小冷水进口温度(℃)': 'operationalConstraints.miniColdWaterInletTemp',
        '最大工作电压(V)': 'operationalConstraints.maxVoltage',
        '最小工作电压(V)': 'operationalConstraints.miniVoltage',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    燃气热水锅炉: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热效率(%)': 'ratedParam.heatingEfficiency',
        '最大热水出口温度(℃)': 'operationalConstraints.maxHeatWaterOutletTemp',
        '最小热水出口温度(℃)': 'operationalConstraints.miniHeatWaterOutletTemp',
        '最大热水进口温度(℃)': 'operationalConstraints.maxHeatWaterInletTemp',
        '最小热水进口温度(℃)': 'operationalConstraints.miniHeatWaterInletTemp',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    燃气蒸汽锅炉: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热效率(%)': 'ratedParam.heatingEfficiency',
        '最大蒸汽出口温度(℃)': 'operationalConstraints.maxSteamOutletTemp',
        '最小蒸汽出口温度(℃)': 'operationalConstraints.miniSteamOutletTemp',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    余热热水锅炉: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '最大烟气出口温度(℃)': 'operationalConstraints.maxExhaustOutletTemp',
        '最小烟气出口温度(℃)': 'operationalConstraints.miniExhaustOutletTemp',
        '最大烟气进口温度(℃)': 'operationalConstraints.maxExhaustInletTemp',
        '最小烟气进口温度(℃)': 'operationalConstraints.miniExhaustInletTemp',
        '最大热水出口温度(℃)': 'operationalConstraints.maxHeatWaterOutletTemp',
        '最小热水出口温度(℃)': 'operationalConstraints.miniHeatWaterOutletTemp',
        '最大热水进口温度(℃)': 'operationalConstraints.maxHeatWaterInletTemp',
        '最小热水进口温度(℃)': 'operationalConstraints.miniHeatWaterInletTemp',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    '余热蒸汽锅炉-单压': {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        压力等级: 'ratedParam.pressureLevel',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '最大烟气出口温度(℃)': 'operationalConstraints.maxExhaustOutletTemp',
        '最小烟气出口温度(℃)': 'operationalConstraints.miniExhaustOutletTemp',
        '最大烟气进口温度(℃)': 'operationalConstraints.maxExhaustInletTemp',
        '最小烟气进口温度(℃)': 'operationalConstraints.miniExhaustInletTemp',
        '最大蒸汽出口温度(℃)': 'operationalConstraints.maxSteamOutletTemp',
        '最小蒸汽出口温度(℃)': 'operationalConstraints.miniSteamOutletTemp',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    '余热蒸汽锅炉-双压': {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        压力等级: 'ratedParam.pressureLevel',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '最大烟气出口温度(℃)': 'operationalConstraints.maxExhaustOutletTemp',
        '最小烟气出口温度(℃)': 'operationalConstraints.miniExhaustOutletTemp',
        '最大烟气进口温度(℃)': 'operationalConstraints.maxExhaustInletTemp',
        '最小烟气进口温度(℃)': 'operationalConstraints.miniExhaustInletTemp',
        '最大次高压蒸汽出口温度(℃)': 'operationalConstraints.maxSubSteamOutletTemp',
        '最小次高压蒸汽出口温度(℃)': 'operationalConstraints.miniSubSteamOutletTemp',
        '最大高压蒸汽出口温度(℃)': 'operationalConstraints.maxHighSteamOutletTemp',
        '最小高压蒸汽出口温度(℃)': 'operationalConstraints.miniHighSteamOutletTemp',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    热管式太阳能集热器: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '单个集热器面积(m²)': 'ratedParam.plateArea',
        '集热效率(%)': 'ratedParam.collectionEfficiency',
        '最大热水出口温度(℃)': 'operationalConstraints.maxHeatWaterOutletTemp',
        '最小热水出口温度(℃)': 'operationalConstraints.miniHeatWaterOutletTemp',
        '最大热水进口温度(℃)': 'operationalConstraints.maxHeatWaterInletTemp',
        '最小热水进口温度(℃)': 'operationalConstraints.miniHeatWaterInletTemp',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    电压缩制冷机: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷能效比COP: 'ratedParam.COP',
        '最大冷水出口温度(℃)': 'operationalConstraints.maxColdWaterOutletTemp',
        '最小冷水出口温度(℃)': 'operationalConstraints.miniColdWaterOutletTemp',
        '最大冷水进口温度(℃)': 'operationalConstraints.maxColdWaterInletTemp',
        '最小冷水进口温度(℃)': 'operationalConstraints.miniColdWaterInletTemp',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    热水吸收式制冷机: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        热源流体类型: 'ratedParam.heatFluidType',
        '制冷状态额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷状态时冷热比: 'ratedParam.coldHeatRatio',
        '制热状态额定制热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热状态时换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '用电功率(kW)': 'ratedParam.ratedPowerConsume',
        '最大热源出口温度(℃)': 'operationalConstraints.maxHeatSourceOutletTemp',
        '最小热源出口温度(℃)': 'operationalConstraints.miniHeatSourceOutletTemp',
        '最大热源进口温度(℃)': 'operationalConstraints.maxHeatSourceInletTemp',
        '最小热源进口温度(℃)': 'operationalConstraints.miniHeatSourceInletTemp',
        '最大冷水出口温度(℃)': 'operationalConstraints.maxColdWaterOutletTemp',
        '最小冷水出口温度(℃)': 'operationalConstraints.miniColdWaterOutletTemp',
        '最大冷水进口温度(℃)': 'operationalConstraints.maxColdWaterInletTemp',
        '最小冷水进口温度(℃)': 'operationalConstraints.miniColdWaterInletTemp',
        '最大热水出口温度(℃)': 'operationalConstraints.maxHeatWaterOutletTemp',
        '最小热水出口温度(℃)': 'operationalConstraints.miniHeatWaterOutletTemp',
        '最大热水进口温度(℃)': 'operationalConstraints.maxHeatWaterInletTemp',
        '最小热水进口温度(℃)': 'operationalConstraints.miniHeatWaterInletTemp',
        '最大工作电压(V)': 'operationalConstraints.maxVoltage',
        '最小工作电压(V)': 'operationalConstraints.miniVoltage',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    烟气吸收式制冷机: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        热源流体类型: 'ratedParam.heatFluidType',
        '制冷状态额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷状态时冷热比: 'ratedParam.coldHeatRatio',
        '制热状态额定制热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热状态时换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '用电功率(kW)': 'ratedParam.ratedPowerConsume',
        '最大烟气出口温度(℃)': 'operationalConstraints.maxExhaustOutletTemp',
        '最小烟气出口温度(℃)': 'operationalConstraints.miniExhaustOutletTemp',
        '最大烟气进口温度(℃)': 'operationalConstraints.maxExhaustInletTemp',
        '最小烟气进口温度(℃)': 'operationalConstraints.miniExhaustInletTemp',
        '最大冷水出口温度(℃)': 'operationalConstraints.maxColdWaterOutletTemp',
        '最小冷水出口温度(℃)': 'operationalConstraints.miniColdWaterOutletTemp',
        '最大冷水进口温度(℃)': 'operationalConstraints.maxColdWaterInletTemp',
        '最小冷水进口温度(℃)': 'operationalConstraints.miniColdWaterInletTemp',
        '最大热水出口温度(℃)': 'operationalConstraints.maxHeatWaterOutletTemp',
        '最小热水出口温度(℃)': 'operationalConstraints.miniHeatWaterOutletTemp',
        '最大热水进口温度(℃)': 'operationalConstraints.maxHeatWaterInletTemp',
        '最小热水进口温度(℃)': 'operationalConstraints.miniHeatWaterInletTemp',
        '最大工作电压(V)': 'operationalConstraints.maxVoltage',
        '最小工作电压(V)': 'operationalConstraints.miniVoltage',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    蒸汽吸收式制冷机: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        热源流体类型: 'ratedParam.heatFluidType',
        '制冷状态额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷状态时冷热比: 'ratedParam.coldHeatRatio',
        '制热状态额定制热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热状态时换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '用电功率(kW)': 'ratedParam.ratedPowerConsume',
        '最大蒸汽进口温度(℃)': 'operationalConstraints.maxSteamInletTemp',
        '最小蒸汽进口温度(℃)': 'operationalConstraints.miniSteamInletTemp',
        '最大冷水出口温度(℃)': 'operationalConstraints.maxColdWaterOutletTemp',
        '最小冷水出口温度(℃)': 'operationalConstraints.miniColdWaterOutletTemp',
        '最大冷水进口温度(℃)': 'operationalConstraints.maxColdWaterInletTemp',
        '最小冷水进口温度(℃)': 'operationalConstraints.miniColdWaterInletTemp',
        '最大热水出口温度(℃)': 'operationalConstraints.maxHeatWaterOutletTemp',
        '最小热水出口温度(℃)': 'operationalConstraints.miniHeatWaterOutletTemp',
        '最大热水进口温度(℃)': 'operationalConstraints.maxHeatWaterInletTemp',
        '最小热水进口温度(℃)': 'operationalConstraints.miniHeatWaterInletTemp',
        '最大工作电压(V)': 'operationalConstraints.maxVoltage',
        '最小工作电压(V)': 'operationalConstraints.miniVoltage',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    蓄冰空调: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定放冷功率(kW)': 'ratedParam.ratedDischargingCool',
        '额定蓄冷功率(kW)': 'ratedParam.ratedChargingCool',
        '放冷效率(%)': 'ratedParam.dischargingEfficiency',
        '蓄冷效率(%)': 'ratedParam.chargingEfficiency',
        '最大冷水出口温度(℃)': 'operationalConstraints.maxColdWaterOutletTemp',
        '最大冷水进口温度(℃)': 'operationalConstraints.maxColdWaterInletTemp',
        '最小冷水出口温度(℃)': 'operationalConstraints.miniColdWaterOutletTemp',
        '最小冷水进口温度(℃)': 'operationalConstraints.miniColdWaterInletTemp',
        '蓄冰空调最大容量(kWh)': 'operationalConstraints.capacity',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    蓄热电锅炉: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '蓄热效率(%)': 'ratedParam.chargingEfficiency',
        '蓄热电锅炉最大容量(kWh)': 'operationalConstraints.capacity',
        '额定放热功率(kW)': 'ratedParam.ratedDischargingHeat',
        '额定蓄热功率(kW)': 'ratedParam.ratedChargingHeat',
        '放热效率(%)': 'ratedParam.dischargingEfficiency',
        '最大热水出口温度(℃)': 'operationalConstraints.maxHeatWaterOutletTemp',
        '最大热水进口温度(℃)': 'operationalConstraints.maxHeatWaterInletTemp',
        '最小热水出口温度(℃)': 'operationalConstraints.miniHeatWaterOutletTemp',
        '最小热水进口温度(℃)': 'operationalConstraints.miniHeatWaterInletTemp',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    蓄电池: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '充电效率(%)': 'ratedParam.chargingEfficiency',
        '放电效率(%)': 'ratedParam.dischargingEfficiency',
        '电池最大容量(kWh)': 'operationalConstraints.capacity',
        '额定充电功率(kW)': 'ratedParam.ratedChargingPower',
        '额定放电功率(kW)': 'ratedParam.ratedDischargingPower',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    变压器: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '副边侧额定电压有效值(V)': 'ratedParam.wind2RatioVoltage',
        '励磁电导(p.u.)': 'ratedParam.excitationConductance',
        '励磁电纳(p.u.)': 'ratedParam.excitationAdmittance',
        '原边侧额定电压有效值(kV)': 'ratedParam.wind1RatioVoltage',
        '变压器非标准变比(p.u.)': 'ratedParam.wind2Ratio',
        '最大非标准变比(p.u.)': 'operationalConstraints.maxWind2Ratio',
        '最小非标准变比(p.u.)': 'operationalConstraints.miniWind2Ratio',
        '短路电抗(p.u.)': 'ratedParam.shortCircuitImpedance',
        '短路电阻(p.u.)': 'ratedParam.shortCircuitResistance',
        '额定容量(MVA)': 'ratedParam.windingMVABase',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    传输线: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '单位长度正序电抗(p.u./km)': 'ratedParam.reactanceOfUnitLength',
        '单位长度正序电纳(p.u./km)': 'ratedParam.chargingBofUnitLength',
        '单位长度正序电阻(p.u./km)': 'ratedParam.resistanceOfUnitLength',
        '额定电压(kV)': 'ratedParam.ratedVoltage',
        '额定频率(Hz)': 'ratedParam.ratedFrequency',
        '采购成本(万元/km)': 'economicParam.purchaseCost',
        '维护成本(元/(km·年))': 'economicParam.fixationMaintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    电容器: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定容量(MVA)': 'ratedParam.ratedVoltage',
        '额定电压有效值(Hz)': 'ratedParam.validRatedVoltage',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    离心泵: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        工作特性曲线系数A: 'ratedParam.operationCurveParamA',
        工作特性曲线系数B: 'ratedParam.operationCurveParamB',
        工作特性曲线系数C: 'ratedParam.operationCurveParamC',
        '最低进口压力(MPa)': 'operationalConstraints.miniInletPressure',
        '最大进口压力(MPa)': 'operationalConstraints.maxInlePressure',
        '泵效率(%)': 'ratedParam.efficency',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    换热器: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        热流体类型: 'ratedParam.heatSourceType',
        '额定热负荷(kW)': 'ratedParam.ratedHeatLoad',
        '换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '最大热流体出口温度(℃)': 'operationalConstraints.maxHeatSourceOutletTemp',
        '最小热流体出口温度(℃)': 'operationalConstraints.miniHeatSourceOutletTemp',
        '最大热流体进口温度(℃)': 'operationalConstraints.maxHeatSourceInletTemp',
        '最小热流体进口温度(℃)': 'operationalConstraints.miniHeatSourceInletTemp',
        '最大冷流体出口温度(℃)': 'operationalConstraints.maxColdFluidOutletTemp',
        '最小冷流体出口温度(℃)': 'operationalConstraints.miniColdFluidOutletTemp',
        '最大冷流体进口温度(℃)': 'operationalConstraints.maxColdFluidInletTemp',
        '最小冷流体进口温度(℃)': 'operationalConstraints.miniColdFluidInletTemp',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    管道: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '管道内径(mm)': 'ratedParam.interDiameter',
        '管道壁厚(mm)': 'ratedParam.thickness',
        '管道总传热系数(W/(m·K))': 'ratedParam.heatExchangeFactor',
        '管道粗糙度(mm)': 'ratedParam.roughness',
        '管道设计压力(MPa)': 'operationalConstraints.maxPressure',
        '采购成本(元/m)': 'economicParam.purchaseCost',
        '维护成本(元/(m·年))': 'economicParam.fixationMaintainCost',
        '设计寿命(年)': 'economicParam.designLife'
    },
    蒸汽制热负荷: {
        负荷名称: 'loadName',
        日运行周期开始时间: 'loadParam.dayCycleStart',
        日运行周期结束时间: 'loadParam.dayCycleEnd',
        '设计蒸汽用量(t/h)': 'loadParam.steamConsumption',
        '蒸汽压力(MPa)': 'loadParam.steamPressure',
        '蒸汽温度(℃)': 'loadParam.steamTemperature',
        周运行周期开始时间: 'loadParam.weekCycleStart',
        周运行周期结束时间: 'loadParam.weekCycleEnd'
    },
    '采暖负荷-粗略': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.single_line_load.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                if(data==='rough')
                    return ['粗略模型'];
                else
                    return ['详细模型'];
            }
        },
        负荷类型: 'loadParam.rough_load.buildingType',
        '建筑物用地面积(m2)': 'loadParam.rough_load.buildingArea',
        周采暖制冷周期开始时间: 'loadParam.rough_load.weekCycleStart',
        周采暖制冷周期结束时间: 'loadParam.rough_load.weekCycleEnd',
        日采暖制冷起始时间: 'loadParam.rough_load.dayCycleStart',
        日采暖制冷结束时间: 'loadParam.rough_load.dayCycleEnd'
    },
    '采暖负荷-详细模型-不区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.single_line_load.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                if(data==='rough')
                    return ['粗略模型'];
                else
                    return ['详细模型'];
            }
        },
        '建筑物用地面积(m2)': 'loadParam.single_line_load.buildingArea',
        区分工作日和休息日: 'loadParam.single_line_load.isDayOff'
    },
    '采暖负荷-详细模型-区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.single_line_load.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                if(data==='rough')
                    return ['粗略模型'];
                else
                    return ['详细模型'];
            }
        },
        '建筑物用地面积(m2)': 'loadParam.single_line_load.buildingArea',
        区分工作日和休息日: 'loadParam.single_line_load.isDayOff'
    },
    '制冷负荷-粗略': {
        负荷名称: 'loadName',
        负荷类型: 'loadParam.rough_load.buildingType',
        负荷模型: {
            route: 'loadParam.single_line_load.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                if(data==='rough')
                    return ['粗略模型'];
                else
                    return ['详细模型'];
            }
        },
        '建筑物用地面积(m2)': 'loadParam.single_line_load.buildingArea',
        周采暖制冷周期开始时间: 'loadParam.rough_load.weekCycleStart',
        周采暖制冷周期结束时间: 'loadParam.rough_load.weekCycleEnd',
        日采暖制冷起始时间: 'loadParam.rough_load.dayCycleStart',
        日采暖制冷结束时间: 'loadParam.rough_load.dayCycleEnd'
    },
    '制冷负荷-详细模型-不区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.single_line_load.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                if(data==='rough')
                    return ['粗略模型'];
                else
                    return ['详细模型'];
            }
        },
        '建筑物用地面积(m2)': 'loadParam.single_line_load.buildingArea',
        区分工作日和休息日: 'loadParam.single_line_load.isDayOff'
    },
    '制冷负荷-详细模型-区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.single_line_load.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                if(data==='rough')
                    return ['粗略模型'];
                else
                    return ['详细模型'];
            }
        },
        '建筑物用地面积(m2)': 'loadParam.single_line_load.buildingArea',
        区分工作日和休息日: 'loadParam.single_line_load.isDayOff'
    },
    '电负荷-粗略': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.loadCurve.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                if(data==='rough')
                    return ['粗略模型'];
                else
                    return ['详细模型'];
            }
        },
        负荷类型: 'loadParam.rough_load.buildingType',
        '年平均负荷(KW)': 'loadParam.rough_load.loadDensity'
    },
    '电负荷-详细-区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.loadCurve.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                if(data==='rough')
                    return ['粗略模型'];
                else
                    return ['详细模型'];
            }
        },
        '建筑物用地面积(m2)': 'loadParam.loadCurve.buildingArea',
        区分工作日和休息日: 'loadParam.loadCurve.isDayOff'
    },
    '电负荷-详细-不区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.loadCurve.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                if(data==='rough')
                    return ['粗略模型'];
                else
                    return ['详细模型'];
            }
        },
        区分工作日和休息日: 'loadParam.loadCurve.isDayOff'
    },
    /**
     * 2021-5-24 更新
     * 建模仿真模块 电负荷
     */
    '电负荷-典型日负荷': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return ['典型日负荷'];
            }
        },
        负荷类型: 'loadParam.rough_load.buildingType',
        '建筑面积(m2)': 'loadParam.rough_load.Floorage',
        '单位建筑面积负荷指标(W/㎡)': 'loadParam.rough_load.UnitFloorageElectricalLoadIndex',
        '电负荷指标(kW)': 'loadParam.rough_load.ElectricalLoadIndex',
        功率因数: 'loadParam.rough_load.PowerFactor'
    },
    '电负荷建模仿真-分月详细负荷-区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return ['分月详细负荷'];
            }
        },
        区分工作日和休息日: 'loadParam.loadCurve.isDayOff',
        功率因数: 'loadParam.detail_load.PowerFactor'
    },
    '电负荷建模仿真-分月详细负荷-不区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return ['分月详细负荷'];
            }
        },
        区分工作日和休息日: 'loadParam.loadCurve.isDayOff',
        功率因数: 'loadParam.detail_load.PowerFactor'
    },
    '电负荷-自定义': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return ['自定义负荷'];
            }
        }
    },
    '充电桩负荷-区分工作日': {
        负荷名称: 'loadName',
        区分工作日和休息日: 'loadParam.loadCurve.isDayOff'
    },
    '充电桩负荷-不区分工作日': {
        负荷名称: 'loadName',
        区分工作日和休息日: 'loadParam.loadCurve.isDayOff'
    },
    //建模仿真 设备信息库
    光伏_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '光伏板面积(m²)': 'ratedParam.SinglePanelArea',
        '光电转换效率(%)': 'ratedParam.ConversionEfficiency',
        '最大发电功功率(kW)': 'operationalConstraints.maxPowerGenerating',
        功率因数: 'ratedParam.PowerFactor'
    },
    风机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定发电量(kW)': 'ratedParam.RatedPowerGenerating',
        '额定风速(m/s)': 'ratedParam.RatedWindSpeed',
        '切出风速(m/s)': 'ratedParam.CutoutWindSpeed',
        '切入风速(m/s)': 'ratedParam.CutinWindSpeed',
        '轮毂高度(m)': 'ratedParam.HubHeight',
        功率因数: 'ratedParam.PowerFactor'
    },
    燃气轮机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '局部压降系数 (kPa/(m³·s⁻¹)²)': 'ratedParam.LocalPressureDropCoe',
        '最小供水温度 (℃)': 'operationalConstraints.MiniOutletTemp',
        '最大供水温度 (℃)': 'operationalConstraints.MaxOutletTemp',
        挡位: {
            route: 'OperateParams.params',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return data.map(function(x) {return x.OperateStatus;});
            }
        },
        功率因数: 'ratedParam.PowerFactor'
    },
    燃气内燃机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定发电功率(kW)': 'ratedParam.powerGenerating',
        '发电效率(%)': 'ratedParam.generatingEfficiency',
        '制热效率(%)': 'ratedParam.heatingEfficiency',
        '循环水流量(t/h)': 'ratedParam.waterMassFlowrate',
        '最大热水出口温度(℃)': 'operationalConstraints.maxHeatWaterOutletTemp',
        '最小热水出口温度(℃)': 'operationalConstraints.miniHeatWaterOutletTemp',
        '最大热水进口温度(℃)': 'operationalConstraints.maxHeatWaterInletTemp',
        '最小热水进口温度(℃)': 'operationalConstraints.miniHeatWaterInletTemp',
        '最大烟气出口温度(℃)': 'operationalConstraints.maxExhaustOutletTemp',
        '最小烟气出口温度(℃)': 'operationalConstraints.miniExhaustOutletTemp',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        功率因数: 'ratedParam.PowerFactor'
    },
    蒸汽轮机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定蒸汽进口温度(℃)': 'ratedParam.ratedSteamInletTemp',
        '蒸汽流量(t/h)': 'ratedParam.steamMassFlowrate',
        '发电效率(%)': 'ratedParam.generatingEfficiency',
        '最大蒸汽进口温度(℃)': 'operationalConstraints.maxSteamInletTemp',
        '最小蒸汽进口温度(℃)': 'operationalConstraints.miniSteamInletTemp',
        '最大发电量(kW)': 'operationalConstraints.maxPowerGenerating',
        '最小发电量(kW)': 'operationalConstraints.miniPowerGenerating',
        '机组最大承压(MPa)': 'operationalConstraints.maxPressure',
        功率因数: 'ratedParam.PowerFactor'
    },
    热泵_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定制热量(kW)': 'ratedParam.ratedHeatSupply',
        额定能效比COP: 'ratedParam.heatingCOP',
        '额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷能效比COP: 'ratedParam.coolingCOP',
        功率因数: 'ratedParam.PowerFactor'
    },
    燃气热水锅炉_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热效率(%)': 'ratedParam.heatingEfficiency'
    },
    燃气蒸汽锅炉_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热效率(%)': 'ratedParam.heatingEfficiency'
    },
    余热热水锅炉_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '换热效率(%)': 'ratedParam.heatExchangeEfficiency'
    },
    '余热蒸汽锅炉-单压_建模仿真': {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        压力等级: 'ratedParam.pressureLevel',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '换热效率(%)': 'ratedParam.heatExchangeEfficiency'
    },
    '余热蒸汽锅炉-双压_建模仿真': {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        压力等级: 'ratedParam.pressureLevel',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '换热效率(%)': 'ratedParam.heatExchangeEfficiency'
    },
    热管式太阳能集热器_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '局部压降系数(kPa/(m³·s⁻¹)²)': 'ratedParam.LocalPressureDropCoe',
        '集热器面积(m²)': 'ratedParam.PlateArea',
        '集热效率(%)': 'ratedParam.CollectionEfficiency'
    },
    电压缩制冷机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷能效比COP: 'ratedParam.COP'
    },
    热水吸收式制冷机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        热源流体类型: 'ratedParam.heatFluidType',
        '制冷状态额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷状态时冷热比: 'ratedParam.coldHeatRatio',
        '制热状态额定制热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热状态时换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '用电功率(kW)': 'ratedParam.ratedPowerConsume'
    },
    烟气吸收式制冷机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        热源流体类型: 'ratedParam.heatFluidType',
        '制冷状态额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷状态时冷热比: 'ratedParam.coldHeatRatio',
        '制热状态额定制热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热状态时换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '用电功率(kW)': 'ratedParam.ratedPowerConsume'
    },
    蒸汽吸收式制冷机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        热源流体类型: 'ratedParam.heatFluidType',
        '制冷状态额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷状态时冷热比: 'ratedParam.coldHeatRatio',
        '制热状态额定制热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热状态时换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '用电功率(kW)': 'ratedParam.ratedPowerConsume'
    },
    蓄冰空调_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定放冷功率(kW)': 'ratedParam.ratedDischargingCool',
        '额定蓄冷功率(kW)': 'ratedParam.ratedChargingCool',
        '放冷效率(%)': 'ratedParam.dischargingEfficiency',
        '蓄冷效率(%)': 'ratedParam.chargingEfficiency',
        功率因数: 'ratedParam.PowerFactor'
    },
    蓄热电锅炉_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '蓄热效率(%)': 'ratedParam.chargingEfficiency',
        '额定放热功率(kW)': 'ratedParam.ratedDischargingHeat',
        '额定蓄热功率(kW)': 'ratedParam.ratedChargingHeat',
        '放热效率(%)': 'ratedParam.dischargingEfficiency'
    },
    蓄电池_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '充电效率(%)': 'ratedParam.ChargingEfficiency',
        '放电效率(%)': 'ratedParam.DischargingEfficiency',
        功率因数: 'ratedParam.PowerFactor',
        '电池最大容量(kWh)': 'operationalConstraints.PowerStorageLimit',
        '最大充电功率(kW)': 'operationalConstraints.MaxChargingPower',
        '最大放电功率(kW)': 'operationalConstraints.MaxDischargingPower'
    },
    储水罐_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '入口侧局部压降系数(kPa/(m³·s⁻¹)²)': 'ratedParam.InletLocalPressureDropCoe',
        '出口侧局部压降系数(kPa/(m³·s⁻¹)²)': 'ratedParam.OutletLocalPressureDropCoe',
        '罐底面积(m²)': 'ratedParam.FloorArea'
    },
    变压器_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '变压器非标准变比(p.u.)': 'ratedParam.wind2Ratio',
        '一次侧短路电抗(Ω)': 'ratedParam.shortCircuitImpedance',
        '一次侧短路电阻(Ω)': 'ratedParam.shortCircuitResistance',
        '额定容量(MVA)': 'ratedParam.windingMVABase'
    },
    传输线_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '单位长度电抗(Ω/km)': 'ratedParam.reactanceOfUnitLength',
        '单位长度容抗(MΩ*km)': 'ratedParam.chargingBofUnitLength',
        '单位长度电阻(Ω/km)': 'ratedParam.resistanceOfUnitLength'
    },
    电容器_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定容量(MVA)': 'ratedParam.ratedVoltage',
        '额定电压有效值(Hz)': 'ratedParam.validRatedVoltage'
    },
    模块化多电平变流器_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定电压(kV)': 'ratedParam.BaseVoltage'
    },
    离心泵_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定转速 (rpm)': 'ratedParam.RatedPumpSpeed',
        最大工作转速: 'ratedParam.MaxPumpSpeed',
        最小工作转速: 'ratedParam.MinPumpSpeed',
        功率因数: 'ratedParam.PowerFactor'
    },
    换热器_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        热流体类型: 'ratedParam.heatSourceType',
        '额定热负荷(kW)': 'ratedParam.ratedHeatLoad',
        '换热效率(%)': 'ratedParam.heatExchangeEfficiency'
    },
    管道_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '管道内径(mm)': 'ratedParam.interDiameter',
        '管道壁厚(mm)': 'ratedParam.thickness',
        '管道总传热系数(W/(m·K))': 'ratedParam.heatExchangeFactor',
        '管道粗糙度(mm)': 'ratedParam.roughness'
    },
    /**
     * 采暖制冷负荷
     * 2021-5-24 更新
     */
    '采暖制冷负荷-典型日负荷': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return ['典型日负荷'];
            }
        },
        负荷类型: 'loadParam.rough_load.buildingType',
        '建筑面积(m2)': 'loadParam.rough_load.Floorage',
        '采暖面积/建筑面积': 'loadParam.rough_load.HeatingAreaRatio',
        '空调面积/建筑面积': 'loadParam.rough_load.CoolingAreaRatio',
        '单位建筑面积热负荷指标(正值，W/㎡)': 'loadParam.rough_load.UnitFloorageHeatingLoadIndex',
        '单位建筑面积冷负荷指标(负值，W/㎡)': 'loadParam.rough_load.UnitFloorageCoolingLoadIndex',
        '热负荷指标(正值/kW)': 'loadParam.rough_load.HeatingLoadIndex',
        '冷负荷指标(负值/kW)': 'loadParam.rough_load.CoolingLoadIndex',
        日采暖制冷起始时间: 'loadParam.rough_load.dayCycleStart',
        日采暖制冷结束时间: 'loadParam.rough_load.dayCycleEnd'
    },
    '采暖制冷负荷-分月详细负荷-不区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return ['分月详细负荷'];
            }
        },
        '建筑面积(m2)': 'loadParam.single_line_load.Floorage',
        区分工作日和休息日: 'loadParam.single_line_load.isDayOff'
    },
    '采暖制冷负荷-分月详细负荷-区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return ['分月详细负荷'];
            }
        },
        '建筑面积(m2)': 'loadParam.single_line_load.Floorage',
        区分工作日和休息日: 'loadParam.single_line_load.isDayOff'
    },
    '采暖制冷负荷-自定义负荷': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: function(data) {
                if(!data) {
                    console.log("ERROR");
                }
                return ['自定义负荷'];
            }
        }
    }
};


equipmentParamDict ={
    PhotovoltaicSys: {
        ratedParam: [
            {
                prop: 'singlePanelArea',
                description: '单个光伏板面积(m²)'
            },
            { prop: 'photoelectricConversionEfficiency', description: '光电转换效率(%)' },
        ],
        operationalConstraints: [
            {
                prop: 'maxPowerGenerating',
                description: '最大发电功率(kW)'
            },
        ]
    },
    WindPowerGenerator: {
        ratedParam: [
            { prop: 'ratedPowerGenerating', description: '额定容量(kW)' },
            {
                prop: 'ratedWindSpeed',
                description: '额定风速(m/s)'
            },
            { prop: 'cutinWindSpeed', description: '切入风速(m/s)' },
            {
                prop: 'cutoutWindSpeed',
                description: '切出风速(m/s)'
            },
            { prop: 'towerHeight', description: '塔筒高度(m)' },
        ],
        operationalConstraints: []
    },
    GasTurbine: {
        ratedParam: [
            { prop: 'powerGenerating', description: '额定发电功率(kW)' },
            {
                prop: 'generatingEfficiency',
                description: '发电效率(%)'
            },
            { prop: 'heatingEfficiency', description: '制热效率(%)' },
        ],
        operationalConstraints: [
            {
                prop: 'maxExhaustOutletTemp',
                description: '最大烟气出口温度(℃)'
            },
            { prop: 'miniExhaustOutletTemp', description: '最小烟气出口温度(℃)' },
            {
                prop: 'maxPressure',
                description: '机组最大承压(MPa)'
            },
        ]
    },
    GasEngine: {
        ratedParam: [
            {
                prop: 'powerGenerating',
                description: '额定发电功率(kW)'
            },
            { prop: 'generatingEfficiency', description: '发电效率(%)' },
            {
                prop: 'heatingEfficiency',
                description: '制热效率(%)'
            },
            { prop: 'waterMassFlowrate', description: '循环水流量(t/h)' },
        ],
        operationalConstraints: [
            {
                prop: 'maxHeatWaterOutletTemp',
                description: '最大热水出口温度(℃)'
            },
            { prop: 'miniHeatWaterOutletTemp', description: '最小热水出口温度(℃)' },
            {
                prop: 'maxHeatWaterInletTemp',
                description: '最大热水进口温度(℃)'
            },
            { prop: 'miniHeatWaterInletTemp', description: '最小热水进口温度(℃)' },
            {
                prop: 'maxExhaustOutletTemp',
                description: '最大烟气出口温度(℃)'
            },
            { prop: 'miniExhaustOutletTemp', description: '最小烟气出口温度(℃)' },
            {
                prop: 'maxPressure',
                description: '机组最大承压(MPa)'
            },
        ]
    },
    SteamTurbine: {
        ratedParam: [
            {
                prop: 'ratedSteamInletTemp',
                description: '额定蒸汽进口温度(℃)'
            },
            { prop: 'steamMassFlowrate', description: '蒸汽流量(t/h)' },
            {
                prop: 'generatingEfficiency',
                description: '发电效率(%)'
            },
        ],
        operationalConstraints: [
            {
                prop: 'maxSteamInletTemp',
                description: '最大蒸汽进口温度(℃)'
            },
            { prop: 'miniSteamInletTemp', description: '最小蒸汽进口温度(℃)' },
            {
                prop: 'maxPowerGenerating',
                description: '最大发电量(kW)'
            },
            { prop: 'miniPowerGenerating', description: '最小发电量(kW)' },
            {
                prop: 'maxPressure',
                description: '机组最大承压(MPa)'
            },
        ]
    },
    HeatPump: {
        ratedParam: [
            { prop: 'ratedHeatSupply', description: '额定制热量(kW)' },
            {
                prop: 'heatingCOP',
                description: '额定能效比COP'
            },
            { prop: 'ratedCoolSupply', description: '额定制冷量(kW)' },
            { prop: 'coolingCOP', description: '制冷能效比COP' },
        ],
        operationalConstraints: [
            {
                prop: 'maxHeatWaterOutletTemp',
                description: '最大热水出口温度(℃)'
            },
            { prop: 'miniHeatWaterOutletTemp', description: '最小热水出口温度(℃)' },
            {
                prop: 'maxHeatWaterInletTemp',
                description: '最大热水进口温度(℃)'
            },
            { prop: 'miniHeatWaterInletTemp', description: '最小热水进口温度(℃)' },
            {
                prop: 'maxColdWaterOutletTemp',
                description: '最大冷水出口温度(℃)'
            },
            { prop: 'miniColdWaterOutletTemp', description: '最小冷水出口温度(℃)' },
            {
                prop: 'maxColdWaterInletTemp',
                description: '最大冷水进口温度(℃)'
            },
            { prop: 'miniColdWaterInletTemp', description: '最小冷水进口温度(℃)' },
            {
                prop: 'maxVoltage',
                description: '最大工作电压(V)'
            },
            { prop: 'miniVoltage', description: '最小工作电压(V)' },
            { prop: 'maxPressure', description: '机组最大承压(MPa)' },
        ]
    },
    HPSolarCollector: {
        ratedParam: [
            {
                prop: 'plateArea',
                description: '单个集热器面积(m²)'
            },
            { prop: 'collectionEfficiency', description: '集热效率(%)' },
        ],
        operationalConstraints: [
            {
                prop: 'maxHeatWaterOutletTemp',
                description: '最大热水出口温度(℃)'
            },
            { prop: 'miniHeatWaterOutletTemp', description: '最小热水出口温度(℃)' },
            {
                prop: 'maxHeatWaterInletTemp',
                description: '最大热水进口温度(℃)'
            },
            { prop: 'miniHeatWaterInletTemp', description: '最小热水进口温度(℃)' },
            {
                prop: 'maxPressure',
                description: '机组最大承压(MPa)'
            },
        ]
    },
    CompRefrg: {
        ratedParam: [
            { prop: 'ratedCoolSupply', description: '额定制冷量(kW)' },
            {
                prop: 'COP',
                description: '制冷能效比COP'
            },
        ],
        operationalConstraints: [
            {
                prop: 'maxColdWaterOutletTemp',
                description: '最大冷水出口温度(℃)'
            },
            { prop: 'miniColdWaterOutletTemp', description: '最小冷水出口温度(℃)' },
            {
                prop: 'maxColdWaterInletTemp',
                description: '最大冷水进口温度(℃)'
            },
            { prop: 'miniColdWaterInletTemp', description: '最小冷水进口温度(℃)' },
            {
                prop: 'maxPressure',
                description: '机组最大承压(MPa)'
            },
        ]
    },
    IceStorageAC: {
        ratedParam: [
            {
                prop: 'ratedChargingCool',
                description: '额定蓄冷功率(kW)'
            },
            { prop: 'chargingEfficiency', description: '蓄冷效率(%)' },
            {
                prop: 'ratedDischargingCool',
                description: '额定放冷功率(kW)'
            },
            { prop: 'dischargingEfficiency', description: '放冷效率(%)' },
        ],
        operationalConstraints: [
            {
                prop: 'maxColdWaterOutletTemp',
                description: '最大冷水出口温度(℃)'
            },
            { prop: 'miniColdWaterOutletTemp', description: '最小冷水出口温度(℃)' },
            {
                prop: 'maxColdWaterInletTemp',
                description: '最大冷水进口温度(℃)'
            },
            { prop: 'miniColdWaterInletTemp', description: '最小冷水进口温度(℃)' },
            {
                prop: 'capacity',
                description: '蓄冰空调最大容量(kWh)'
            },
        ]
    },
    HeatStorageElectricalBoiler: {
        ratedParam: [
            {
                prop: 'ratedChargingHeat',
                description: '额定蓄热功率(kW)'
            },
            { prop: 'chargingEfficiency', description: '蓄热效率(%)' },
            {
                prop: 'ratedDischargingHeat',
                description: '额定放热功率(kW)'
            },
            { prop: 'dischargingEfficiency', description: '放热效率(%)' },
        ],
        operationalConstraints: [
            {
                prop: 'maxHeatWaterOutletTemp',
                description: '最大热水出口温度(℃)'
            },
            { prop: 'miniHeatWaterOutletTemp', description: '最小热水出口温度(℃)' },
            {
                prop: 'maxHeatWaterInletTemp',
                description: '最大热水进口温度(℃)'
            },
            { prop: 'miniHeatWaterInletTemp', description: '最小热水进口温度(℃)' },
            {
                prop: 'capacity',
                description: '蓄热电锅炉最大容量(kWh)'
            },
        ]
    },
    Battery: {
        ratedParam: [
            { prop: 'ratedChargingPower', description: '额定充电功率(kW)' },
            {
                prop: 'chargingEfficiency',
                description: '充电效率(%)'
            },
            { prop: 'ratedDischargingPower', description: '额定放电功率(kW)' },
            {
                prop: 'dischargingEfficiency',
                description: '放电效率(%)'
            },
        ],
        operationalConstraints: [{ prop: 'capacity', description: '电池最大容量(kWh)' }]
    },
    Transformer: {
        ratedParam: [
            {
                prop: 'wind1RatioVoltage',
                description: '原边侧额定电压有效值(kV)'
            },
            { prop: 'wind2RatioVoltage', description: '副边侧额定电压有效值(V)' },
            {
                prop: 'excitationConductance',
                description: '励磁电导(p.u.)'
            },
            { prop: 'excitationAdmittance', description: '励磁电纳(p.u.)' },
        ],
        operationalConstraints: [
            { prop: 'maxWind2Ratio', description: '最大非标准变比(p.u.)' },
            {
                prop: 'miniWind2Ratio',
                description: '最小非标准变比(p.u.)'
            },
        ]
    },
    TransferLine: {
        ratedParam: [
            { prop: 'ratedVoltage', description: '额定电压(kV)' },
            {
                prop: 'ratedFrequency',
                description: '额定频率(Hz)'
            },
            {
                prop: 'resistanceOfUnitLength',
                description: '单位长度正序电阻(p.u./km)'
            },
            { prop: 'reactanceOfUnitLength', description: '单位长度正序电抗(p.u./km)' },
            {
                prop: 'chargingBofUnitLength',
                description: '单位长度正序电纳(p.u./km)'
            },
        ],
        operationalConstraints: [],
        economicParam: [
            { prop: 'purchaseCost', description: '采购成本(万元/km)' },
            { prop: 'maintainCost', description: '维护成本(元/(km·年))' },
            { prop: 'designLife', description: '设计寿命(年)' },
        ]
    },
    Capacitance: {
        ratedParam: [
            { prop: 'ratedVoltage', description: '额定容量(MVA)' },
            {
                prop: 'validRatedVoltage',
                description: '额定电压有效值(Hz)'
            },
        ],
        operationalConstraints: []
    },
    CentrifugalPump: {
        ratedParam: [
            { prop: 'operationCurveParamA', description: '工作特性曲线系数A' },
            {
                prop: 'operationCurveParamB',
                description: '工作特性曲线系数B'
            },
            { prop: 'operationCurveParamC', description: '工作特性曲线系数C' },
            { prop: 'efficency', description: '泵效率(%)' },
        ],
        operationalConstraints: [
            {
                prop: 'miniInletPressure',
                description: '最低进口压力(MPa)'
            },
            { prop: 'maxInlePressure', description: '最大进口压力(MPa)' },
        ]
    },
    Pump: {
        ratedParam: [
            { prop: 'operationCurveParamA', description: '工作特性曲线系数A' },
            {
                prop: 'operationCurveParamB',
                description: '工作特性曲线系数B'
            },
            { prop: 'operationCurveParamC', description: '工作特性曲线系数C' },
            { prop: 'efficency', description: '泵效率(%)' },
        ],
        operationalConstraints: [
            {
                prop: 'miniInletPressure',
                description: '最低进口压力(MPa)'
            },
            { prop: 'maxInlePressure', description: '最大进口压力(MPa)' },
        ]
    },
    Pipe: {
        ratedParam: [
            { prop: 'interDiameter', description: '管道内径(mm)' },
            {
                prop: 'thickness',
                description: '管道壁厚(mm)'
            },
            { prop: 'roughness', description: '管道粗糙度(mm)' },
            {
                prop: 'heatExchangeFactor',
                description: '管道总传热系数(W/(m·K))'
            },
        ],
        operationalConstraints: [{ prop: 'maxPressure', description: '管道设计压力(MPa)' }],
        economicParam: [
            { prop: 'purchaseCost', description: '采购成本(元/m)' },
            { prop: 'maintainCost', description: '维护成本(元/(m·年))' },
            { prop: 'designLife', description: '设计寿命(年)' },
        ]
    }
};
/** */
specialEquipmentParamDict = {
    GasBoiler: [
        {
            conditions: [{ value: '燃气热水锅炉', path: ['ratedParam', 'boilerType'], defaultValue: '燃气热水锅炉' }],
            paramDict: {
                ratedParam: [
                    {
                        prop: 'boilerType',
                        description: '燃气锅炉类型',
                        option: ['燃气热水锅炉', '燃气蒸汽锅炉']
                    },
                    { prop: 'ratedHeatSupply', description: '额定供热量(kW)' },
                    { prop: 'heatingEfficiency', description: '制热效率(%)' },
                ],
                operationalConstraints: [
                    { prop: 'maxHeatWaterOutletTemp', description: '最大热水出口温度(℃)' },
                    { prop: 'miniHeatWaterOutletTemp', description: '最小热水出口温度(℃)' },
                    { prop: 'maxHeatWaterInletTemp', description: '最大热水进口温度(℃)' },
                    { prop: 'miniHeatWaterInletTemp', description: '最小热水进口温度(℃)' },
                    { prop: 'maxPressure', description: '机组最大承压(MPa)' },
                ]
            }
        },
        {
            conditions: [{ value: '燃气蒸汽锅炉', path: ['ratedParam', 'boilerType'], defaultValue: '燃气热水锅炉' }],
            paramDict: {
                ratedParam: [
                    {
                        prop: 'boilerType',
                        description: '燃气锅炉类型',
                        option: ['燃气热水锅炉', '燃气蒸汽锅炉']
                    },
                    { prop: 'ratedHeatSupply', description: '额定供热量(kW)' },
                    { prop: 'heatingEfficiency', description: '制热效率(%)' },
                ],
                operationalConstraints: [
                    { prop: 'maxSteamOutletTemp', description: '最大蒸汽出口温度(℃)' },
                    { prop: 'miniSteamOutletTemp', description: '最小蒸汽出口温度(℃)' },
                    { prop: 'maxPressure', description: '机组最大承压(MPa)' },
                ]
            }
        },
    ],
    HeatRecoveryBoiler: [
        {
            conditions: [{ value: '余热热水锅炉', path: ['ratedParam', 'boilerType'], defaultValue: '余热热水锅炉' }],
            paramDict: {
                ratedParam: [
                    {
                        prop: 'boilerType',
                        description: '燃气锅炉类型',
                        option: ['余热热水锅炉', '余热蒸汽锅炉']
                    },
                    { prop: 'ratedHeatSupply', description: '额定供热量(kW)' },
                    { prop: 'heatExchangeEfficiency', description: '换热效率(%)' },
                ],
                operationalConstraints: [
                    { prop: 'maxExhaustOutletTemp', description: '最大烟气出口温度(℃)' },
                    { prop: 'miniExhaustOutletTemp', description: '最小烟气出口温度(℃)' },
                    { prop: 'maxExhaustInletTemp', description: '最大烟气进口温度(℃)' },
                    { prop: 'miniExhaustInletTemp', description: '最小烟气进口温度(℃)' },
                    { prop: 'maxHeatWaterOutletTemp', description: '最大热水出口温度(℃)' },
                    { prop: 'miniHeatWaterOutletTemp', description: '最小热水出口温度(℃)' },
                    { prop: 'maxHeatWaterInletTemp', description: '最大热水进口温度(℃)' },
                    { prop: 'miniHeatWaterInletTemp', description: '最小热水进口温度(℃)' },
                    { prop: 'maxPressure', description: '机组最大承压(MPa)' },
                ]
            }
        },
        {
            conditions: [
                { value: '余热蒸汽锅炉', path: ['ratedParam', 'boilerType'], defaultValue: '余热热水锅炉' },
                { value: '单压', path: ['ratedParam', 'pressureLevel'], defaultValue: '单压' },
            ],
            paramDict: {
                ratedParam: [
                    {
                        prop: 'boilerType',
                        description: '燃气锅炉类型',
                        option: ['余热热水锅炉', '余热蒸汽锅炉']
                    },
                    {
                        prop: 'pressureLevel',
                        description: '压力等级',
                        option: ['单压', '双压']
                    },
                    { prop: 'ratedHeatSupply', description: '额定供热量(kW)' },
                    { prop: 'heatExchangeEfficiency', description: '换热效率(%)' },
                ],
                operationalConstraints: [
                    { prop: 'maxExhaustOutletTemp', description: '最大烟气出口温度(℃)' },
                    { prop: 'miniExhaustOutletTemp', description: '最小烟气出口温度(℃)' },
                    { prop: 'maxExhaustInletTemp', description: '最大烟气进口温度(℃)' },
                    { prop: 'miniExhaustInletTemp', description: '最小烟气进口温度(℃)' },
                    { prop: 'maxSteamOutletTemp', description: '最大蒸汽出口温度(℃)' },
                    { prop: 'miniSteamOutletTemp', description: '最小蒸汽出口温度(℃)' },
                    { prop: 'maxPressure', description: '机组最大承压(MPa)' },
                ]
            }
        },
        {
            conditions: [
                { value: '余热蒸汽锅炉', path: ['ratedParam', 'boilerType'], defaultValue: '余热热水锅炉' },
                { value: '双压', path: ['ratedParam', 'pressureLevel'], defaultValue: '单压' },
            ],
            paramDict: {
                ratedParam: [
                    {
                        prop: 'boilerType',
                        description: '燃气锅炉类型',
                        option: ['余热热水锅炉', '余热蒸汽锅炉']
                    },
                    {
                        prop: 'pressureLevel',
                        description: '压力等级',
                        option: ['单压', '双压']
                    },
                    { prop: 'ratedHeatSupply', description: '额定供热量(kW)' },
                    { prop: 'heatExchangeEfficiency', description: '换热效率(%)' },
                ],
                operationalConstraints: [
                    { prop: 'maxExhaustOutletTemp', description: '最大烟气出口温度(℃)' },
                    { prop: 'miniExhaustOutletTemp', description: '最小烟气出口温度(℃)' },
                    { prop: 'maxExhaustInletTemp', description: '最大烟气进口温度(℃)' },
                    { prop: 'miniExhaustInletTemp', description: '最小烟气进口温度(℃)' },
                    { prop: 'maxSteamOutletTemp', description: '最大蒸汽出口温度(℃)' },
                    { prop: 'miniSteamOutletTemp', description: '最小蒸汽出口温度(℃)' },
                    { prop: 'maxSubSteamOutletTemp', description: '最大次高压蒸汽出口温度(℃)' },
                    { prop: 'miniSubSteamOutletTemp', description: '最小次高压蒸汽出口温度(℃)' },
                    { prop: 'maxHighSteamOutletTemp', description: '最大高压蒸汽出口温度(℃)' },
                    { prop: 'miniHighSteamOutletTemp', description: '最小高压蒸汽出口温度(℃)' },
                    { prop: 'maxPressure', description: '机组最大承压(MPa)' },
                ]
            }
        },
    ],
    AbsorptionChiller: [
        {
            conditions: [{ value: '热水', path: ['ratedParam', 'heatFluidType'], defaultValue: '热水' }],
            paramDict: {
                ratedParam: [
                    { prop: 'heatFluidType', description: '热源流体类型', option: ['热水', '蒸汽', '烟气'] },
                    { prop: 'ratedCoolSupply', description: '制冷状态额定制冷量(kW)' },
                    { prop: 'coldHeatRatio', description: '制冷状态时冷热比' },
                    { prop: 'ratedHeatSupply', description: '制热状态额定制热量(kW)' },
                    { prop: 'heatExchangeEfficiency', description: '制热状态时换热效率(%)' },
                    { prop: 'ratedPowerConsume', description: '用电功率(kW)' },
                ],
                operationalConstraints: [
                    { prop: 'maxHeatSourceOutletTemp', description: '最大热源出口温度(℃)' },
                    { prop: 'miniHeatSourceOutletTemp', description: '最小热源出口温度(℃)' },
                    { prop: 'maxHeatSourceInletTemp', description: '最大热源进口温度(℃)' },
                    { prop: 'miniHeatSourceInletTemp', description: '最小热源进口温度(℃)' },
                    { prop: 'maxColdWaterOutletTemp', description: '最大冷水出口温度(℃)' },
                    { prop: 'miniColdWaterOutletTemp', description: '最小冷水出口温度(℃)' },
                    { prop: 'maxColdWaterInletTemp', description: '最大冷水进口温度(℃)' },
                    { prop: 'miniColdWaterInletTemp', description: '最小冷水进口温度(℃)' },
                    { prop: 'maxHeatWaterOutletTemp', description: '最大热水出口温度(℃)' },
                    { prop: 'miniHeatWaterOutletTemp', description: '最小热水出口温度(℃)' },
                    { prop: 'maxHeatWaterInletTemp', description: '最大热水进口温度(℃)' },
                    { prop: 'miniHeatWaterInletTemp', description: '最小热水进口温度(℃)' },
                    { prop: 'maxVoltage', description: '最大工作电压(V)' },
                    { prop: 'miniVoltage', description: '最小工作电压(V)' },
                    { prop: 'maxPressure', description: '机组最大承压(MPa)' },
                ]
            }
        },
        {
            conditions: [{ value: '蒸汽', path: ['ratedParam', 'heatFluidType'], defaultValue: '热水' }],
            paramDict: {
                ratedParam: [
                    { prop: 'heatFluidType', description: '热源流体类型', option: ['热水', '蒸汽', '烟气'] },
                    { prop: 'ratedCoolSupply', description: '制冷状态额定制冷量(kW)' },
                    { prop: 'coldHeatRatio', description: '制冷状态时冷热比' },
                    { prop: 'ratedHeatSupply', description: '制热状态额定制热量(kW)' },
                    { prop: 'heatExchangeEfficiency', description: '制热状态时换热效率(%)' },
                    { prop: 'ratedPowerConsume', description: '用电功率(kW)' },
                ],
                operationalConstraints: [
                    { prop: 'maxSteamInletTemp', description: '最大蒸汽进口温度(℃)' },
                    { prop: 'miniSteamInletTemp', description: '最小蒸汽进口温度(℃)' },
                    { prop: 'maxColdWaterOutletTemp', description: '最大冷水出口温度(℃)' },
                    { prop: 'miniColdWaterOutletTemp', description: '最小冷水出口温度(℃)' },
                    { prop: 'maxColdWaterInletTemp', description: '最大冷水进口温度(℃)' },
                    { prop: 'miniColdWaterInletTemp', description: '最小冷水进口温度(℃)' },
                    { prop: 'maxHeatWaterOutletTemp', description: '最大热水出口温度(℃)' },
                    { prop: 'miniHeatWaterOutletTemp', description: '最小热水出口温度(℃)' },
                    { prop: 'maxHeatWaterInletTemp', description: '最大热水进口温度(℃)' },
                    { prop: 'miniHeatWaterInletTemp', description: '最小热水进口温度(℃)' },
                    { prop: 'maxVoltage', description: '最大工作电压(V)' },
                    { prop: 'miniVoltage', description: '最小工作电压(V)' },
                    { prop: 'maxPressure', description: '机组最大承压(MPa)' },
                ]
            }
        },
        {
            conditions: [{ value: '烟气', path: ['ratedParam', 'heatFluidType'], defaultValue: '热水' }],
            paramDict: {
                ratedParam: [
                    { prop: 'heatFluidType', description: '热源流体类型', option: ['热水', '蒸汽', '烟气'] },
                    { prop: 'ratedCoolSupply', description: '制冷状态额定制冷量(kW)' },
                    { prop: 'coldHeatRatio', description: '制冷状态时冷热比' },
                    { prop: 'ratedHeatSupply', description: '制热状态额定制热量(kW)' },
                    { prop: 'heatExchangeEfficiency', description: '制热状态时换热效率(%)' },
                    { prop: 'ratedPowerConsume', description: '用电功率(kW)' },
                ],
                operationalConstraints: [
                    { prop: 'maxExhaustOutletTemp', description: '最大烟气出口温度(℃)' },
                    { prop: 'miniExhaustOutletTemp', description: '最小烟气出口温度(℃)' },
                    { prop: 'maxExhaustInletTemp', description: '最大烟气进口温度(℃)' },
                    { prop: 'miniExhaustInletTemp', description: '最小烟气进口温度(℃)' },
                    { prop: 'maxColdWaterOutletTemp', description: '最大冷水出口温度(℃)' },
                    { prop: 'miniColdWaterOutletTemp', description: '最小冷水出口温度(℃)' },
                    { prop: 'maxColdWaterInletTemp', description: '最大冷水进口温度(℃)' },
                    { prop: 'miniColdWaterInletTemp', description: '最小冷水进口温度(℃)' },
                    { prop: 'maxHeatWaterOutletTemp', description: '最大热水出口温度(℃)' },
                    { prop: 'miniHeatWaterOutletTemp', description: '最小热水出口温度(℃)' },
                    { prop: 'maxHeatWaterInletTemp', description: '最大热水进口温度(℃)' },
                    { prop: 'miniHeatWaterInletTemp', description: '最小热水进口温度(℃)' },
                    { prop: 'maxVoltage', description: '最大工作电压(V)' },
                    { prop: 'miniVoltage', description: '最小工作电压(V)' },
                    { prop: 'maxPressure', description: '机组最大承压(MPa)' },
                ]
            }
        },
    ],
    HeatExchanger: [
        {
            paramDict: {
                ratedParam: [
                    { prop: 'heatSourceType', description: '热流体类型', option: ['热水', '烟气'] },
                    { prop: 'ratedHeatLoad', description: '额定热负荷(kW)' },
                    { prop: 'heatExchangeEfficiency', description: '换热效率(%)' },
                ],
                operationalConstraints: [
                    { prop: 'maxHeatSourceOutletTemp', description: '最大热流体出口温度(℃)' },
                    { prop: 'miniHeatSourceOutletTemp', description: '最小热流体出口温度(℃)' },
                    { prop: 'maxHeatSourceInletTemp', description: '最大热流体进口温度(℃)' },
                    { prop: 'miniHeatSourceInletTemp', description: '最小热流体进口温度(℃)' },
                    { prop: 'maxColdFluidOutletTemp', description: '最大冷流体出口温度(℃)' },
                    { prop: 'miniColdFluidOutletTemp', description: '最小冷流体出口温度(℃)' },
                    { prop: 'maxColdFluidInletTemp', description: '最大冷流体进口温度(℃)' },
                    { prop: 'miniColdFluidInletTemp', description: '最小冷流体进口温度(℃)' },
                    { prop: 'maxPressure', description: '机组最大承压(MPa)' },
                ]
            }
        },
    ]
};
/** */
commonEconomicParams = [
    { prop: 'purchaseCost', description: '采购成本(万元/台)' },
    { prop: 'maintainCost', description: '固定维护成本(万元/年)' },
    { prop: 'maintainCost', description: '可变维护成本(元/kWh)' },
    { prop: 'designLife', description: '设计寿命(年)' },
];

equipmentParamDict2 = {
    PhotovoltaicSys_ies: {
        ratedParam: [
            {
                prop: 'SinglePanelArea',
                description: '光伏板面积(m²)',
            },
            { prop: 'ConversionEfficiency', description: '光电转换效率(%)' },
            {
                prop: 'PowerFactor',
                description: '功率因数',
                option: 'number',
            },
        ],
        operationalConstraints: [
            {
                prop: 'maxPowerGenerating',
                description: '最大发电功率(kW)',
            },
        ],
    },
    WindPowerGenerator_ies: {
        ratedParam: [
            { prop: 'RatedPowerGenerating', description: '额定发电量(kW)' },
            {
                prop: 'RatedWindSpeed',
                description: '额定风速(m/s)',
            },
            { prop: 'CutinWindSpeed', description: '切入风速(m/s)' },
            {
                prop: 'CutoutWindSpeed',
                description: '切出风速(m/s)',
            },
            { prop: 'HubHeight', description: '轮毂高度(m)' },
            {
                prop: 'PowerFactor',
                description: '功率因数',
                option: 'number',
            },
        ],
        operationalConstraints: [],
    },
    GasEngine_ies: {
        ratedParam: [
            {
                prop: 'powerGenerating',
                description: '额定发电功率(kW)',
            },
            { prop: 'generatingEfficiency', description: '发电效率(%)' },
            {
                prop: 'heatingEfficiency',
                description: '制热效率(%)',
            },
            { prop: 'waterMassFlowrate', description: '循环水流量(t/h)' },
            {
                prop: 'PowerFactor',
                description: '功率因数',
                option: 'number',
            },
        ],
        operationalConstraints: [
            {
                prop: 'maxHeatWaterOutletTemp',
                description: '最大热水出口温度(℃)',
            },
            { prop: 'miniHeatWaterOutletTemp', description: '最小热水出口温度(℃)' },
            {
                prop: 'maxHeatWaterInletTemp',
                description: '最大热水进口温度(℃)',
            },
            { prop: 'miniHeatWaterInletTemp', description: '最小热水进口温度(℃)' },
            {
                prop: 'maxExhaustOutletTemp',
                description: '最大烟气出口温度(℃)',
            },
            { prop: 'miniExhaustOutletTemp', description: '最小烟气出口温度(℃)' },
            {
                prop: 'maxPressure',
                description: '机组最大承压(MPa)',
            },
        ],
    },
    SteamTurbine_ies: {
        ratedParam: [
            {
                prop: 'ratedSteamInletTemp',
                description: '额定蒸汽进口温度(℃)',
            },
            { prop: 'steamMassFlowrate', description: '蒸汽流量(t/h)' },
            {
                prop: 'generatingEfficiency',
                description: '发电效率(%)',
            },
            {
                prop: 'PowerFactor',
                description: '功率因数',
                option: 'number',
            },
        ],
        operationalConstraints: [
            {
                prop: 'maxSteamInletTemp',
                description: '最大蒸汽进口温度(℃)',
            },
            { prop: 'miniSteamInletTemp', description: '最小蒸汽进口温度(℃)' },
            {
                prop: 'maxPowerGenerating',
                description: '最大发电量(kW)',
            },
            { prop: 'miniPowerGenerating', description: '最小发电量(kW)' },
            {
                prop: 'maxPressure',
                description: '机组最大承压(MPa)',
            },
        ],
    },
    HPSolarCollector_ies: {
        ratedParam: [
            {
                prop: 'LocalPressureDropCoe',
                description: '局部压降系数 (kPa/(m³·s⁻¹)²)',
            },
            {
                prop: 'PlateArea',
                description: '集热器面积(m²)',
            },
            { prop: 'CollectionEfficiency', description: '集热效率(%)' },
        ],
        operationalConstraints: [
            {
                prop: 'MiniOutletTemp',
                description: '最小供水温度 (℃)',
            },
            { prop: 'MaxOutletTemp', description: '最大供水温度 (℃)' },
        ],
    },
    IceStorageAC_ies: {
        ratedParam: [
            {
                prop: 'ratedChargingCool',
                description: '额定蓄冷功率(kW)',
            },
            { prop: 'chargingEfficiency', description: '蓄冷效率(%)' },
            {
                prop: 'ratedDischargingCool',
                description: '额定放冷功率(kW)',
            },
            { prop: 'dischargingEfficiency', description: '放冷效率(%)' },
            {
                prop: 'PowerFactor',
                description: '功率因数',
                option: 'number',
            },
        ],
        operationalConstraints: [
            {
                prop: 'maxColdWaterOutletTemp',
                description: '最大冷水出口温度(℃)',
            },
            { prop: 'miniColdWaterOutletTemp', description: '最小冷水出口温度(℃)' },
            {
                prop: 'maxColdWaterInletTemp',
                description: '最大冷水进口温度(℃)',
            },
            { prop: 'miniColdWaterInletTemp', description: '最小冷水进口温度(℃)' },
            {
                prop: 'capacity',
                description: '蓄冰空调最大容量(kWh)',
            },
        ],
    },
    HeatStorageElectricalBoiler_ies: {
        ratedParam: [
            {
                prop: 'ratedChargingHeat',
                description: '额定蓄热功率(kW)',
            },
            { prop: 'chargingEfficiency', description: '蓄热效率(%)' },
            {
                prop: 'ratedDischargingHeat',
                description: '额定放热功率(kW)',
            },
            { prop: 'dischargingEfficiency', description: '放热效率(%)' },
        ],
        operationalConstraints: [
            {
                prop: 'maxHeatWaterOutletTemp',
                description: '最大热水出口温度(℃)',
            },
            { prop: 'miniHeatWaterOutletTemp', description: '最小热水出口温度(℃)' },
            {
                prop: 'maxHeatWaterInletTemp',
                description: '最大热水进口温度(℃)',
            },
            { prop: 'miniHeatWaterInletTemp', description: '最小热水进口温度(℃)' },
            {
                prop: 'capacity',
                description: '蓄热电锅炉最大容量(kWh)',
            },
        ],
    },
    Battery_ies: {
        ratedParam: [
            {
                prop: 'ChargingEfficiency',
                description: '充电效率(%)',
            },
            {
                prop: 'DischargingEfficiency',
                description: '放电效率(%)',
            },
            {
                prop: 'PowerFactor',
                description: '功率因数',
                option: 'number',
            },
        ],
        operationalConstraints: [
            {
                prop: 'MaxChargingPower',
                description: '最大充电功率(kW)',
            },
            {
                prop: 'MaxDischargingPower',
                description: '最大放电功率(kW)',
            },
            {
                prop: 'PowerStorageLimit',
                description: '电池最大容量(kWh)',
            },
        ],
    },
    WaterTank_ies: {
        ratedParam: [
            { prop: 'InletLocalPressureDropCoe', description: '入口侧局部压降系数(kPa/(m³·s⁻¹)²)' },
            {
                prop: 'OutletLocalPressureDropCoe',
                description: '出口侧局部压降系数(kPa/(m³·s⁻¹)²)',
            },
            { prop: 'FloorArea', description: '罐底面积(m²)' },
        ],
        operationalConstraints: [
            { prop: 'MaxWaterLevel', description: '最大允许水位高度(m)' },
            { prop: 'MiniWaterLevel', description: '最小允许水位高度(m)' },
        ],
    },
    // 光伏
    Transformer_ies: {
        ratedParam: [
            { prop: 'windingMVABase', description: '额定容量(MVA)' },
            {
                prop: 'shortCircuitResistance',
                description: '一次侧短路电阻(Ω)',
            },
            { prop: 'shortCircuitImpedance', description: '一次侧短路电抗(Ω)' },
            {
                prop: 'wind2Ratio',
                description: '变压器非标准变比(p.u.)',
            },
        ],
        operationalConstraints: [
            { prop: 'maxWind2Ratio', description: '最大非标准变比(p.u.)' },
            {
                prop: 'miniWind2Ratio',
                description: '最小非标准变比(p.u.)',
            },
        ],
    },
    TransferLine_ies: {
        ratedParam: [
            {
                prop: 'resistanceOfUnitLength',
                description: '单位长度电阻(Ω/km)',
            },
            { prop: 'reactanceOfUnitLength', description: '单位长度电抗(Ω/km)' },
            {
                prop: 'chargingBofUnitLength',
                description: '单位长度容抗(MΩ*km)',
            },
        ],
        operationalConstraints: [],
        economicParam: [
            { prop: 'purchaseCost', description: '采购成本(万元/km)' },
            { prop: 'maintainCost', description: '维护成本(元/(km·年))' },
            { prop: 'designLife', description: '设计寿命(年)' },
        ],
    },
    Capacitance_ies: {
        ratedParam: [
            { prop: 'ratedVoltage', description: '额定容量(MVA)' },
            {
                prop: 'validRatedVoltage',
                description: '额定电压有效值(Hz)',
            },
        ],
        operationalConstraints: [],
    },
    MMC_ies: {
        ratedParam: [{ prop: 'BaseVoltage', description: '额定电压(kV)' }],
        operationalConstraints: [],
    },
    Pipe_ies: {
        ratedParam: [
            { prop: 'interDiameter', description: '管道内径(mm)' },
            {
                prop: 'thickness',
                description: '管道壁厚(mm)',
            },
            { prop: 'roughness', description: '管道粗糙度(mm)' },
            {
                prop: 'heatExchangeFactor',
                description: '管道总传热系数(W/(m·K))',
            },
        ],
        operationalConstraints: [{ prop: 'maxPressure', description: '管道设计压力(MPa)' }],
        economicParam: [
            { prop: 'purchaseCost', description: '采购成本(元/m)' },
            { prop: 'maintainCost', description: '维护成本(元/(m·年))' },
            { prop: 'designLife', description: '设计寿命(年)' },
        ],
    },
    // 燃气轮机
    GasTurbine_ies: {
        ratedParam: [
            {
                prop: 'LocalPressureDropCoe',
                description: '局部压降系数 (kPa/(m³·s⁻¹)²)',
            },
            {
                prop: 'PowerFactor',
                description: '功率因数',
                option: 'number',
            },
        ],
        operationalConstraints: [
            {
                prop: 'MiniOutletTemp',
                description: '最小供水温度 (℃)',
            },
            { prop: 'MaxOutletTemp', description: '最大供水温度 (℃)' },
        ],
        OperateParam: [
            {
                data: 'OperateStatus',
                key: 'OperateStatus',
                title: '挡位',
                type: 'text',
            },
            {
                data: 'GeneratingPower',
                key: 'GeneratingPower',
                title: '发电功率[kW]',
                type: 'text',
            },
            {
                data: 'GeneratingEfficiency',
                key: 'GeneratingEfficiency',
                title: '发电效率[%]',
                type: 'text',
            },
            {
                data: 'HeatEfficiency',
                key: 'HeatEfficiency',
                title: '制热效率[%]',
                type: 'text',
            },
        ],
    },
    // 热泵
    HeatPump_ies: {
        ratedParam: [
            { prop: 'LocalPressureDropCoe', description: '局部压降系数 (kPa/(m³·s⁻¹)²)' },
            {
                prop: 'PowerFactor',
                description: '功率因数',
                option: 'number',
            },
        ],
        operationalConstraints: [
            {
                prop: 'MiniHeatOutletTemp',
                description: '制热最小供水温度 (℃)',
            },
            {
                prop: 'MaxHeatOutletTemp',
                description: '制热最大供水温度 (℃)',
            },
            {
                prop: 'MiniCoolOutletTemp',
                description: '制冷最小供水温度 (℃)',
            },
            {
                prop: 'MaxCoolOutletTemp',
                description: '制冷最大供水温度 (℃)',
            },
        ],
        OperateParam: [
            {
                data: 'OperateStatus',
                key: 'OperateStatus',
                title: '挡位',
                type: 'text',
            },
            {
                data: 'COP',
                key: 'COP',
                title: 'COP',
                type: 'text',
            },
            {
                data: 'EnergySupply',
                key: 'EnergySupply',
                title: '制冷制热功率[kW](制冷为负，制热为正)',
                type: 'text',
            },
        ],
    },
    // 燃气锅炉
    GasBoiler_ies: {
        ratedParam: [
            {
                prop: 'LocalPressureDropCoe',
                description: '局部压降系数 (kPa/(m³·s⁻¹)²)',
            },
        ],
        operationalConstraints: [
            {
                prop: 'MiniOutletTemp',
                description: '最小供水温度 (℃)',
            },
            {
                prop: 'MaxOutletTemp',
                description: '最大供水温度 (℃)',
            },
        ],
        OperateParam: [
            {
                data: 'OperateStatus',
                key: 'OperateStatus',
                title: '挡位',
                type: 'text',
            },
            {
                data: 'HeatEfficiency',
                key: 'HeatEfficiency',
                title: '制热效率[%]',
                type: 'text',
            },
            {
                data: 'HeatPower',
                key: 'HeatPower',
                title: '供热功率[kW]',
                type: 'text',
            },
        ],
    },
    // 电压缩制冷机
    CompRefrg_ies: {
        ratedParam: [
            {
                prop: 'LocalPressureDropCoe',
                description: '局部压降系数 (kPa/(m³·s⁻¹)²)',
            },
            {
                prop: 'PowerFactor',
                description: '功率因数',
                option: 'number',
            },
        ],
        operationalConstraints: [
            {
                prop: 'MiniOutletTemp',
                description: '最小供水温度 (℃)',
            },
            { prop: 'MaxOutletTemp', description: '最大供水温度 (℃)' },
        ],
        OperateParam: [
            {
                data: 'OperateStatus',
                key: 'OperateStatus',
                title: '挡位',
                type: 'text',
            },
            {
                data: 'COP',
                key: 'COP',
                title: 'COP',
                type: 'text',
            },
            {
                data: 'CoolSupply',
                key: 'CoolSupply',
                title: '制冷功率[kW]',
                type: 'text',
            },
        ],
    },
    // 吸收式制冷机模板
    AbsorptionChiller_ies: {
        ratedParam: [
            {
                prop: 'PrimaryLocalPressureDropCoe',
                description: '热水侧局部压降系数 (kPa/(m³·s⁻¹)²)',
            },
            {
                prop: 'SecondaryLocalPressureDropCoe',
                description: '冷水侧局部压降系数 (kPa/(m³·s⁻¹)²)',
            },
            {
                prop: 'PowerFactor',
                description: '功率因数',
                option: 'number',
            },
        ],
        operationalConstraints: [
            {
                prop: 'PrimaryMaxOutletTemp',
                description: '热水侧最大出口温度(℃)',
            },
            { prop: 'PrimaryMiniOutletTemp', description: '热水侧最小出口温度(℃)' },
            { prop: 'SecondaryMaxOutletTemp', description: '冷水侧最大出口温度 (℃)' },
            { prop: 'SecondaryMiniOutletTemp', description: '冷水侧最小出口温度 (℃)' },
        ],
        OperateParam: [
            {
                data: 'OperateStatus',
                key: 'OperateStatus',
                title: '挡位',
                type: 'text',
            },
            {
                data: 'CoolHeatRatio',
                key: 'CoolHeatRatio',
                title: '冷热比',
                type: 'text',
            },
            {
                data: 'CoolSupply',
                key: 'CoolSupply',
                title: '制冷功率[kW]',
                type: 'text',
            },
            {
                data: 'PowerConsume',
                key: 'PowerConsume',
                title: '电功率[kW]',
                type: 'text',
            },
        ],
    },
    // 离心泵
    CentrifugalPump_ies: {
        ratedParam: [
            { prop: 'RatedPumpSpeed', description: '额定转速 (rpm)' },
            {
                prop: 'MaxPumpSpeed',
                description: '最大工作转速',
            },
            {
                prop: 'MinPumpSpeed',
                description: '最小工作转速',
            },
            {
                prop: 'PowerFactor',
                description: '功率因数',
                option: 'number',
            },
        ],
        operationalConstraints: [],
        OperateParam: [
            {
                data: 'MassFlowrate',
                key: 'MassFlowrate',
                title: '流量（m³/h）',
                type: 'text',
            },
            {
                data: 'Lift',
                key: 'Lift',
                title: '扬程（m）',
                type: 'text',
            },
            {
                data: 'Effiency',
                key: 'Effiency',
                title: '效率（%）',
                type: 'text',
            },
        ],
    },
};

module.exports={excelMap,equipmentParamDict,commonEconomicParams,specialEquipmentParamDict,equipmentParamDict2}