
# 建模仿真和规划设计的输入参数和区别

规划设计在设备信息库内添加了经济性参数，而建模仿真对某些设备将额定工况变为了多工况的输入。
下面介绍在能流拓扑图中两种模式的输入项区别：



## 建模仿真参数

### 参数分类

| 参数分类            | 中文名称                     | 有关设备                                                                                                                                                                                                                           |
|:--------------------|:-----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DeviceParameters    | 机组参数, 设备参数, 母线参数 | 母线, 吸收式制冷机, 蓄电池, 电容器, 电压缩制冷机, 尾气排放装置, 燃气锅炉, 余热锅炉, 换热器, 热泵, 蓄热电锅炉, 热管式太阳能集热器, 蓄冰空调, 光伏系统, 管道, 离心泵, 传输线, 变压器, 风机, 蒸汽轮机, 燃气轮机, 燃气内燃机, 外部电源 |
| OperationParameters | 运行参数组                   | 吸收式制冷机, 电压缩制冷机, 尾气排放装置, 燃气锅炉, 余热锅炉, 换热器, 热泵, 蓄热电锅炉, 热管式太阳能集热器, 蓄冰空调, 负荷, 蒸汽轮机, 燃气轮机, 燃气内燃机, 外部电源                                                               |
| ComputingParameters | 计算参数组                   | 蓄电池, 电压缩制冷机, 燃气锅炉, 热泵, 蒸汽轮机, 燃气轮机, 燃气内燃机                                                                                                                                                               |
| LoadSettings        | 负荷设置                     | 负荷                                                                                                                                                                                                                               |

#### 基础参数
要指定设备台数
#### 仿真参数
配电传输设备除模块化多电平变流器都不具备仿真参数，及管道、采暖制冷负荷、电负荷都不具备
#### 优化参数
具备优化参数的设备可选是否优化，部分设备优化参数具有其他参数，例如柔性电负荷的最大负荷
#### 运行约束
采暖制冷负荷具备运行约束，供热/制冷最大、最小出口温度。

### 详细说明


### 母线

#### 设备信息

|    | classname   | name   |   type | thutype    |   ver |   id | sym     |
|---:|:------------|:-------|-------:|:-----------|------:|-----:|:--------|
|  0 | BusNode     | 母线   |  15000 | electrical |     1 |    0 | BusNode |

#### 针脚定义

|    |   node | label   |   conntype |
|---:|-------:|:--------|-----------:|
|  0 |     -1 |         |          1 |

#### 参数填写

##### DeviceParameters

| ID       | type   | value   | desc     | cond   | unit   | inputType   | choices                                       | help     |
|:---------|:-------|:--------|:---------|:-------|:-------|:------------|:----------------------------------------------|:---------|
| Name     | text   |         | 母线名称 | true   | nan    | nan         | nan                                           | nan      |
| VBase    | real   | 115.0   | 额定电压 | true   | kV     | constant    | nan                                           | nan      |
| V        | real   | 1.0     | 电压     | true   | pu     | constant    | nan                                           | nan      |
| Angle    | real   | 0.0     | 相角     | true   | deg    | constant    | nan                                           | nan      |
| NodeType | choice | 1       | 节点类型 | nan    | nan    | nan         | {'1': 'PQBus', '2': 'PVBus', '3': 'SlackBus'} | 节点类型 |


### 吸收式制冷机

#### 设备信息

|    | classname         | name         |   type | thutype   |   ver |   id | sym                  |
|---:|:------------------|:-------------|-------:|:----------|------:|-----:|:---------------------|
|  0 | AbsorptionChiller | 吸收式制冷机 |  11000 | heatelec  |    59 |    0 | NewAbsorptionChiller |

#### 针脚定义

|    |   node | label   | cond                                          |   conntype |
|---:|-------:|:--------|:----------------------------------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2                        |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==3)&&(HeatSourceType==0) |         42 |
|  2 |     -1 |         | (!show_pin||show_pin==3)&&(HeatSourceType==1) |         41 |
|  3 |     -1 |         | (!show_pin||show_pin==3)&&(HeatSourceType==2) |         43 |
|  4 |     -1 |         | (!show_pin||show_pin==3)&&(HeatSourceType==2) |         43 |
|  5 |     -1 |         | !show_pin||show_pin==3                        |         44 |
|  6 |     -1 |         | !show_pin||show_pin==3                        |         42 |

#### 参数填写

##### DeviceParameters

| ID                   | type    | value        | desc             | choices                                    | inputType   | cond               | unit   |   min |    max |
|:---------------------|:--------|:-------------|:-----------------|:-------------------------------------------|:------------|:-------------------|:-------|------:|-------:|
| CompName             | text    | 吸收式制冷机 | 元件名称         | nan                                        | nan         | nan                | nan    |   nan |    nan |
| HeatSourceType       | choice  | 0            | 热源流体类型     | {'0': '热水', '1': '蒸汽', '2': '烟气'}    | nan         | nan                | nan    |   nan |    nan |
| DeviceSelection      | choice  | 0            | 设备选型         | {'0': '设备类型待选', '1': '东星/dx-30wd'} | nan         | nan                | nan    |   nan |    nan |
| DeviceNumber         | integer | 1            | 设备台数         | nan                                        | constant    | DeviceSelection!=0 | nan    |   nan |    nan |
| MiniCoolSupply       | real    | 0.0          | 最小制冷功率     | nan                                        | constant    | DeviceSelection==0 | kW     |   nan |    nan |
| MaxCoolSupply        | real    | 1000.0       | 最大制冷功率     | nan                                        | constant    | DeviceSelection==0 | kW     |   nan |    nan |
| MiniHeatSupply       | real    | 0.0          | 最小制热功率     | nan                                        | constant    | DeviceSelection==0 | kW     |     0 | 999999 |
| MaxHeatSupply        | real    | 1000.0       | 最大制热功率     | nan                                        | constant    | DeviceSelection==0 | kW     |     0 | 999999 |
| HeatingPriceModel    | choice  | 0            | 热水用热计价模型 | {'0': '无'}                                | nan         | HeatSourceType==0  | nan    |   nan |    nan |
| SteamPriceModel      | choice  | 0            | 蒸汽用热计价模型 | {'0': '无'}                                | nan         | HeatSourceType==1  | nan    |   nan |    nan |
| CoolSupplyPriceModel | choice  | 0            | 供冷过网计价模型 | {'0': '无'}                                | nan         | nan                | nan    |   nan |    nan |
| HeatSupplyPriceModel | choice  | 0            | 供热过网计价模型 | {'0': '无'}                                | nan         | nan                | nan    |   nan |    nan |

##### OperationParameters

| ID                          | type   |   value | choices                | desc                     | cond                                                                   | unit   |   min |   max | inputType   |
|:----------------------------|:-------|--------:|:-----------------------|:-------------------------|:-----------------------------------------------------------------------|:-------|------:|------:|:------------|
| IsSourceReturnTempSpecified | choice |     0   | {'0': '否', '1': '是'} | 热源流体出口温度是否指定 | HeatSourceType==2                                                      | nan    |   nan |   nan | nan         |
| SourceReturnTemp            | real   |    50   | nan                    | 热源流体出口温度         | HeatSourceType==0||(HeatSourceType==2&&IsSourceReturnTempSpecified==1) | ℃      |     0 |  1000 | constant    |
| IsSourcePressureSpecified   | choice |     0   | {'0': '否', '1': '是'} | 热源流体进口压力是否指定 | HeatSourceType==2                                                      | nan    |   nan |   nan | nan         |
| SourceInletPressure         | real   |     0.5 | nan                    | 热源流体进口压力         | (HeatSourceType==2&&IsSourcePressureSpecified==1)||HeatSourceType==1   | MPa    |     0 |    99 | constant    |
| ColdWaterSupplyTemp         | real   |    10   | nan                    | 冷水出口温度             | nan                                                                    | ℃      |   -20 |    99 | constant    |
| HeatWaterSupplyTemp         | real   |    60   | nan                    | 热水出口温度             | nan                                                                    | ℃      |     0 |   200 | constant    |


### 蓄电池

#### 设备信息

|    | classname   | name   |   type | thutype    |   ver |   id | sym        |
|---:|:------------|:-------|-------:|:-----------|------:|-----:|:-----------|
|  0 | Battery     | 蓄电池 |  14000 | electrical |    19 |    0 | NewBattery |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |          1 |

#### 参数填写

##### DeviceParameters

| ID                    | type    | value   | desc             | choices                                          |   min |   max | inputType   | cond               | unit   |
|:----------------------|:--------|:--------|:-----------------|:-------------------------------------------------|------:|------:|:------------|:-------------------|:-------|
| CompName              | text    | 蓄电池  | 元件名称         | nan                                              |   nan |   nan | nan         | nan                | nan    |
| DeviceSelection       | choice  | 0       | 设备选型         | {'0': '设备类型待选', '1': '盛弘电气/PWS2-250K'} |   nan |   nan | nan         | nan                | nan    |
| DeviceNumber          | integer | 1       | 设备台数         | nan                                              |     0 |  9999 | constant    | DeviceSelection!=0 | nan    |
| MiniPowerStorage      | real    | 0.0     | 最小蓄电量       | nan                                              |   nan |   nan | constant    | DeviceSelection==0 | kWh    |
| MaxPowerStorage       | real    | 1000.0  | 最大蓄电量       | nan                                              |   nan |   nan | constant    | DeviceSelection==0 | kWh    |
| ChargingPriceModel    | choice  | 0       | 用电计价模型     | {'0': '无'}                                      |   nan |   nan | nan         | nan                | nan    |
| DischargingPriceModel | choice  | 0       | 供电上网计价模型 | {'0': '无'}                                      |   nan |   nan | nan         | nan                | nan    |

##### ComputingParameters

| ID          | type   |   value | choices                | desc                 |
|:------------|:-------|--------:|:-----------------------|:---------------------|
| IsSlackNode | choice |       0 | {'0': '否', '1': '是'} | 是否作为系统参考节点 |


### 电容器

#### 设备信息

|    | classname   | name   |   type | thutype    |   ver |   id | sym            |
|---:|:------------|:-------|-------:|:-----------|------:|-----:|:---------------|
|  0 | Capacitance | 电容器 |  15000 | electrical |    11 |    0 | NewCapacitance |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |          1 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value   | desc     | choices   |
|:----------------|:-------|:--------|:---------|:----------|
| CompName        | text   | 电容器  | 元件名称 | nan       |
| DeviceSelection | choice | 0       | 设备选型 | {}        |


### 电压缩制冷机

#### 设备信息

|    | classname   | name         |   type | thutype   |   ver |   id | sym          |
|---:|:------------|:-------------|-------:|:----------|------:|-----:|:-------------|
|  0 | CompRefrg   | 电压缩制冷机 |  11000 | heatelec  |    58 |    0 | NewCompRefrg |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2 |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         44 |

#### 参数填写

##### DeviceParameters

| ID                | type    | value        | desc             | choices                                                                                                                                                                                                                                                                                                            | inputType   | cond               | unit   |   min |     max |
|:------------------|:--------|:-------------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|:-------------------|:-------|------:|--------:|
| CompName          | text    | 电压缩制冷机 | 元件名称         | nan                                                                                                                                                                                                                                                                                                                | nan         | nan                | nan    |   nan | nan     |
| DeviceSelection   | choice  | 0            | 设备选型         | {'0': '设备类型待选', '1': '凯德利/KDSL02050P'}                                                                                                                                                                                                                                                                    | nan         | nan                | nan    |   nan | nan     |
| DeviceNumber      | integer | 1            | 设备台数         | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection!=0 | nan    |   nan | nan     |
| MiniCoolSupply    | real    | 0.0          | 最小制冷量       | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kW     |     0 |   1e+08 |
| MaxCoolSupply     | real    | 10000.0      | 最大制冷量       | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kW     |     0 |   1e+08 |
| PowerPriceModel   | choice  | 0            | 用电计价模型     | {'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'} | nan         | nan                | nan    |   nan | nan     |
| CoolingPriceModel | choice  | 0            | 供冷过网计价模型 | {'0': '无'}                                                                                                                                                                                                                                                                                                        | nan         | nan                | nan    |   nan | nan     |

##### OperationParameters

| ID         | type   | unit   |   min |   max |   value | inputType   | desc     |
|:-----------|:-------|:-------|------:|------:|--------:|:------------|:---------|
| SupplyTemp | real   | ℃      |   -20 |    99 |      15 | constant    | 供水温度 |

##### ComputingParameters

| ID          | type   |   value | choices                | desc                 |
|:------------|:-------|--------:|:-----------------------|:---------------------|
| IsSlackNode | choice |       0 | {'0': '否', '1': '是'} | 是否作为系统参考节点 |


### 尾气排放装置

#### 设备信息

|    | classname      | name         |   type | thutype   |   ver |   id | sym               |
|---:|:---------------|:-------------|-------:|:----------|------:|-----:|:------------------|
|  0 | ExhaustTreater | 尾气排放装置 |  16000 | heat      |    11 |    0 | NewExhaustTreater |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |         43 |

#### 参数填写

##### DeviceParameters

| ID       | type   | value        | desc     |
|:---------|:-------|:-------------|:---------|
| CompName | text   | 尾气排放装置 | 元件名称 |

##### OperationParameters

| ID                         | type   |   value | choices                | desc                 | unit   |   min |   max | inputType   | cond                          |
|:---------------------------|:-------|--------:|:-----------------------|:---------------------|:-------|------:|------:|:------------|:------------------------------|
| IsExhaustPressureSpecified | choice |       0 | {'0': '否', '1': '是'} | 进口烟气压力是否指定 | nan    |   nan |   nan | nan         | nan                           |
| ExhaustPressure            | real   |       2 | nan                    | 进口烟气压力         | MPa    |     0 |    99 | constant    | IsExhaustPressureSpecified==1 |


### 燃气锅炉

#### 设备信息

|    | classname   | name     |   type | thutype   |   ver |   id | sym          |
|---:|:------------|:---------|-------:|:----------|------:|-----:|:-------------|
|  0 | GasBoiler   | 燃气锅炉 |  11000 | heat      |    93 |    0 | NewGasBoiler |

#### 针脚定义

|    |   node | label   | cond          |   conntype |
|---:|-------:|:--------|:--------------|-----------:|
|  0 |     -1 |         | BoilerType==0 |         42 |
|  1 |     -1 |         | BoilerType==1 |         41 |

#### 参数填写

##### DeviceParameters

| ID                | type    | value    | desc             | choices                                                                           | inputType   | cond               | unit   |   min |    max |
|:------------------|:--------|:---------|:-----------------|:----------------------------------------------------------------------------------|:------------|:-------------------|:-------|------:|-------:|
| CompName          | text    | 燃气锅炉 | 元件名称         | nan                                                                               | nan         | nan                | nan    |   nan |    nan |
| BoilerType        | choice  | 0        | 锅炉类型         | {'0': '热水锅炉', '1': '蒸汽锅炉'}                                                | nan         | nan                | nan    |   nan |    nan |
| DeviceSelection   | choice  | 0        | 设备选型         | {'0': '设备类型待选', '1': '泰康锅炉/SZS10-2.5-YQ', '2': '泰康锅炉/SZS40-2.5-YQ'} | nan         | nan                | nan    |   nan |    nan |
| DeviceNumber      | integer | 1        | 设备台数         | nan                                                                               | constant    | DeviceSelection!=0 | nan    |   nan |    nan |
| MiniHeatSupply    | real    | 0.0      | 最小制热功率     | nan                                                                               | constant    | DeviceSelection==0 | kW     |     0 | 999999 |
| MaxHeatSupply     | real    | 1000.0   | 最大制热功率     | nan                                                                               | constant    | DeviceSelection==0 | kW     |     0 | 999999 |
| FuelPriceModel    | choice  | 0        | 燃料计价模型     | {'0': '无', '1': '天然气-居民'}                                                   | nan         | nan                | nan    |   nan |    nan |
| HeatingPriceModel | choice  | 0        | 供热过网计价模型 | {'0': '无', '1': '燃气电站供热价格'}                                              | nan         | nan                | nan    |   nan |    nan |

