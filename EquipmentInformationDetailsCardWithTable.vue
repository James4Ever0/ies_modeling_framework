import BaseInformationDetailsCard from '@/component/LibraryOfInformationCardBase/BaseInformationDetailsCard';
import { Prop } from 'vue-property-decorator';
import { get } from 'lodash';
import tools from '@/component/template/tools/tools';
import { FormModel } from 'ant-design-vue';
import store from '@/store/store';
import Tools from '@/component/template/tools/tools';
import MessageBus from '@/Utils/message/message-bus';

/**
 *
 */
interface ParamDict {
    /**
     *
     */
    ratedParam: Array<{ prop: string; description: string; option?: Array<string | number> }>;
    /**
     *
     */
    operationalConstraints: Array<{ prop: string; description: string; option?: Array<string | number> }>;

    /**
     *
     */
    economicParam?: Array<{ prop: string; description: string }>;
}

/**
 *
 */
export interface CardData {
    /**
     *
     */
    id: number;
    /**
     *
     */
    name: '';
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
    ratedParam: Record<string, string>;
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
export default class EquipmentInformationDetails extends BaseInformationDetailsCard {
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
     *
     */
    get dataStructure(): ParamDict {
        if (this.specialEquipmentParamDict[this.cardData.kind] != null) {
            const paramDict = this.specialEquipmentParamDict[this.cardData.kind].find((item) => {
                if (item.conditions == null) {
                    return true;
                } else {
                    return (
                        item.conditions
                            // eslint-disable-next-line eqeqeq
                            .map((condition) => {
                                if (get(this.cardData, condition.path) == null) {
                                    const newPath = [...condition.path];
                                    const lastPath = newPath.pop();
                                    if (lastPath != null) {
                                        this.$set(get(this.cardData, newPath), lastPath, condition.defaultValue);
                                    }
                                }
                                // eslint-disable-next-line eqeqeq
                                return get(this.cardData, condition.path) == condition.value;
                            })
                            .reduce((isSatisfy, isPass) => isSatisfy && isPass)
                    );
                }
            });
            if (paramDict != null) {
                return paramDict.paramDict;
            } else {
                return this.specialEquipmentParamDict[this.cardData.kind][0].paramDict;
            }
        } else {
            return this.equipmentParamDict[this.cardData.kind];
        }
    }

