import jinja2
import json
import rich

load_path = "cloudpss_inputs.json"

entry_keys = [
    "excelMap", # 电价，燃料，负荷计价方式，设备信息
    "equipmentParamDict", # ratedP
    "commonEconomicParams",
    "specialEquipmentParamDict",
    "equipmentParamDict2",
]

with open(load_path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())
    # rich.print(data)

excelMap = data["excelMap"]

dataParams = {
    "ratedParam": "设备额定运行参数",
    "operationalConstraints": "设备运行约束",
    "economicParam": "设备经济性参数",
    "OperateParam": "设备工况",
}

# 设备额定运行参数
# 设备运行约束
# 设备经济性参数
# 设备工况

# unknown property:
# 燃气轮机 -> 挡位 -> dict ({"route": "OperateParams.params"})
# 这个参数没有用于建模仿真或者优化

for key, value in excelMap.items():
    if type(value) == dict:
        if "生产厂商" in value.keys():  # with or without unit?
            print("DEVICE NAME:", key)
            # this is a device for sure.
            # rich.print(value)
            for k, v in value.items():
                if type(v) == str:
                    if v.split(".")[0] in dataParams.keys():
                        k0 = dataParams[v.split(".")[0]]
                        print(k0, k, v.split(".")[-1])
                    else:
                        if v not in ["manufacturer", "equipType"]:
                            print(">> UNIDENTIFIED PARAM TYPE <<")
                        print(k, v)
                else:
                    print(">> UNIDENTIFIED VALUE TYPE <<")
                    print(k, type(v), v)
        elif "负荷名称" in value.keys():  # load for sure.
            for k, v in value.items():
                ...
        print("_" * 30)


equipmentParamDict = data["equipmentParamDict"]
# print({k:"" for k in list(equipmentParamDict)})

translationMap = {
    "PhotovoltaicSys": "光伏",
    "WindPowerGenerator": "风机",
    "GasTurbine": "燃气轮机",
    "GasEngine": "燃气内燃机",
    "SteamTurbine": "蒸汽轮机",
    "HeatPump": "热泵",
    "HPSolarCollector": "热管式太阳能集热器",
    "CompRefrg": "电压缩制冷机",
    "IceStorageAC": "蓄冰空调",
    "HeatStorageElectricalBoiler": "蓄热电锅炉",
    "Battery": "蓄电池",
    "Transformer": "变压器",
    "TransferLine": "传输线",
    "Capacitance": "电容器",
    "CentrifugalPump": "离心泵",
    # "Pump": "", # unused?
    # just discard this.
    "Pipe": "管道",
}

print("_____")
for key, value in equipmentParamDict.items():
    item_name = translationMap.get(key, None)
    if item_name:
        # selected!
        k = value.keys()
        print(key, item_name, k)
        # 'ratedParam': list of dict ({"prop", "description"})
        # 'operationalConstraints': list of dict ({"prop", "description"})
        # 'economicParam': list of dict ({"prop", "description"})


print("_____")
equipmentParamDict2 = data["equipmentParamDict2"]
# print({k:"" for k in list(equipmentParamDict2)})

# 建模仿真 不是优化
translationMap2 = {
    "PhotovoltaicSys_ies": "光伏",
    "WindPowerGenerator_ies": "风机",
    "GasEngine_ies": "燃气内燃机",
    "SteamTurbine_ies": "蒸汽轮机",
    "HPSolarCollector_ies": "热管式太阳能集热器",
    "IceStorageAC_ies": "蓄冰空调",
    "HeatStorageElectricalBoiler_ies": "蓄热电锅炉",
    "Battery_ies": "蓄电池",
    "WaterTank_ies": "储水罐",
    "Transformer_ies": "变压器",
    "TransferLine_ies": "传输线",
    "Capacitance_ies": "电容器",
    "MMC_ies": "模块化多电平变流器",
    "Pipe_ies": "管道",
    "GasTurbine_ies": "燃气轮机",
    "HeatPump_ies": "热泵",
    "GasBoiler_ies": "燃气锅炉",
    "CompRefrg_ies": "电压缩制冷机",
    "AbsorptionChiller_ies": "吸收式制冷机",
    "CentrifugalPump_ies": "离心泵",
}
# for key, value in equipmentParamDict2.items():
#     item_name = translationMap2.get(key)
#     # everything is included.
#     k = value.keys()
#     print(key, item_name, k)
# 'ratedParam': list of dict ({"prop", "description"})
# 'operationalConstraints': list of dict ({"prop", "description"})
# 'economicParam': list of dict ({"prop", "description"})
# 'OperateParam': list of dict ({"data", "key", "title", "type"})
