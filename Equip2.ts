





































































































































import { Prop, Component } from 'vue-property-decorator';
import tools from '@/component/template/tools/tools';
import Tools from '@/component/template/tools/tools';
// import { get } from 'lodash';
import MessageBus from '@/Utils/message/message-bus';
import { FormModel } from 'ant-design-vue';
import BaseInformationDetailsCard from '@/component/LibraryOfInformationCardBase/BaseInformationDetailsCard';
import store from '@/store/store';
import { HotTable } from '@handsontable/vue';
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { Column, Worksheet } from 'exceljs';
import { cloneDeep } from 'lodash';
import templateData from '@/component/template/tools/template';
import Handsontable from 'handsontable';

/**
 *
 */
interface ParamDict {
    /**
     *
     */
    ratedParam: Array<{ prop: string; description: string; option?: Array<string | number> | string }>;
    /**
     *
     */
    operationalConstraints: Array<{ prop: string; description: string; option?: Array<string | number> }>;

    /**
     *
     */
    economicParam?: Array<{ prop: string; description: string }>;

    /**
     * columns
     */
    OperateParam?: Array<{ data: string; key: string; title: string; type: string }>;
}

/**
 *
 */
interface CardData {
    /**
     *
     */
    id: number;
    /**
     *
     */
    name: string;
    /**
     *
     */
    manufacturer: string;
    /**
     *
     */
    kind: string;
    /**
     *
     */
    equipType: string;
    /**
     *
     */
    ratedParam: Record<string, string | Array<Record<string, string>>>;
    /**
     *
     */
    operationalConstraints: Record<string, string>;
    /**
     *
     */
    economicParam: {
        purchaseCost: string;
        maintainCost: string;
        fixationMaintainCost: string;
        designLife: string;
    };
    /**
     *
     */
    isDelete: boolean;
    /**
     *
     */
    simu: number;
}

/**
 *
 */
@Component({
    components: {
        'hot-table': HotTable,
    },
})
export default class EquipmentInformationDetailsCardWithTable extends BaseInformationDetailsCard {
    /** */
    @Prop()
    type!: string;
    /** */
    @Prop({
        default: () => {
            return {};
        },
    })
    cardData!: CardData;
    /** */
    @Prop()
    title!: string;
    /** */
    @Prop({ default: () => false })
    disable!: boolean;

    /** */
    canBatchOperation = true;
    /** */
    private hotSettingsData = [] as Array<Record<string, string>>;

    /**
     *获取数字字段校验规则
     */
    get numberFieldRules(): Array<Record<string, unknown>> {
        return this.$store.state.numberFieldRules;
    }

    /**
     *获取文字字段校对规则
     */
    get stringFieldRules(): Array<Record<string, unknown>> {
        return this.$store.state.stringFieldRules;
    }

    /**
     * 根据模板kind
     * 返回不同页面显示数据
     */
    get dataStructure(): ParamDict {
        if (this.cardData.kind.lastIndexOf('ies') > -1 && this.cardData.kind !== '') {
            if (this.cardData.ratedParam.OperateParam || this.cardData.ratedParam.PerformanceCurve) {
                this.hotSettingsData = (this.cardData.ratedParam.OperateParam || this.cardData.ratedParam.PerformanceCurve) as Array<Record<string, string>>;
            } else {
                this.hotSettingsData = EquipmentInformationDetailsCardWithTable.defaultHotTableData[this.cardData.kind];
            }
            return this.equipmentParamDict[this.cardData.kind];
        } else if (this.cardData.kind !== '') {
            if (this.cardData.ratedParam.OperateParam || this.cardData.ratedParam.PerformanceCurve) {
                this.hotSettingsData = (this.cardData.ratedParam.OperateParam || this.cardData.ratedParam.PerformanceCurve) as Array<Record<string, string>>;
            } else {
                this.hotSettingsData = EquipmentInformationDetailsCardWithTable.defaultHotTableData[this.cardData.kind];
            }
            const type = this.cardData.kind + '_' + 'ies';
            return this.equipmentParamDict[type];
        } else {
            return this.equipmentParamDict['PhotovoltaicSys_ies'];
        }
    }

