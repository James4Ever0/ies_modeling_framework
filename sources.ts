// import MessageBus from '@/Utils/message/message-bus';
const excelMap = {
    fuels: {
        燃料类型: 'fuelType',
        计量单位: 'calculatingUnit',
        '热值（MJ/计量单位)': 'calorificFuel',
        '价格(元/计量单位)': 'priceFuel',
        CO2排放系数: 'PollutantDischargeFactor.pollutionCO2',
        NOx排放系数: 'PollutantDischargeFactor.pollutionNOX',
        SO2排放系数: 'PollutantDischargeFactor.pollutionSO2',
        灰尘排放系数: 'PollutantDischargeFactor.dust',
    },
    常数电价: {
        类型: 'name',
        '电价(元/kWh)': {
            route: 'purchasePriceModel.params',
            deal: (data: Array<{ value: string[] }>): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return [data[0].value[0]];
            },
        },
    },
    分时电价: {
        类型: 'name',
        时间: {
            route: 'purchasePriceModel.params',
            deal: (data: Array<{ value: string[] }>): number[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return [...Array(data[0].value.length)].map((x, index) => index);
            },
        },
        '分时电价(元/kwh)': {
            route: 'purchasePriceModel.params',
            deal: (data: Array<{ value: string[] }>): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return data[0].value;
            },
        },
    },
    阶梯电价: {
        类型: 'name',
        '容量下限(kwh)': {
            route: 'purchasePriceModel.params',
            deal: (data: Array<{ value: string[]; quantity: string }>): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return data.map((x) => x.quantity);
            },
        },
        '阶梯电价(元/kwh)': {
            route: 'purchasePriceModel.params',
            deal: (data: Array<{ value: string[]; quantity: string }>): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return data.map((x) => x.value[0]);
            },
        },
    },
    '分时+阶梯': {
        类型: 'name',
        '阶段(kwh)': {
            route: 'purchasePriceModel.params',
            deal: (data: Array<{ value: string[] }>): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return [...Array(24)].map((x, index) => `${index}h`);
            },
        },
    },
    '热-按热量计价': {
        模型名称: 'name',
        计价方式: 'purchasePriceModel.pricingMethod',
        '价格（元/kWh）': 'purchasePriceModel.price',
    },
    '热-按用量计价': {
        模型名称: 'name',
        计价方式: 'purchasePriceModel.pricingMethod',
        '价格（元/t）': 'purchasePriceModel.price',
    },
    '热-按采暖面积计价': {
        模型名称: 'name',
        计价方式: 'purchasePriceModel.pricingMethod',
        '价格（元/㎡）': 'purchasePriceModel.price',
    },
    '冷-按热量计价': {
        模型名称: 'name',
        计价方式: 'purchasePriceModel.pricingMethod',
        '价格（元/kWh）': 'purchasePriceModel.price',
    },
    '冷-按用量计价': {
        模型名称: 'name',
        计价方式: 'purchasePriceModel.pricingMethod',
        '价格（元/t）': 'purchasePriceModel.price',
    },
    '冷-按供冷面积计价': {
        模型名称: 'name',
        计价方式: 'purchasePriceModel.pricingMethod',
        '价格（元/㎡）': 'purchasePriceModel.price',
    },
    光伏: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '单个光伏板面积(m²)': 'ratedParam.singlePanelArea',
        '光电转换效率(%)': 'ratedParam.photoelectricConversionEfficiency',
        '最大发电功率(kW)': 'operationalConstraints.maxPowerGenerating',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
    },
    电容器: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定容量(MVA)': 'ratedParam.ratedVoltage',
        '额定电压有效值(Hz)': 'ratedParam.validRatedVoltage',
        '采购成本(万元/台)': 'economicParam.purchaseCost',
        '固定维护成本(万元/年)': 'economicParam.fixationMaintainCost',
        '可变维护成本(元/kWh)': 'economicParam.maintainCost',
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
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
        '设计寿命(年)': 'economicParam.designLife',
    },
    蒸汽制热负荷: {
        负荷名称: 'loadName',
        日运行周期开始时间: 'loadParam.dayCycleStart',
        日运行周期结束时间: 'loadParam.dayCycleEnd',
        '设计蒸汽用量(t/h)': 'loadParam.steamConsumption',
        '蒸汽压力(MPa)': 'loadParam.steamPressure',
        '蒸汽温度(℃)': 'loadParam.steamTemperature',
        周运行周期开始时间: 'loadParam.weekCycleStart',
        周运行周期结束时间: 'loadParam.weekCycleEnd',
    },
    '采暖负荷-粗略': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.single_line_load.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                if (data === 'rough') return ['粗略模型'];
                else return ['详细模型'];
            },
        },
        负荷类型: 'loadParam.rough_load.buildingType',
        '建筑物用地面积(m2)': 'loadParam.rough_load.buildingArea',
        周采暖制冷周期开始时间: 'loadParam.rough_load.weekCycleStart',
        周采暖制冷周期结束时间: 'loadParam.rough_load.weekCycleEnd',
        日采暖制冷起始时间: 'loadParam.rough_load.dayCycleStart',
        日采暖制冷结束时间: 'loadParam.rough_load.dayCycleEnd',
    },
    '采暖负荷-详细模型-不区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.single_line_load.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                if (data === 'rough') return ['粗略模型'];
                else return ['详细模型'];
            },
        },
        '建筑物用地面积(m2)': 'loadParam.single_line_load.buildingArea',
        区分工作日和休息日: 'loadParam.single_line_load.isDayOff',
    },
    '采暖负荷-详细模型-区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.single_line_load.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                if (data === 'rough') return ['粗略模型'];
                else return ['详细模型'];
            },
        },
        '建筑物用地面积(m2)': 'loadParam.single_line_load.buildingArea',
        区分工作日和休息日: 'loadParam.single_line_load.isDayOff',
    },

    '制冷负荷-粗略': {
        负荷名称: 'loadName',
        负荷类型: 'loadParam.rough_load.buildingType',
        负荷模型: {
            route: 'loadParam.single_line_load.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                if (data === 'rough') return ['粗略模型'];
                else return ['详细模型'];
            },
        },
        '建筑物用地面积(m2)': 'loadParam.single_line_load.buildingArea',
        周采暖制冷周期开始时间: 'loadParam.rough_load.weekCycleStart',
        周采暖制冷周期结束时间: 'loadParam.rough_load.weekCycleEnd',
        日采暖制冷起始时间: 'loadParam.rough_load.dayCycleStart',
        日采暖制冷结束时间: 'loadParam.rough_load.dayCycleEnd',
    },
    '制冷负荷-详细模型-不区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.single_line_load.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                if (data === 'rough') return ['粗略模型'];
                else return ['详细模型'];
            },
        },
        '建筑物用地面积(m2)': 'loadParam.single_line_load.buildingArea',
        区分工作日和休息日: 'loadParam.single_line_load.isDayOff',
    },
    '制冷负荷-详细模型-区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.single_line_load.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                if (data === 'rough') return ['粗略模型'];
                else return ['详细模型'];
            },
        },
        '建筑物用地面积(m2)': 'loadParam.single_line_load.buildingArea',
        区分工作日和休息日: 'loadParam.single_line_load.isDayOff',
    },

    '电负荷-粗略': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.loadCurve.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                if (data === 'rough') return ['粗略模型'];
                else return ['详细模型'];
            },
        },
        负荷类型: 'loadParam.rough_load.buildingType',
        '年平均负荷(KW)': 'loadParam.rough_load.loadDensity',
    },
    '电负荷-详细-区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.loadCurve.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                if (data === 'rough') return ['粗略模型'];
                else return ['详细模型'];
            },
        },
        '建筑物用地面积(m2)': 'loadParam.loadCurve.buildingArea',
        区分工作日和休息日: 'loadParam.loadCurve.isDayOff',
    },
    '电负荷-详细-不区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.loadCurve.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                if (data === 'rough') return ['粗略模型'];
                else return ['详细模型'];
            },
        },
        区分工作日和休息日: 'loadParam.loadCurve.isDayOff',
    },
    /**
     * 2021-5-24 更新
     * 建模仿真模块 电负荷
     */
    '电负荷-典型日负荷': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return ['典型日负荷'];
            },
        },
        负荷类型: 'loadParam.rough_load.buildingType',
        '建筑面积(m2)': 'loadParam.rough_load.Floorage',
        '单位建筑面积负荷指标(W/㎡)': 'loadParam.rough_load.UnitFloorageElectricalLoadIndex',
        '电负荷指标(kW)': 'loadParam.rough_load.ElectricalLoadIndex',
        功率因数: 'loadParam.rough_load.PowerFactor',
    },
    '电负荷建模仿真-分月详细负荷-区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return ['分月详细负荷'];
            },
        },
        区分工作日和休息日: 'loadParam.loadCurve.isDayOff',
        功率因数: 'loadParam.detail_load.PowerFactor',
    },
    '电负荷建模仿真-分月详细负荷-不区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return ['分月详细负荷'];
            },
        },
        区分工作日和休息日: 'loadParam.loadCurve.isDayOff',
        功率因数: 'loadParam.detail_load.PowerFactor',
    },
    '电负荷-自定义': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return ['自定义负荷'];
            },
        },
        // 功率因数: 'loadParam.PowerFactor',
    },

    '充电桩负荷-区分工作日': {
        负荷名称: 'loadName',
        区分工作日和休息日: 'loadParam.loadCurve.isDayOff',
    },
    '充电桩负荷-不区分工作日': {
        负荷名称: 'loadName',
        区分工作日和休息日: 'loadParam.loadCurve.isDayOff',
    },
    //建模仿真 设备信息库
    光伏_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '光伏板面积(m²)': 'ratedParam.SinglePanelArea',
        '光电转换效率(%)': 'ratedParam.ConversionEfficiency',
        '最大发电功功率(kW)': 'operationalConstraints.maxPowerGenerating',
        功率因数: 'ratedParam.PowerFactor',
    },
    风机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定发电量(kW)': 'ratedParam.RatedPowerGenerating',
        '额定风速(m/s)': 'ratedParam.RatedWindSpeed',
        '切出风速(m/s)': 'ratedParam.CutoutWindSpeed',
        '切入风速(m/s)': 'ratedParam.CutinWindSpeed',
        '轮毂高度(m)': 'ratedParam.HubHeight',
        功率因数: 'ratedParam.PowerFactor',
    },
    燃气轮机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '局部压降系数 (kPa/(m³·s⁻¹)²)': 'ratedParam.LocalPressureDropCoe',
        '最小供水温度 (℃)': 'operationalConstraints.MiniOutletTemp',
        '最大供水温度 (℃)': 'operationalConstraints.MaxOutletTemp',
        挡位: {
            route: 'OperateParams.params',
            deal: (data: Array<{ value: string[]; OperateStatus: string }>): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return data.map((x) => x.OperateStatus);
            },
        },
        功率因数: 'ratedParam.PowerFactor',
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
        功率因数: 'ratedParam.PowerFactor',
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
        功率因数: 'ratedParam.PowerFactor',
    },
    热泵_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定制热量(kW)': 'ratedParam.ratedHeatSupply',
        额定能效比COP: 'ratedParam.heatingCOP',
        '额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷能效比COP: 'ratedParam.coolingCOP',
        功率因数: 'ratedParam.PowerFactor',
    },
    燃气热水锅炉_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热效率(%)': 'ratedParam.heatingEfficiency',
    },
    燃气蒸汽锅炉_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热效率(%)': 'ratedParam.heatingEfficiency',
    },
    余热热水锅炉_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '换热效率(%)': 'ratedParam.heatExchangeEfficiency',
    },
    '余热蒸汽锅炉-单压_建模仿真': {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        压力等级: 'ratedParam.pressureLevel',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '换热效率(%)': 'ratedParam.heatExchangeEfficiency',
    },
    '余热蒸汽锅炉-双压_建模仿真': {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        燃气锅炉类型: 'ratedParam.boilerType',
        压力等级: 'ratedParam.pressureLevel',
        '额定供热量(kW)': 'ratedParam.ratedHeatSupply',
        '换热效率(%)': 'ratedParam.heatExchangeEfficiency',
    },
    热管式太阳能集热器_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '局部压降系数(kPa/(m³·s⁻¹)²)': 'ratedParam.LocalPressureDropCoe',
        '集热器面积(m²)': 'ratedParam.PlateArea',
        '集热效率(%)': 'ratedParam.CollectionEfficiency',
    },
    电压缩制冷机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷能效比COP: 'ratedParam.COP',
    },
    热水吸收式制冷机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        热源流体类型: 'ratedParam.heatFluidType',
        '制冷状态额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷状态时冷热比: 'ratedParam.coldHeatRatio',
        '制热状态额定制热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热状态时换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '用电功率(kW)': 'ratedParam.ratedPowerConsume',
    },
    烟气吸收式制冷机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        热源流体类型: 'ratedParam.heatFluidType',
        '制冷状态额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷状态时冷热比: 'ratedParam.coldHeatRatio',
        '制热状态额定制热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热状态时换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '用电功率(kW)': 'ratedParam.ratedPowerConsume',
    },
    蒸汽吸收式制冷机_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        热源流体类型: 'ratedParam.heatFluidType',
        '制冷状态额定制冷量(kW)': 'ratedParam.ratedCoolSupply',
        制冷状态时冷热比: 'ratedParam.coldHeatRatio',
        '制热状态额定制热量(kW)': 'ratedParam.ratedHeatSupply',
        '制热状态时换热效率(%)': 'ratedParam.heatExchangeEfficiency',
        '用电功率(kW)': 'ratedParam.ratedPowerConsume',
    },
    蓄冰空调_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定放冷功率(kW)': 'ratedParam.ratedDischargingCool',
        '额定蓄冷功率(kW)': 'ratedParam.ratedChargingCool',
        '放冷效率(%)': 'ratedParam.dischargingEfficiency',
        '蓄冷效率(%)': 'ratedParam.chargingEfficiency',
        功率因数: 'ratedParam.PowerFactor',
    },
    蓄热电锅炉_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '蓄热效率(%)': 'ratedParam.chargingEfficiency',
        '额定放热功率(kW)': 'ratedParam.ratedDischargingHeat',
        '额定蓄热功率(kW)': 'ratedParam.ratedChargingHeat',
        '放热效率(%)': 'ratedParam.dischargingEfficiency',
    },
    蓄电池_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '充电效率(%)': 'ratedParam.ChargingEfficiency',
        '放电效率(%)': 'ratedParam.DischargingEfficiency',
        功率因数: 'ratedParam.PowerFactor',
        '电池最大容量(kWh)': 'operationalConstraints.PowerStorageLimit',
        '最大充电功率(kW)': 'operationalConstraints.MaxChargingPower',
        '最大放电功率(kW)': 'operationalConstraints.MaxDischargingPower',
    },
    储水罐_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '入口侧局部压降系数(kPa/(m³·s⁻¹)²)': 'ratedParam.InletLocalPressureDropCoe',
        '出口侧局部压降系数(kPa/(m³·s⁻¹)²)': 'ratedParam.OutletLocalPressureDropCoe',
        '罐底面积(m²)': 'ratedParam.FloorArea',
    },
    变压器_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '变压器非标准变比(p.u.)': 'ratedParam.wind2Ratio',
        '一次侧短路电抗(Ω)': 'ratedParam.shortCircuitImpedance',
        '一次侧短路电阻(Ω)': 'ratedParam.shortCircuitResistance',
        '额定容量(MVA)': 'ratedParam.windingMVABase',
    },
    传输线_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '单位长度电抗(Ω/km)': 'ratedParam.reactanceOfUnitLength',
        '单位长度容抗(MΩ*km)': 'ratedParam.chargingBofUnitLength',
        '单位长度电阻(Ω/km)': 'ratedParam.resistanceOfUnitLength',
    },
    电容器_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定容量(MVA)': 'ratedParam.ratedVoltage',
        '额定电压有效值(Hz)': 'ratedParam.validRatedVoltage',
    },
    模块化多电平变流器_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定电压(kV)': 'ratedParam.BaseVoltage',
    },
    离心泵_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '额定转速 (rpm)': 'ratedParam.RatedPumpSpeed',
        最大工作转速: 'ratedParam.MaxPumpSpeed',
        最小工作转速: 'ratedParam.MinPumpSpeed',
        功率因数: 'ratedParam.PowerFactor',
    },
    换热器_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        热流体类型: 'ratedParam.heatSourceType',
        '额定热负荷(kW)': 'ratedParam.ratedHeatLoad',
        '换热效率(%)': 'ratedParam.heatExchangeEfficiency',
    },
    管道_建模仿真: {
        生产厂商: 'manufacturer',
        设备型号: 'equipType',
        '管道内径(mm)': 'ratedParam.interDiameter',
        '管道壁厚(mm)': 'ratedParam.thickness',
        '管道总传热系数(W/(m·K))': 'ratedParam.heatExchangeFactor',
        '管道粗糙度(mm)': 'ratedParam.roughness',
    },
    /**
     * 采暖制冷负荷
     * 2021-5-24 更新
     */
    '采暖制冷负荷-典型日负荷': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return ['典型日负荷'];
            },
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
        日采暖制冷结束时间: 'loadParam.rough_load.dayCycleEnd',
    },
    '采暖制冷负荷-分月详细负荷-不区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return ['分月详细负荷'];
            },
        },
        '建筑面积(m2)': 'loadParam.single_line_load.Floorage',
        区分工作日和休息日: 'loadParam.single_line_load.isDayOff',
    },
    '采暖制冷负荷-分月详细负荷-区分工作日': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return ['分月详细负荷'];
            },
        },
        '建筑面积(m2)': 'loadParam.single_line_load.Floorage',
        区分工作日和休息日: 'loadParam.single_line_load.isDayOff',
    },
    '采暖制冷负荷-自定义负荷': {
        负荷名称: 'loadName',
        负荷模型: {
            route: 'loadParam.model',
            deal: (data: string): string[] => {
                if (!data) {
                    console.log("ERROR");
                }
                return ['自定义负荷'];
            },
        },
    },
};