##### OperationParameters

| ID              | type   | unit   |   min |   max |   value | inputType   | desc     | cond          |
|:----------------|:-------|:-------|------:|------:|--------:|:------------|:---------|:--------------|
| SteamSupplyTemp | real   | ℃      |     0 |   500 |     180 | constant    | 蒸汽温度 | BoilerType==1 |
| WaterSupplyTemp | real   | ℃      |     0 |   200 |      80 | constant    | 供水温度 | BoilerType==0 |

##### ComputingParameters

| ID          | type   |   value | choices                | desc                 |
|:------------|:-------|--------:|:-----------------------|:---------------------|
| IsSlackNode | choice |       0 | {'0': '否', '1': '是'} | 是否作为系统参考节点 |


### 余热锅炉

#### 设备信息

|    | classname          | name     |   type | thutype   |   ver |   id | sym                   |
|---:|:-------------------|:---------|-------:|:----------|------:|-----:|:----------------------|
|  0 | HeatRecoveryBoiler | 余热锅炉 |  11000 | heat      |    24 |    0 | NewHeatRecoveryBoiler |

#### 针脚定义

|    |   node | label   | cond                            |   conntype |
|---:|-------:|:--------|:--------------------------------|-----------:|
|  0 |     -1 |         | true                            |         43 |
|  1 |     -1 |         | true                            |         43 |
|  2 |     -1 |         | BoilerType==0                   |         42 |
|  3 |     -1 |         | BoilerType==1&&PressureLevel==0 |         41 |
|  4 |     -1 |         | BoilerType==1&&PressureLevel==1 |         41 |
|  5 |     -1 |         | BoilerType==1&&PressureLevel==1 |         41 |

#### 参数填写

##### DeviceParameters

| ID                | type    | value        | desc             | choices                                                      | cond               |   min | inputType   | unit   |    max |
|:------------------|:--------|:-------------|:-----------------|:-------------------------------------------------------------|:-------------------|------:|:------------|:-------|-------:|
| CompName          | text    | 余热蒸汽锅炉 | 元件名称         | nan                                                          | nan                |   nan | nan         | nan    |    nan |
| BoilerType        | choice  | 0            | 锅炉类型         | {'0': '热水锅炉', '1': '蒸汽锅炉'}                           | nan                |   nan | nan         | nan    |    nan |
| PressureLevel     | choice  | 0            | 压力等级         | {'0': '单压', '1': '双压'}                                   | BoilerType==1      |   nan | nan         | nan    |    nan |
| DeviceSelection   | choice  | 0            | 设备选型         | {'0': '设备类型待选', '1': '郑锅股份/QC110/625-22-3.82/450'} | nan                |   nan | nan         | nan    |    nan |
| DeviceNumber      | integer | 1            | 设备台数         | nan                                                          | DeviceSelection!=0 |     1 | constant    | nan    |    nan |
| MiniHeatSupply    | real    | 0.0          | 最小制热功率     | nan                                                          | DeviceSelection==0 |     0 | constant    | kW     | 999999 |
| MaxHeatSupply     | real    | 1000.0       | 最大制热功率     | nan                                                          | DeviceSelection==0 |     0 | constant    | kW     | 999999 |
| HeatingPriceModel | choice  | 0            | 供热过网计价模型 | {'0': '无', '1': '燃气电站供热价格'}                         | nan                |   nan | nan         | nan    |    nan |

##### OperationParameters

| ID                           | type   | unit   |   min |   max |   value | inputType   | desc                 | cond                            | choices                |
|:-----------------------------|:-------|:-------|------:|------:|--------:|:------------|:---------------------|:--------------------------------|:-----------------------|
| WaterSupplyTemp              | real   | ℃      |     0 |   200 |    80   | constant    | 供水温度             | BoilerType==0                   | nan                    |
| SteamSupplyTemp              | real   | ℃      |     0 |   500 |   180   | constant    | 蒸汽温度             | BoilerType==1&&PressureLevel==0 | nan                    |
| SubSteamSupplyTemp           | real   | ℃      |     0 |   500 |   150   | constant    | 次高压蒸汽温度       | BoilerType==1&&PressureLevel==1 | nan                    |
| HighSteamSupplyTemp          | real   | ℃      |     0 |   500 |   200   | constant    | 高压蒸汽温度         | BoilerType==1&&PressureLevel==1 | nan                    |
| IsExhaustOutletTempSpecified | choice | nan    |   nan |   nan |     0   | nan         | 烟气出口温度是否指定 | nan                             | {'0': '否', '1': '是'} |
| ExhaustOutletTemp            | real   | ℃      |   nan |   nan |   300   | constant    | 烟气出口温度         | IsExhaustOutletTempSpecified==1 | nan                    |
| IsExhaustPressureSepecified  | choice | nan    |   nan |   nan |     0   | nan         | 烟气进口压力是否指定 | nan                             | {'0': '否', '1': '是'} |
| InletExhaustPressure         | real   | MPa    |     0 |    99 |     0.5 | constant    | 烟气进口压力         | IsExhaustPressureSepecified==1  | nan                    |


### 换热器

#### 设备信息

|    | classname     | name   |   type | thutype   |   ver |   id | sym              |
|---:|:--------------|:-------|-------:|:----------|------:|-----:|:-----------------|
|  0 | HeatExchanger | 换热器 |  16000 | heat      |    14 |    0 | NewHeatExchanger |

#### 针脚定义

|    |   node | label   | cond             |   conntype |
|---:|-------:|:--------|:-----------------|-----------:|
|  0 |     -1 |         | HeatFliudType==0 |         43 |
|  1 |     -1 |         | HeatFliudType==0 |         43 |
|  2 |     -1 |         | HeatFliudType==1 |         42 |
|  3 |     -1 |         | true             |         42 |

#### 参数填写

##### DeviceParameters

| ID                  | type    | value   | desc             | choices                                      | inputType   | cond               | unit   |
|:--------------------|:--------|:--------|:-----------------|:---------------------------------------------|:------------|:-------------------|:-------|
| CompName            | text    | 换热器  | 元件名称         | nan                                          | nan         | nan                | nan    |
| HeatFliudType       | choice  | 0       | 热流体类型       | {'0': '烟气', '1': '热水'}                   | nan         | nan                | nan    |
| DeviceSelection     | choice  | 0       | 设备选型         | {'0': '设备类型待选', '1': '无锡科技/BR1.0'} | nan         | nan                | nan    |
| DeviceNumber        | integer | 1       | 设备台数         | nan                                          | constant    | DeviceSelection!=0 | nan    |
| MiniHeatExchange    | real    | 0.0     | 最小换热量       | nan                                          | constant    | DeviceSelection==0 | kW     |
| MaxHeatExchange     | real    | 1000.0  | 最大换热量       | nan                                          | constant    | DeviceSelection==0 | kW     |
| HeatFluidPriceModel | choice  | 0       | 用热计价模型     | {'0': '无', '1': '燃气电站供热价格'}         | nan         | nan                | nan    |
| ColdFluidPriceModel | choice  | 0       | 供热过网计价模型 | {'0': '无'}                                  | nan         | nan                | nan    |

##### OperationParameters

| ID                              | type   | unit   |   min |   max |   value | inputType   | desc                         | cond                                                 | choices                |
|:--------------------------------|:-------|:-------|------:|------:|--------:|:------------|:-----------------------------|:-----------------------------------------------------|:-----------------------|
| HeatWaterOutletTemp             | real   | ℃      |     0 |   200 |      70 | constant    | 热流体(水)回水温度           | HeatFliudType==1                                     | nan                    |
| IsExhaustOutletTempSpecified    | choice | nan    |   nan |   nan |       0 | nan         | 热流体(烟气)出口温度是否指定 | HeatFliudType==0                                     | {'0': '否', '1': '是'} |
| ExhaustOutletTemp               | real   |        |   nan |   nan |     200 | constant    | 热流体(烟气)出口温度         | HeatFliudType==0&&IsExhaustOutletTempSpecified==1    | nan                    |
| IsExhaustInletPressureSpecified | choice | nan    |   nan |   nan |       0 | nan         | 热流体(烟气)进口压力是否指定 | HeatFliudType==0                                     | {'0': '否', '1': '是'} |
| ExhaustInletPressure            | real   | MPa    |     0 |    99 |       2 | constant    | 热流体(烟气)进口压力         | HeatFliudType==0&&IsExhaustInletPressureSpecified==1 | nan                    |
| ColdFluidOutletTemp             | real   | ℃      |     0 |   200 |      60 | constant    | 冷流体(水)出口温度           | nan                                                  | nan                    |


### 热泵

#### 设备信息

|    | classname   | name   |   type | thutype   |   ver |   id | sym         |
|---:|:------------|:-------|-------:|:----------|------:|-----:|:------------|
|  0 | HeatPump    | 热泵   |  11000 | heatelec  |    78 |    0 | NewHeatPump |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2 |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         42 |
|  2 |     -1 |         | !show_pin||show_pin==3 |         44 |

#### 参数填写

##### DeviceParameters

| ID                | type    | value   | desc             | choices                                                                                                                                                                                                                                                                                                            | inputType   | cond               | unit   |   min |    max |
|:------------------|:--------|:--------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|:-------------------|:-------|------:|-------:|
| CompName          | text    | 热泵    | 元件名称         | nan                                                                                                                                                                                                                                                                                                                | nan         | nan                | nan    |   nan |    nan |
| DeviceSelection   | choice  | 0       | 设备选型         | {'0': '设备类型待选', '1': '华誉能源/R22'}                                                                                                                                                                                                                                                                         | nan         | nan                | nan    |   nan |    nan |
| DeviceNumber      | integer | 1       | 设备台数         | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection!=0 | nan    |   nan |    nan |
| MiniHeatSupply    | real    | 0.0     | 最小制热功率     | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kW     |     0 | 999999 |
| MaxHeatSupply     | real    | 1000.0  | 最大制热功率     | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kW     |     0 | 999999 |
| MiniCoolSupply    | real    | 0.0     | 最小制冷功率     | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kW     |     0 | 999999 |
| MaxCoolSupply     | real    | 1000.0  | 最大制冷功率     | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kW     |     0 | 999999 |
| PowerPriceModel   | choice  | 0       | 用电计价模型     | {'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'} | nan         | nan                | nan    |   nan |    nan |
| HeatingPriceModel | choice  | 0       | 供热过网计价模型 | {'0': '无'}                                                                                                                                                                                                                                                                                                        | nan         | nan                | nan    |   nan |    nan |
| CoolingPriceModel | choice  | 0       | 供冷过网计价模型 | {'0': '无'}                                                                                                                                                                                                                                                                                                        | nan         | nan                | nan    |   nan |    nan |

##### OperationParameters

| ID                | type   | unit   |   min |   max |   value | inputType   | desc         |
|:------------------|:-------|:-------|------:|------:|--------:|:------------|:-------------|
| HeatingSupplyTemp | real   | ℃      |     0 |   200 |      50 | constant    | 热水出口温度 |
| CoolingSupplyTemp | real   | ℃      |   -10 |    50 |       5 | constant    | 冷水出口温度 |

##### ComputingParameters

| ID              | type   |   value | choices                | desc                       |
|:----------------|:-------|--------:|:-----------------------|:---------------------------|
| IsHeatSlackNode | choice |       0 | {'0': '否', '1': '是'} | 供热时是否作为系统参考节点 |
| IsCoolSlackNode | choice |       0 | {'0': '否', '1': '是'} | 供冷时是否作为系统参考节点 |


### 蓄热电锅炉

#### 设备信息

|    | classname                   | name       |   type | thutype   |   ver |   id | sym                           |
|---:|:----------------------------|:-----------|-------:|:----------|------:|-----:|:------------------------------|
|  0 | HeatStorageElectricalBoiler | 蓄热电锅炉 |  14000 | heatelec  |    13 |    0 | NewHeatStorageElectricalBoile |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2 |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         42 |

#### 参数填写

##### DeviceParameters

| ID                | type    | value      | desc             | choices                                                                                                                                                                                                                                                                                                            | inputType   | cond               | unit   |
|:------------------|:--------|:-----------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|:-------------------|:-------|
| CompName          | text    | 蓄热电锅炉 | 元件名称         | nan                                                                                                                                                                                                                                                                                                                | nan         | nan                | nan    |
| DeviceSelection   | choice  | 0          | 设备选型         | {'0': '设备类型待选'}                                                                                                                                                                                                                                                                                              | nan         | nan                | nan    |
| DeviceNumber      | integer | 1          | 设备台数         | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection!=0 | nan    |
| MiniHeatStorage   | real    | 0.0        | 最小蓄热量       | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kWh    |
| MaxHeatStorage    | real    | 1000.0     | 最大蓄热量       | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kWh    |
| PowerPriceModel   | choice  | 0          | 用电计价模型     | {'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'} | nan         | nan                | nan    |
| HeatingPriceModel | choice  | 0          | 供热过网计价模型 | {'0': '无'}                                                                                                                                                                                                                                                                                                        | nan         | nan                | nan    |

##### OperationParameters

| ID         | type   | unit   |   min |   max |   value | inputType   | desc     |
|:-----------|:-------|:-------|------:|------:|--------:|:------------|:---------|
| SupplyTemp | real   | ℃      |     0 |   200 |      60 | constant    | 供水温度 |


### 热管式太阳能集热器

#### 设备信息

|    | classname        | name               |   type | thutype   |   ver |   id | sym                 |
|---:|:-----------------|:-------------------|-------:|:----------|------:|-----:|:--------------------|
|  0 | HPSolarCollector | 热管式太阳能集热器 |  11000 | heat      |    31 |    0 | NewHPSolarCollector |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |         42 |

#### 参数填写

##### DeviceParameters

| ID                | type   | value              | desc             | choices                                     | unit   | inputType   | cond               |
|:------------------|:-------|:-------------------|:-----------------|:--------------------------------------------|:-------|:------------|:-------------------|
| CompName          | text   | 热管式太阳能集热器 | 元件名称         | nan                                         | nan    | nan         | nan                |
| DeviceSelection   | choice | 0                  | 设备选型         | {'0': '设备类型待选', '1': 'VITOSOL/222-T'} | nan    | nan         | nan                |
| DeviceNumber      | real   | 1.0                | 安装台数         | nan                                         |        | constant    | DeviceSelection!=0 |
| MiniInstallArea   | real   | 0.0                | 最小安装面积     | nan                                         | m2     | constant    | DeviceSelection==0 |
| MaxInstallArea    | real   | 10000.0            | 最大安装面积     | nan                                         |        | constant    | DeviceSelection==0 |
| HeatingPriceModel | choice | 0                  | 供热过网计价模型 | {'0': '无'}                                 | nan    | nan         | nan                |

##### OperationParameters

| ID         | type   | unit   |   min |   max |   value | inputType   | desc     |
|:-----------|:-------|:-------|------:|------:|--------:|:------------|:---------|
| SupplyTemp | real   | ℃      |     0 |   200 |      60 | constant    | 供水温度 |


### 蓄冰空调

#### 设备信息

|    | classname    | name     |   type | thutype   |   ver |   id | sym             |
|---:|:-------------|:---------|-------:|:----------|------:|-----:|:----------------|
|  0 | IceStorageAC | 蓄冰空调 |  14000 | heatelec  |    68 |    0 | NewIceStorageAC |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2 |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         44 |

#### 参数填写

##### DeviceParameters

