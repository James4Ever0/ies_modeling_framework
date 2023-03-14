//eslint-disable-next-line
type T = any;
const EquipmentFilterMap = {
    /** 热泵模板 */
    HeatPump: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 燃气锅炉模板 */
    GasBoiler: {
        option: [
            {
                des: '锅炉类型:',
                option: ['燃气热水锅炉', '燃气蒸汽锅炉'],
            },
        ],
        filterMethod: (data: T[], checkList: string[][]): string[] => {
            return data.filter((x) => checkList[0].includes(x['ratedParam']['boilerType']));
        },
    },
    /** 余热锅炉模板 */
    HeatRecoveryBoiler: {
        option: [
            {
                des: '锅炉类型:',
                option: ['余热热水锅炉', '余热单压蒸汽锅炉', '余热双压蒸汽锅炉'],
            },
        ],
        filterMethod: (data: T[], checkList: string[][]): string[] => {
            return data.filter((x) => {
                if (checkList[0].includes('余热热水锅炉')) {
                    if (x.ratedParam.boilerType === '余热热水锅炉') return true;
                }
                if (checkList[0].includes('余热单压蒸汽锅炉')) {
                    if (x.ratedParam.boilerType === '余热蒸汽锅炉' && x.ratedParam.pressureLevel === '单压') return true;
                }
                if (checkList[0].includes('余热双压蒸汽锅炉')) {
                    if (x.ratedParam.boilerType === '余热蒸汽锅炉' && x.ratedParam.pressureLevel === '双压') return true;
                }
                return false;
            });
        },
    },
    /** 热管式太阳能集热器模板 */
    HPSolarCollector: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 电压缩制冷机模板 */
    CompRefrg: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 吸收式制冷机模板 */
    AbsorptionChiller: {
        option: [
            {
                des: '热源流体类型:',
                option: ['热水', '蒸汽', '烟气'],
            },
        ],
        filterMethod: (data: T[], checkList: string[][]): string[] => {
            return data.filter((x) => checkList[0].includes(x['ratedParam']['heatFluidType']));
        },
    },
    /** 变压器模板 */
    Transformer: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 传输线模板 */
    TransferLine: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 电容器模板 */
    Capacitance: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /**
     * 模块化多电平变流器
     */
    MMC: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 光伏模板 */
    PhotovoltaicSys: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 风机模板 */
    WindPowerGenerator: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 燃气轮机模板 */
    GasTurbine: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 燃气内燃机模板 */
    GasEngine: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 蒸汽轮机模板 */
    SteamTurbine: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 离心泵模板 */
    Pump: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 离心泵模板 */
    CentrifugalPump: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 换热器模板 */
    HeatExchanger: {
        option: [
            {
                des: '热源类型:',
                option: ['热水', '烟气'],
            },
        ],
        filterMethod: (data: T[], checkList: string[][]): string[] => {
            return data.filter((x) => checkList[0].includes(x['ratedParam']['heatSourceType']));
        },
    },
    /** 管道模板 */
    Pipe: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
    /** 蓄冰空调 */
    IceStorageAC: {
        option: [
            {
                des: '暂无筛选条件!',
            },
        ],
    },
    /** 蓄热电锅炉 */
    HeatStorageElectricalBoiler: {
        option: [
            {
                des: '暂无筛选条件!',
            },
        ],
    },
    /** 蓄电池 */
    Battery: {
        option: [
            {
                des: '暂无筛选条件!',
            },
        ],
    },
    /**
     * 储水罐
     */
    WaterTank: {
        option: [
            {
                des: '暂无筛选条件!',
                // option: [''],
            },
        ],
    },
};
export default EquipmentFilterMap;
