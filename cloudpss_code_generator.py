import jinja2
import json
import rich

load_path = "cloudpss_inputs.json"

with open(load_path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())
    # rich.print(data)

excelMap = data["excelMap"]

dataParams = {
    "ratedParam": "设备额定运行参数",
    "operationalConstraints": "设备运行约束",
    "economicParam": "设备经济性参数",
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
        if "生产厂商" in value.keys():
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
    "IceStorageAC": "",
    "HeatStorageElectricalBoiler": "",
    "Battery": "",
    "Transformer": "",
    "TransferLine": "",
    "Capacitance": "",
    "CentrifugalPump": "",
    "Pump": "",
    "Pipe": "",
}