| ID                | type    | value    | desc             | choices                                                                                                                                                                                                                                                                                                            | inputType   | cond               | unit   |   min |    max |
|:------------------|:--------|:---------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|:-------------------|:-------|------:|-------:|
| CompName          | text    | 蓄冰空调 | 元件名称         | nan                                                                                                                                                                                                                                                                                                                | nan         | nan                | nan    |   nan |    nan |
| DeviceSelection   | choice  | 0        | 设备选型         | {'0': '设备类型待选', '1': '光华创世/GC-ICU-587-P'}                                                                                                                                                                                                                                                                | nan         | nan                | nan    |   nan |    nan |
| DeviceNumber      | integer | 1        | 设备台数         | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection!=0 | nan    |   nan |    nan |
| MiniCoolStorage   | real    | 0.0      | 最小蓄冷量       | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kWh    |     0 | 999999 |
| MaxCoolStorage    | real    | 1000.0   | 最大蓄冷量       | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kWh    |     0 | 999999 |
| PowerPriceModel   | choice  | 0        | 用电计价模型     | {'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'} | nan         | nan                | nan    |   nan |    nan |
| CoolingPriceModel | choice  | 0        | 供冷过网计价模型 | {'0': '无'}                                                                                                                                                                                                                                                                                                        | nan         | nan                | nan    |   nan |    nan |

##### OperationParameters

| ID         | type   | unit   |   min |   max |   value | inputType   | desc     |
|:-----------|:-------|:-------|------:|------:|--------:|:------------|:---------|
| SupplyTemp | real   | ℃      |   -20 |    50 |      15 | constant    | 供水温度 |


### 负荷

#### 设备信息

|    | classname   | name   |   type | thutype   |   ver |   id | sym     |
|---:|:------------|:-------|-------:|:----------|------:|-----:|:--------|
|  0 | Load        | 负荷   |  17000 | heatelec  |    62 |    0 | NewLoad |

#### 针脚定义

|    |   node | label   | cond                                          |   dimx |   dimy |   conntype |
|---:|-------:|:--------|:----------------------------------------------|-------:|-------:|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(ElectircalLoad!=0) |      1 |      1 |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==3)&&(HeatingLoad!=0)    |    nan |    nan |         42 |
|  2 |     -1 |         | (!show_pin||show_pin==3)&&(CoolingLoad!=0)    |    nan |    nan |         44 |
|  3 |     -1 |         | (!show_pin||show_pin==3)&&(SteamLoad!=0)      |    nan |    nan |         41 |

#### 参数填写

##### LoadSettings

| ID                | type   | value   | desc         | choices                                                                                                                                                                                                                                                                                                            | cond              |
|:------------------|:-------|:--------|:-------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------|
| CompName          | text   | 负荷    | 负荷名称     | nan                                                                                                                                                                                                                                                                                                                | nan               |
| ElectircalLoad    | choice | 0       | 电负荷       | {'0': '无', '1': '居住片区电负荷', '2': '滨湖核心服务区电负荷', '3': '食品生产工业片区电负荷', '4': '工业研发片区电负荷', '5': '装备制造工业片区电负荷'}                                                                                                                                                           | nan               |
| PowerPriceModel   | choice | 0       | 用电计价模型 | {'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'} | ElectircalLoad!=0 |
| HeatingLoad       | choice | 0       | 采暖负荷     | {'0': '无', '1': '沪苏产业联动集聚区管委会负荷', '2': '能源站内负荷'}                                                                                                                                                                                                                                              | nan               |
| HeatPriceModel    | choice | 0       | 采暖计价模型 | {'0': '无'}                                                                                                                                                                                                                                                                                                        | HeatingLoad!=0    |
| CoolingLoad       | choice | 0       | 制冷负荷     | {'0': '无'}                                                                                                                                                                                                                                                                                                        | nan               |
| CoolingPriceModel | choice | 0       | 制冷计价模型 | {'0': '无'}                                                                                                                                                                                                                                                                                                        | CoolingLoad!=0    |
| SteamLoad         | choice | 0       | 蒸汽制热负荷 | {'0': '无', '1': '江苏人酒业', '2': '明珠重工', '3': '紫菜精深加工', '4': '思凯林家居', '5': '奥为节能科技', '6': '翔牛食品', '7': '电巴新能源', '8': '海丰米业', '9': '人民医院', '10': '世贸天阶制药', '11': '维德木业', '12': '久王（铵盐）', '13': '英伦倍健'}                                                 | nan               |
| SteamPriceModel   | choice | 0       | 蒸气计价模型 | {'0': '无', '1': '燃气电站供热价格'}                                                                                                                                                                                                                                                                               | SteamLoad!=0      |

##### OperationParameters

| ID                  | type   | unit   |   min |   max |   value | inputType   | desc         | cond           |
|:--------------------|:-------|:-------|------:|------:|--------:|:------------|:-------------|:---------------|
| ReturnHeatWaterTemp | real   | ℃      |     0 |   200 |      40 | constant    | 热水回水温度 | HeatingLoad!=0 |
| ReturnColdWaterTemp | real   | ℃      |   -10 |    50 |      15 | constant    | 冷水回水温度 | CoolingLoad!=0 |


### 光伏系统

#### 设备信息

|    | classname       | name     |   type | thutype    |   ver |   id | sym             |
|---:|:----------------|:---------|-------:|:-----------|------:|-----:|:----------------|
|  0 | PhotovoltaicSys | 光伏系统 |  10000 | electrical |    21 |    0 | PhotovoltaicSys |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |          1 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value    | desc             | choices                                                                                                                                                                                                                                                                                                            | unit   |   min |        max | inputType   | cond               |
|:----------------|:-------|:---------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------|------:|-----------:|:------------|:-------------------|
| CompName        | text   | 光伏系统 | 元件名称         | nan                                                                                                                                                                                                                                                                                                                | nan    |   nan |    nan     | nan         | nan                |
| DeviceSelection | choice | 0        | 设备选型         | {'0': '设备类型待选'}                                                                                                                                                                                                                                                                                              | nan    |   nan |    nan     | nan         | nan                |
| DeviceNumber    | real   | 100.0    | 安装台数         | nan                                                                                                                                                                                                                                                                                                                | m2     |     0 | 999999     | constant    | DeviceSelection!=0 |
| MiniInstallArea | real   | 0.0      | 最小安装面积     | nan                                                                                                                                                                                                                                                                                                                | m2     |     0 | 999999     | constant    | DeviceSelection==0 |
| MaxInstallArea  | real   | 1000.0   | 最大安装面积     | nan                                                                                                                                                                                                                                                                                                                | m2     |     0 |      1e+08 | constant    | DeviceSelection==0 |
| PowerPriceModel | choice | 0        | 发电上网计价模型 | {'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'} | nan    |   nan |    nan     | nan         | nan                |


### 管道

#### 设备信息

|    | classname   | name   |   type | thutype   |   ver |   id | sym     |
|---:|:------------|:-------|-------:|:----------|------:|-----:|:--------|
|  0 | Pipe        | 管道   |  16000 | heat      |     8 |    0 | NewPipe |

#### 针脚定义

|    |   node | label   | cond         |   conntype |
|---:|-------:|:--------|:-------------|-----------:|
|  0 |     -1 |         | MediaType==0 |         42 |
|  1 |     -1 |         | MediaType==0 |         42 |
|  2 |     -1 |         | MediaType==1 |         44 |
|  3 |     -1 |         | MediaType==1 |         44 |
|  4 |     -1 |         | MediaType==2 |         41 |
|  5 |     -1 |         | MediaType==2 |         41 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value   | desc         | unit   |   min |    max | inputType   | choices                                 |
|:----------------|:-------|:--------|:-------------|:-------|------:|-------:|:------------|:----------------------------------------|
| CompName        | text   | 管道    | 元件名称     | nan    |   nan |    nan | nan         | nan                                     |
| Length          | real   | 200.0   | 管道长度     | m      |     0 | 999999 | constant    | nan                                     |
| MediaType       | choice | 0       | 流通介质类型 | nan    |   nan |    nan | nan         | {'0': '热水', '1': '冷水', '2': '蒸汽'} |
| DeviceSelection | choice | 0       | 设备选型     | nan    |   nan |    nan | nan         | {}                                      |


### 离心泵

#### 设备信息

|    | classname   | name   |   type | thutype   |   ver |   id | sym     |
|---:|:------------|:-------|-------:|:----------|------:|-----:|:--------|
|  0 | Pump        | 离心泵 |  16000 | heatelec  |    40 |    0 | NewPump |

#### 针脚定义

|    |   node | label   | cond                                     | desc   | dimx   | dimy   |   conntype |
|---:|-------:|:--------|:-----------------------------------------|:-------|:-------|:-------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2                   |        |        |        |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==3)&&(MediaType==0) | 泵入口 | 1      | 1      |         42 |
|  2 |     -1 |         | (!show_pin||show_pin==3)&&(MediaType==0) | 泵出口 | 1      | 1      |         42 |
|  3 |     -1 |         | (!show_pin||show_pin==3)&&(MediaType==1) | nan    | nan    | nan    |         44 |
|  4 |     -1 |         | (!show_pin||show_pin==3)&&(MediaType==1) | nan    | nan    | nan    |         44 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value   | desc     | choices                    |
|:----------------|:-------|:--------|:---------|:---------------------------|
| CompName        | text   | 离心泵  | 元件名称 | nan                        |
| DeviceSelection | choice | 0       | 设备选型 | {}                         |
| MediaType       | choice | 0       | 介质类型 | {'0': '热水', '1': '冷水'} |


### 传输线

#### 设备信息

|    | classname    | name   |   type | thutype    |   ver |   id | sym          |
|---:|:-------------|:-------|-------:|:-----------|------:|-----:|:-------------|
|  0 | TransferLine | 传输线 |  15000 | electrical |    18 |    0 | TransferLine |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |          1 |
|  1 |     -1 |         | true   |          1 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value   | desc       | unit   |   min |   max | inputType   | choices   |
|:----------------|:-------|:--------|:-----------|:-------|------:|------:|:------------|:----------|
| CompName        | text   | 传输线  | 元件名称   | nan    |   nan |   nan | nan         | nan       |
| Length          | real   | 1.0     | 传输线长度 | km     |     0 |  9999 | constant    | nan       |
| DeviceSelection | choice | 0       | 设备选型   | nan    |   nan |   nan | nan         | {}        |


### 变压器

#### 设备信息

|    | classname   | name   |   type | thutype    |   ver |   id | sym         |
|---:|:------------|:-------|-------:|:-----------|------:|-----:|:------------|
|  0 | Transformer | 变压器 |  15000 | electrical |    13 |    0 | Transformer |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |          1 |
|  1 |     -1 |         | true   |          1 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value   | desc     | choices   |
|:----------------|:-------|:--------|:---------|:----------|
| CompName        | text   | 变压器  | 元件名称 | nan       |
| DeviceSelection | choice | 0       | 设备选型 | {}        |


### 风机

#### 设备信息

|    | classname          | name   |   type | thutype    |   ver |   id | sym                |
|---:|:-------------------|:-------|-------:|:-----------|------:|-----:|:-------------------|
|  0 | WindPowerGenerator | 风机   |  10000 | electrical |    19 |    0 | WindPowerGenerator |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |          1 |

#### 参数填写

##### DeviceParameters

| ID               | type    | value   | desc             | choices                                                                                                                                                                                                                                                                                                            |   min | inputType   | cond               |   unit |    max |
|:-----------------|:--------|:--------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------:|:------------|:-------------------|-------:|-------:|
| CompName         | text    | 风机    | 元件名称         | nan                                                                                                                                                                                                                                                                                                                |   nan | nan         | nan                |    nan |    nan |
| DeviceSelection  | choice  | 0       | 设备选型         | {'0': '设备类型待选'}                                                                                                                                                                                                                                                                                              |   nan | nan         | nan                |    nan |    nan |
| DeviceNumber     | integer | 1       | 设备台数         | nan                                                                                                                                                                                                                                                                                                                |     0 | constant    | DeviceSelection!=0 |    nan |    nan |
| MiniDeviceNumber | real    | 0.0     | 最小风机台数     | nan                                                                                                                                                                                                                                                                                                                |     0 | constant    | DeviceSelection==0 |    nan |   9999 |
| MaxDeviceNumber  | integer | 20      | 最大风机台数     | nan                                                                                                                                                                                                                                                                                                                |     0 | constant    | DeviceSelection==0 |    nan | 999999 |
| PowerPriceModel  | choice  | 0       | 发电过网计价模型 | {'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'} |   nan | nan         | nan                |    nan |    nan |


### 蒸汽轮机

#### 设备信息

|    | classname    | name     |   type | thutype   |   ver |   id | sym             |
|---:|:-------------|:---------|-------:|:----------|------:|-----:|:----------------|
|  0 | SteamTurbine | 蒸汽轮机 |  10000 | heatelec  |    22 |    0 | NewSteamTurbine |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2 |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         41 |

#### 参数填写

##### DeviceParameters

| ID                 | type    | value    | desc             | choices                                                                                                                                                                                                                                                                                                            | inputType   | cond               | unit   |   min |    max |
|:-------------------|:--------|:---------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|:-------------------|:-------|------:|-------:|
| CompName           | text    | 蒸汽轮机 | 元件名称         | nan                                                                                                                                                                                                                                                                                                                | nan         | nan                | nan    |   nan |    nan |
| DeviceSelection    | choice  | 0        | 设备选型         | {'0': '设备类型待选', '1': '青能动力/QFW-8-4'}                                                                                                                                                                                                                                                                     | nan         | nan                | nan    |   nan |    nan |
| DeviceNumber       | integer | 1        | 设备台数         | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection!=0 | nan    |   nan |    nan |
| MiniPowerGenerate  | real    | 0.0      | 最小发电功率     | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kW     |     0 | 999999 |
| MaxPowerGenerate   | real    | 10000.0  | 最大发电功率     | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kW     |     0 | 999999 |
| PowerPriceModel    | choice  | 0        | 发电过网计价模型 | {'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'} | nan         | nan                | nan    |   nan |    nan |
| SteamUsePriceModel | choice  | 0        | 蒸汽用热计价模型 | {'0': '无', '1': '燃气电站供热价格'}                                                                                                                                                                                                                                                                               | nan         | nan                | nan    |   nan |    nan |

##### OperationParameters

| ID            | type   | unit   |   min |   max |   value | inputType   | desc     |
|:--------------|:-------|:-------|------:|------:|--------:|:------------|:---------|
| SteamPressure | real   | MPa    |     0 |    99 |       2 | constant    | 蒸汽压力 |

##### ComputingParameters

| ID          | type   |   value | choices                | desc                 |
|:------------|:-------|--------:|:-----------------------|:---------------------|
| IsSlackNode | choice |       0 | {'0': '否', '1': '是'} | 是否作为系统参考节点 |


### 燃气轮机

#### 设备信息

|    | classname   | name     |   type | thutype   |   ver |   id | sym        |
|---:|:------------|:---------|-------:|:----------|------:|-----:|:-----------|
|  0 | GasTurbine  | 燃气轮机 |  10000 | heatelec  |    24 |    0 | GasTurbine |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2 |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         43 |

#### 参数填写

##### DeviceParameters

| ID                | type    | value    | desc             | choices                                                                                                                                                                                                                                                                                                            | inputType   | cond               | unit   |
|:------------------|:--------|:---------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|:-------------------|:-------|
| CompName          | text    | 燃气轮机 | 元件名称         | nan                                                                                                                                                                                                                                                                                                                | nan         | nan                | nan    |
| DeviceSelection   | choice  | 0        | 设备选型         | {'0': '设备类型待选', '1': '西门子/SGT-800', '2': '东汽日立/H-25(42)', '3': '南汽/PG6581B', '4': '南汽/GT-6F.01', '5': '华电/LM6000PF', '6': '普惠/FT8'}                                                                                                                                                           | nan         | nan                | nan    |
| DeviceNumber      | integer | 1        | 设备台数         | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection!=0 | nan    |
| MiniPowerGenerate | real    | 0.0      | 最小发电功率     | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kW     |
| MaxPowerGenerate  | real    | 100000.0 | 最大发电功率     | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kW     |
| FuelPriceModel    | choice  | 0        | 燃料计价模型     | {'0': '无', '1': '天然气-居民'}                                                                                                                                                                                                                                                                                    | nan         | nan                | nan    |
| PowerPriceModel   | choice  | 0        | 发电过网计价模型 | {'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'} | nan         | nan                | nan    |

