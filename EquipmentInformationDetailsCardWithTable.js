"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
exports.__esModule = true;
var BaseInformationDetailsCard_1 = require("@/component/LibraryOfInformationCardBase/BaseInformationDetailsCard");
var vue_property_decorator_1 = require("vue-property-decorator");
var lodash_1 = require("lodash");
var tools_1 = require("@/component/template/tools/tools");
var store_1 = require("@/store/store");
var tools_2 = require("@/component/template/tools/tools");
var message_bus_1 = require("@/Utils/message/message-bus");
/**
 *
 */
var EquipmentInformationDetails = /** @class */ (function (_super) {
    __extends(EquipmentInformationDetails, _super);
    function EquipmentInformationDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /** */
        _this.canBatchOperation = true;
        /** */
        _this.proactiveTrigger = false;
        /**  */
        _this.equipmentParamDict = {
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
        _this.specialEquipmentParamDict = {
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
        _this.commonEconomicParams = [
            { prop: 'purchaseCost', description: '采购成本(万元/台)' },
            { prop: 'maintainCost', description: '固定维护成本(万元/年)' },
            { prop: 'maintainCost', description: '可变维护成本(元/kWh)' },
            { prop: 'designLife', description: '设计寿命(年)' },
        ];
        return _this;
    }
    Object.defineProperty(EquipmentInformationDetails.prototype, "numberFieldRules", {
        /**
         *获取数字字段校验规则
         */
        get: function () {
            return this.$store.state.numberFieldRules;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(EquipmentInformationDetails.prototype, "stringFieldRules", {
        /**
         *获取文字字段校对规则
         */
        get: function () {
            return this.$store.state.stringFieldRules;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(EquipmentInformationDetails.prototype, "dataStructure", {
        /**
         *
         */
        get: function () {
            var _this = this;
            if (this.specialEquipmentParamDict[this.cardData.kind] != null) {
                var paramDict = this.specialEquipmentParamDict[this.cardData.kind].find(function (item) {
                    if (item.conditions == null) {
                        return true;
                    }
                    else {
                        return (item.conditions
                            // eslint-disable-next-line eqeqeq
                            .map(function (condition) {
                            if ((0, lodash_1.get)(_this.cardData, condition.path) == null) {
                                var newPath = __spreadArray([], condition.path, true);
                                var lastPath = newPath.pop();
                                if (lastPath != null) {
                                    _this.$set((0, lodash_1.get)(_this.cardData, newPath), lastPath, condition.defaultValue);
                                }
                            }
                            // eslint-disable-next-line eqeqeq
                            return (0, lodash_1.get)(_this.cardData, condition.path) == condition.value;
                        })
                            .reduce(function (isSatisfy, isPass) { return isSatisfy && isPass; }));
                    }
                });
                if (paramDict != null) {
                    return paramDict.paramDict;
                }
                else {
                    return this.specialEquipmentParamDict[this.cardData.kind][0].paramDict;
                }
            }
            else {
                return this.equipmentParamDict[this.cardData.kind];
            }
        },
        enumerable: false,
        configurable: true
    });
    /**
     * @author dev_yms
     * @description
     * @return void
     */
    EquipmentInformationDetails.prototype.saveToFile = function () {
        if (!this.$store.state.iesMode) {
            if (this.title === '燃气锅炉' && this.cardData.ratedParam.boilerType === '燃气热水锅炉') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u71C3\u6C14\u70ED\u6C34\u9505\u7089-").concat(this.cardData.manufacturer), '燃气热水锅炉', this.cardData);
            }
            else if (this.title === '燃气锅炉') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u71C3\u6C14\u84B8\u6C7D\u9505\u7089-").concat(this.cardData.manufacturer), '燃气蒸汽锅炉', this.cardData);
            }
            else if (this.title === '余热锅炉' && this.cardData.ratedParam.boilerType === '余热热水锅炉') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u4F59\u70ED\u70ED\u6C34\u9505\u7089-").concat(this.cardData.manufacturer), '余热热水锅炉', this.cardData);
            }
            else if (this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '单压') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u4F59\u70ED\u84B8\u6C7D\u9505\u7089-\u5355\u538B-").concat(this.cardData.manufacturer), '余热蒸汽锅炉-单压', this.cardData);
            }
            else if (this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '双压') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u4F59\u70ED\u84B8\u6C7D\u9505\u7089-\u53CC\u538B-").concat(this.cardData.manufacturer), '余热蒸汽锅炉-双压', this.cardData);
            }
            else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '热水') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u70ED\u6C34-").concat(this.cardData.manufacturer), '热水吸收式制冷机', this.cardData);
            }
            else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '烟气') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u70DF\u6C14-").concat(this.cardData.manufacturer), '烟气吸收式制冷机', this.cardData);
            }
            else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '蒸汽') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u84B8\u6C7D-").concat(this.cardData.manufacturer), '蒸汽吸收式制冷机', this.cardData);
            }
            else
                tools_1["default"].initXlsxFile("".concat(this.title, "-").concat(this.cardData.manufacturer), this.title, this.cardData);
        }
        else {
            if (this.title === '燃气锅炉' && this.cardData.ratedParam.boilerType === '燃气热水锅炉_建模仿真') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u71C3\u6C14\u70ED\u6C34\u9505\u7089-").concat(this.cardData.manufacturer), '燃气热水锅炉_建模仿真', this.cardData);
            }
            else if (this.title === '燃气锅炉') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u71C3\u6C14\u84B8\u6C7D\u9505\u7089-").concat(this.cardData.manufacturer), '燃气蒸汽锅炉_建模仿真', this.cardData);
            }
            else if (this.title === '余热锅炉' && this.cardData.ratedParam.boilerType === '余热热水锅炉') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u4F59\u70ED\u70ED\u6C34\u9505\u7089-").concat(this.cardData.manufacturer), '余热热水锅炉_建模仿真', this.cardData);
            }
            else if (this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '单压') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u4F59\u70ED\u84B8\u6C7D\u9505\u7089-\u5355\u538B-").concat(this.cardData.manufacturer), '余热蒸汽锅炉-单压_建模仿真', this.cardData);
            }
            else if (this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '双压') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u4F59\u70ED\u84B8\u6C7D\u9505\u7089-\u53CC\u538B-").concat(this.cardData.manufacturer), '余热蒸汽锅炉-双压_建模仿真', this.cardData);
            }
            else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '热水') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u70ED\u6C34-").concat(this.cardData.manufacturer), '热水吸收式制冷机_建模仿真', this.cardData);
            }
            else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '烟气') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u70DF\u6C14-").concat(this.cardData.manufacturer), '烟气吸收式制冷机_建模仿真', this.cardData);
            }
            else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '蒸汽') {
                tools_1["default"].initXlsxFile("".concat(this.title, "-\u84B8\u6C7D-").concat(this.cardData.manufacturer), '蒸汽吸收式制冷机_建模仿真', this.cardData);
            }
            else
                tools_1["default"].initXlsxFile("".concat(this.title, "-").concat(this.cardData.manufacturer), "".concat(this.title, "_\u5EFA\u6A21\u4EFF\u771F"), this.cardData);
        }
    };
    /**
     *
     */
    EquipmentInformationDetails.prototype.exportRowData = function () {
        if (!store_1["default"].state.iesMode) {
            if (this.title === '燃气锅炉' && this.cardData.ratedParam.boilerType === '燃气热水锅炉') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u71C3\u6C14\u70ED\u6C34\u9505\u7089-").concat(this.cardData.manufacturer), '燃气热水锅炉', this.cardData);
            }
            else if (this.title === '燃气锅炉') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u71C3\u6C14\u84B8\u6C7D\u9505\u7089-").concat(this.cardData.manufacturer), '燃气蒸汽锅炉', this.cardData);
            }
            else if (this.title === '余热锅炉' && this.cardData.ratedParam.boilerType === '余热热水锅炉') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u4F59\u70ED\u70ED\u6C34\u9505\u7089-").concat(this.cardData.manufacturer), '余热热水锅炉', this.cardData);
            }
            else if (this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '单压') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u4F59\u70ED\u84B8\u6C7D\u9505\u7089-\u5355\u538B-").concat(this.cardData.manufacturer), '余热蒸汽锅炉-单压', this.cardData);
            }
            else if (this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '双压') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u4F59\u70ED\u84B8\u6C7D\u9505\u7089-\u53CC\u538B-").concat(this.cardData.manufacturer), '余热蒸汽锅炉-双压', this.cardData);
            }
            else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '热水') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u70ED\u6C34-").concat(this.cardData.manufacturer), '热水吸收式制冷机', this.cardData);
            }
            else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '烟气') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u70DF\u6C14-").concat(this.cardData.manufacturer), '烟气吸收式制冷机', this.cardData);
            }
            else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '蒸汽') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u84B8\u6C7D-").concat(this.cardData.manufacturer), '蒸汽吸收式制冷机', this.cardData);
            }
            else
                return tools_1["default"].initXlsxData("".concat(this.title, "-").concat(this.cardData.manufacturer), this.title, this.cardData);
        }
        else {
            if (this.title === '燃气锅炉' && this.cardData.ratedParam.boilerType === '燃气热水锅炉_建模仿真') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u71C3\u6C14\u70ED\u6C34\u9505\u7089-").concat(this.cardData.manufacturer), '燃气热水锅炉_建模仿真', this.cardData);
            }
            else if (this.title === '燃气锅炉') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u71C3\u6C14\u84B8\u6C7D\u9505\u7089-").concat(this.cardData.manufacturer), '燃气蒸汽锅炉_建模仿真', this.cardData);
            }
            else if (this.title === '余热锅炉' && this.cardData.ratedParam.boilerType === '余热热水锅炉') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u4F59\u70ED\u70ED\u6C34\u9505\u7089-").concat(this.cardData.manufacturer), '余热热水锅炉_建模仿真', this.cardData);
            }
            else if (this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '单压') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u4F59\u70ED\u84B8\u6C7D\u9505\u7089-\u5355\u538B-").concat(this.cardData.manufacturer), '余热蒸汽锅炉-单压_建模仿真', this.cardData);
            }
            else if (this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '双压') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u4F59\u70ED\u84B8\u6C7D\u9505\u7089-\u53CC\u538B-").concat(this.cardData.manufacturer), '余热蒸汽锅炉-双压_建模仿真', this.cardData);
            }
            else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '热水') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u70ED\u6C34-").concat(this.cardData.manufacturer), '热水吸收式制冷机_建模仿真', this.cardData);
            }
            else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '烟气') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u70DF\u6C14-").concat(this.cardData.manufacturer), '烟气吸收式制冷机_建模仿真', this.cardData);
            }
            else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '蒸汽') {
                return tools_1["default"].initXlsxData("".concat(this.title, "-\u84B8\u6C7D-").concat(this.cardData.manufacturer), '蒸汽吸收式制冷机_建模仿真', this.cardData);
            }
            else
                return tools_1["default"].initXlsxData("".concat(this.title, "-").concat(this.cardData.manufacturer), "".concat(this.title, "_\u5EFA\u6A21\u4EFF\u771F"), this.cardData);
        }
    };
    /**
     *表单验证
     */
    EquipmentInformationDetails.prototype.formValidate = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _this = this;
            return __generator(this, function (_a) {
                return [2 /*return*/, new Promise(function (resolve, reject) {
                        try {
                            void _this.$refs['form'].validate(function (valid) {
                                if (valid) {
                                    resolve(true);
                                }
                                else {
                                    resolve(false);
                                }
                            });
                        }
                        catch (e) {
                            reject(e);
                        }
                    })];
            });
        });
    };
    /**
     *
     */
    EquipmentInformationDetails.prototype.loadRowData = function (rowData, filedList) {
        var _this = this;
        var newCardData = JSON.parse(JSON.stringify(this.cardData));
        if (!this.isIesMode) {
            var option = this.dataStructure;
            //判断是否每个字段都存在
            if (option.ratedParam.length > 0 &&
                !option.ratedParam
                    .map(function (paramItem) {
                    var index = filedList.indexOf(paramItem.description);
                    if (index === -1) {
                        return false;
                    }
                    else if (paramItem.option != null) {
                        return paramItem.option.indexOf(rowData[index]) !== -1;
                    }
                    else {
                        return true;
                    }
                })
                    .reduce(function (result, item) { return result && item; })) {
                throw new Error('格式不正确: 设备额定运行参数有缺失,或者它的值非法!');
            }
            if (option.operationalConstraints.length > 0 &&
                !option.operationalConstraints
                    .map(function (paramItem) {
                    var index = filedList.indexOf(paramItem.description);
                    if (index === -1) {
                        return false;
                    }
                    else if (paramItem.option != null) {
                        return paramItem.option.indexOf(rowData[index]) !== -1;
                    }
                    else {
                        return true;
                    }
                })
                    .reduce(function (result, item) { return result && item; })) {
                throw new Error('格式不正确: 设备运行约束参数有缺失,或者它的值非法!');
            }
            newCardData.manufacturer = rowData[0];
            newCardData.equipType = rowData[1];
            option.ratedParam.forEach(function (item) {
                var column = filedList.indexOf(item.description);
                if (column !== -1) {
                    _this.$set(newCardData.ratedParam, item.prop, rowData[column]);
                }
            });
            option.operationalConstraints.forEach(function (item) {
                var column = filedList.indexOf(item.description);
                if (column !== -1) {
                    _this.$set(newCardData.operationalConstraints, item.prop, rowData[column]);
                }
            });
            var economicParam = option.economicParam == null || option.economicParam.length === 0 ? this.commonEconomicParams : option.economicParam;
            //经济参数
            economicParam.forEach(function (item) {
                var column = filedList.indexOf(item.description);
                if (column !== -1) {
                    _this.$set(newCardData.economicParam, item.prop, rowData[column]);
                }
            });
            return newCardData;
        }
        else {
            var option = this.dataStructure;
            //判断是否每个字段都存在
            if (!option.ratedParam
                .map(function (paramItem) {
                var index = filedList.indexOf(paramItem.description);
                if (index === -1) {
                    return false;
                }
                else if (paramItem.option != null) {
                    return paramItem.option.indexOf(rowData[index]) !== -1;
                }
                else {
                    return true;
                }
            })
                .reduce(function (result, item) { return result && item; })) {
                throw new Error('格式不正确: 设备额定运行参数有缺失,或者它的值非法!');
            }
            newCardData.manufacturer = rowData[0];
            newCardData.equipType = rowData[1];
            option.ratedParam.forEach(function (item) {
                var column = filedList.indexOf(item.description);
                if (column !== -1) {
                    _this.$set(newCardData.ratedParam, item.prop, rowData[column]);
                }
            });
            return newCardData;
        }
    };
    /**
     *
     */
    EquipmentInformationDetails.prototype.batchLoadDataByExcel = function (file) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.loadFile(file)];
                    case 1: return [2 /*return*/, _a.sent()];
                }
            });
        });
    };
    Object.defineProperty(EquipmentInformationDetails.prototype, "isIesMode", {
        /**
         *
         */
        get: function () {
            //组件没有被渲染出来的时候,这个上下文的this中不包含$store,所以直接导入来解决
            return store_1["default"].state.iesMode;
        },
        enumerable: false,
        configurable: true
    });
    /**
     *从Excel导入数据
     */
    EquipmentInformationDetails.prototype.loadFile = function (file) {
        return __awaiter(this, void 0, void 0, function () {
            var economicParams, data_1, fieldList_1, data_2, option, fieldList_2;
            var _this = this;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!!this.isIesMode) return [3 /*break*/, 2];
                        economicParams = this.dataStructure.economicParam == null || this.dataStructure.economicParam.length === 0
                            ? this.commonEconomicParams
                            : this.dataStructure.economicParam;
                        return [4 /*yield*/, tools_2["default"].loadDataByExcel(file, ['生产厂商', '设备型号'])];
                    case 1:
                        data_1 = _a.sent();
                        //判断是否三个经济性参数都有
                        if (!economicParams
                            .map(function (economicParam) {
                            return data_1[0].find(function (item) { return item.includes(economicParam.description); }) != null;
                        })
                            .reduce(function (result, item) { return result && item; })) {
                            throw new Error('格式不正确: 缺少经济性参数!');
                        }
                        fieldList_1 = data_1.shift();
                        return [2 /*return*/, data_1.map(function (item) { return _this.loadRowData(item, fieldList_1); })];
                    case 2: return [4 /*yield*/, tools_2["default"].loadDataByExcel(file, ['生产厂商', '设备型号'])];
                    case 3:
                        data_2 = _a.sent();
                        option = this.dataStructure;
                        //判断是否每个字段都存在
                        if (!option.ratedParam
                            .map(function (paramItem) {
                            var index = data_2[0].indexOf(paramItem.description);
                            if (index === -1) {
                                return false;
                            }
                            else if (paramItem.option != null) {
                                return paramItem.option.indexOf(data_2[1][index]) !== -1;
                            }
                            else {
                                return true;
                            }
                        })
                            .reduce(function (result, item) { return result && item; })) {
                            throw new Error('格式不正确: 设备额定运行参数有缺失,或者它的值非法!');
                        }
                        fieldList_2 = data_2.shift();
                        return [2 /*return*/, data_2.map(function (item) { return _this.loadRowData(item, fieldList_2); })];
                }
            });
        });
    };
    /**
     *
     */
    EquipmentInformationDetails.prototype.loadDataByExcel = function (file) {
        return __awaiter(this, void 0, void 0, function () {
            var newData, e_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        message_bus_1["default"].Notification('success', { message: '成功上传数据!', description: '', key: '设备信息库卡片导入文件成功提示' });
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.loadFile(file)];
                    case 2:
                        newData = (_a.sent())[0];
                        Object.assign(this.cardData, newData);
                        message_bus_1["default"].Notification('success', { message: '成功上传数据!', description: '', key: '设备信息库卡片导入文件成功提示' });
                        return [3 /*break*/, 4];
                    case 3:
                        e_1 = _a.sent();
                        message_bus_1["default"].Notification('warning', { description: String(e_1), message: '提示', key: '设备信息库卡片导入文件失败提示' });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    __decorate([
        (0, vue_property_decorator_1.Prop)()
    ], EquipmentInformationDetails.prototype, "type");
    __decorate([
        (0, vue_property_decorator_1.Prop)({
            "default": function () {
                return {};
            }
        })
    ], EquipmentInformationDetails.prototype, "cardData");
    __decorate([
        (0, vue_property_decorator_1.Prop)()
    ], EquipmentInformationDetails.prototype, "title");
    __decorate([
        (0, vue_property_decorator_1.Prop)({ "default": function () { return false; } })
    ], EquipmentInformationDetails.prototype, "disable");
    return EquipmentInformationDetails;
}(BaseInformationDetailsCard_1["default"]));
exports["default"] = EquipmentInformationDetails;