    /** */
    proactiveTrigger = false;
    /**
     * @author dev_yms
     * @description
     * @return void
     */
    async saveToFile(): Promise<void> {
        if (!this.hotSettings.data) {
            tools.initXlsxFile(`${this.title}-${this.cardData.manufacturer}`, `${this.title}_建模仿真`, this.cardData);
        }
        await Tools.init(this.cardData.kind, undefined, undefined, (Worksheet) => {
            return this.initXlsxData(Worksheet);
        });
    }

    /** */
    static excelData = templateData;

    /**
     * initXlsxData
     */
    async initXlsxData(Worksheet: Worksheet): Promise<Worksheet> {
        // 设置表头
        const columns: Array<Partial<Column>> = EquipmentInformationDetailsCardWithTable.excelData[this.cardData.kind].map((x) => {
            return { header: x.name, key: x.key, style: { alignment: { horizontal: 'center', vertical: 'middle' } } };
        });
        Worksheet.columns = columns;

        // 行数据转为列数据
        const result = this.ArrayObjectToArray(this.cardData);

        // 通过列添加数据
        columns.map((x) => {
            const idCol = Worksheet.getColumn(x.key as string);
            idCol.values = [x.header as string].concat(result[x.key as string]);
        });

        return new Promise((resolve) => {
            resolve(Worksheet);
        });
    }

    /**
     * 数据处理
     * 将所需数据按照key提取出来组成数组
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ArrayObjectToArray(data: CardData): any {
        // eslint-disable-line
        const result = cloneDeep(data) as any; // eslint-disable-line
        if (Object.keys(result.operationalConstraints).length > 0) {
            Object.keys(result.operationalConstraints).forEach((x) => {
                result[x] = result.operationalConstraints[x];
            });
        }
        Object.keys(result.ratedParam).forEach((x) => {
            result[x] = result.ratedParam[x];
        });
        if (result.OperateParam) {
            Object.keys(result.OperateParam[0]).forEach((item) => {
                result[item] = [];
            });
            result.OperateParam.forEach((x) => {
                Object.keys(result.OperateParam[0]).forEach((item) => {
                    result[item].push(x[item]);
                });
            });
        } else if (result.PerformanceCurve) {
            Object.keys(result.PerformanceCurve[0]).forEach((item) => {
                result[item] = [];
            });
            result.PerformanceCurve.forEach((x) => {
                Object.keys(result.PerformanceCurve[0]).forEach((item) => {
                    result[item].push(x[item]);
                });
            });
        } else {
            MessageBus.Notification('warning', { description: '未保存数据，请先保存', message: '提示', key: '设备信息库导出excel提示' });
        }
        return result;
    }

    /**
     * 2021-5-21 修改
     * 批量导出
     */
    exportRowData(): { tHeader: string[]; data: string[][] } {
        const isIesMode = this.$store.state.iesMode;
        if (!isIesMode) {
            return tools.initXlsxData(`${this.title}-${this.cardData.manufacturer}`, this.title, this.cardData);
        } else {
            return tools.initXlsxData(`${this.title}-${this.cardData.manufacturer}`, `${this.title}_建模仿真`, this.cardData);
        }
    }