##### OperationParameters

| ID          | type   | unit   |   min |   max |   value | inputType   | desc     |
|:------------|:-------|:-------|------:|------:|--------:|:------------|:---------|
| ExhaustTemp | real   | ℃      |     0 |  1000 |     500 | constant    | 烟气温度 |

##### ComputingParameters

| ID            | type   |   value | choices                                                                 | desc         |
|:--------------|:-------|--------:|:------------------------------------------------------------------------|:-------------|
| SlackNodeMode | choice |       0 | {'0': '不是参考节点', '1': '电力系统参考节点', '2': '热力系统参考节点'} | 参考节点模式 |


### 燃气内燃机

#### 设备信息

|    | classname   | name       |   type | thutype   |   ver |   id | sym          |
|---:|:------------|:-----------|-------:|:----------|------:|-----:|:-------------|
|  0 | GasEngine   | 燃气内燃机 |  10000 | heatelec  |    15 |    0 | NewGasEngine |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2 |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         42 |
|  2 |     -1 |         | !show_pin||show_pin==3 |         43 |

#### 参数填写

##### DeviceParameters

| ID                | type    | value      | desc             | choices                                                                                                                                                                                                                                                                                                            | inputType   | cond               | unit   |   min |    max |
|:------------------|:--------|:-----------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|:-------------------|:-------|------:|-------:|
| CompName          | text    | 燃气内燃机 | 元件名称         | nan                                                                                                                                                                                                                                                                                                                | nan         | nan                | nan    |   nan |    nan |
| DeviceSelection   | choice  | 0          | 设备选型         | {'0': '设备类型待选', '1': '杰瑞/J612'}                                                                                                                                                                                                                                                                            | nan         | nan                | nan    |   nan |    nan |
| DeviceNumber      | integer | 1          | 设备台数         | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection!=0 | nan    |   nan |    nan |
| MiniPowerGenerate | real    | 0.0        | 最小发电量       | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kW     |     0 | 999999 |
| MaxPowerGenerate  | real    | 1000.0     | 最大发电量       | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection==0 | kW     |     0 | 999999 |
| FuelPriceModel    | choice  | 0          | 燃料计价模型     | {'0': '无', '1': '天然气-居民'}                                                                                                                                                                                                                                                                                    | nan         | nan                | nan    |   nan |    nan |
| PowerPriceModel   | choice  | 0          | 发电过网计价模型 | {'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'} | nan         | nan                | nan    |   nan |    nan |
| HeatingPriceModel | choice  | 0          | 供热过网计价模型 | {'0': '无'}                                                                                                                                                                                                                                                                                                        | nan         | nan                | nan    |   nan |    nan |

##### OperationParameters

| ID                 | type   | unit   |   min |   max |   value | inputType   | desc     |
|:-------------------|:-------|:-------|------:|------:|--------:|:------------|:---------|
| WaterSupplyTemp    | real   | ℃      |     0 |   200 |      80 | constant    | 供水温度 |
| ExhaustTemperature | real   | ℃      |     0 |  1000 |     300 | constant    | 烟气温度 |

##### ComputingParameters

| ID            | type   |   value | choices                                                                 | desc         |
|:--------------|:-------|--------:|:------------------------------------------------------------------------|:-------------|
| SlackNodeMode | choice |       0 | {'0': '不是参考节点', '1': '电力系统参考节点', '2': '热力系统参考节点'} | 参考节点模式 |


### 外部电源

#### 设备信息

|    | classname           | name     |   type | thutype    |   ver |   id | sym                 |
|---:|:--------------------|:---------|-------:|:-----------|------:|-----:|:--------------------|
|  0 | ExternalPowerSource | 外部电源 |  10000 | electrical |    27 |    0 | ExternalPowerSource |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |          1 |

#### 参数填写

##### DeviceParameters

| ID                     | type   | value              | desc             | choices     |
|:-----------------------|:-------|:-------------------|:-----------------|:------------|
| CompName               | text   | 外部电源(参考节点) | 元件名称         | nan         |
| PowerConsumePriceModel | choice | 0                  | 上网计价模型     | {'0': '无'} |
| PowerSupplyPriceModel  | choice | 0                  | 供电计价模型     | {'0': '无'} |
| FuelModel              | choice | 0                  | 电厂发电燃料模型 | {'0': '无'} |

##### OperationParameters

| ID      | type   | unit   |   min |   value | inputType   | desc     |
|:--------|:-------|:-------|------:|--------:|:------------|:---------|
| BasekV  | real   | kV     |     0 |     115 | constant    | 基准电压 |
| Voltage | real   | pu     |   nan |       1 | constant    | 电压     |
| Angle   | real   | deg    |   nan |       0 | constant    | 相角     |



## 规划设计参数

| 参数分类              | 中文名称                       | 有关设备                                                                                                                                                                                                                                                                   |
|:----------------------|:-------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BasicParameters       | 基础参数, 机组参数, 母线参数   | 母线, 储水罐, 模块化多电平变流器, 光伏系统, 风机, 交流变压器, 离心泵, 传输线, 电压缩制冷机, 采暖制冷负荷, 电负荷, 燃气锅炉, 热泵, 燃气轮机, 蓄电池, 吸收式制冷机, 柔性电负荷, 建筑物冷热负荷围护模型, 直流变压器, 外部电源, 热管式太阳能集热器, 储气罐, 压气机, 透平发电机 |
| DeviceParameters      | 机组参数, 设备参数             | 燃气内燃机, 换热器, 尾气排放装置, 离心泵, 蒸汽轮机, 电容器, 蓄冰空调, 蓄热电锅炉, 余热锅炉, 管道                                                                                                                                                                           |
| OperationParameters   | 运行约束, 运行参数组, 优化参数 | 燃气内燃机, 负荷, 换热器, 尾气排放装置, 蒸汽轮机, 蓄冰空调, 蓄热电锅炉, 余热锅炉, 储水罐, 光伏系统, 风机, 离心泵, 电压缩制冷机, 采暖制冷负荷, 燃气锅炉, 热泵, 燃气轮机, 蓄电池, 吸收式制冷机, 建筑物冷热负荷围护模型, 热管式太阳能集热器, 储气罐, 压气机, 透平发电机       |
| LoadSettings          | 充电桩设置, 负荷设置           | 负荷, 充电桩                                                                                                                                                                                                                                                               |
| SimuParameters        | 仿真参数                       | 储水罐, 模块化多电平变流器, 光伏系统, 风机, 电压缩制冷机, 燃气锅炉, 热泵, 燃气轮机, 蓄电池, 吸收式制冷机, 柔性电负荷, 建筑物冷热负荷围护模型, 外部电源, 热管式太阳能集热器, 储气罐, 压气机, 透平发电机                                                                     |
| SImuParameters        | 仿真参数                       | 离心泵                                                                                                                                                                                                                                                                     |
| OptimizationParamters | 优化参数                       | 柔性电负荷                                                                                                                                                                                                                                                                 |
| HouseParameters       | 建筑物围护参数                 | 建筑物冷热负荷围护模型                                                                                                                                                                                                                                                     |

### 机组参数
在没有选择具体设备时，不能指定设备台数，但可以指定设备额定运行参数。指定了设备类型时，可以指定设备台数，但是不能指定额定运行参数。
部分参数
### 运行参数组
不能指定部分参数，或者可选指定部分参数
### 计算参数组
有的设备没有计算参数组，例如吸收式制冷机，余热锅炉
### 负荷设置
负荷元件特有的设置

### 详细说明


### 母线

#### 设备信息

|    | classname   | name   |   type | thutype    |   ver |   id | sym     |
|---:|:------------|:-------|-------:|:-----------|------:|-----:|:--------|
|  0 | BusNode     | 母线   |  15001 | electrical |     4 |    0 | BusNode |

#### 针脚定义

|    |   node | label   | cond        |   conntype |
|---:|-------:|:--------|:------------|-----------:|
|  0 |     -1 |         | CompType==0 |          1 |
|  1 |     -1 |         | CompType==1 |         44 |

#### 参数填写

##### BasicParameters

| ID       | type   | value   | desc     | cond        | choices                            | choiceSource   | unit   | inputType   |
|:---------|:-------|:--------|:---------|:------------|:-----------------------------------|:---------------|:-------|:------------|
| Name     | text   |         | 母线名称 | true        | nan                                | nan            | nan    | nan         |
| CompType | choice | 0       | 元件类型 | nan         | {'0': '交流元件', '1': '直流元件'} |                | nan    | nan         |
| VBase    | real   | 115.0   | 基准电压 | true        | nan                                | nan            | kV     | constant    |
| V        | real   | 115.0   | 初始电压 | true        | nan                                | nan            | kV     | constant    |
| Angle    | real   | 0.0     | 初始相角 | CompType==0 | nan                                | nan            | deg    | constant    |


### 燃气内燃机

#### 设备信息

|    | classname   | name       |   type | thutype   |   ver |   id | sym       |
|---:|:------------|:-----------|-------:|:----------|------:|-----:|:----------|
|  0 | GasEngine   | 燃气内燃机 |  10000 | heatelec  |    29 |    0 | GasEngine |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2 |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         42 |
|  2 |     -1 |         | !show_pin||show_pin==3 |         43 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value      | desc     | choices                                 |
|:----------------|:-------|:-----------|:---------|:----------------------------------------|
| CompName        | text   | 燃气内燃机 | 元件名称 | nan                                     |
| DeviceSelection | choice | 0          | 设备选型 | {'0': '设备类型待选', '1': '杰瑞/J612'} |

##### OperationParameters

| ID                 | type   | unit   |   min |   max |   value | inputType   | desc         | choices                                        |
|:-------------------|:-------|:-------|------:|------:|--------:|:------------|:-------------|:-----------------------------------------------|
| WaterSupplyTemp    | real   | ℃      |     0 |   200 |      80 | constant    | 供水温度     | nan                                            |
| ExhaustTemperature | real   | ℃      |     0 |  1000 |     300 | constant    | 烟气温度     | nan                                            |
| SlackNodeMode      | choice | nan    |   nan |   nan |       0 | nan         | 参考节点模式 | {'0': '电力系统参考点', '1': '热力系统参考点'} |


### 负荷

#### 设备信息

|    | classname   | name   |   type | thutype   |   ver |   id | sym   |
|---:|:------------|:-------|-------:|:----------|------:|-----:|:------|
|  0 | Load        | 负荷   |  17000 | heatelec  |    70 |    0 | Load  |

#### 针脚定义

|    |   node | label   | cond                                          |   dimx |   dimy |   conntype |
|---:|-------:|:--------|:----------------------------------------------|-------:|-------:|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(ElectircalLoad!=0) |      1 |      1 |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==3)&&(HeatingLoad!=0)    |    nan |    nan |         42 |
|  2 |     -1 |         | (!show_pin||show_pin==3)&&(CoolingLoad!=0)    |    nan |    nan |         44 |
|  3 |     -1 |         | (!show_pin||show_pin==3)&&(SteamLoad!=0)      |    nan |    nan |         41 |

#### 参数填写

##### LoadSettings

| ID             | type   | value   | desc         | choices                                                                                                                                                                                                                                                            |
|:---------------|:-------|:--------|:-------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CompName       | text   | 负荷    | 负荷名称     | nan                                                                                                                                                                                                                                                                |
| ElectircalLoad | choice | 0       | 电负荷       | {'0': '无', '1': '居住片区电负荷', '2': '滨湖核心服务区电负荷', '3': '食品生产工业片区电负荷', '4': '工业研发片区电负荷', '5': '装备制造工业片区电负荷'}                                                                                                           |
| HeatingLoad    | choice | 0       | 采暖负荷     | {'0': '无', '1': '沪苏产业联动集聚区管委会负荷', '2': '能源站内负荷'}                                                                                                                                                                                              |
| CoolingLoad    | choice | 0       | 制冷负荷     | {'0': '无'}                                                                                                                                                                                                                                                        |
| SteamLoad      | choice | 0       | 蒸汽制热负荷 | {'0': '无', '1': '江苏人酒业', '2': '明珠重工', '3': '紫菜精深加工', '4': '思凯林家居', '5': '奥为节能科技', '6': '翔牛食品', '7': '电巴新能源', '8': '海丰米业', '9': '人民医院', '10': '世贸天阶制药', '11': '维德木业', '12': '久王（铵盐）', '13': '英伦倍健'} |

##### OperationParameters

| ID                  | type   | unit   |   min |   max |   value | inputType   | desc         | cond           |
|:--------------------|:-------|:-------|------:|------:|--------:|:------------|:-------------|:---------------|
| ReturnHeatWaterTemp | real   | ℃      |     0 |   200 |      40 | constant    | 热水回水温度 | HeatingLoad!=0 |
| ReturnColdWaterTemp | real   | ℃      |   -10 |    50 |      25 | constant    | 冷水回水温度 | CoolingLoad!=0 |


### 换热器

#### 设备信息

|    | classname     | name   |   type | thutype   |   ver |   id | sym           |
|---:|:--------------|:-------|-------:|:----------|------:|-----:|:--------------|
|  0 | HeatExchanger | 换热器 |  16000 | heat      |    24 |    0 | HeatExchanger |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |         42 |
|  1 |     -1 |         | true   |         42 |
|  2 |     -1 |         | true   |         43 |
|  3 |     -1 |         | true   |         43 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value   | desc       | choices                                      | choiceSource   |
|:----------------|:-------|:--------|:-----------|:---------------------------------------------|:---------------|
| CompName        | text   | 换热器  | 元件名称   | nan                                          | nan            |
| HeatFliudType   | choice | 0       | 热流体类型 | {'0': '烟气', '1': '热水'}                   |                |
| DeviceSelection | choice | 0       | 设备选型   | {'0': '设备类型待选', '1': '无锡科技/BR1.0'} |                |

##### OperationParameters

| ID                              | type   | unit   |   min |   max |   value | inputType   | desc                         | cond                                                 | choices                | choiceSource   |
|:--------------------------------|:-------|:-------|------:|------:|--------:|:------------|:-----------------------------|:-----------------------------------------------------|:-----------------------|:---------------|
| HeatWaterOutletTemp             | real   | ℃      |     0 |   200 |      70 | constant    | 热流体(水)回水温度           | HeatFliudType==1                                     | nan                    | nan            |
| IsExhaustOutletTempSpecified    | choice | nan    |   nan |   nan |       0 | nan         | 热流体(烟气)出口温度是否指定 | HeatFliudType==0                                     | {'0': '否', '1': '是'} |                |
| ExhaustOutletTemp               | real   |        |   nan |   nan |     200 | constant    | 热流体(烟气)出口温度         | HeatFliudType==0&&IsExhaustOutletTempSpecified==1    | nan                    | nan            |
| IsExhaustInletPressureSpecified | choice | nan    |   nan |   nan |       0 | nan         | 热流体(烟气)进口压力是否指定 | HeatFliudType==0                                     | {'0': '否', '1': '是'} |                |
| ExhaustInletPressure            | real   | MPa    |     0 |    99 |       2 | constant    | 热流体(烟气)进口压力         | HeatFliudType==0&&IsExhaustInletPressureSpecified==1 | nan                    | nan            |
| ColdFluidOutletTemp             | real   | ℃      |     0 |   200 |      60 | constant    | 冷流体(水)出口温度           | nan                                                  | nan                    | nan            |


