import { messageItem } from '@/component/template/params-template/energy-information';

const EquipmentInformation = {
    /** 热泵模板 */
    HeatPump: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            ratedHeatSupply: '250',
            heatingCOP: '3.5',
            ratedCoolSupply: '200',
            coolingCOP: '3.5',
        },
        operationalConstraints: {
            maxHeatWaterOutletTemp: '100',
            miniHeatWaterOutletTemp: '40',
            maxHeatWaterInletTemp: '70',
            miniHeatWaterInletTemp: '30',
            maxColdWaterOutletTemp: '25',
            miniColdWaterOutletTemp: '5',
            maxColdWaterInletTemp: '35',
            miniColdWaterInletTemp: '15',
            maxVoltage: '400',
            miniVoltage: '100',
            maxPressure: '1',
        },
        economicParam: { purchaseCost: '20', fixationMaintainCost: '5000', maintainCost: '0.0001', designLife: '25' },
        isDelete: false,
        kind: 'HeatPump',
    },
    /** 热泵模板_建模仿真 */
    HeatPump_ies: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            // 以下为建模新增 2021-3-24
            LocalPressureDropCoe: '100',
            PowerFactor: '0.85',
            OperateParam: [
                {
                    OperateStatus: '1',
                    COP: '4',
                    EnergySupply: '-180',
                },
                {
                    OperateStatus: '2',
                    COP: '4',
                    EnergySupply: '-190',
                },
                {
                    OperateStatus: '3',
                    COP: '4.5',
                    EnergySupply: '-200',
                },
                {
                    OperateStatus: '4',
                    COP: '4.5',
                    EnergySupply: '-210',
                },
                {
                    OperateStatus: '5',
                    COP: '4.5',
                    EnergySupply: '-220',
                },
                {
                    OperateStatus: '6',
                    COP: '4.8',
                    EnergySupply: '180',
                },
                {
                    OperateStatus: '7',
                    COP: '4.8',
                    EnergySupply: '190',
                },
                {
                    OperateStatus: '8',
                    COP: '5',
                    EnergySupply: '200',
                },
                {
                    OperateStatus: '9',
                    COP: '5',
                    EnergySupply: '210',
                },
                {
                    OperateStatus: '10',
                    COP: '5',
                    EnergySupply: '220',
                },
            ],
        },
        operationalConstraints: {
            // 以下为建模新增 2021-3-24
            MiniHeatOutletTemp: '50',
            MaxHeatOutletTemp: '100',
            MiniCoolOutletTemp: '5',
            MaxCoolOutletTemp: '20',
        },
        economicParam: { purchaseCost: '20', fixationMaintainCost: '5000', maintainCost: '0.0001', designLife: '25' },
        isDelete: false,
        kind: 'HeatPump',
    },
    /** 燃气锅炉模板 */
    GasBoiler: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxHeatWaterInletTemp: '70',
            maxHeatWaterOutletTemp: '80',
            maxPressure: '1',
            maxSteamOutletTemp: '15',
            miniHeatWaterInletTemp: '50',
            miniHeatWaterOutletTemp: '60',
            miniSteamOutletTemp: '10',
        },
        ratedParam: {
            boilerType: '燃气热水锅炉',
            heatingEfficiency: '90',
            ratedHeatSupply: '200',
        },
        economicParam: { purchaseCost: '30', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'GasBoiler',
    },
    /** 燃气锅炉模板_建模仿真 */
    GasBoiler_ies: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            // 以下为建模新增 2021-3-24
            MiniOutletTemp: '40',
            MaxOutletTemp: '100',
        },
        ratedParam: {
            // 以下为建模新增 2021-3-24
            LocalPressureDropCoe: '100',
            OperateParam: [
                {
                    OperateStatus: '1',
                    HeatEfficiency: '85',
                    HeatPower: '180',
                },
                {
                    OperateStatus: '2',
                    HeatEfficiency: '90',
                    HeatPower: '190',
                },
                {
                    OperateStatus: '3',
                    HeatEfficiency: '95',
                    HeatPower: '200',
                },
                {
                    OperateStatus: '4',
                    HeatEfficiency: '90',
                    HeatPower: '210',
                },
                {
                    OperateStatus: '5',
                    HeatEfficiency: '90',
                    HeatPower: '220',
                },
            ],
        },
        economicParam: { purchaseCost: '30', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'GasBoiler',
    },
    /** 余热锅炉模板 */
    HeatRecoveryBoiler: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxExhaustOutletTemp: '70',
            miniExhaustOutletTemp: '70',
            maxExhaustInletTemp: '80',
            miniExhaustInletTemp: '80',
            maxHeatWaterInletTemp: '70',
            maxHeatWaterOutletTemp: '80',
            maxPressure: '1',
            miniHeatWaterInletTemp: '50',
            miniHeatWaterOutletTemp: '60',
            maxSteamOutletTemp: '50',
            miniSteamOutletTemp: '50',
            maxSubSteamOutletTemp: '120',
            miniSubSteamOutletTemp: '120',
            maxHighSteamOutletTemp: '120',
            miniHighSteamOutletTemp: '120',
        },
        ratedParam: { boilerType: '余热热水锅炉', heatingEfficiency: '90', ratedHeatSupply: '200', heatExchangeEfficiency: '80' },
        economicParam: { purchaseCost: '50', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'HeatRecoveryBoiler',
    },
    /** 余热锅炉模板_建模仿真 */
    HeatRecoveryBoiler_ies: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxExhaustOutletTemp: '70',
            miniExhaustOutletTemp: '70',
            maxExhaustInletTemp: '80',
            miniExhaustInletTemp: '80',
            maxHeatWaterInletTemp: '70',
            maxHeatWaterOutletTemp: '80',
            maxPressure: '1',
            miniHeatWaterInletTemp: '50',
            miniHeatWaterOutletTemp: '60',
            maxSteamOutletTemp: '50',
            miniSteamOutletTemp: '50',
            maxSubSteamOutletTemp: '120',
            miniSubSteamOutletTemp: '120',
            maxHighSteamOutletTemp: '120',
            miniHighSteamOutletTemp: '120',
        },
        ratedParam: { boilerType: '余热热水锅炉', heatingEfficiency: '90', ratedHeatSupply: '200', heatExchangeEfficiency: '80' },
        economicParam: { purchaseCost: '50', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'HeatRecoveryBoiler',
    },
    /** 热管式太阳能集热器模板 */
    HPSolarCollector: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxHeatWaterInletTemp: '70',
            maxHeatWaterOutletTemp: '100',
            maxPressure: '1',
            miniHeatWaterInletTemp: '20',
            miniHeatWaterOutletTemp: '40',
        },
        ratedParam: {
            collectionEfficiency: '50',
            plateArea: '15',
        },
        economicParam: { purchaseCost: '1', fixationMaintainCost: '500', maintainCost: '0.0002', designLife: '0' },
        isDelete: false,
        kind: 'HPSolarCollector',
    },
    /** 热管式太阳能集热器模板_建模仿真 */
    HPSolarCollector_ies: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            // 以下为建模新增 2021-3-24
            MiniOutletTemp: '40',
            MaxOutletTemp: '100',
        },
        ratedParam: {
            // 以下为建模新增 2021-3-24
            LocalPressureDropCoe: '100',
            CollectionEfficiency: '50',
            PlateArea: '100',
        },
        economicParam: { purchaseCost: '1', fixationMaintainCost: '500', maintainCost: '0.0002', designLife: '0' },
        isDelete: false,
        kind: 'HPSolarCollector',
    },
    /** 电压缩制冷机模板 */
    CompRefrg: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxColdWaterInletTemp: '35',
            maxColdWaterOutletTemp: '20',
            maxPressure: '1.5',
            miniColdWaterInletTemp: '12',
            miniColdWaterOutletTemp: '5',
        },
        ratedParam: {
            COP: '6',
            ratedCoolSupply: '700',
        },
        economicParam: { purchaseCost: '40', fixationMaintainCost: '1000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'CompRefrg',
    },
    /** 电压缩制冷机模板_建模仿真 */
    CompRefrg_ies: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            // 以下为建模新增 2021-3-24
            MiniOutletTemp: '5',
            MaxOutletTemp: '20',
        },
        ratedParam: {
            // 以下为建模新增 2021-3-24
            LocalPressureDropCoe: '100',
            PowerFactor: '0.85',
            OperateParam: [
                {
                    OperateStatus: '1',
                    COP: '4.8',
                    CoolSupply: '180',
                },
                {
                    OperateStatus: '2',
                    COP: '4.8',
                    CoolSupply: '190',
                },
                {
                    OperateStatus: '3',
                    COP: '5',
                    CoolSupply: '200',
                },
                {
                    OperateStatus: '4',
                    COP: '5',
                    CoolSupply: '210',
                },
                {
                    OperateStatus: '5',
                    COP: '5',
                    CoolSupply: '220',
                },
            ],
        },
        economicParam: { purchaseCost: '40', fixationMaintainCost: '1000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'CompRefrg',
    },
    /** 吸收式制冷机模板 */
    AbsorptionChiller: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxColdWaterInletTemp: '35',
            maxColdWaterOutletTemp: '25',
            maxHeatSourceInletTemp: '80',
            maxHeatSourceOutletTemp: '50',
            maxHeatWaterInletTemp: '40',
            maxHeatWaterOutletTemp: '50',
            maxPressure: '1',
            maxVoltage: '1500',
            miniColdWaterInletTemp: '15',
            miniColdWaterOutletTemp: '5',
            miniHeatSourceInletTemp: '60',
            miniHeatSourceOutletTemp: '30',
            miniHeatWaterInletTemp: '20',
            miniHeatWaterOutletTemp: '30',
            miniVoltage: '110',
        },
        ratedParam: {
            coldHeatRatio: '3.5',
            heatExchangeEfficiency: '80',
            heatFluidType: '热水',
            ratedCoolSupply: '200',
            ratedHeatSupply: '200',
            ratedPowerConsume: '50',
        },
        economicParam: { purchaseCost: '130', fixationMaintainCost: '1000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'AbsorptionChiller',
    },
    /** 吸收式制冷机模板_建模仿真 */
    AbsorptionChiller_ies: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            // 以下为建模新增 2021-3-24
            PrimaryMaxOutletTemp: '80',
            PrimaryMiniOutletTemp: '50',
            SecondaryMaxOutletTemp: '20',
            SecondaryMiniOutletTemp: '5',
        },
        ratedParam: {
            // 以下为建模新增 2021-3-24
            PrimaryLocalPressureDropCoe: '100',
            SecondaryLocalPressureDropCoe: '100',
            PowerFactor: '0.85',
            OperateParam: [
                {
                    OperateStatus: '1',
                    CoolHeatRatio: '0.5',
                    CoolSupply: '100',
                    PowerConsume: '2',
                },
                {
                    OperateStatus: '2',
                    CoolHeatRatio: '0.6',
                    CoolSupply: '180',
                    PowerConsume: '2.5',
                },
                {
                    OperateStatus: '3',
                    CoolHeatRatio: '0.7',
                    CoolSupply: '280',
                    PowerConsume: '3',
                },
                {
                    OperateStatus: '4',
                    CoolHeatRatio: '0.75',
                    CoolSupply: '360',
                    PowerConsume: '3',
                },
                {
                    OperateStatus: '5',
                    CoolHeatRatio: '0.8',
                    CoolSupply: '400',
                    PowerConsume: '3',
                },
            ],
        },
        economicParam: { purchaseCost: '130', fixationMaintainCost: '1000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'AbsorptionChiller',
    },
    /** 变压器模板 */
    Transformer: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            wind1RatioVoltage: '10',
            wind2RatioVoltage: '220',
            excitationConductance: '0',
            excitationAdmittance: '0',
        },
        operationalConstraints: {
            maxWind2Ratio: '2',
            miniWind2Ratio: '1',
        },
        economicParam: { purchaseCost: '100', fixationMaintainCost: '10000', maintainCost: '500', designLife: '25' },
        isDelete: false,
        kind: 'Transformer',
    },
    /** 变压器模板_建模仿真 */
    Transformer_ies: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            // 以下为建模新增 2021-3-24
            windingMVABase: '100',
            shortCircuitResistance: '0.1',
            shortCircuitImpedance: '0.1',
            wind2Ratio: '1',
        },
        operationalConstraints: {},
        economicParam: { purchaseCost: '100', fixationMaintainCost: '10000', maintainCost: '500', designLife: '25' },
        isDelete: false,
        kind: 'Transformer',
    },
    /** 传输线模板 */
    TransferLine: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            lineLength: '1',
            ratedFrequency: '50',
            ratedVoltage: '10',
            // 以下为建模新增 2021-5-13
            chargingBofUnitLength: '0.000001',
            reactanceOfUnitLength: '0.00001',
            resistanceOfUnitLength: '0.00001',
        },
        operationalConstraints: {},
        economicParam: { purchaseCost: '2', fixationMaintainCost: '100', maintainCost: '500', designLife: '25' },
        isDelete: false,
        kind: 'TransferLine',
    },
    /** 传输线模板_建模仿真 */
    TransferLine_ies: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            // 以下为建模新增 2021-3-24
            chargingBofUnitLength: '1',
            reactanceOfUnitLength: '0.1',
            resistanceOfUnitLength: '0.1',
        },
        operationalConstraints: {},
        economicParam: { purchaseCost: '2', fixationMaintainCost: '100', maintainCost: '500', designLife: '25' },
        isDelete: false,
        kind: 'TransferLine',
    },
    /** 电容器模板 */
    Capacitance: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            ratedVoltage: '100',
            validRatedVoltage: '10',
        },
        operationalConstraints: {},
        economicParam: { purchaseCost: '2', fixationMaintainCost: '100', maintainCost: '500', designLife: '25' },
        isDelete: false,
        kind: 'Capacitance',
    },
    /** 电容器模板_建模仿真 */
    Capacitance_ies: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            ratedVoltage: '100',
            validRatedVoltage: '10',
        },
        operationalConstraints: {},
        economicParam: { purchaseCost: '2', fixationMaintainCost: '100', maintainCost: '500', designLife: '25' },
        isDelete: false,
        kind: 'Capacitance',
    },
    /**
     * 模块化多电平变流器_建模仿真
     */
    MMC_ies: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            BaseVoltage: '0.4',
        },
        operationalConstraints: {},
        economicParam: { purchaseCost: '2', fixationMaintainCost: '100', maintainCost: '500', designLife: '25' },
        isDelete: false,
        kind: 'MMC',
    },
    /** 光伏模板 */
    PhotovoltaicSys: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        ratedParam: {
            photoelectricConversionEfficiency: '16.5',
            singlePanelArea: '1.95',
        },
        operationalConstraints: { maxPowerGenerating: '0.31' },
        economicParam: { purchaseCost: '0.06', fixationMaintainCost: '10', maintainCost: '0.001', designLife: '0' },
        isDelete: false,
        kind: 'PhotovoltaicSys',
    },
    /** 光伏模板_建模仿真 */
    PhotovoltaicSys_ies: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        ratedParam: {
            // 以下为建模新增 2021-3-24
            ConversionEfficiency: '16.5',
            SinglePanelArea: '1.95',
            PowerFactor: '1.0',
        },
        operationalConstraints: { maxPowerGenerating: '0.31' },
        economicParam: { purchaseCost: '0.06', fixationMaintainCost: '10', maintainCost: '0.001', designLife: '0' },
        isDelete: false,
        kind: 'PhotovoltaicSys',
    },
    /** 风机模板 */
    WindPowerGenerator: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {},
        ratedParam: {
            cutinWindSpeed: '4',
            cutoutWindSpeed: '20',
            ratedPowerGenerating: '3000',
            ratedWindSpeed: '8',
            towerHeight: '120',
        },
        economicParam: { purchaseCost: '900', fixationMaintainCost: '50000', maintainCost: '0.00015', designLife: '25' },
        isDelete: false,
        kind: 'WindPowerGenerator',
    },
    /** 风机模板_建模仿真 */
    WindPowerGenerator_ies: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {},
        ratedParam: {
            // 以下为建模新增 2021-3-24
            CutinWindSpeed: '4',
            CutoutWindSpeed: '20',
            RatedPowerGenerating: '3000',
            RatedWindSpeed: '8',
            HubHeight: '120',
            PowerFactor: '1.0',
        },
        economicParam: { purchaseCost: '900', fixationMaintainCost: '50000', maintainCost: '0.00015', designLife: '25' },
        isDelete: false,
        kind: 'WindPowerGenerator',
    },
    /** 燃气轮机模板 */
    GasTurbine: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxExhaustOutletTemp: '600',
            maxPressure: '5',
            miniExhaustOutletTemp: '200',
        },
        ratedParam: {
            generatingEfficiency: '30',
            heatingEfficiency: '40',
            powerGenerating: '500',
        },
        economicParam: { purchaseCost: '80', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'GasTurbine',
    },
    /** 燃气轮机_建模仿真模板 */
    GasTurbine_ies: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            MiniOutletTemp: '60',
            MaxOutletTemp: '100',
        },
        ratedParam: {
            LocalPressureDropCoe: '100',
            PowerFactor: '0.85',
            OperateParam: [
                {
                    OperateStatus: '1',
                    GeneratingPower: '200',
                    GeneratingEfficiency: '20',
                    HeatEfficiency: '10',
                },
                {
                    OperateStatus: '2',
                    GeneratingPower: '500',
                    GeneratingEfficiency: '25',
                    HeatEfficiency: '15',
                },
                {
                    OperateStatus: '3',
                    GeneratingPower: '900',
                    GeneratingEfficiency: '30',
                    HeatEfficiency: '20',
                },
                {
                    OperateStatus: '4',
                    GeneratingPower: '1600',
                    GeneratingEfficiency: '40',
                    HeatEfficiency: '25',
                },
                {
                    OperateStatus: '5',
                    GeneratingPower: '1800',
                    GeneratingEfficiency: '45',
                    HeatEfficiency: '30',
                },
            ],
        },
        economicParam: { purchaseCost: '80', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'GasTurbine',
    },
    /** 燃气内燃机模板 */
    GasEngine: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxExhaustOutletTemp: '600',
            maxHeatWaterInletTemp: '70',
            maxHeatWaterOutletTemp: '100',
            maxPressure: '5',
            miniExhaustOutletTemp: '250',
            miniHeatWaterInletTemp: '50',
            miniHeatWaterOutletTemp: '60',
        },
        ratedParam: { generatingEfficiency: '40', heatingEfficiency: '30', powerGenerating: '500', waterMassFlowrate: '10' },
        economicParam: { purchaseCost: '100', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'GasEngine',
    },
    /** 燃气内燃机模板_建模仿真*/
    GasEngine_ies: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxExhaustOutletTemp: '600',
            maxHeatWaterInletTemp: '70',
            maxHeatWaterOutletTemp: '100',
            maxPressure: '5',
            miniExhaustOutletTemp: '250',
            miniHeatWaterInletTemp: '50',
            miniHeatWaterOutletTemp: '60',
        },
        ratedParam: { generatingEfficiency: '40', heatingEfficiency: '30', powerGenerating: '500', waterMassFlowrate: '10', PowerFactor: '0.85' },
        economicParam: { purchaseCost: '100', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'GasEngine',
    },
    /** 蒸汽轮机模板 */
    SteamTurbine: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxPowerGenerating: '1200',
            maxPressure: '5',
            maxSteamInletTemp: '250',
            miniPowerGenerating: '850',
            miniSteamInletTemp: '150',
        },
        ratedParam: { generatingEfficiency: '80', ratedSteamInletTemp: '250', steamMassFlowrate: '5' },
        economicParam: { purchaseCost: '1000', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '0' },
        isDelete: false,
        kind: 'SteamTurbine',
    },
    /** 蒸汽轮机模板_建模仿真 */
    SteamTurbine_ies: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxPowerGenerating: '1200',
            maxPressure: '5',
            maxSteamInletTemp: '250',
            miniPowerGenerating: '850',
            miniSteamInletTemp: '150',
        },
        ratedParam: { generatingEfficiency: '80', ratedSteamInletTemp: '250', steamMassFlowrate: '5', PowerFactor: '0.85' },
        economicParam: { purchaseCost: '1000', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '0' },
        isDelete: false,
        kind: 'SteamTurbine',
    },
    /** 离心泵模板 */
    Pump: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            operationCurveParamA: '-0.000013',
            operationCurveParamB: '0.3905',
            operationCurveParamC: '15',
            efficency: '70',
        },
        operationalConstraints: {
            miniInletPressure: '0.05',
            maxInlePressure: '5',
        },
        economicParam: { purchaseCost: '5', fixationMaintainCost: '100', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'Pump',
    },
    /**
     * 离心泵_建模仿真
     */
    CentrifugalPump_ies: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            // 以下为建模新增 2021-4-6
            RatedPumpSpeed: '2900',
            // 建模新增 2021-5-24
            MaxPumpSpeed: '3300',
            MinPumpSpeed: '2000',
            PowerFactor: '0.85',
            PerformanceCurve: [
                {
                    MassFlowrate: '0',
                    Lift: '450',
                    Effiency: '0',
                },
                {
                    MassFlowrate: '360',
                    Lift: '420',
                    Effiency: '40',
                },
                {
                    MassFlowrate: '720',
                    Lift: '380',
                    Effiency: '60',
                },
                {
                    MassFlowrate: '1080',
                    Lift: '320',
                    Effiency: '70',
                },
                {
                    MassFlowrate: '1440',
                    Lift: '235',
                    Effiency: '78',
                },
            ],
        },
        operationalConstraints: {
            // miniInletPressure: '0.05',
            // maxInlePressure: '5',
        },
        economicParam: { purchaseCost: '5', fixationMaintainCost: '100', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'CentrifugalPump',
    },
    /** 换热器模板 */
    HeatExchanger: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxColdFluidInletTemp: '60',
            maxColdFluidOutletTemp: '80',
            maxHeatSourceInletTemp: '100',
            maxHeatSourceOutletTemp: '70',
            maxPressure: '5',
            miniColdFluidInletTemp: '40',
            miniColdFluidOutletTemp: '60',
            miniHeatSourceInletTemp: '80',
            miniHeatSourceOutletTemp: '50',
        },
        ratedParam: { heatExchangeEfficiency: '80', heatSourceType: '热水', ratedHeatLoad: '200' },
        economicParam: { purchaseCost: '30', fixationMaintainCost: '1000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'HeatExchanger',
    },
    /** 换热器模板_建模仿真 */
    HeatExchanger_ies: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxColdFluidInletTemp: '60',
            maxColdFluidOutletTemp: '80',
            maxHeatSourceInletTemp: '100',
            maxHeatSourceOutletTemp: '70',
            maxPressure: '5',
            miniColdFluidInletTemp: '40',
            miniColdFluidOutletTemp: '60',
            miniHeatSourceInletTemp: '80',
            miniHeatSourceOutletTemp: '50',
        },
        ratedParam: { heatExchangeEfficiency: '80', heatSourceType: '热水', ratedHeatLoad: '200' },
        economicParam: { purchaseCost: '30', fixationMaintainCost: '1000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'HeatExchanger',
    },
    /** 管道模板 */
    Pipe: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxPressure: '10',
        },
        ratedParam: { heatExchangeFactor: '0.25', interDiameter: '120', roughness: '0.5', thickness: '8' },
        economicParam: { purchaseCost: '2', fixationMaintainCost: '1000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'Pipe',
    },
    /** 管道模板_建模仿真*/
    Pipe_ies: {
        manufacturer: '请输入',
        name: '请输入',
        equipType: '请输入',
        operationalConstraints: {
            maxPressure: '10',
        },
        ratedParam: { heatExchangeFactor: '0.25', interDiameter: '120', roughness: '0.5', thickness: '8' },
        economicParam: { purchaseCost: '2', fixationMaintainCost: '1000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'Pipe',
    },
    /** 蓄冰空调 */
    IceStorageAC: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            ratedChargingCool: '250',
            chargingEfficiency: '90',
            ratedDischargingCool: '250',
            dischargingEfficiency: '90',
        },
        operationalConstraints: {
            maxColdWaterOutletTemp: '25',
            miniColdWaterOutletTemp: '5',
            maxColdWaterInletTemp: '35',
            miniColdWaterInletTemp: '15',
            capacity: '5000',
        },
        economicParam: { purchaseCost: '100', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'IceStorageAC',
    },
    /** 蓄冰空调_建模仿真 */
    IceStorageAC_ies: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            ratedChargingCool: '250',
            chargingEfficiency: '90',
            ratedDischargingCool: '250',
            dischargingEfficiency: '90',
            PowerFactor: '0.85',
        },
        operationalConstraints: {
            maxColdWaterOutletTemp: '25',
            miniColdWaterOutletTemp: '5',
            maxColdWaterInletTemp: '35',
            miniColdWaterInletTemp: '15',
            capacity: '5000',
        },
        economicParam: { purchaseCost: '100', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'IceStorageAC',
    },
    /** 蓄热电锅炉 */
    HeatStorageElectricalBoiler: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            chargingEfficiency: '90',
            dischargingEfficiency: '90',
            ratedChargingHeat: '250',
            ratedDischargingHeat: '250',
        },
        operationalConstraints: {
            capacity: '1000',
            maxHeatWaterInletTemp: '60',
            maxHeatWaterOutletTemp: '70',
            miniHeatWaterInletTemp: '40',
            miniHeatWaterOutletTemp: '50',
        },
        economicParam: { purchaseCost: '20', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'HeatStorageElectricalBoiler',
    },
    /** 蓄热电锅炉_建模仿真 */
    HeatStorageElectricalBoiler_ies: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            chargingEfficiency: '90',
            dischargingEfficiency: '90',
            ratedChargingHeat: '250',
            ratedDischargingHeat: '250',
        },
        operationalConstraints: {
            capacity: '1000',
            maxHeatWaterInletTemp: '60',
            maxHeatWaterOutletTemp: '70',
            miniHeatWaterInletTemp: '40',
            miniHeatWaterOutletTemp: '50',
        },
        economicParam: { purchaseCost: '20', fixationMaintainCost: '10000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'HeatStorageElectricalBoiler',
    },
    /** 蓄电池 */
    Battery: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            chargingEfficiency: '90',
            dischargingEfficiency: '90',
            ratedChargingPower: '200',
            ratedDischargingPower: '150',
        },
        operationalConstraints: { capacity: '1000' },
        economicParam: { purchaseCost: '20', fixationMaintainCost: '1000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'Battery',
    },
    /** 蓄电池_建模仿真 */
    Battery_ies: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            // 以下为建模新增 2021-04-01修改
            ChargingEfficiency: '90',
            DischargingEfficiency: '90',
            PowerFactor: '1.0',
        },
        operationalConstraints: {
            // 以下为建模新增 2021-04-07修改
            MaxChargingPower: '200',
            MaxDischargingPower: '100',
            PowerStorageLimit: '1500',
        },
        economicParam: { purchaseCost: '20', fixationMaintainCost: '1000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'Battery',
    },
    /**
     * 储水罐_建模仿真
     */
    WaterTank_ies: {
        manufacturer: '请输入',
        equipType: '请输入',
        name: '请输入',
        ratedParam: {
            InletLocalPressureDropCoe: '100',
            OutletLocalPressureDropCoe: '100',
            FloorArea: '15',
        },
        operationalConstraints: { MaxWaterLevel: '10', MiniWaterLevel: '1' },
        economicParam: { purchaseCost: '20', fixationMaintainCost: '1000', maintainCost: '0.0002', designLife: '25' },
        isDelete: false,
        kind: 'WaterTank',
    },
};
const EquipmentMessageContent = {
    /** 热泵模板 */
    HeatPump: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'icondiyuanrebeng',
    },
    /** 燃气锅炉模板 */
    GasBoiler: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconguolu2',
    },
    /** 余热锅炉模板 */
    HeatRecoveryBoiler: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconguolu1',
    },
    /** 热管式太阳能集热器模板 */
    HPSolarCollector: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconhekriconshebeitaiyangnengreshuiqi',
    },
    /** 电压缩制冷机模板 */
    CompRefrg: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconkongtiao1',
    },
    /** 吸收式制冷机模板 */
    AbsorptionChiller: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconzhilengji',
    },
    /** 变压器模板 */
    Transformer: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconbianyaqiyunhangpingjia',
    },
    /** 传输线模板 */
    TransferLine: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconshudianxianlu',
    },
    /** 电容器模板 */
    Capacitance: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconmuxiandianrong',
    },
    /** 光伏模板 */
    PhotovoltaicSys: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconguangfuban',
    },
    /** 光伏模板_建模仿真 */
    PhotovoltaicSys_ies: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconguangfuban',
    },
    /** 风机模板 */
    WindPowerGenerator: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconfengji1',
    },
    /** 燃气轮机模板 */
    GasTurbine: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconhuodianjizu',
    },
    /** 燃气内燃机模板 */
    GasEngine: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconfadianji',
    },
    /** 蒸汽轮机模板 */
    SteamTurbine: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'icondanceqilunji',
    },
    /** 离心泵模板 */
    Pump: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconshuibeng',
    },
    /** 离心泵模板 */
    CentrifugalPump: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconshuibeng',
    },
    /** 换热器模板 */
    HeatExchanger: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconicon_huanrezhan_dingkong-01',
    },
    /** 管道模板 */
    Pipe: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconguandao1',
    },
    /** 蓄冰空调 */
    IceStorageAC: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconxulengguanjianhuaban',
    },
    /** 蓄热电锅炉 */
    HeatStorageElectricalBoiler: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconshebeiku-',
    },
    /** 蓄电池 */
    Battery: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconxudianchidianya',
    },
    /**
     * 储水罐
     */
    WaterTank: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconxudianchidianya',
    },
    /**
     * 模块化多电平变流器
     */
    MMC: {
        name: 'manufacturer',
        message: (item: typeof EquipmentInformation['HeatPump']): messageItem[] => {
            return [
                { des: '生产厂商', value: item['manufacturer'], unit: '' },
                { des: '设备型号', value: item['equipType'], unit: '' },
            ];
        },
        icon: 'iconxudianchidianya',
    },
};
export { EquipmentInformation, EquipmentMessageContent };