    /**
     * 2021-03-24 修改建模仿真数据
     */
    private equipmentParamDict: Record<string, ParamDict> = {
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

    /** */
    commonEconomicParams = [
        { prop: 'purchaseCost', description: '采购成本(万元/台)' },
        { prop: 'maintainCost', description: '固定维护成本(元/kWh)' },
        { prop: 'maintainCost', description: '可变维护成本(元/kWh)' },
        { prop: 'designLife', description: '设计寿命(年)' },
    ];
    /**
     *表单验证
     */
    async formValidate(): Promise<boolean> {
        return new Promise<boolean>((resolve, reject) => {
            try {
                void (this.$refs['form'] as FormModel).validate((valid) => {
                    if (valid) {
                        resolve(true);
                    } else {
                        resolve(false);
                    }
                });
            } catch (e) {
                reject(e);
            }
        });
    }

    /**
     *
     */
    async batchLoadDataByExcel(file: File): Promise<unknown[]> {
        return await this.loadFile(file);
    }

    /**
     *
     */
    get isIesMode(): boolean {
        //组件没有被渲染出来的时候,这个上下文的this中不包含$store,所以直接导入来解决
        return store.state.iesMode;
    }

    /**
     * 从文件导入
     */
    async loadDataByExcel(file: File): Promise<void> {
        try {
            const newData = (await this.loadFile(file))[0] as any; //eslint-disable-line
            Object.assign(this.cardData, newData);
            /**
             * 以下为页面表格数据更新
             * 判断是否为Pump类型，参数不同
             */
            if (this.hotSettings.data) {
                const data = (await this.loadFile(file)) as any; //eslint-disable-line
                const temp = [] as Array<Record<string, string>>;
                if (this.cardData.kind === 'Pump' || this.cardData.kind === 'CentrifugalPump') {
                    data.forEach((x, index) => {
                        temp.push(x.ratedParam.PerformanceCurve[index]);
                    });
                } else {
                    data.forEach((x, index) => {
                        temp.push(x.ratedParam.OperateParam[index]);
                    });
                }
                this.hotSettings.data = temp;
            }
            MessageBus.Notification('success', { message: '成功上传数据!', description: '', key: '设备信息库卡片导入文件成功提示' });
        } catch (e) {
            MessageBus.Notification('warning', { description: String(e), message: '提示', key: '设备信息库卡片导入文件失败提示' });
        }
    }

    /**
     *从Excel导入数据
     */
    async loadFile(file: File): Promise<unknown[]> {
        const data = await Tools.loadDataByExcel(file, ['生产厂商', '设备型号']);
        const fieldList = data.shift() as string[];
        return data.map((item, index) => this.loadRowData(item, fieldList, index));
    }

    /**
     * 解析数据并返回页面需要的格式
     */
    loadRowData(rowData: string[], filedList: string[], idnex: number): CardData {
        const newCardData = JSON.parse(JSON.stringify(this.cardData));
        const option = this.dataStructure as any; // eslint-disable-line
        //判断是否每个字段都存在
        option.ratedParam.map((paramItem) => {
            const index = filedList.indexOf(paramItem.description);
            if (index === -1) {
                throw new Error('格式不正确: 设备额定运行参数有缺失!');
            }
            if (rowData[index].length === 0) {
                throw new Error('格式不正确: 设备额定运行参数值缺失!');
            }
            if (paramItem.option === 'number' && isNaN(Number(rowData[index]))) {
                throw new Error('格式不正确: 设备额定运行参数值错误!');
            }
        });
        // 修改生产厂商与设备型号
        newCardData.manufacturer = rowData[0];
        newCardData.equipType = rowData[1];
        //  修改运行参数
        option.ratedParam.forEach((item) => {
            const column = filedList.indexOf(item.description);
            if (column !== -1) {
                this.$set(newCardData.ratedParam, item.prop, rowData[column]);
            }
        });
        // 修改运行约束
        option.operationalConstraints.forEach((item) => {
            const column = filedList.indexOf(item.description);
            if (column !== -1) {
                this.$set(newCardData.operationalConstraints, item.prop, rowData[column]);
            }
        });
        /**
         * 修改表格数据
         * 判断是否为Pump类型，参数不同
         */
        if ((option.OperateParam && this.cardData.kind === 'Pump') || this.cardData.kind === 'CentrifugalPump') {
            option.OperateParam.forEach((item) => {
                const column = filedList.indexOf(item.title);
                if (column !== -1) {
                    this.$set(newCardData.ratedParam.PerformanceCurve[idnex], item.key, rowData[column].toString());
                }
            });
        } else if (option.OperateParam) {
            option.OperateParam.forEach((item) => {
                const column = filedList.indexOf(item.title);
                if (column !== -1) {
                    this.$set(newCardData.ratedParam.OperateParam[idnex], item.key, rowData[column].toString());
                }
            });
        }
        return newCardData;
    }

    /**
     * 2021-03-24建模仿真新增默认数据
     *
     */
    static readonly defaultHotTableData = {
        // 燃气轮机
        GasTurbine: [
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
        // 热泵
        HeatPump: [
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
        // 燃气锅炉
        GasBoiler: [
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
        // 电压缩制冷机
        CompRefrg: [
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
        // 吸收式制冷机模板
        AbsorptionChiller: [
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
        // 离心泵
        CentrifugalPump: [
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
    };

    /** hotTableSetting */
    get hotSettings(): Handsontable.GridSettings {
        return {
            stretchH: 'all',
            width: '100%',
            colHeaders: true,
            columns: this.dataStructure.OperateParam,
            autoColumnSize: true,
            height: 150,
            className: 'htCenter', //单元格文字对齐方式(htLeft,htRight,htCenter)
            data: this.hotSettingsData,
            // data: this.cardData.ratedParam.OperateParam ? this.cardData.ratedParam.OperateParam :EquipmentInformationDetailsCardWithTable.defaultHotTableData[this.cardData.kind] || this.cardData.ratedParam.PerformanceCurve ? this.cardData.ratedParam.PerformanceCurve :EquipmentInformationDetailsCardWithTable.defaultHotTableData[this.cardData.kind],
            // 开始改变单元格前被调用
            beforeChange: (changes: string[][]): boolean => {
                return this.beforeTableDataChange(changes);
            },
            //数据改变时触发此方法
            afterChange: (): void => {
                (this.$refs['hotTable'] as any).hotInstance.render(); // eslint-disable-line
                this.changeData();
            },
        };
    }

    /**
     * @author dev_yms
     * @description 监听输入同步结果
     * @return void
     */
    changeData(): void {
        if (this.cardData.kind === 'Pump' || this.cardData.kind === 'CentrifugalPump') {
            const data = {
                PerformanceCurve: this.hotSettings.data,
            };
            this.$store.commit('sethotSettingsData', data);
        } else {
            const data = {
                OperateParam: this.hotSettings.data,
            };
            this.$store.commit('sethotSettingsData', data);
        }
    }

    /**
     * 表格数据改变之前的验证
     * 0: 行; 1: key; 2: undefined; 3: 输入的值
     * 判断输入的值是否合法
     */
    beforeTableDataChange(changes: string[][]): boolean {
        let result = true;
        changes.forEach((x) => {
            if (x[3] == null || x[3] === '' || isNaN(Number(x[3]))) {
                MessageBus.Message('error', `行${x[0] + 1}，列${x[1] + 1}非法的值修改`);
                result = false;
            }
        });
        return result;
    }

    /**
     * @author dev_yms
     * @description 删除最后一行阶梯
     * @return void
     */
    deleteLadder(): void {
        this.$nextTick(() => {
            if (!this.hotSettings.data) {
                MessageBus.Notification('error', { message: '提示', description: '表格数据为空' });
                throw new Error('表格数据为空');
            }
            if (this.hotSettings.data.length <= 1) {
                MessageBus.Notification('warning', { message: '提示', description: '最小阶梯为1,已不可删除' });
            } else this.hotSettings.data.pop();
        });
    }
    /**
     * @author dev_yms
     * @description 新增一行数据
     * @return void
     */
    handleAdd(): void {
        this.$nextTick(() => {
            if (!this.hotSettings.data) {
                MessageBus.Notification('error', { message: '提示', description: '表格数据为空' });
                throw new Error('表格数据为空');
            }
            const max = this.hotSettings.data.length;
            const tableData = this.hotSettings.data as Handsontable.RowObject[];
            if (this.cardData.kind === 'Pump' || this.cardData.kind === 'CentrifugalPump') {
                tableData.push({});
            } else {
                tableData.push({
                    OperateStatus: (max + 1).toString(),
                });
            }
        });
    }
}