### 尾气排放装置

#### 设备信息

|    | classname      | name         |   type | thutype   |   ver |   id | sym            |
|---:|:---------------|:-------------|-------:|:----------|------:|-----:|:---------------|
|  0 | ExhaustTreater | 尾气排放装置 |  16000 | heat      |    13 |    0 | ExhaustTreater |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |         43 |

#### 参数填写

##### DeviceParameters

| ID       | type   | value        | desc     |
|:---------|:-------|:-------------|:---------|
| CompName | text   | 尾气排放装置 | 元件名称 |

##### OperationParameters

| ID                         | type   |   value | choices                | desc                 | unit   |   min |   max | inputType   | cond                          |
|:---------------------------|:-------|--------:|:-----------------------|:---------------------|:-------|------:|------:|:------------|:------------------------------|
| IsExhaustPressureSpecified | choice |       0 | {'0': '否', '1': '是'} | 进口烟气压力是否指定 | nan    |   nan |   nan | nan         | nan                           |
| ExhaustPressure            | real   |       2 | nan                    | 进口烟气压力         | MPa    |     0 |    99 | constant    | IsExhaustPressureSpecified==1 |


### 离心泵

#### 设备信息

|    | classname   | name   |   type | thutype   |   ver |   id | sym     |
|---:|:------------|:-------|-------:|:----------|------:|-----:|:--------|
|  0 | Pump        | 离心泵 |  16000 | heatelec  |    41 |    0 | NewPump |

#### 针脚定义

|    |   node | label   | cond                                     | desc   | dimx   | dimy   |   conntype |
|---:|-------:|:--------|:-----------------------------------------|:-------|:-------|:-------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2                   |        |        |        |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==3)&&(MediaType==0) | 泵入口 | 1      | 1      |         42 |
|  2 |     -1 |         | (!show_pin||show_pin==3)&&(MediaType==0) | 泵出口 | 1      | 1      |         42 |
|  3 |     -1 |         | (!show_pin||show_pin==3)&&(MediaType==1) | nan    | nan    | nan    |         44 |
|  4 |     -1 |         | (!show_pin||show_pin==3)&&(MediaType==1) | nan    | nan    | nan    |         44 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value   | desc     | choices                    |
|:----------------|:-------|:--------|:---------|:---------------------------|
| CompName        | text   | 离心泵  | 元件名称 | nan                        |
| DeviceSelection | choice | 0       | 设备选型 | {}                         |
| MediaType       | choice | 0       | 介质类型 | {'0': '热水', '1': '冷水'} |


### 蒸汽轮机

#### 设备信息

|    | classname    | name     |   type | thutype   |   ver |   id | sym             |
|---:|:-------------|:---------|-------:|:----------|------:|-----:|:----------------|
|  0 | SteamTurbine | 蒸汽轮机 |  10000 | heatelec  |    25 |    0 | NewSteamTurbine |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2 |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         41 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value    | desc     | choices                             |
|:----------------|:-------|:---------|:---------|:------------------------------------|
| CompName        | text   | 蒸汽轮机 | 元件名称 | nan                                 |
| DeviceSelection | choice | 0        | 设备选型 | {'0': '设备类型待选（作为参考点）'} |

##### OperationParameters

| ID                | type   | unit        |   min |   max | value   | inputType   | desc                   | choices                | coldef                   |   minrowcount |   maxrowcount | cond           |
|:------------------|:-------|:------------|------:|------:|:--------|:------------|:-----------------------|:-----------------------|:-------------------------|--------------:|--------------:|:---------------|
| SteamPressure     | real   | MPa         |     0 |    99 | 2.0     | constant    | 蒸汽压力               | nan                    | nan                      |           nan |           nan | nan            |
| IsSlackNode       | choice | nan         |   nan |   nan | 0       | nan         | 是否作为电力系统参考点 | {'0': '否', '1': '是'} | nan                      |           nan |           nan | nan            |
| OperationStrategy | table  | ['h', '台'] |   nan |   nan | []      | nan         | 机组运行策略           | nan                    | ['时间', '启动机组台数'] |             0 |          2016 | IsSlackNode==0 |


### 电容器

#### 设备信息

|    | classname   | name   |   type | thutype    |   ver |   id | sym         |
|---:|:------------|:-------|-------:|:-----------|------:|-----:|:------------|
|  0 | Capacitance | 电容器 |  15000 | electrical |     8 |    0 | Capacitance |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |          1 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value   | desc     | choices   |
|:----------------|:-------|:--------|:---------|:----------|
| CompName        | text   | 电容器  | 元件名称 | nan       |
| DeviceSelection | choice | 0       | 设备选型 | {}        |


### 蓄冰空调

#### 设备信息

|    | classname    | name     |   type | thutype   |   ver |   id | sym          |
|---:|:-------------|:---------|-------:|:----------|------:|-----:|:-------------|
|  0 | IceStorageAC | 蓄冰空调 |  14000 | heatelec  |    72 |    0 | IceStorageAC |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2 |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         44 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value    | desc     | choices   |
|:----------------|:-------|:---------|:---------|:----------|
| CompName        | text   | 蓄冰空调 | 元件名称 | nan       |
| DeviceSelection | choice | 0        | 设备选型 | {}        |

##### OperationParameters

| ID                | type   | unit        |   min |   max | value   | inputType   | desc         | coldef                               |   minrowcount |   maxrowcount |
|:------------------|:-------|:------------|------:|------:|:--------|:------------|:-------------|:-------------------------------------|--------------:|--------------:|
| SupplyTemp        | real   | ℃           |   -20 |    50 | 15.0    | constant    | 供水温度     | nan                                  |           nan |           nan |
| OperationStrategy | table  | ['h', '台'] |   nan |   nan | []      | nan         | 机组运行策略 | ['时间', '启动机组台数（正放负充）'] |             0 |          2016 |


### 蓄热电锅炉

#### 设备信息

|    | classname                   | name       |   type | thutype   |   ver |   id | sym                        |
|---:|:----------------------------|:-----------|-------:|:----------|------:|-----:|:---------------------------|
|  0 | HeatStorageElectricalBoiler | 蓄热电锅炉 |  14000 | heatelec  |    18 |    0 | HeatStorageElectricalBoile |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2 |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         42 |

#### 参数填写

##### DeviceParameters

| ID                | type    | value      | desc             | choices                                                                                                                                                                                                                                                                                                            | inputType   | cond               |
|:------------------|:--------|:-----------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|:-------------------|
| CompName          | text    | 蓄热电锅炉 | 元件名称         | nan                                                                                                                                                                                                                                                                                                                | nan         | nan                |
| DeviceSelection   | choice  | 0          | 设备选型         | {}                                                                                                                                                                                                                                                                                                                 | nan         | nan                |
| DeviceNumber      | integer | 1          | 设备台数         | nan                                                                                                                                                                                                                                                                                                                | constant    | DeviceSelection!=0 |
| PowerPriceModel   | choice  | 0          | 用电计价模型     | {'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'} | nan         | nan                |
| HeatingPriceModel | choice  | 0          | 供热过网计价模型 | {'0': '无'}                                                                                                                                                                                                                                                                                                        | nan         | nan                |

##### OperationParameters

| ID                | type   | unit        |   min |   max | value   | inputType   | desc         | coldef                               |   minrowcount |   maxrowcount |
|:------------------|:-------|:------------|------:|------:|:--------|:------------|:-------------|:-------------------------------------|--------------:|--------------:|
| SupplyTemp        | real   | ℃           |     0 |   200 | 60.0    | constant    | 供水温度     | nan                                  |           nan |           nan |
| OperationStrategy | table  | ['h', '台'] |   nan |   nan | []      | nan         | 机组运行策略 | ['时间', '启动机组台数（正放负充）'] |             0 |          2016 |


### 余热锅炉

#### 设备信息

|    | classname          | name     |   type | thutype   |   ver |   id | sym                |
|---:|:-------------------|:---------|-------:|:----------|------:|-----:|:-------------------|
|  0 | HeatRecoveryBoiler | 余热锅炉 |  11000 | heat      |    31 |    0 | HeatRecoveryBoiler |

#### 针脚定义

|    |   node | label   | cond                            |   conntype |
|---:|-------:|:--------|:--------------------------------|-----------:|
|  0 |     -1 |         | true                            |         43 |
|  1 |     -1 |         | true                            |         43 |
|  2 |     -1 |         | BoilerType==0                   |         42 |
|  3 |     -1 |         | BoilerType==1&&PressureLevel==0 |         41 |
|  4 |     -1 |         | BoilerType==1&&PressureLevel==1 |         41 |
|  5 |     -1 |         | BoilerType==1&&PressureLevel==1 |         41 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value    | desc     | choices                             | cond          |
|:----------------|:-------|:---------|:---------|:------------------------------------|:--------------|
| CompName        | text   | 余热锅炉 | 元件名称 | nan                                 | nan           |
| BoilerType      | choice | 0        | 锅炉类型 | {'0': '热水锅炉', '1': '蒸汽锅炉'}  | nan           |
| PressureLevel   | choice | 0        | 压力等级 | {'0': '单压', '1': '双压'}          | BoilerType==1 |
| DeviceSelection | choice | 0        | 设备选型 | {'0': '设备类型待选（作为参考点）'} | nan           |

##### OperationParameters

| ID                           | type   | unit   |   min |   max |   value | inputType   | desc                 | cond                            | choices                |
|:-----------------------------|:-------|:-------|------:|------:|--------:|:------------|:---------------------|:--------------------------------|:-----------------------|
| WaterSupplyTemp              | real   | ℃      |     0 |   200 |    80   | constant    | 供水温度             | BoilerType==0                   | nan                    |
| SteamSupplyTemp              | real   | ℃      |     0 |   500 |   180   | constant    | 蒸汽温度             | BoilerType==1&&PressureLevel==0 | nan                    |
| SubSteamSupplyTemp           | real   | ℃      |     0 |   500 |   150   | constant    | 次高压蒸汽温度       | BoilerType==1&&PressureLevel==1 | nan                    |
| HighSteamSupplyTemp          | real   | ℃      |     0 |   500 |   200   | constant    | 高压蒸汽温度         | BoilerType==1&&PressureLevel==1 | nan                    |
| IsExhaustOutletTempSpecified | choice | nan    |   nan |   nan |     0   | nan         | 烟气出口温度是否指定 | nan                             | {'0': '否', '1': '是'} |
| ExhaustOutletTemp            | real   | ℃      |   nan |   nan |   300   | constant    | 烟气出口温度         | IsExhaustOutletTempSpecified==1 | nan                    |
| IsExhaustPressureSepecified  | choice | nan    |   nan |   nan |     0   | nan         | 烟气进口压力是否指定 | nan                             | {'0': '否', '1': '是'} |
| InletExhaustPressure         | real   | MPa    |     0 |    99 |     0.5 | constant    | 烟气进口压力         | IsExhaustPressureSepecified==1  | nan                    |


### 充电桩

#### 设备信息

|    | classname    | name   |   type | thutype    |   ver |   id | sym          |
|---:|:-------------|:-------|-------:|:-----------|------:|-----:|:-------------|
|  0 | ChargingPile | 充电桩 |  17000 | electrical |    65 |    0 | ChargingPile |

#### 针脚定义

|    |   node | label   | cond                   |   dimx |   dimy |   conntype |
|---:|-------:|:--------|:-----------------------|-------:|-------:|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==2 |      1 |      1 |          1 |

#### 参数填写

##### LoadSettings

| ID               | type   | value   | desc       | choices                                                                                                                                                  |
|:-----------------|:-------|:--------|:-----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| CompName         | text   | 充电桩  | 充电桩名称 | nan                                                                                                                                                      |
| ChargingPileLoad | choice | 0       | 充电桩负荷 | {'0': '无', '1': '居住片区电负荷', '2': '滨湖核心服务区电负荷', '3': '食品生产工业片区电负荷', '4': '工业研发片区电负荷', '5': '装备制造工业片区电负荷'} |


### 储水罐

#### 设备信息

|    | classname   | name   |   type | thutype   |   ver |   id | sym       |
|---:|:------------|:-------|-------:|:----------|------:|-----:|:----------|
|  0 | WaterTank   | 储水罐 |  14001 | heat      |     9 |    0 | WaterTank |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==3 |         42 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         42 |

#### 参数填写

##### BasicParameters

| ID              | type   | value   | desc     | choices               | choiceSource   |
|:----------------|:-------|:--------|:---------|:----------------------|:---------------|
| CompName        | text   | 储水罐  | 元件名称 | nan                   | nan            |
| DeviceSelection | choice | 0       | 设备选型 | {'0': '设备类型待选'} |                |

##### SimuParameters

| ID                | type   | unit   |   min |   max |   value | inputType   | desc         |
|:------------------|:-------|:-------|------:|------:|--------:|:------------|:-------------|
| InitialWaterLevel | real   | m      |     1 |    99 |       3 | constant    | 初始水位高度 |
| InitialWaterTemp  | real   | ℃      |     0 |   999 |      25 | constant    | 初始水温     |

##### OperationParameters

| ID                       | type   | unit   |   min |   max |   value | inputType   | desc           |
|:-------------------------|:-------|:-------|------:|------:|--------:|:------------|:---------------|
| MaxLevelDifference       | real   | %      |     0 |   100 |      20 | constant    | 始末最大水位差 |
| MaxTemperatureDifference | real   | ℃      |     0 |   100 |      20 | constant    | 始末最大水温差 |


### 模块化多电平变流器

#### 设备信息

|    | classname   | name               |   type | thutype    |   ver |   id | sym   |
|---:|:------------|:-------------------|-------:|:-----------|------:|-----:|:------|
|  0 | MMC         | 模块化多电平变流器 |  15001 | electrical |    46 |    0 | MMC   |

#### 针脚定义

|    |   node | label   | cond   | desc              |   dimx |   dimy |   conntype |
|---:|-------:|:--------|:-------|:------------------|-------:|-------:|-----------:|
|  0 |     -1 |         | true   | Sending (i) Pin   |      1 |      1 |          1 |
|  1 |     -1 |         | true   | Receiving (j) Pin |      1 |      1 |         44 |

#### 参数填写

##### BasicParameters

| ID              | type   | value              | desc     | cond   | choices               |
|:----------------|:-------|:-------------------|:---------|:-------|:----------------------|
| CompName        | text   | 模块化多电平变流器 | 元件名称 | true   | nan                   |
| DeviceSelection | choice | 0                  | 设备选型 | nan    | {'0': '设备类型待选'} |

##### SimuParameters

| ID           | type   |   value | choices                                                                                                               | desc     | unit   |   min |     max | inputType   | cond                                                  |
|:-------------|:-------|--------:|:----------------------------------------------------------------------------------------------------------------------|:---------|:-------|------:|--------:|:------------|:------------------------------------------------------|
| ControlStyle | choice |       0 | {'0': '控制交流侧PQ', '1': '控制交流侧PV', '2': '控制交流侧Vθ', '3': '控制直流侧V交流侧Q', '4': '控制直流侧V交流侧V'} | 控制方式 | nan    |   nan | nan     | nan         | nan                                                   |
| ACP          | real   |     100 | nan                                                                                                                   | 交流有功 | kW     |     0 |   1e+06 | constant    | ControlStyle==0 || ControlStyle==1                    |
| ACQ          | real   |       0 | nan                                                                                                                   | 交流无功 | kW     |     0 |   1e+06 | constant    | ControlStyle==0 || ControlStyle==3                    |
| ACV          | real   |      10 | nan                                                                                                                   | 交流电压 | kV     |     0 |   1e+06 | constant    | ControlStyle==1 || ControlStyle==2 || ControlStyle==4 |
| ACTHETA      | real   |       0 | nan                                                                                                                   | 交流相角 | deg    |  -360 | 360     | constant    | ControlStyle==2                                       |
| DCV          | real   |      10 | nan                                                                                                                   | 直流电压 | kV     |     0 |   1e+06 | constant    | ControlStyle==3 || ControlStyle==4                    |