    /** */
    proactiveTrigger = false;
    /**
     * @author dev_yms
     * @description
     * @return void
     */
    saveToFile(): void {
        if (!this.$store.state.iesMode) {
            if (this.title === '燃气锅炉' && this.cardData.ratedParam.boilerType === '燃气热水锅炉') {
                tools.initXlsxFile(`${this.title}-燃气热水锅炉-${this.cardData.manufacturer}`, '燃气热水锅炉', this.cardData);
            } else if (this.title === '燃气锅炉') {
                tools.initXlsxFile(`${this.title}-燃气蒸汽锅炉-${this.cardData.manufacturer}`, '燃气蒸汽锅炉', this.cardData);
            } else if (this.title === '余热锅炉' && this.cardData.ratedParam.boilerType === '余热热水锅炉') {
                tools.initXlsxFile(`${this.title}-余热热水锅炉-${this.cardData.manufacturer}`, '余热热水锅炉', this.cardData);
            } else if (
                this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '单压'
            ) {
                tools.initXlsxFile(`${this.title}-余热蒸汽锅炉-单压-${this.cardData.manufacturer}`, '余热蒸汽锅炉-单压', this.cardData);
            } else if (
                this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '双压'
            ) {
                tools.initXlsxFile(`${this.title}-余热蒸汽锅炉-双压-${this.cardData.manufacturer}`, '余热蒸汽锅炉-双压', this.cardData);
            } else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '热水') {
                tools.initXlsxFile(`${this.title}-热水-${this.cardData.manufacturer}`, '热水吸收式制冷机', this.cardData);
            } else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '烟气') {
                tools.initXlsxFile(`${this.title}-烟气-${this.cardData.manufacturer}`, '烟气吸收式制冷机', this.cardData);
            } else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '蒸汽') {
                tools.initXlsxFile(`${this.title}-蒸汽-${this.cardData.manufacturer}`, '蒸汽吸收式制冷机', this.cardData);
            } else tools.initXlsxFile(`${this.title}-${this.cardData.manufacturer}`, this.title, this.cardData);
        } else {
            if (this.title === '燃气锅炉' && this.cardData.ratedParam.boilerType === '燃气热水锅炉_建模仿真') {
                tools.initXlsxFile(`${this.title}-燃气热水锅炉-${this.cardData.manufacturer}`, '燃气热水锅炉_建模仿真', this.cardData);
            } else if (this.title === '燃气锅炉') {
                tools.initXlsxFile(`${this.title}-燃气蒸汽锅炉-${this.cardData.manufacturer}`, '燃气蒸汽锅炉_建模仿真', this.cardData);
            } else if (this.title === '余热锅炉' && this.cardData.ratedParam.boilerType === '余热热水锅炉') {
                tools.initXlsxFile(`${this.title}-余热热水锅炉-${this.cardData.manufacturer}`, '余热热水锅炉_建模仿真', this.cardData);
            } else if (
                this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '单压'
            ) {
                tools.initXlsxFile(`${this.title}-余热蒸汽锅炉-单压-${this.cardData.manufacturer}`, '余热蒸汽锅炉-单压_建模仿真', this.cardData);
            } else if (
                this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '双压'
            ) {
                tools.initXlsxFile(`${this.title}-余热蒸汽锅炉-双压-${this.cardData.manufacturer}`, '余热蒸汽锅炉-双压_建模仿真', this.cardData);
            } else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '热水') {
                tools.initXlsxFile(`${this.title}-热水-${this.cardData.manufacturer}`, '热水吸收式制冷机_建模仿真', this.cardData);
            } else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '烟气') {
                tools.initXlsxFile(`${this.title}-烟气-${this.cardData.manufacturer}`, '烟气吸收式制冷机_建模仿真', this.cardData);
            } else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '蒸汽') {
                tools.initXlsxFile(`${this.title}-蒸汽-${this.cardData.manufacturer}`, '蒸汽吸收式制冷机_建模仿真', this.cardData);
            } else tools.initXlsxFile(`${this.title}-${this.cardData.manufacturer}`, `${this.title}_建模仿真`, this.cardData);
        }
    }

    /**
     *
     */
    exportRowData(): { tHeader: string[]; data: string[][] } {
        if (!store.state.iesMode) {
            if (this.title === '燃气锅炉' && this.cardData.ratedParam.boilerType === '燃气热水锅炉') {
                return tools.initXlsxData(`${this.title}-燃气热水锅炉-${this.cardData.manufacturer}`, '燃气热水锅炉', this.cardData);
            } else if (this.title === '燃气锅炉') {
                return tools.initXlsxData(`${this.title}-燃气蒸汽锅炉-${this.cardData.manufacturer}`, '燃气蒸汽锅炉', this.cardData);
            } else if (this.title === '余热锅炉' && this.cardData.ratedParam.boilerType === '余热热水锅炉') {
                return tools.initXlsxData(`${this.title}-余热热水锅炉-${this.cardData.manufacturer}`, '余热热水锅炉', this.cardData);
            } else if (
                this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '单压'
            ) {
                return tools.initXlsxData(`${this.title}-余热蒸汽锅炉-单压-${this.cardData.manufacturer}`, '余热蒸汽锅炉-单压', this.cardData);
            } else if (
                this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '双压'
            ) {
                return tools.initXlsxData(`${this.title}-余热蒸汽锅炉-双压-${this.cardData.manufacturer}`, '余热蒸汽锅炉-双压', this.cardData);
            } else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '热水') {
                return tools.initXlsxData(`${this.title}-热水-${this.cardData.manufacturer}`, '热水吸收式制冷机', this.cardData);
            } else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '烟气') {
                return tools.initXlsxData(`${this.title}-烟气-${this.cardData.manufacturer}`, '烟气吸收式制冷机', this.cardData);
            } else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '蒸汽') {
                return tools.initXlsxData(`${this.title}-蒸汽-${this.cardData.manufacturer}`, '蒸汽吸收式制冷机', this.cardData);
            } else return tools.initXlsxData(`${this.title}-${this.cardData.manufacturer}`, this.title, this.cardData);
        } else {
            if (this.title === '燃气锅炉' && this.cardData.ratedParam.boilerType === '燃气热水锅炉_建模仿真') {
                return tools.initXlsxData(`${this.title}-燃气热水锅炉-${this.cardData.manufacturer}`, '燃气热水锅炉_建模仿真', this.cardData);
            } else if (this.title === '燃气锅炉') {
                return tools.initXlsxData(`${this.title}-燃气蒸汽锅炉-${this.cardData.manufacturer}`, '燃气蒸汽锅炉_建模仿真', this.cardData);
            } else if (this.title === '余热锅炉' && this.cardData.ratedParam.boilerType === '余热热水锅炉') {
                return tools.initXlsxData(`${this.title}-余热热水锅炉-${this.cardData.manufacturer}`, '余热热水锅炉_建模仿真', this.cardData);
            } else if (
                this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '单压'
            ) {
                return tools.initXlsxData(`${this.title}-余热蒸汽锅炉-单压-${this.cardData.manufacturer}`, '余热蒸汽锅炉-单压_建模仿真', this.cardData);
            } else if (
                this.title === '余热锅炉' &&
                this.cardData.ratedParam.boilerType === '余热蒸汽锅炉' &&
                this.cardData.ratedParam.pressureLevel === '双压'
            ) {
                return tools.initXlsxData(`${this.title}-余热蒸汽锅炉-双压-${this.cardData.manufacturer}`, '余热蒸汽锅炉-双压_建模仿真', this.cardData);
            } else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '热水') {
                return tools.initXlsxData(`${this.title}-热水-${this.cardData.manufacturer}`, '热水吸收式制冷机_建模仿真', this.cardData);
            } else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '烟气') {
                return tools.initXlsxData(`${this.title}-烟气-${this.cardData.manufacturer}`, '烟气吸收式制冷机_建模仿真', this.cardData);
            } else if (this.title === '吸收式制冷机' && this.cardData.ratedParam.heatFluidType === '蒸汽') {
                return tools.initXlsxData(`${this.title}-蒸汽-${this.cardData.manufacturer}`, '蒸汽吸收式制冷机_建模仿真', this.cardData);
            } else return tools.initXlsxData(`${this.title}-${this.cardData.manufacturer}`, `${this.title}_建模仿真`, this.cardData);
        }
    }

    /**  */
    equipmentParamDict: Record<string, ParamDict> = {
        PhotovoltaicSys: {
            ratedParam: [
                {
                    prop: 'singlePanelArea',
                    description: '单个光伏板面积(m²)',
                },
                { prop: 'photoelectricConversionEfficiency', description: '光电转换效率(%)' },
            ],
            operationalConstraints: [
                {
                    prop: 'maxPowerGenerating',
                    description: '最大发电功率(kW)',
                },
            ],
        },
        WindPowerGenerator: {
            ratedParam: [
                { prop: 'ratedPowerGenerating', description: '额定容量(kW)' },
                {
                    prop: 'ratedWindSpeed',
                    description: '额定风速(m/s)',
                },
                { prop: 'cutinWindSpeed', description: '切入风速(m/s)' },
                {
                    prop: 'cutoutWindSpeed',
                    description: '切出风速(m/s)',
                },
                { prop: 'towerHeight', description: '塔筒高度(m)' },
            ],
            operationalConstraints: [],
        },
        GasTurbine: {
            ratedParam: [
                { prop: 'powerGenerating', description: '额定发电功率(kW)' },
                {
                    prop: 'generatingEfficiency',
                    description: '发电效率(%)',
                },
                { prop: 'heatingEfficiency', description: '制热效率(%)' },
            ],
            operationalConstraints: [
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
        GasEngine: {
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
        SteamTurbine: {
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
        HeatPump: {
            ratedParam: [
                { prop: 'ratedHeatSupply', description: '额定制热量(kW)' },
                {
                    prop: 'heatingCOP',
                    description: '额定能效比COP',
                },
                { prop: 'ratedCoolSupply', description: '额定制冷量(kW)' },
                { prop: 'coolingCOP', description: '制冷能效比COP' },
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
                    prop: 'maxVoltage',
                    description: '最大工作电压(V)',
                },
                { prop: 'miniVoltage', description: '最小工作电压(V)' },
                { prop: 'maxPressure', description: '机组最大承压(MPa)' },
            ],
        },
        HPSolarCollector: {
            ratedParam: [
                {
                    prop: 'plateArea',
                    description: '单个集热器面积(m²)',
                },
                { prop: 'collectionEfficiency', description: '集热效率(%)' },
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
                    prop: 'maxPressure',
                    description: '机组最大承压(MPa)',
                },
            ],
        },
        CompRefrg: {
            ratedParam: [
                { prop: 'ratedCoolSupply', description: '额定制冷量(kW)' },
                {
                    prop: 'COP',
                    description: '制冷能效比COP',
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
                    prop: 'maxPressure',
                    description: '机组最大承压(MPa)',
                },
            ],
        },
        IceStorageAC: {
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
        HeatStorageElectricalBoiler: {
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
        Battery: {
            ratedParam: [
                { prop: 'ratedChargingPower', description: '额定充电功率(kW)' },
                {
                    prop: 'chargingEfficiency',
                    description: '充电效率(%)',
                },
                { prop: 'ratedDischargingPower', description: '额定放电功率(kW)' },
                {
                    prop: 'dischargingEfficiency',
                    description: '放电效率(%)',
                },
            ],
            operationalConstraints: [{ prop: 'capacity', description: '电池最大容量(kWh)' }],
        },
        Transformer: {
            ratedParam: [
                {
                    prop: 'wind1RatioVoltage',
                    description: '原边侧额定电压有效值(kV)',
                },
                { prop: 'wind2RatioVoltage', description: '副边侧额定电压有效值(V)' },
                {
                    prop: 'excitationConductance',
                    description: '励磁电导(p.u.)',
                },
                { prop: 'excitationAdmittance', description: '励磁电纳(p.u.)' },
            ],
            operationalConstraints: [
                { prop: 'maxWind2Ratio', description: '最大非标准变比(p.u.)' },
                {
                    prop: 'miniWind2Ratio',
                    description: '最小非标准变比(p.u.)',
                },
            ],
        },
        TransferLine: {
            ratedParam: [
                { prop: 'ratedVoltage', description: '额定电压(kV)' },
                {
                    prop: 'ratedFrequency',
                    description: '额定频率(Hz)',
                },
                {
                    prop: 'resistanceOfUnitLength',
                    description: '单位长度正序电阻(p.u./km)',
                },
                { prop: 'reactanceOfUnitLength', description: '单位长度正序电抗(p.u./km)' },
                {
                    prop: 'chargingBofUnitLength',
                    description: '单位长度正序电纳(p.u./km)',
                },
            ],
            operationalConstraints: [],
            economicParam: [
                { prop: 'purchaseCost', description: '采购成本(万元/km)' },
                { prop: 'maintainCost', description: '维护成本(元/(km·年))' },
                { prop: 'designLife', description: '设计寿命(年)' },
            ],
        },
        Capacitance: {
            ratedParam: [
                { prop: 'ratedVoltage', description: '额定容量(MVA)' },
                {
                    prop: 'validRatedVoltage',
                    description: '额定电压有效值(Hz)',
                },
            ],
            operationalConstraints: [],
        },
        CentrifugalPump: {
            ratedParam: [
                { prop: 'operationCurveParamA', description: '工作特性曲线系数A' },
                {
                    prop: 'operationCurveParamB',
                    description: '工作特性曲线系数B',
                },
                { prop: 'operationCurveParamC', description: '工作特性曲线系数C' },
                { prop: 'efficency', description: '泵效率(%)' },
            ],
            operationalConstraints: [
                {
                    prop: 'miniInletPressure',
                    description: '最低进口压力(MPa)',
                },
                { prop: 'maxInlePressure', description: '最大进口压力(MPa)' },
            ],
        },
        Pump: {
            ratedParam: [
                { prop: 'operationCurveParamA', description: '工作特性曲线系数A' },
                {
                    prop: 'operationCurveParamB',
                    description: '工作特性曲线系数B',
                },
                { prop: 'operationCurveParamC', description: '工作特性曲线系数C' },
                { prop: 'efficency', description: '泵效率(%)' },
            ],
            operationalConstraints: [
                {
                    prop: 'miniInletPressure',
                    description: '最低进口压力(MPa)',
                },
                { prop: 'maxInlePressure', description: '最大进口压力(MPa)' },
            ],
        },
        Pipe: {
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
    };

    /** */
    specialEquipmentParamDict: Record<
        string,
        Array<{
            conditions?: Array<{ value: string; defaultValue: string; path: string[] }>;
            paramDict: ParamDict;
        }>
    > = {
        GasBoiler: [
            {
                conditions: [{ value: '燃气热水锅炉', path: ['ratedParam', 'boilerType'], defaultValue: '燃气热水锅炉' }],
                paramDict: {
                    ratedParam: [
                        {
                            prop: 'boilerType',
                            description: '燃气锅炉类型',
                            option: ['燃气热水锅炉', '燃气蒸汽锅炉'],
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
                    ],
                },
            },
            {
                conditions: [{ value: '燃气蒸汽锅炉', path: ['ratedParam', 'boilerType'], defaultValue: '燃气热水锅炉' }],
                paramDict: {
                    ratedParam: [
                        {
                            prop: 'boilerType',
                            description: '燃气锅炉类型',
                            option: ['燃气热水锅炉', '燃气蒸汽锅炉'],
                        },
                        { prop: 'ratedHeatSupply', description: '额定供热量(kW)' },
                        { prop: 'heatingEfficiency', description: '制热效率(%)' },
                    ],
                    operationalConstraints: [
                        { prop: 'maxSteamOutletTemp', description: '最大蒸汽出口温度(℃)' },
                        { prop: 'miniSteamOutletTemp', description: '最小蒸汽出口温度(℃)' },
                        { prop: 'maxPressure', description: '机组最大承压(MPa)' },
                    ],
                },
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
                            option: ['余热热水锅炉', '余热蒸汽锅炉'],
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
                    ],
                },
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
                            option: ['余热热水锅炉', '余热蒸汽锅炉'],
                        },
                        {
                            prop: 'pressureLevel',
                            description: '压力等级',
                            option: ['单压', '双压'],
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
                    ],
                },
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
                            option: ['余热热水锅炉', '余热蒸汽锅炉'],
                        },
                        {
                            prop: 'pressureLevel',
                            description: '压力等级',
                            option: ['单压', '双压'],
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
                    ],
                },
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
                    ],
                },
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
                    ],
                },
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
                    ],
                },
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
                    ],
                },
            },
        ],
    };

    /** */
    commonEconomicParams = [
        { prop: 'purchaseCost', description: '采购成本(万元/台)' },
        { prop: 'maintainCost', description: '固定维护成本(万元/年)' },
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
    loadRowData(rowData: string[], filedList: string[]): CardData {
        const newCardData = JSON.parse(JSON.stringify(this.cardData));
        if (!this.isIesMode) {
            const option = this.dataStructure;
            //判断是否每个字段都存在
            if (
                option.ratedParam.length > 0 &&
                !option.ratedParam
                    .map((paramItem) => {
                        const index = filedList.indexOf(paramItem.description);
                        if (index === -1) {
                            return false;
                        } else if (paramItem.option != null) {
                            return paramItem.option.indexOf(rowData[index]) !== -1;
                        } else {
                            return true;
                        }
                    })
                    .reduce((result, item) => result && item)
            ) {
                throw new Error('格式不正确: 设备额定运行参数有缺失,或者它的值非法!');
            }

            if (
                option.operationalConstraints.length > 0 &&
                !option.operationalConstraints
                    .map((paramItem) => {
                        const index = filedList.indexOf(paramItem.description);
                        if (index === -1) {
                            return false;
                        } else if (paramItem.option != null) {
                            return paramItem.option.indexOf(rowData[index]) !== -1;
                        } else {
                            return true;
                        }
                    })
                    .reduce((result, item) => result && item)
            ) {
                throw new Error('格式不正确: 设备运行约束参数有缺失,或者它的值非法!');
            }

            newCardData.manufacturer = rowData[0];
            newCardData.equipType = rowData[1];
            option.ratedParam.forEach((item) => {
                const column = filedList.indexOf(item.description);
                if (column !== -1) {
                    this.$set(newCardData.ratedParam, item.prop, rowData[column]);
                }
            });
            option.operationalConstraints.forEach((item) => {
                const column = filedList.indexOf(item.description);
                if (column !== -1) {
                    this.$set(newCardData.operationalConstraints, item.prop, rowData[column]);
                }
            });

            const economicParam = option.economicParam == null || option.economicParam.length === 0 ? this.commonEconomicParams : option.economicParam;

            //经济参数

            economicParam.forEach((item) => {
                const column = filedList.indexOf(item.description);
                if (column !== -1) {
                    this.$set(newCardData.economicParam, item.prop, rowData[column]);
                }
            });

            return newCardData;
        } else {
            const option = this.dataStructure;
            //判断是否每个字段都存在
            if (
                !option.ratedParam
                    .map((paramItem) => {
                        const index = filedList.indexOf(paramItem.description);
                        if (index === -1) {
                            return false;
                        } else if (paramItem.option != null) {
                            return paramItem.option.indexOf(rowData[index]) !== -1;
                        } else {
                            return true;
                        }
                    })
                    .reduce((result, item) => result && item)
            ) {
                throw new Error('格式不正确: 设备额定运行参数有缺失,或者它的值非法!');
            }
            newCardData.manufacturer = rowData[0];
            newCardData.equipType = rowData[1];
            option.ratedParam.forEach((item) => {
                const column = filedList.indexOf(item.description);
                if (column !== -1) {
                    this.$set(newCardData.ratedParam, item.prop, rowData[column]);
                }
            });
            return newCardData;
        }
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
     *从Excel导入数据
     */
    async loadFile(file: File): Promise<unknown[]> {
        if (!this.isIesMode) {
            const economicParams =
                this.dataStructure.economicParam == null || this.dataStructure.economicParam.length === 0
                    ? this.commonEconomicParams
                    : this.dataStructure.economicParam;
            const data = await Tools.loadDataByExcel(file, ['生产厂商', '设备型号']);
            //判断是否三个经济性参数都有
            if (
                !economicParams
                    .map((economicParam) => {
                        return data[0].find((item) => item.includes(economicParam.description)) != null;
                    })
                    .reduce((result, item) => result && item)
            ) {
                throw new Error('格式不正确: 缺少经济性参数!');
            }
            const fieldList = data.shift() as string[];
            return data.map((item) => this.loadRowData(item, fieldList));
        } else {
            const data = await Tools.loadDataByExcel(file, ['生产厂商', '设备型号']);
            const option = this.dataStructure;
            //判断是否每个字段都存在
            if (
                !option.ratedParam
                    .map((paramItem) => {
                        const index = data[0].indexOf(paramItem.description);
                        if (index === -1) {
                            return false;
                        } else if (paramItem.option != null) {
                            return paramItem.option.indexOf(data[1][index]) !== -1;
                        } else {
                            return true;
                        }
                    })
                    .reduce((result, item) => result && item)
            ) {
                throw new Error('格式不正确: 设备额定运行参数有缺失,或者它的值非法!');
            }
            const fieldList = data.shift() as string[];
            return data.map((item) => this.loadRowData(item, fieldList));
        }
    }
    /**
     *
     */
    async loadDataByExcel(file: File): Promise<void> {
        MessageBus.Notification('success', { message: '成功上传数据!', description: '', key: '设备信息库卡片导入文件成功提示' });
        try {
            const newData = (await this.loadFile(file))[0];
            Object.assign(this.cardData, newData);
            MessageBus.Notification('success', { message: '成功上传数据!', description: '', key: '设备信息库卡片导入文件成功提示' });
        } catch (e) {
            MessageBus.Notification('warning', { description: String(e), message: '提示', key: '设备信息库卡片导入文件失败提示' });
        }
    }
}