### 光伏系统

#### 设备信息

|    | classname       | name     |   type | thutype    |   ver |   id | sym             |
|---:|:----------------|:---------|-------:|:-----------|------:|-----:|:----------------|
|  0 | PhotovoltaicSys | 光伏系统 |  10001 | electrical |    44 |    0 | PhotovoltaicSys |

#### 针脚定义

|    |   node | label   | cond                                    |   conntype |
|---:|-------:|:--------|:----------------------------------------|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==0) |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==1) |         44 |

#### 参数填写

##### BasicParameters

| ID              | type   | value    | desc         | choices                                        | choiceSource   |   unit |   min |     max | inputType   |
|:----------------|:-------|:---------|:-------------|:-----------------------------------------------|:---------------|-------:|------:|--------:|:------------|
| CompName        | text   | 光伏系统 | 元件名称     | nan                                            | nan            |    nan |   nan | nan     | nan         |
| CompType        | choice | 0        | 元件类型     | {'0': '交流元件（含逆变器）', '1': '直流元件'} |                |    nan |   nan | nan     | nan         |
| DeviceSelection | choice | 0        | 设备选型     | {'0': '设备类型待选'}                          |                |    nan |   nan | nan     | nan         |
| DeviceNumber    | real   | 1.0      | 设备配置台数 | nan                                            | nan            |    nan |     0 |   1e+09 | constant    |

##### SimuParameters

| ID         | type   | value   | choices                                      | choiceSource   | desc     | coldef                       | colType                                                                                                                                                                          | unit         |   minrowcount |   maxrowcount | cond         |
|:-----------|:-------|:--------|:---------------------------------------------|:---------------|:---------|:-----------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------|--------------:|--------------:|:-------------|
| PowerMode  | choice | 0       | {'0': '由气象参数计算', '1': '指定出力曲线'} |                | 出力模式 | nan                          | nan                                                                                                                                                                              | nan          |           nan |           nan | nan          |
| Strategy   | table  | []      | nan                                          | nan            | 启停策略 | ['开始时间', '设备启动台数'] | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"Unit","Value":1,"Parameter type":"Real","Help":"","Condition":""}']   | [None, '台'] |             0 |          9999 | PowerMode==0 |
| PowerCurve | table  | []      | nan                                          | nan            | 出力曲线 | ['开始时间', '发电功率']     | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"Unit","Value":100,"Parameter type":"Real","Help":"","Condition":""}'] | ['', 'kW']   |             0 |          9999 | PowerMode==1 |

##### OperationParameters

| ID                 | type   |   value | choices                              | choiceSource   | desc           | cond          |
|:-------------------|:-------|--------:|:-------------------------------------|:---------------|:---------------|:--------------|
| OptimizationChoice | choice |       1 | {'0': '否，使用仿真策略', '1': '是'} |                | 是否优化该设备 | PowerMode ==0 |


### 风机

#### 设备信息

|    | classname          | name   |   type | thutype    |   ver |   id | sym                |
|---:|:-------------------|:-------|-------:|:-----------|------:|-----:|:-------------------|
|  0 | WindPowerGenerator | 风机   |  10001 | electrical |    37 |    0 | WindPowerGenerator |

#### 针脚定义

|    |   node | label   | cond                                    |   conntype |
|---:|-------:|:--------|:----------------------------------------|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==0) |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==1) |         44 |

#### 参数填写

##### BasicParameters

| ID              | type   | value   | desc         | choices                            | choiceSource   |   unit |   min |   max | inputType   |
|:----------------|:-------|:--------|:-------------|:-----------------------------------|:---------------|-------:|------:|------:|:------------|
| CompName        | text   | 风机    | 元件名称     | nan                                | nan            |    nan |   nan |   nan | nan         |
| CompType        | choice | 0       | 元件类型     | {'0': '交流元件', '1': '直流元件'} |                |    nan |   nan |   nan | nan         |
| DeviceSelection | choice | 0       | 设备选型     | {'0': '设备类型待选'}              |                |    nan |   nan |   nan | nan         |
| DeviceNumber    | real   | 1.0     | 设备配置台数 | nan                                | nan            |    nan |     0 |    20 | constant    |

##### SimuParameters

| ID           | type   | value   | choices                                      | choiceSource   | desc     | coldef                       | colType                                                                                                                                                                            | unit         |   minrowcount |   maxrowcount | cond         |
|:-------------|:-------|:--------|:---------------------------------------------|:---------------|:---------|:-----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------|--------------:|--------------:|:-------------|
| PowerMode    | choice | 0       | {'0': '由气象参数计算', '1': '指定出力曲线'} |                | 出力模式 | nan                          | nan                                                                                                                                                                                | nan          |           nan |           nan | nan          |
| OperateParam | table  | []      | nan                                          | nan            | 启停策略 | ['开始时间', '设备启动台数'] | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"Unit","Value":1,"Parameter type":"Real","Help":"","Condition":""}']     | [None, '台'] |             0 |          9999 | PowerMode==0 |
| PowerCurve   | table  | []      | nan                                          | nan            | 出力曲线 | ['时间', '发电功率']         | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"Unit","Value":100.0,"Parameter type":"Real","Help":"","Condition":""}'] | ['', 'kW']   |             0 |          9999 | PowerMode==1 |

##### OperationParameters

| ID                 | type   |   value | choices                              | choiceSource   | desc           |
|:-------------------|:-------|--------:|:-------------------------------------|:---------------|:---------------|
| OptimizationChoice | choice |       1 | {'0': '否，使用仿真策略', '1': '是'} |                | 是否优化该设备 |


### 交流变压器

#### 设备信息

|    | classname   | name       |   type | thutype    |   ver |   id | sym         |
|---:|:------------|:-----------|-------:|:-----------|------:|-----:|:------------|
|  0 | Transformer | 交流变压器 |  15001 | electrical |    24 |    0 | Transformer |

#### 针脚定义

|    |   node | label   | cond                     |   conntype |   isVisible |
|---:|-------:|:--------|:-------------------------|-----------:|------------:|
|  0 |     -1 |         | (!show_pin||show_pin==2) |          1 |         nan |
|  1 |     -1 |         | (!show_pin||show_pin==2) |          1 |         nan |
|  2 |     -1 |         |                          |        nan |           0 |
|  3 |     -1 |         |                          |        nan |           0 |

#### 参数填写

##### BasicParameters

| ID              | type   | value      | desc     | choices               | choiceSource   |
|:----------------|:-------|:-----------|:---------|:----------------------|:---------------|
| CompName        | text   | 交流变压器 | 元件名称 | nan                   | nan            |
| DeviceSelection | choice | 0          | 设备选型 | {'0': '设备类型待选'} |                |


### 离心泵

#### 设备信息

|    | classname       | name   |   type | thutype   |   ver |   id | sym             |
|---:|:----------------|:-------|-------:|:----------|------:|-----:|:----------------|
|  0 | CentrifugalPump | 离心泵 |  16001 | heatelec  |    55 |    0 | CentrifugalPump |

#### 针脚定义

|    |   node | label   | cond                                    | desc   | dimx   | dimy   |   conntype |
|---:|-------:|:--------|:----------------------------------------|:-------|:-------|:-------|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==0) |        |        |        |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==3)                |        |        |        |         42 |
|  2 |     -1 |         | (!show_pin||show_pin==3)                |        |        |        |         42 |
|  3 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==1) | nan    | nan    | nan    |         44 |

#### 参数填写

##### BasicParameters

| ID              | type   | value   | desc     | choices                            | choiceSource   |
|:----------------|:-------|:--------|:---------|:-----------------------------------|:---------------|
| CompName        | text   | 离心泵  | 元件名称 | nan                                | nan            |
| CompType        | choice | 0       | 元件类型 | {'0': '交流元件', '1': '直流元件'} |                |
| DeviceSelection | choice | 0       | 设备选型 | {'0': '设备类型待选'}              |                |

##### SImuParameters

| ID        | type   | value   | coldef               | colType                                                                                                                                                                                    | unit          |   minrowcount |   maxrowcount | desc       |
|:----------|:-------|:--------|:---------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------|--------------:|--------------:|:-----------|
| PumpSpeed | table  | []      | ['开始时间', '转速'] | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"RotationSpeed","Value":2900,"Parameter type":"Real","Help":"","Condition":""}'] | [None, 'rpm'] |             0 |          9999 | 离心泵转速 |

##### OperationParameters

| ID                 | type   |   value | choices                              | choiceSource   | desc           |
|:-------------------|:-------|--------:|:-------------------------------------|:---------------|:---------------|
| OptimizationChoice | choice |       1 | {'0': '否，使用仿真策略', '1': '是'} |                | 是否优化该设备 |


### 传输线

#### 设备信息

|    | classname    | name   |   type | thutype    |   ver |   id | sym          |
|---:|:-------------|:-------|-------:|:-----------|------:|-----:|:-------------|
|  0 | TransferLine | 传输线 |  15001 | electrical |    24 |    0 | TransferLine |

#### 针脚定义

|    |   node | label   | cond                                    |   conntype |
|---:|-------:|:--------|:----------------------------------------|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==0) |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==0) |          1 |
|  2 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==1) |         44 |
|  3 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==1) |         44 |

#### 参数填写

##### BasicParameters

| ID              | type   | value   | desc     | choices                            | choiceSource   | unit   |   min |   max | inputType   |
|:----------------|:-------|:--------|:---------|:-----------------------------------|:---------------|:-------|------:|------:|:------------|
| CompName        | text   | 传输线  | 元件名称 | nan                                | nan            | nan    |   nan |   nan | nan         |
| CompType        | choice | 0       | 元件类型 | {'0': '交流元件', '1': '直流元件'} |                | nan    |   nan |   nan | nan         |
| Length          | real   | 1.0     | 长度     | nan                                | nan            | km     |     0 |  9999 | constant    |
| DeviceSelection | choice | 0       | 设备选型 | {'0': '设备型号待选'}              |                | nan    |   nan |   nan | nan         |


### 电压缩制冷机

#### 设备信息

|    | classname   | name         |   type | thutype   |   ver |   id | sym       |
|---:|:------------|:-------------|-------:|:----------|------:|-----:|:----------|
|  0 | CompRefrg   | 电压缩制冷机 |  11001 | heatelec  |   115 |    0 | CompRefrg |

#### 针脚定义

|    |   node | label   | cond                                    |   conntype |
|---:|-------:|:--------|:----------------------------------------|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==0) |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3                  |         42 |
|  2 |     -1 |         | !show_pin||show_pin==3                  |         42 |
|  3 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==1) |         44 |

#### 参数填写

##### BasicParameters

| ID              | type   | value        | desc         | choices                            | choiceSource   |   unit |   min |   max | inputType   |
|:----------------|:-------|:-------------|:-------------|:-----------------------------------|:---------------|-------:|------:|------:|:------------|
| CompName        | text   | 电压缩制冷机 | 元件名称     | nan                                | nan            |    nan |   nan |   nan | nan         |
| CompType        | choice | 0            | 元件类型     | {'0': '交流元件', '1': '直流元件'} |                |    nan |   nan |   nan | nan         |
| DeviceSelection | choice | 0            | 设备选型     | {'0': '设备类型待选'}              |                |    nan |   nan |   nan | nan         |
| DeviceNumber    | real   | 1.0          | 设备配置台数 | nan                                | nan            |    nan |     1 |    20 | constant    |

##### SimuParameters

| ID              | type   | value   | choices                            | choiceSource   | desc             | coldef                           | colType                                                                                                                                                                                                                                                                                                         | unit        |   minrowcount |   maxrowcount | cond               |
|:----------------|:-------|:--------|:-----------------------------------|:---------------|:-----------------|:---------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|--------------:|--------------:|:-------------------|
| SettingParaType | choice | 0       | {'0': '供水温度', '1': '制冷功率'} |                | 设定参数类型     | nan                              | nan                                                                                                                                                                                                                                                                                                             | nan         |           nan |           nan | nan                |
| OutletTemp      | table  | []      | nan                                | nan            | 温度模式运行策略 | ['开始时间', '供水温度']         | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"Temperature","Value":10,"Parameter type":"Real","Help":"","Condition":""}']                                                                                                                          | [None, '℃'] |             0 |          9999 | SettingParaType==0 |
| CoolSupply      | table  | []      | nan                                | nan            | 功率模式运行策略 | ['开始时间', '设备启停运行策略'] | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"OperateParam","Value":{"default_value":[1,10],"type":"table","value":[[1,10]],"coldef":["挡位","台数"],"unit":["",""],"desc":"设备启停运行策略"},"Parametertype":"Table","Help":"","Condition":""}'] | [None, '']  |             0 |          9999 | SettingParaType==1 |

##### OperationParameters

| ID                 | type   |   value | choices                              | choiceSource   | desc           |
|:-------------------|:-------|--------:|:-------------------------------------|:---------------|:---------------|
| OptimizationChoice | choice |       1 | {'0': '否，使用仿真策略', '1': '是'} |                | 是否优化该设备 |


### 采暖制冷负荷

#### 设备信息

|    | classname   | name         |   type | thutype   |   ver |   id | sym         |
|---:|:------------|:-------------|-------:|:----------|------:|-----:|:------------|
|  0 | ThermalLoad | 采暖制冷负荷 |  17001 | heat      |    89 |    0 | ThermalLoad |

#### 针脚定义

|    |   node | label   | cond                     |   conntype |
|---:|-------:|:--------|:-------------------------|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==3) |         42 |
|  1 |     -1 |         | (!show_pin||show_pin==3) |         42 |

#### 参数填写

##### BasicParameters

| ID                   | type   | value        | desc         | unit          | inputType   | choices     | choiceSource   |
|:---------------------|:-------|:-------------|:-------------|:--------------|:------------|:------------|:---------------|
| CompName             | text   | 采暖制冷负荷 | 负荷名称     | nan           | nan         | nan         | nan            |
| LocalPressureDropCoe | real   | 100.0        | 局部压降系数 | kPa/(m³·s⁻¹)² | constant    | nan         | nan            |
| HeatingLoad          | choice | 0            | 采暖制冷负荷 | nan           | nan         | {'0': '无'} |                |
| HeatPriceModel       | choice | 0            | 采暖计价模型 | nan           | nan         | {'0': '无'} |                |
| CoolingPriceModel    | choice | 0            | 用冷计价模型 | nan           | nan         | {'0': '无'} |                |

##### OperationParameters

| ID                 | type   | unit   |   value | inputType   | desc               |
|:-------------------|:-------|:-------|--------:|:------------|:-------------------|
| MiniOutletColdTemp | real   | ℃      |       5 | constant    | 制冷时最小出口温度 |
| MaxOutletColdTemp  | real   | ℃      |      40 | constant    | 制冷时最大出口温度 |
| MiniOutletHeatTemp | real   | ℃      |      30 | constant    | 供热时最小出口温度 |
| MaxOutletHeatTemp  | real   | ℃      |      90 | constant    | 供热时最大出口温度 |


### 电负荷

#### 设备信息

|    | classname      | name   |   type | thutype    |   ver |   id | sym            |
|---:|:---------------|:-------|-------:|:-----------|------:|-----:|:---------------|
|  0 | ElectricalLoad | 电负荷 |  17001 | electrical |    83 |    0 | ElectricalLoad |

#### 针脚定义

|    |   node | label   | cond                                    |   dimx |   dimy |   conntype |
|---:|-------:|:--------|:----------------------------------------|-------:|-------:|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==0) |      1 |      1 |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==1) |    nan |    nan |         44 |

#### 参数填写

##### BasicParameters

| ID              | type   | value   | desc                 | choices                            | choiceSource   |
|:----------------|:-------|:--------|:---------------------|:-----------------------------------|:---------------|
| CompName        | text   | 电负荷  | 负荷名称             | nan                                | nan            |
| CompType        | choice | 0       | 元件类型             | {'0': '交流元件', '1': '直流元件'} |                |
| ElectircalLoad  | choice | 0       | 电负荷               | {'0': '无'}                        |                |
| PowerPriceModel | choice | 0       | 用电计价模型（收入） | {'0': '无'}                        |                |


### 燃气锅炉

#### 设备信息

|    | classname   | name     |   type | thutype   |   ver |   id | sym       |
|---:|:------------|:---------|-------:|:----------|------:|-----:|:----------|
|  0 | GasBoiler   | 燃气锅炉 |  11001 | heat      |   119 |    0 | GasBoiler |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |         42 |
|  1 |     -1 |         | true   |         42 |

#### 参数填写

##### BasicParameters

| ID              | type   | value    | desc         | choices               | choiceSource   |   unit |   min |   max | inputType   |
|:----------------|:-------|:---------|:-------------|:----------------------|:---------------|-------:|------:|------:|:------------|
| CompName        | text   | 燃气锅炉 | 元件名称     | nan                   | nan            |    nan |   nan |   nan | nan         |
| DeviceSelection | choice | 0        | 设备选型     | {'0': '设备类型待选'} |                |    nan |   nan |   nan | nan         |
| DeviceNumber    | real   | 1.0      | 设备配置台数 | nan                   | nan            |    nan |     1 |    20 | constant    |
| FuelPriceModel  | choice | 0        | 燃料计价模型 | {'0': '无'}           |                |    nan |   nan |   nan | nan         |

##### SimuParameters

| ID              | type   | value   | choices                            | choiceSource   | desc             | coldef                   | colType                                                                                                                                                                                                                                                                                                                 | unit         |   minrowcount |   maxrowcount | cond               |
|:----------------|:-------|:--------|:-----------------------------------|:---------------|:-----------------|:-------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------|--------------:|--------------:|:-------------------|
| SettingParaType | choice | 0       | {'0': '供水温度', '1': '加热功率'} |                | 设定参数类型     | nan                      | nan                                                                                                                                                                                                                                                                                                                     | nan          |           nan |           nan | nan                |
| OutletTemp      | table  | []      | nan                                | nan            | 温度模式运行策略 | ['开始时间', '供水温度'] | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"Temperature","Value":80,"Parameter type":"Real","Help":"","Condition":""}']                                                                                                                                  | [None, '℃']  |             0 |          9999 | SettingParaType==0 |
| HeatPower       | table  | []      | nan                                | nan            | 功率模式运行策略 | ['开始时间', '加热功率'] | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"OperateParam","Value":{"default_value":["1","10"],"type":"table","value":[["1","10"]],"coldef":["挡位","台数"],"unit":["",""],"desc":"设备启停运行策略"},"Parametertype":"Table","Help":"","Condition":""}'] | [None, 'kW'] |             0 |          9999 | SettingParaType==1 |

##### OperationParameters

| ID                 | type   |   value | choices                              | choiceSource   | desc           |
|:-------------------|:-------|--------:|:-------------------------------------|:---------------|:---------------|
| OptimizationChoice | choice |       1 | {'0': '否，使用仿真策略', '1': '是'} |                | 是否优化该设备 |


### 热泵

#### 设备信息

|    | classname   | name   |   type | thutype   |   ver |   id | sym      |
|---:|:------------|:-------|-------:|:----------|------:|-----:|:---------|
|  0 | HeatPump    | 热泵   |  11001 | heatelec  |   107 |    0 | HeatPump |

#### 针脚定义

|    |   node | label   | cond                                    |   conntype |
|---:|-------:|:--------|:----------------------------------------|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==0) |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3                  |         42 |
|  2 |     -1 |         | !show_pin||show_pin==3                  |         42 |
|  3 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==1) |         44 |

#### 参数填写

##### BasicParameters

| ID              | type   | value   | desc         | choices                            | choiceSource   |   unit |   min |   max | inputType   |
|:----------------|:-------|:--------|:-------------|:-----------------------------------|:---------------|-------:|------:|------:|:------------|
| CompName        | text   | 热泵    | 元件名称     | nan                                | nan            |    nan |   nan |   nan | nan         |
| CompType        | choice | 0       | 元件类型     | {'0': '交流元件', '1': '直流元件'} |                |    nan |   nan |   nan | nan         |
| DeviceSelection | choice | 0       | 设备选型     | {'0': '设备类型待选'}              |                |    nan |   nan |   nan | nan         |
| DeviceNumber    | real   | 1.0     | 设备配置台数 | nan                                | nan            |    nan |     0 |    20 | constant    |

##### SimuParameters

| ID              | type   | value   | choices                                | choiceSource   | desc             | coldef                           | colType                                                                                                                                                                                                                                                                                     | unit        |   minrowcount |   maxrowcount | cond               |
|:----------------|:-------|:--------|:---------------------------------------|:---------------|:-----------------|:---------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|--------------:|--------------:|:-------------------|
| SettingParaType | choice | 0       | {'0': '供水温度', '1': '制冷制热功率'} |                | 设定参数类型     | nan                              | nan                                                                                                                                                                                                                                                                                         | nan         |           nan |           nan | nan                |
| OutletTemp      | table  | []      | nan                                    | nan            | 温度模式运行策略 | ['开始时间', '供水温度']         | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"Temperature","Value":80,"Parameter type":"Real","Help":"","Condition":""}']                                                                                                      | [None, '℃'] |             0 |          9999 | SettingParaType==0 |
| EnergySupply    | table  | []      | nan                                    | nan            | 功率模式运行策略 | ['开始时间', '设备启停运行策略'] | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"OperateParam","Value":{"default_value":["1","1"],"type":"table","value":[["1","1"]],"coldef":["挡位","台数"],"unit":["",""]},"Parametertype":"Table","Help":"","Condition":""}'] | [None, '']  |             0 |          9999 | SettingParaType==1 |

##### OperationParameters

| ID                 | type   |   value | choices                              | choiceSource   | desc           |
|:-------------------|:-------|--------:|:-------------------------------------|:---------------|:---------------|
| OptimizationChoice | choice |       1 | {'0': '否，使用仿真策略', '1': '是'} |                | 是否优化该设备 |


### 燃气轮机

#### 设备信息

|    | classname   | name     |   type | thutype   |   ver |   id | sym        |
|---:|:------------|:---------|-------:|:----------|------:|-----:|:-----------|
|  0 | GasTurbine  | 燃气轮机 |  10001 | heatelec  |    48 |    0 | GasTurbine |

#### 针脚定义

|    |   node | label   | cond                                    |   conntype |
|---:|-------:|:--------|:----------------------------------------|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==0) |          1 |
|  1 |     -1 |         | !show_pin||show_pin==3                  |         42 |
|  2 |     -1 |         | !show_pin||show_pin==3                  |         42 |
|  3 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==1) |         44 |

#### 参数填写

##### BasicParameters

| ID              | type   | value    | desc                 | choices                            | choiceSource   |   unit |   min |   max | inputType   |
|:----------------|:-------|:---------|:---------------------|:-----------------------------------|:---------------|-------:|------:|------:|:------------|
| CompName        | text   | 燃气轮机 | 元件名称             | nan                                | nan            |    nan |   nan |   nan | nan         |
| CompType        | choice | 0        | 元件类型             | {'0': '交流元件', '1': '直流元件'} |                |    nan |   nan |   nan | nan         |
| DeviceSelection | choice | 0        | 设备选型             | {'0': '设备类型待选'}              |                |    nan |   nan |   nan | nan         |
| DeviceNumber    | real   | 1.0      | 设备配置台数         | nan                                | nan            |    nan |     0 |    20 | constant    |
| FuelPriceModel  | choice | 0        | 燃料计价模型（支出） | {'0': '无'}                        |                |    nan |   nan |   nan | nan         |

##### SimuParameters

| ID              | type   | value   | choices                            | choiceSource   | desc             | coldef                           | colType                                                                                                                                                                                                                                                                                                         | unit        |   minrowcount |   maxrowcount | cond               |
|:----------------|:-------|:--------|:-----------------------------------|:---------------|:-----------------|:---------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|--------------:|--------------:|:-------------------|
| SettingParaType | choice | 0       | {'0': '供水温度', '1': '发电功率'} |                | 设定参数类型     | nan                              | nan                                                                                                                                                                                                                                                                                                             | nan         |           nan |           nan | nan                |
| OutletTemp      | table  | []      | nan                                | nan            | 温度模式运行策略 | ['开始时间', '供水温度']         | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"Temperature","Value":100,"Parameter type":"Real","Help":"","Condition":""}']                                                                                                                         | [None, '℃'] |             0 |          9999 | SettingParaType==0 |
| PowerGenerating | table  | []      | nan                                | nan            | 功率模式运行策略 | ['开始时间', '设备启停运行策略'] | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"OperateParam","Value":{"default_value":[1,10],"type":"table","value":[[1,10]],"coldef":["挡位","台数"],"unit":["",""],"desc":"设备启停运行策略"},"Parametertype":"Table","Help":"","Condition":""}'] | [None, '']  |             0 |          9999 | SettingParaType==1 |

##### OperationParameters

| ID                 | type   |   value | choices                              | choiceSource   | desc           |
|:-------------------|:-------|--------:|:-------------------------------------|:---------------|:---------------|
| OptimizationChoice | choice |       1 | {'0': '否，使用仿真策略', '1': '是'} |                | 是否优化该设备 |


### 蓄电池

#### 设备信息

|    | classname   | name   |   type | thutype    |   ver |   id | sym     |
|---:|:------------|:-------|-------:|:-----------|------:|-----:|:--------|
|  0 | Battery     | 蓄电池 |  14001 | electrical |    44 |    0 | Battery |

#### 针脚定义

|    |   node | label   | cond                                    |   conntype |
|---:|-------:|:--------|:----------------------------------------|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==0) |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==1) |         44 |

#### 参数填写

##### BasicParameters

| ID              | type   | value   | desc         | choices                                      | choiceSource   |   unit |   min |   max | inputType   |
|:----------------|:-------|:--------|:-------------|:---------------------------------------------|:---------------|-------:|------:|------:|:------------|
| CompName        | text   | 蓄电池  | 元件名称     | nan                                          | nan            |    nan |   nan |   nan | nan         |
| CompType        | choice | 0       | 元件类型     | {'0': '交流元件(含变流器)', '1': '直流元件'} |                |    nan |   nan |   nan | nan         |
| DeviceSelection | choice | 0       | 设备选型     | {'0': '设备类型待选'}                        |                |    nan |   nan |   nan | nan         |
| DeviceNumber    | real   | 1.0     | 设备配置台数 | nan                                          | nan            |    nan |     0 |    20 | constant    |

##### SimuParameters

| ID                  | type   | unit         |   min |    max | value   | inputType   | desc                 | coldef                             | colType                                                                                                                                                                           |   minrowcount |   maxrowcount |
|:--------------------|:-------|:-------------|------:|-------:|:--------|:------------|:---------------------|:-----------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------:|--------------:|
| InitialPowerStorage | real   | kWh          |     0 | 999999 | 1000.0  | constant    | 初始蓄电量           | nan                                | nan                                                                                                                                                                               |           nan |           nan |
| Power               | table  | [None, 'kW'] |   nan |    nan | []      | nan         | 充放功率（正充负放） | ['开始时间', '充放功率(正充负放)'] | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"Power","Value":100,"Parameter type":"Real","Help":"","Condition":""}'] |             0 |          9999 |

##### OperationParameters

| ID                  | type   |   value | choices                              | choiceSource   | desc                   | unit   |   min |   max | inputType   | cond                  |
|:--------------------|:-------|--------:|:-------------------------------------|:---------------|:-----------------------|:-------|------:|------:|:------------|:----------------------|
| OptimizationChoice  | choice |       1 | {'0': '否，使用仿真策略', '1': '是'} |                | 是否优化该设备         | nan    |   nan |   nan | nan         | nan                   |
| MaxPowerStorageDiff | real   |      10 | nan                                  | nan            | 蓄电量始末最大偏差比例 | %      |     0 |   100 | constant    | OptimizationChoice==1 |


### 吸收式制冷机

#### 设备信息

|    | classname         | name         |   type | thutype   |   ver |   id | sym               |
|---:|:------------------|:-------------|-------:|:----------|------:|-----:|:------------------|
|  0 | AbsorptionChiller | 吸收式制冷机 |  11001 | heatelec  |   101 |    0 | AbsorptionChiller |

#### 针脚定义

|    |   node | label   | cond                                    |   conntype |
|---:|-------:|:--------|:----------------------------------------|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==0) |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==3)                |         42 |
|  2 |     -1 |         | (!show_pin||show_pin==3)                |         42 |
|  3 |     -1 |         | (!show_pin||show_pin==3)                |         42 |
|  4 |     -1 |         | (!show_pin||show_pin==3)                |         42 |
|  5 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==1) |         44 |

#### 参数填写

##### BasicParameters

| ID              | type   | value        | desc         | choices                            | choiceSource   |   unit |   min |   max | inputType   |
|:----------------|:-------|:-------------|:-------------|:-----------------------------------|:---------------|-------:|------:|------:|:------------|
| CompName        | text   | 吸收式制冷机 | 元件名称     | nan                                | nan            |    nan |   nan |   nan | nan         |
| CompType        | choice | 0            | 元件类型     | {'0': '交流元件', '1': '直流元件'} |                |    nan |   nan |   nan | nan         |
| DeviceSelection | choice | 0            | 设备选型     | {'0': '设备类型待选'}              |                |    nan |   nan |   nan | nan         |
| DeviceNumber    | real   | 1.0          | 设备配置台数 | nan                                | nan            |    nan |     0 |    20 | constant    |

##### SimuParameters

| ID              | type   | value   | choices                            | choiceSource   | desc             | coldef                           | colType                                                                                                                                                                                                                                                                             | unit         |   minrowcount |   maxrowcount | cond               |
|:----------------|:-------|:--------|:-----------------------------------|:---------------|:-----------------|:---------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------|--------------:|--------------:|:-------------------|
| SettingParaType | choice | 0       | {'0': '供水温度', '1': '制冷功率'} |                | 设定参数类型     | nan                              | nan                                                                                                                                                                                                                                                                                 | nan          |           nan |           nan | nan                |
| OutletTemp      | table  | []      | nan                                | nan            | 温度模式运行策略 | ['开始时间', '冷水侧供水温度']   | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"Temperature","Value":10,"Parameter type":"Real","Help":"","Condition":""}']                                                                                              | [None, '℃']  |             0 |          9999 | SettingParaType==0 |
| CoolSupply      | table  | []      | nan                                | nan            | 功率模式运行策略 | ['开始时间', '设备启停运行策略'] | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"OperateParam","Value":{"default_value":[1,1],"type":"table","value":[[1,1]],"coldef":["挡位","台数"],"unit":["",""]},"Parametertype":"Table","Help":"","Condition":""}'] | [None, None] |             0 |          9999 | SettingParaType==1 |

##### OperationParameters

| ID                 | type   |   value | choices                              | choiceSource   | desc           |
|:-------------------|:-------|--------:|:-------------------------------------|:---------------|:---------------|
| OptimizationChoice | choice |       1 | {'0': '否，使用仿真策略', '1': '是'} |                | 是否优化该设备 |


### 柔性电负荷

#### 设备信息

|    | classname          | name       |   type | thutype    |   ver |   id | sym                |
|---:|:-------------------|:-----------|-------:|:-----------|------:|-----:|:-------------------|
|  0 | FlexElectricalLoad | 柔性电负荷 |  17001 | electrical |    86 |    0 | FlexElectricalLoad |

#### 针脚定义

|    |   node | label   | cond                                    |   dimx |   dimy |   conntype |
|---:|-------:|:--------|:----------------------------------------|-------:|-------:|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==0) |      1 |      1 |          1 |
|  1 |     -1 |         | (!show_pin||show_pin==2)&&(CompType==1) |    nan |    nan |         44 |

#### 参数填写

##### BasicParameters

| ID              | type   | value   | desc                 | choices                            | choiceSource   |
|:----------------|:-------|:--------|:---------------------|:-----------------------------------|:---------------|
| CompName        | text   | 电负荷  | 负荷名称             | nan                                | nan            |
| CompType        | choice | 0       | 元件类型             | {'0': '交流元件', '1': '直流元件'} |                |
| PowerPriceModel | choice | 0       | 用电计价模型（收入） | {'0': '无'}                        |                |

##### SimuParameters

| ID             | type   |   value | choices     | choiceSource   | desc   |
|:---------------|:-------|--------:|:------------|:---------------|:-------|
| ElectircalLoad | choice |       0 | {'0': '无'} |                | 电负荷 |

##### OptimizationParamters

| ID                 | type   |   value | choices                              | choiceSource   | desc           | unit   |   min |    max | inputType   | cond                  |
|:-------------------|:-------|--------:|:-------------------------------------|:---------------|:---------------|:-------|------:|-------:|:------------|:----------------------|
| OptimizationChoice | choice |       1 | {'0': '否，使用仿真负荷', '1': '是'} |                | 是否优化该负荷 | nan    |   nan |    nan | nan         | nan                   |
| MaxLoad            | real   |    1000 | nan                                  | nan            | 最大负荷       | kW     |     0 | 999999 | constant    | OptimizationChoice==1 |


### 建筑物冷热负荷围护模型

#### 设备信息

|    | classname   | name                   |   type | thutype   |   ver |   id | sym       |
|---:|:------------|:-----------------------|-------:|:----------|------:|-----:|:----------|
|  0 | HouseLoad   | 建筑物冷热负荷围护模型 |  17001 | heat      |    91 |    0 | HouseLoad |

#### 针脚定义

|    |   node | label   | cond                     |   conntype |
|---:|-------:|:--------|:-------------------------|-----------:|
|  0 |     -1 |         | (!show_pin||show_pin==3) |         42 |
|  1 |     -1 |         | (!show_pin||show_pin==3) |         42 |

#### 参数填写

##### BasicParameters

| ID                   | type   | value                  | desc         | unit          | inputType   | choices     | choiceSource   |
|:---------------------|:-------|:-----------------------|:-------------|:--------------|:------------|:------------|:---------------|
| CompName             | text   | 建筑物冷热负荷围护模型 | 负荷名称     | nan           | nan         | nan         | nan            |
| LocalPressureDropCoe | real   | 100.0                  | 局部压降系数 | kPa/(m³·s⁻¹)² | constant    | nan         | nan            |
| HeatPriceModel       | choice | 0                      | 采暖计价模型 | nan           | nan         | {'0': '无'} |                |
| CoolingPriceModel    | choice | 0                      | 用冷计价模型 | nan           | nan         | {'0': '无'} |                |

##### HouseParameters

| ID                         | type   | unit      |   min |    max |   value | inputType   | desc                        |
|:---------------------------|:-------|:----------|------:|-------:|--------:|:------------|:----------------------------|
| HousePerimeter             | real   | m         |     0 | 999999 |   70    | constant    | 围护结构周长                |
| FloorArea                  | real   | m²        |     0 | 999999 |   80    | constant    | 建筑占地面积                |
| HouseHeight                | real   | m         |     0 |    999 |    8    | constant    | 建筑高度                    |
| PanelArea                  | real   | m²        |     0 |  99999 |   10    | constant    | 冷/热媒与室内的有效换热面积 |
| WallThick                  | real   | mm        |     0 | 999999 |  200    | constant    | 墙体厚度                    |
| WallDensity                | real   | kg/m³     |     0 |   9999 | 2400    | constant    | 墙体密度                    |
| WallHeatConductivity       | real   | W/(m·K)   |     0 |     99 |    0.2  | constant    | 墙体导热系数                |
| WallHeatCapacity           | real   | kJ/(kg·℃) |     0 |     99 |    1    | constant    | 墙体比热容                  |
| WallRadAbsorbCoe           | real   |           |     0 |      1 |    0.65 | constant    | 墙体辐射吸收系数            |
| WindowAreaRatio            | real   | %         |     0 |    100 |   65    | constant    | 窗面占比                    |
| WindowHeatTransCoe         | real   | W/(m²·℃)  |     0 |     99 |    2    | constant    | 窗户传热系数                |
| FurnitureTotalHeatCapacity | real   | kJ/℃      |     0 | 999999 |  100    | constant    | 家具总热容                  |

##### SimuParameters

| ID                 | type   | unit   |   min |   max |   value | inputType   | desc         |
|:-------------------|:-------|:-------|------:|------:|--------:|:------------|:-------------|
| InitialTemperature | real   | ℃      |   -50 |    50 |      25 | constant    | 室内初始温度 |

##### OperationParameters

| ID             | type   | unit   |   value | inputType   | desc     |
|:---------------|:-------|:-------|--------:|:------------|:---------|
| MiniIndoorTemp | real   | ℃      |      20 | constant    | 最低室温 |
| MaxIndoorTemp  | real   | ℃      |      28 | constant    | 最高室温 |


### 直流变压器

#### 设备信息

|    | classname           | name       |   type | thutype    |   ver |   id | sym                 |
|---:|:--------------------|:-----------|-------:|:-----------|------:|-----:|:--------------------|
|  0 | FullBridgeConverter | 直流变压器 |  15001 | electrical |    29 |    0 | FullBridgeConverter |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |         44 |
|  1 |     -1 |         | true   |         44 |

#### 参数填写

##### BasicParameters

| ID       | type   | value      | desc                    | unit   |   min |    max | inputType   |
|:---------|:-------|:-----------|:------------------------|:-------|------:|-------:|:------------|
| CompName | text   | 直流变压器 | 元件名称                | nan    |   nan |    nan | nan         |
| D        | real   | 0.25       | 占空比                  |        |     0 | 999999 | constant    |
| n        | real   | 2.0        | 隔离变压器变比          |        |     0 |  99999 | constant    |
| RT1      | real   | 0.25       | 隔离变压器1次侧漏电阻   | Ω      |     0 | 999999 | constant    |
| RT2      | real   | 0.04       | 隔离变压器2次侧漏电阻   | Ω      |     0 | 999999 | constant    |
| RD       | real   | 0.075      | 二极管导通电阻          | Ω      |     0 | 999999 | constant    |
| RL       | real   | 0.72       | 隔离变压器2次侧励磁电阻 | Ω      |     0 | 999999 | constant    |


### 管道

#### 设备信息

|    | classname   | name   |   type | thutype   |   ver |   id | sym   |
|---:|:------------|:-------|-------:|:----------|------:|-----:|:------|
|  0 | Pipe        | 管道   |  16001 | heat      |    13 |    0 | Pipe  |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |         42 |
|  1 |     -1 |         | true   |         42 |

#### 参数填写

##### DeviceParameters

| ID              | type   | value   | desc     | unit   |   min |    max | inputType   | choices   | choiceSource   |
|:----------------|:-------|:--------|:---------|:-------|------:|-------:|:------------|:----------|:---------------|
| CompName        | text   | 管道    | 元件名称 | nan    |   nan |    nan | nan         | nan       | nan            |
| Length          | real   | 200.0   | 管道长度 | m      |     0 | 999999 | constant    | nan       | nan            |
| DeviceSelection | choice | 0       | 设备选型 | nan    |   nan |    nan | nan         | {}        |                |


### 外部电源

#### 设备信息

|    | classname           | name     |   type | thutype    |   ver |   id | sym                   |
|---:|:--------------------|:---------|-------:|:-----------|------:|-----:|:----------------------|
|  0 | ExternalPowerSource | 外部电源 |  10001 | electrical |    36 |    0 | ExternalPowerSource-1 |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |          1 |

#### 参数填写

##### BasicParameters

| ID                 | type   | value              | desc                 | choices     | choiceSource   |
|:-------------------|:-------|:-------------------|:---------------------|:------------|:---------------|
| CompName           | text   | 外部电源(参考节点) | 元件名称             | nan         | nan            |
| PurchasePriceModel | choice | 0                  | 购电计价模型（支出） | {'0': '无'} |                |
| SalePriceModel     | choice | 0                  | 上网计价模型（收入） | {'0': '无'} |                |

##### SimuParameters

| ID      | type   | unit   |   value | inputType   | desc   |
|:--------|:-------|:-------|--------:|:------------|:-------|
| Voltage | real   | kV     |     110 | constant    | 电压   |
| Angle   | real   | deg    |       0 | constant    | 相角   |


### 热管式太阳能集热器

#### 设备信息

|    | classname        | name               |   type | thutype   |   ver |   id | sym              |
|---:|:-----------------|:-------------------|-------:|:----------|------:|-----:|:-----------------|
|  0 | HPSolarCollector | 热管式太阳能集热器 |  11001 | heat      |    48 |    0 | HPSolarCollector |

#### 针脚定义

|    |   node | label   | cond   |   conntype |
|---:|-------:|:--------|:-------|-----------:|
|  0 |     -1 |         | true   |         42 |
|  1 |     -1 |         | true   |         42 |

#### 参数填写

##### BasicParameters

| ID              | type    | value              | desc         | choices               | choiceSource   |   min |     max | inputType   |
|:----------------|:--------|:-------------------|:-------------|:----------------------|:---------------|------:|--------:|:------------|
| CompName        | text    | 热管式太阳能集热器 | 元件名称     | nan                   | nan            |   nan | nan     | nan         |
| DeviceSelection | choice  | 0                  | 设备选型     | {'0': '设备类型待选'} |                |   nan | nan     | nan         |
| DeviceNumber    | integer | 1                  | 设备配置台数 | nan                   | nan            |     0 |   1e+08 | constant    |

##### SimuParameters

| ID       | type   | value   | coldef                       | colType                                                                                                                                                                        | unit     |   minrowcount |   maxrowcount | desc     |
|:---------|:-------|:--------|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|--------------:|--------------:|:---------|
| Strategy | table  | []      | ['开始时间', '设备启动台数'] | ['{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}', '{"Key":"Unit","Value":1,"Parameter type":"Real","Help":"","Condition":""}'] | ['', ''] |             0 |         10000 | 启停策略 |

##### OperationParameters

| ID                 | type   |   value | choices                              | choiceSource   | desc           |
|:-------------------|:-------|--------:|:-------------------------------------|:---------------|:---------------|
| OptimizationChoice | choice |       1 | {'0': '否，使用仿真策略', '1': '是'} |                | 是否优化该设备 |


### 储气罐

#### 设备信息

|    | classname   | name   |   type | thutype   |   ver |   id | sym     |
|---:|:------------|:-------|-------:|:----------|------:|-----:|:--------|
|  0 | AirTank     | 储气罐 |  14000 | heat      |    11 |    0 | AirTank |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==3 |         43 |
|  1 |     -1 |         | !show_pin||show_pin==3 |         43 |

#### 参数填写

##### BasicParameters

| ID              | type   | value   | desc     | choices               | choiceSource   |
|:----------------|:-------|:--------|:---------|:----------------------|:---------------|
| CompName        | text   | 储气罐  | 元件名称 | nan                   | nan            |
| DeviceSelection | choice | 0       | 设备选型 | {'0': '设备类型待选'} |                |

##### SimuParameters

| ID                | type   | unit   |   min |   max |   value | inputType   | desc         |
|:------------------|:-------|:-------|------:|------:|--------:|:------------|:-------------|
| InitialWaterLevel | real   | m      |     1 |    99 |       3 | constant    | 初始水位高度 |
| InitialWaterTemp  | real   | ℃      |     0 |   999 |      25 | constant    | 初始水温     |

##### OperationParameters

| ID                       | type   | unit   |   min |   max |   value | inputType   | desc           |
|:-------------------------|:-------|:-------|------:|------:|--------:|:------------|:---------------|
| MaxLevelDifference       | real   | %      |     0 |   100 |      20 | constant    | 始末最大水位差 |
| MaxTemperatureDifference | real   | ℃      |     0 |   100 |      20 | constant    | 始末最大水温差 |


### 压气机

#### 设备信息

|    | classname   | name   |   type | thutype   |   ver |   id | sym        |
|---:|:------------|:-------|-------:|:----------|------:|-----:|:-----------|
|  0 | Compressor  | 压气机 |  16000 | heatelec  |    13 |    0 | Compressor |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==3 |         43 |
|  1 |     -1 |         | !show_pin||show_pin==2 |          1 |

#### 参数填写

##### BasicParameters

| ID              | type   | value   | desc     | choices               | choiceSource   |
|:----------------|:-------|:--------|:---------|:----------------------|:---------------|
| CompName        | text   | 压气机  | 元件名称 | nan                   | nan            |
| DeviceSelection | choice | 0       | 设备选型 | {'0': '设备类型待选'} |                |

##### SimuParameters

| ID                | type   | unit   |   min |   max |   value | inputType   | desc         |
|:------------------|:-------|:-------|------:|------:|--------:|:------------|:-------------|
| InitialWaterLevel | real   | m      |     1 |    99 |       3 | constant    | 初始水位高度 |
| InitialWaterTemp  | real   | ℃      |     0 |   999 |      25 | constant    | 初始水温     |

##### OperationParameters

| ID                       | type   | unit   |   min |   max |   value | inputType   | desc           |
|:-------------------------|:-------|:-------|------:|------:|--------:|:------------|:---------------|
| MaxLevelDifference       | real   | %      |     0 |   100 |      20 | constant    | 始末最大水位差 |
| MaxTemperatureDifference | real   | ℃      |     0 |   100 |      20 | constant    | 始末最大水温差 |


### 透平发电机

#### 设备信息

|    | classname        | name       |   type | thutype   |   ver |   id | sym              |
|---:|:-----------------|:-----------|-------:|:----------|------:|-----:|:-----------------|
|  0 | TurbineGenerator | 透平发电机 |  10000 | heatelec  |    14 |    0 | TurbineGenerator |

#### 针脚定义

|    |   node | label   | cond                   |   conntype |
|---:|-------:|:--------|:-----------------------|-----------:|
|  0 |     -1 |         | !show_pin||show_pin==3 |         43 |
|  1 |     -1 |         | !show_pin||show_pin==2 |          1 |

#### 参数填写

##### BasicParameters

| ID              | type   | value      | desc     | choices               | choiceSource   |
|:----------------|:-------|:-----------|:---------|:----------------------|:---------------|
| CompName        | text   | 透平发电机 | 元件名称 | nan                   | nan            |
| DeviceSelection | choice | 0          | 设备选型 | {'0': '设备类型待选'} |                |

##### SimuParameters

| ID                | type   | unit   |   min |   max |   value | inputType   | desc         |
|:------------------|:-------|:-------|------:|------:|--------:|:------------|:-------------|
| InitialWaterLevel | real   | m      |     1 |    99 |       3 | constant    | 初始水位高度 |
| InitialWaterTemp  | real   | ℃      |     0 |   999 |      25 | constant    | 初始水温     |

##### OperationParameters

| ID                       | type   | unit   |   min |   max |   value | inputType   | desc           |
|:-------------------------|:-------|:-------|------:|------:|--------:|:------------|:---------------|
| MaxLevelDifference       | real   | %      |     0 |   100 |      20 | constant    | 始末最大水位差 |
| MaxTemperatureDifference | real   | ℃      |     0 |   100 |      20 | constant    | 始末最大水温差 |


