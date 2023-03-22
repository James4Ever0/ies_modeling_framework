
# 建模仿真和规划设计的输入参数和区别

规划设计在设备信息库内添加了经济性参数，而建模仿真对某些设备将额定工况变为了多工况的输入。
<br><br>根据布尔表达式，有的输入项所填写的值决定其他参数是否能够填写。
<br><br>下面介绍在能流拓扑图中两种模式的输入项区别：




## 建模仿真参数

### 参数分类

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>参数分类</th>
      <th>中文名称</th>
      <th>有关设备</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>BasicParameters</td>
      <td>基础参数, 机组参数, 母线参数</td>
      <td>母线, 储水罐, 模块化多电平变流器, 光伏系统, 风机, 交流变压器, 离心泵, 传输线, 电压缩制冷机, 采暖制冷负荷, 电负荷, 燃气锅炉, 热泵, 燃气轮机, 蓄电池, 吸收式制冷机, 柔性电负荷, 建筑物冷热负荷围护模型, 直流变压器, 外部电源, 热管式太阳能集热器, 储气罐, 压气机, 透平发电机</td>
    </tr>
    <tr>
      <td>DeviceParameters</td>
      <td>机组参数, 设备参数</td>
      <td>燃气内燃机, 换热器, 尾气排放装置, 离心泵, 蒸汽轮机, 电容器, 蓄冰空调, 蓄热电锅炉, 余热锅炉, 管道</td>
    </tr>
    <tr>
      <td>OperationParameters</td>
      <td>运行参数组, 优化参数, 运行约束</td>
      <td>燃气内燃机, 负荷, 换热器, 尾气排放装置, 蒸汽轮机, 蓄冰空调, 蓄热电锅炉, 余热锅炉, 储水罐, 光伏系统, 风机, 离心泵, 电压缩制冷机, 采暖制冷负荷, 燃气锅炉, 热泵, 燃气轮机, 蓄电池, 吸收式制冷机, 建筑物冷热负荷围护模型, 热管式太阳能集热器, 储气罐, 压气机, 透平发电机</td>
    </tr>
    <tr>
      <td>LoadSettings</td>
      <td>负荷设置, 充电桩设置</td>
      <td>负荷, 充电桩</td>
    </tr>
    <tr>
      <td>SimuParameters</td>
      <td>仿真参数</td>
      <td>储水罐, 模块化多电平变流器, 光伏系统, 风机, 离心泵, 电压缩制冷机, 燃气锅炉, 热泵, 燃气轮机, 蓄电池, 吸收式制冷机, 柔性电负荷, 建筑物冷热负荷围护模型, 外部电源, 热管式太阳能集热器, 储气罐, 压气机, 透平发电机</td>
    </tr>
    <tr>
      <td>OptimizationParamters</td>
      <td>优化参数</td>
      <td>柔性电负荷</td>
    </tr>
    <tr>
      <td>HouseParameters</td>
      <td>建筑物围护参数</td>
      <td>建筑物冷热负荷围护模型</td>
    </tr>
  </tbody>
</table>

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

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BusNode</td>
      <td>母线</td>
      <td>15001</td>
      <td>electrical</td>
      <td>4</td>
      <td>0</td>
      <td>BusNode</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>CompType==0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>CompType==1</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>cond</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>unit</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Name</td>
      <td>text</td>
      <td></td>
      <td>母线名称</td>
      <td>true</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CompType</td>
      <td>choice</td>
      <td>0</td>
      <td>元件类型</td>
      <td>NaN</td>
      <td>{'0': '交流元件', '1': '直流元件'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>VBase</td>
      <td>real</td>
      <td>115.0</td>
      <td>基准电压</td>
      <td>true</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>kV</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>V</td>
      <td>real</td>
      <td>115.0</td>
      <td>初始电压</td>
      <td>true</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>kV</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>Angle</td>
      <td>real</td>
      <td>0.0</td>
      <td>初始相角</td>
      <td>CompType==0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>deg</td>
      <td>constant</td>
    </tr>
  </tbody>
</table>


### 燃气内燃机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GasEngine</td>
      <td>燃气内燃机</td>
      <td>10000</td>
      <td>heatelec</td>
      <td>29</td>
      <td>0</td>
      <td>GasEngine</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>43</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>燃气内燃机</td>
      <td>元件名称</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '杰瑞/J612'}</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>WaterSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>80.0</td>
      <td>constant</td>
      <td>供水温度</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>ExhaustTemperature</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>300.0</td>
      <td>constant</td>
      <td>烟气温度</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>SlackNodeMode</td>
      <td>choice</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>参考节点模式</td>
      <td>{'0': '电力系统参考点', '1': '热力系统参考点'}</td>
    </tr>
  </tbody>
</table>


### 负荷

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Load</td>
      <td>负荷</td>
      <td>17000</td>
      <td>heatelec</td>
      <td>70</td>
      <td>0</td>
      <td>Load</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>dimx</th>
      <th>dimy</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(ElectircalLoad!=0)</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(HeatingLoad!=0)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(CoolingLoad!=0)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>44</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(SteamLoad!=0)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>41</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### LoadSettings

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>负荷</td>
      <td>负荷名称</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>ElectircalLoad</td>
      <td>choice</td>
      <td>0</td>
      <td>电负荷</td>
      <td>{'0': '无', '1': '居住片区电负荷', '2': '滨湖核心服务区电负荷', '3': '食品生产工业片区电负荷', '4': '工业研发片区电负荷', '5': '装备制造工业片区电负荷'}</td>
    </tr>
    <tr>
      <td>HeatingLoad</td>
      <td>choice</td>
      <td>0</td>
      <td>采暖负荷</td>
      <td>{'0': '无', '1': '沪苏产业联动集聚区管委会负荷', '2': '能源站内负荷'}</td>
    </tr>
    <tr>
      <td>CoolingLoad</td>
      <td>choice</td>
      <td>0</td>
      <td>制冷负荷</td>
      <td>{'0': '无'}</td>
    </tr>
    <tr>
      <td>SteamLoad</td>
      <td>choice</td>
      <td>0</td>
      <td>蒸汽制热负荷</td>
      <td>{'0': '无', '1': '江苏人酒业', '2': '明珠重工', '3': '紫菜精深加工', '4': '思凯林家居', '5': '奥为节能科技', '6': '翔牛食品', '7': '电巴新能源', '8': '海丰米业', '9': '人民医院', '10': '世贸天阶制药', '11': '维德木业', '12': '久王（铵盐）', '13': '英伦倍健'}</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ReturnHeatWaterTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>40.0</td>
      <td>constant</td>
      <td>热水回水温度</td>
      <td>HeatingLoad!=0</td>
    </tr>
    <tr>
      <td>ReturnColdWaterTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>-10.0</td>
      <td>50.0</td>
      <td>25.0</td>
      <td>constant</td>
      <td>冷水回水温度</td>
      <td>CoolingLoad!=0</td>
    </tr>
  </tbody>
</table>


### 换热器

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HeatExchanger</td>
      <td>换热器</td>
      <td>16000</td>
      <td>heat</td>
      <td>24</td>
      <td>0</td>
      <td>HeatExchanger</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>42</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>43</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>43</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>换热器</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HeatFliudType</td>
      <td>choice</td>
      <td>0</td>
      <td>热流体类型</td>
      <td>{'0': '烟气', '1': '热水'}</td>
      <td></td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '无锡科技/BR1.0'}</td>
      <td></td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
      <th>cond</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HeatWaterOutletTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>70.0</td>
      <td>constant</td>
      <td>热流体(水)回水温度</td>
      <td>HeatFliudType==1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>IsExhaustOutletTempSpecified</td>
      <td>choice</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>热流体(烟气)出口温度是否指定</td>
      <td>HeatFliudType==0</td>
      <td>{'0': '否', '1': '是'}</td>
      <td></td>
    </tr>
    <tr>
      <td>ExhaustOutletTemp</td>
      <td>real</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>200.0</td>
      <td>constant</td>
      <td>热流体(烟气)出口温度</td>
      <td>HeatFliudType==0&amp;&amp;IsExhaustOutletTempSpecified==1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>IsExhaustInletPressureSpecified</td>
      <td>choice</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>热流体(烟气)进口压力是否指定</td>
      <td>HeatFliudType==0</td>
      <td>{'0': '否', '1': '是'}</td>
      <td></td>
    </tr>
    <tr>
      <td>ExhaustInletPressure</td>
      <td>real</td>
      <td>MPa</td>
      <td>0.0</td>
      <td>99.0</td>
      <td>2.0</td>
      <td>constant</td>
      <td>热流体(烟气)进口压力</td>
      <td>HeatFliudType==0&amp;&amp;IsExhaustInletPressureSpecified==1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>ColdFluidOutletTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>60.0</td>
      <td>constant</td>
      <td>冷流体(水)出口温度</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>


### 尾气排放装置

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ExhaustTreater</td>
      <td>尾气排放装置</td>
      <td>16000</td>
      <td>heat</td>
      <td>13</td>
      <td>0</td>
      <td>ExhaustTreater</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>43</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>尾气排放装置</td>
      <td>元件名称</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>desc</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>IsExhaustPressureSpecified</td>
      <td>choice</td>
      <td>0.0</td>
      <td>{'0': '否', '1': '是'}</td>
      <td>进口烟气压力是否指定</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>ExhaustPressure</td>
      <td>real</td>
      <td>2.0</td>
      <td>NaN</td>
      <td>进口烟气压力</td>
      <td>MPa</td>
      <td>0.0</td>
      <td>99.0</td>
      <td>constant</td>
      <td>IsExhaustPressureSpecified==1</td>
    </tr>
  </tbody>
</table>


### 离心泵

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Pump</td>
      <td>离心泵</td>
      <td>16000</td>
      <td>heatelec</td>
      <td>41</td>
      <td>0</td>
      <td>NewPump</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>desc</th>
      <th>dimx</th>
      <th>dimy</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td></td>
      <td></td>
      <td></td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(MediaType==0)</td>
      <td>泵入口</td>
      <td>1</td>
      <td>1</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(MediaType==0)</td>
      <td>泵出口</td>
      <td>1</td>
      <td>1</td>
      <td>42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(MediaType==1)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>44</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(MediaType==1)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>离心泵</td>
      <td>元件名称</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{}</td>
    </tr>
    <tr>
      <td>MediaType</td>
      <td>choice</td>
      <td>0</td>
      <td>介质类型</td>
      <td>{'0': '热水', '1': '冷水'}</td>
    </tr>
  </tbody>
</table>


### 蒸汽轮机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SteamTurbine</td>
      <td>蒸汽轮机</td>
      <td>10000</td>
      <td>heatelec</td>
      <td>25</td>
      <td>0</td>
      <td>NewSteamTurbine</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>41</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>蒸汽轮机</td>
      <td>元件名称</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选（作为参考点）'}</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
      <th>choices</th>
      <th>coldef</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SteamPressure</td>
      <td>real</td>
      <td>MPa</td>
      <td>0.0</td>
      <td>99.0</td>
      <td>2.0</td>
      <td>constant</td>
      <td>蒸汽压力</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>IsSlackNode</td>
      <td>choice</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0</td>
      <td>NaN</td>
      <td>是否作为电力系统参考点</td>
      <td>{'0': '否', '1': '是'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>OperationStrategy</td>
      <td>table</td>
      <td>[h, 台]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>[]</td>
      <td>NaN</td>
      <td>机组运行策略</td>
      <td>NaN</td>
      <td>[时间, 启动机组台数]</td>
      <td>0.0</td>
      <td>2016.0</td>
      <td>IsSlackNode==0</td>
    </tr>
  </tbody>
</table>


### 电容器

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Capacitance</td>
      <td>电容器</td>
      <td>15000</td>
      <td>electrical</td>
      <td>8</td>
      <td>0</td>
      <td>Capacitance</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>电容器</td>
      <td>元件名称</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{}</td>
    </tr>
  </tbody>
</table>


### 蓄冰空调

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>IceStorageAC</td>
      <td>蓄冰空调</td>
      <td>14000</td>
      <td>heatelec</td>
      <td>72</td>
      <td>0</td>
      <td>IceStorageAC</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>蓄冰空调</td>
      <td>元件名称</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{}</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
      <th>coldef</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>-20.0</td>
      <td>50.0</td>
      <td>15.0</td>
      <td>constant</td>
      <td>供水温度</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>OperationStrategy</td>
      <td>table</td>
      <td>[h, 台]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>[]</td>
      <td>NaN</td>
      <td>机组运行策略</td>
      <td>[时间, 启动机组台数（正放负充）]</td>
      <td>0.0</td>
      <td>2016.0</td>
    </tr>
  </tbody>
</table>


### 蓄热电锅炉

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HeatStorageElectricalBoiler</td>
      <td>蓄热电锅炉</td>
      <td>14000</td>
      <td>heatelec</td>
      <td>18</td>
      <td>0</td>
      <td>HeatStorageElectricalBoile</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>inputType</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>蓄热电锅炉</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{}</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>用电计价模型</td>
      <td>{'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'}</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HeatingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供热过网计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
      <th>coldef</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>60.0</td>
      <td>constant</td>
      <td>供水温度</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>OperationStrategy</td>
      <td>table</td>
      <td>[h, 台]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>[]</td>
      <td>NaN</td>
      <td>机组运行策略</td>
      <td>[时间, 启动机组台数（正放负充）]</td>
      <td>0.0</td>
      <td>2016.0</td>
    </tr>
  </tbody>
</table>


### 余热锅炉

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HeatRecoveryBoiler</td>
      <td>余热锅炉</td>
      <td>11000</td>
      <td>heat</td>
      <td>31</td>
      <td>0</td>
      <td>HeatRecoveryBoiler</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>43</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>43</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>BoilerType==0</td>
      <td>42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>BoilerType==1&amp;&amp;PressureLevel==0</td>
      <td>41</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-1</td>
      <td></td>
      <td>BoilerType==1&amp;&amp;PressureLevel==1</td>
      <td>41</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-1</td>
      <td></td>
      <td>BoilerType==1&amp;&amp;PressureLevel==1</td>
      <td>41</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>余热锅炉</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>BoilerType</td>
      <td>choice</td>
      <td>0</td>
      <td>锅炉类型</td>
      <td>{'0': '热水锅炉', '1': '蒸汽锅炉'}</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>PressureLevel</td>
      <td>choice</td>
      <td>0</td>
      <td>压力等级</td>
      <td>{'0': '单压', '1': '双压'}</td>
      <td>BoilerType==1</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选（作为参考点）'}</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
      <th>cond</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>WaterSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>80.0</td>
      <td>constant</td>
      <td>供水温度</td>
      <td>BoilerType==0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>SteamSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>500.0</td>
      <td>180.0</td>
      <td>constant</td>
      <td>蒸汽温度</td>
      <td>BoilerType==1&amp;&amp;PressureLevel==0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>SubSteamSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>500.0</td>
      <td>150.0</td>
      <td>constant</td>
      <td>次高压蒸汽温度</td>
      <td>BoilerType==1&amp;&amp;PressureLevel==1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HighSteamSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>500.0</td>
      <td>200.0</td>
      <td>constant</td>
      <td>高压蒸汽温度</td>
      <td>BoilerType==1&amp;&amp;PressureLevel==1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>IsExhaustOutletTempSpecified</td>
      <td>choice</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>烟气出口温度是否指定</td>
      <td>NaN</td>
      <td>{'0': '否', '1': '是'}</td>
    </tr>
    <tr>
      <td>ExhaustOutletTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>300.0</td>
      <td>constant</td>
      <td>烟气出口温度</td>
      <td>IsExhaustOutletTempSpecified==1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>IsExhaustPressureSepecified</td>
      <td>choice</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>烟气进口压力是否指定</td>
      <td>NaN</td>
      <td>{'0': '否', '1': '是'}</td>
    </tr>
    <tr>
      <td>InletExhaustPressure</td>
      <td>real</td>
      <td>MPa</td>
      <td>0.0</td>
      <td>99.0</td>
      <td>0.5</td>
      <td>constant</td>
      <td>烟气进口压力</td>
      <td>IsExhaustPressureSepecified==1</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>


### 充电桩

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ChargingPile</td>
      <td>充电桩</td>
      <td>17000</td>
      <td>electrical</td>
      <td>65</td>
      <td>0</td>
      <td>ChargingPile</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>dimx</th>
      <th>dimy</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### LoadSettings

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>充电桩</td>
      <td>充电桩名称</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>ChargingPileLoad</td>
      <td>choice</td>
      <td>0</td>
      <td>充电桩负荷</td>
      <td>{'0': '无', '1': '居住片区电负荷', '2': '滨湖核心服务区电负荷', '3': '食品生产工业片区电负荷', '4': '工业研发片区电负荷', '5': '装备制造工业片区电负荷'}</td>
    </tr>
  </tbody>
</table>


### 储水罐

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>WaterTank</td>
      <td>储水罐</td>
      <td>14001</td>
      <td>heat</td>
      <td>9</td>
      <td>0</td>
      <td>WaterTank</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>储水罐</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>InitialWaterLevel</td>
      <td>real</td>
      <td>m</td>
      <td>1.0</td>
      <td>99.0</td>
      <td>3.0</td>
      <td>constant</td>
      <td>初始水位高度</td>
    </tr>
    <tr>
      <td>InitialWaterTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>999.0</td>
      <td>25.0</td>
      <td>constant</td>
      <td>初始水温</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MaxLevelDifference</td>
      <td>real</td>
      <td>%</td>
      <td>0.0</td>
      <td>100.0</td>
      <td>20.0</td>
      <td>constant</td>
      <td>始末最大水位差</td>
    </tr>
    <tr>
      <td>MaxTemperatureDifference</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>100.0</td>
      <td>20.0</td>
      <td>constant</td>
      <td>始末最大水温差</td>
    </tr>
  </tbody>
</table>


### 模块化多电平变流器

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>MMC</td>
      <td>模块化多电平变流器</td>
      <td>15001</td>
      <td>electrical</td>
      <td>46</td>
      <td>0</td>
      <td>MMC</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>desc</th>
      <th>dimx</th>
      <th>dimy</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>Sending (i) Pin</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>Receiving (j) Pin</td>
      <td>1</td>
      <td>1</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>cond</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>模块化多电平变流器</td>
      <td>元件名称</td>
      <td>true</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>NaN</td>
      <td>{'0': '设备类型待选'}</td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>desc</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ControlStyle</td>
      <td>choice</td>
      <td>0.0</td>
      <td>{'0': '控制交流侧PQ', '1': '控制交流侧PV', '2': '控制交流侧Vθ', '3': '控制直流侧V交流侧Q', '4': '控制直流侧V交流侧V'}</td>
      <td>控制方式</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>ACP</td>
      <td>real</td>
      <td>100.0</td>
      <td>NaN</td>
      <td>交流有功</td>
      <td>kW</td>
      <td>0.0</td>
      <td>1000000.0</td>
      <td>constant</td>
      <td>ControlStyle==0 || ControlStyle==1</td>
    </tr>
    <tr>
      <td>ACQ</td>
      <td>real</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>交流无功</td>
      <td>kW</td>
      <td>0.0</td>
      <td>1000000.0</td>
      <td>constant</td>
      <td>ControlStyle==0 || ControlStyle==3</td>
    </tr>
    <tr>
      <td>ACV</td>
      <td>real</td>
      <td>10.0</td>
      <td>NaN</td>
      <td>交流电压</td>
      <td>kV</td>
      <td>0.0</td>
      <td>1000000.0</td>
      <td>constant</td>
      <td>ControlStyle==1 || ControlStyle==2 || ControlStyle==4</td>
    </tr>
    <tr>
      <td>ACTHETA</td>
      <td>real</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>交流相角</td>
      <td>deg</td>
      <td>-360.0</td>
      <td>360.0</td>
      <td>constant</td>
      <td>ControlStyle==2</td>
    </tr>
    <tr>
      <td>DCV</td>
      <td>real</td>
      <td>10.0</td>
      <td>NaN</td>
      <td>直流电压</td>
      <td>kV</td>
      <td>0.0</td>
      <td>1000000.0</td>
      <td>constant</td>
      <td>ControlStyle==3 || ControlStyle==4</td>
    </tr>
  </tbody>
</table>


### 光伏系统

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>PhotovoltaicSys</td>
      <td>光伏系统</td>
      <td>10001</td>
      <td>electrical</td>
      <td>44</td>
      <td>0</td>
      <td>PhotovoltaicSys</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==0)</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==1)</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>光伏系统</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CompType</td>
      <td>choice</td>
      <td>0</td>
      <td>元件类型</td>
      <td>{'0': '交流元件（含逆变器）', '1': '直流元件'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>real</td>
      <td>1.0</td>
      <td>设备配置台数</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>1000000000.0</td>
      <td>constant</td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
      <th>coldef</th>
      <th>colType</th>
      <th>unit</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PowerMode</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '由气象参数计算', '1': '指定出力曲线'}</td>
      <td></td>
      <td>出力模式</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>Strategy</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>启停策略</td>
      <td>[开始时间, 设备启动台数]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"Unit","Value":1,"Parameter type":"Real","Help":"","Condition":""}]</td>
      <td>[None, 台]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>PowerMode==0</td>
    </tr>
    <tr>
      <td>PowerCurve</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>出力曲线</td>
      <td>[开始时间, 发电功率]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"Unit","Value":100,"Parameter type":"Real","Help":"","Condition":""}]</td>
      <td>[, kW]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>PowerMode==1</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OptimizationChoice</td>
      <td>choice</td>
      <td>1</td>
      <td>{'0': '否，使用仿真策略', '1': '是'}</td>
      <td></td>
      <td>是否优化该设备</td>
      <td>PowerMode ==0</td>
    </tr>
  </tbody>
</table>


### 风机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>WindPowerGenerator</td>
      <td>风机</td>
      <td>10001</td>
      <td>electrical</td>
      <td>37</td>
      <td>0</td>
      <td>WindPowerGenerator</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==0)</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==1)</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>风机</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CompType</td>
      <td>choice</td>
      <td>0</td>
      <td>元件类型</td>
      <td>{'0': '交流元件', '1': '直流元件'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>real</td>
      <td>1.0</td>
      <td>设备配置台数</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>20.0</td>
      <td>constant</td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
      <th>coldef</th>
      <th>colType</th>
      <th>unit</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PowerMode</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '由气象参数计算', '1': '指定出力曲线'}</td>
      <td></td>
      <td>出力模式</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>OperateParam</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>启停策略</td>
      <td>[开始时间, 设备启动台数]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"Unit","Value":1,"Parameter type":"Real","Help":"","Condition":""}]</td>
      <td>[None, 台]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>PowerMode==0</td>
    </tr>
    <tr>
      <td>PowerCurve</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>出力曲线</td>
      <td>[时间, 发电功率]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"Unit","Value":100.0,"Parameter type":"Real","Help":"","Condition":""}]</td>
      <td>[, kW]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>PowerMode==1</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OptimizationChoice</td>
      <td>choice</td>
      <td>1</td>
      <td>{'0': '否，使用仿真策略', '1': '是'}</td>
      <td></td>
      <td>是否优化该设备</td>
    </tr>
  </tbody>
</table>


### 交流变压器

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Transformer</td>
      <td>交流变压器</td>
      <td>15001</td>
      <td>electrical</td>
      <td>24</td>
      <td>0</td>
      <td>Transformer</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
      <th>isVisible</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)</td>
      <td>1.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)</td>
      <td>1.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td></td>
      <td>NaN</td>
      <td>False</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td></td>
      <td>NaN</td>
      <td>False</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>交流变压器</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
    </tr>
  </tbody>
</table>


### 离心泵

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CentrifugalPump</td>
      <td>离心泵</td>
      <td>16001</td>
      <td>heatelec</td>
      <td>55</td>
      <td>0</td>
      <td>CentrifugalPump</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>desc</th>
      <th>dimx</th>
      <th>dimy</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==0)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==1)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>离心泵</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CompType</td>
      <td>choice</td>
      <td>0</td>
      <td>元件类型</td>
      <td>{'0': '交流元件', '1': '直流元件'}</td>
      <td></td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>coldef</th>
      <th>colType</th>
      <th>unit</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PumpSpeed</td>
      <td>table</td>
      <td>[]</td>
      <td>[开始时间, 转速]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"RotationSpeed","Value":2900,"Parameter type":"Real","Help":"","Condition":""}]</td>
      <td>[None, rpm]</td>
      <td>0</td>
      <td>9999</td>
      <td>离心泵转速</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OptimizationChoice</td>
      <td>choice</td>
      <td>1</td>
      <td>{'0': '否，使用仿真策略', '1': '是'}</td>
      <td></td>
      <td>是否优化该设备</td>
    </tr>
  </tbody>
</table>


### 传输线

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>TransferLine</td>
      <td>传输线</td>
      <td>15001</td>
      <td>electrical</td>
      <td>24</td>
      <td>0</td>
      <td>TransferLine</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==0)</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==0)</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==1)</td>
      <td>44</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==1)</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>传输线</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CompType</td>
      <td>choice</td>
      <td>0</td>
      <td>元件类型</td>
      <td>{'0': '交流元件', '1': '直流元件'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>Length</td>
      <td>real</td>
      <td>1.0</td>
      <td>长度</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>km</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备型号待选'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>


### 电压缩制冷机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CompRefrg</td>
      <td>电压缩制冷机</td>
      <td>11001</td>
      <td>heatelec</td>
      <td>115</td>
      <td>0</td>
      <td>CompRefrg</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==0)</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==1)</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>电压缩制冷机</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CompType</td>
      <td>choice</td>
      <td>0</td>
      <td>元件类型</td>
      <td>{'0': '交流元件', '1': '直流元件'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>real</td>
      <td>1.0</td>
      <td>设备配置台数</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>20.0</td>
      <td>constant</td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
      <th>coldef</th>
      <th>colType</th>
      <th>unit</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SettingParaType</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '供水温度', '1': '制冷功率'}</td>
      <td></td>
      <td>设定参数类型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>OutletTemp</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>温度模式运行策略</td>
      <td>[开始时间, 供水温度]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"Temperature","Value":10,"Parameter type":"Real","Help":"","Condition":""}]</td>
      <td>[None, ℃]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>SettingParaType==0</td>
    </tr>
    <tr>
      <td>CoolSupply</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>功率模式运行策略</td>
      <td>[开始时间, 设备启停运行策略]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"OperateParam","Value":{"default_value":[1,10],"type":"table","value":[[1,10]],"coldef":["挡位","台数"],"unit":["",""],"desc":"设备启停运行策略"},"Parametertype":"Table","Help":"","Condition":""}]</td>
      <td>[None, ]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>SettingParaType==1</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OptimizationChoice</td>
      <td>choice</td>
      <td>1</td>
      <td>{'0': '否，使用仿真策略', '1': '是'}</td>
      <td></td>
      <td>是否优化该设备</td>
    </tr>
  </tbody>
</table>


### 采暖制冷负荷

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ThermalLoad</td>
      <td>采暖制冷负荷</td>
      <td>17001</td>
      <td>heat</td>
      <td>89</td>
      <td>0</td>
      <td>ThermalLoad</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)</td>
      <td>42</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)</td>
      <td>42</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>unit</th>
      <th>inputType</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>采暖制冷负荷</td>
      <td>负荷名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>LocalPressureDropCoe</td>
      <td>real</td>
      <td>100.0</td>
      <td>局部压降系数</td>
      <td>kPa/(m³·s⁻¹)²</td>
      <td>constant</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HeatingLoad</td>
      <td>choice</td>
      <td>0</td>
      <td>采暖制冷负荷</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>{'0': '无'}</td>
      <td></td>
    </tr>
    <tr>
      <td>HeatPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>采暖计价模型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>{'0': '无'}</td>
      <td></td>
    </tr>
    <tr>
      <td>CoolingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>用冷计价模型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>{'0': '无'}</td>
      <td></td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MiniOutletColdTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>5.0</td>
      <td>constant</td>
      <td>制冷时最小出口温度</td>
    </tr>
    <tr>
      <td>MaxOutletColdTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>40.0</td>
      <td>constant</td>
      <td>制冷时最大出口温度</td>
    </tr>
    <tr>
      <td>MiniOutletHeatTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>30.0</td>
      <td>constant</td>
      <td>供热时最小出口温度</td>
    </tr>
    <tr>
      <td>MaxOutletHeatTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>90.0</td>
      <td>constant</td>
      <td>供热时最大出口温度</td>
    </tr>
  </tbody>
</table>


### 电负荷

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ElectricalLoad</td>
      <td>电负荷</td>
      <td>17001</td>
      <td>electrical</td>
      <td>83</td>
      <td>0</td>
      <td>ElectricalLoad</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>dimx</th>
      <th>dimy</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==0)</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==1)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>电负荷</td>
      <td>负荷名称</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CompType</td>
      <td>choice</td>
      <td>0</td>
      <td>元件类型</td>
      <td>{'0': '交流元件', '1': '直流元件'}</td>
      <td></td>
    </tr>
    <tr>
      <td>ElectircalLoad</td>
      <td>choice</td>
      <td>0</td>
      <td>电负荷</td>
      <td>{'0': '无'}</td>
      <td></td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>用电计价模型（收入）</td>
      <td>{'0': '无'}</td>
      <td></td>
    </tr>
  </tbody>
</table>


### 燃气锅炉

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GasBoiler</td>
      <td>燃气锅炉</td>
      <td>11001</td>
      <td>heat</td>
      <td>119</td>
      <td>0</td>
      <td>GasBoiler</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>42</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>42</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>燃气锅炉</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>real</td>
      <td>1.0</td>
      <td>设备配置台数</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>20.0</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>FuelPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>燃料计价模型</td>
      <td>{'0': '无'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
      <th>coldef</th>
      <th>colType</th>
      <th>unit</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SettingParaType</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '供水温度', '1': '加热功率'}</td>
      <td></td>
      <td>设定参数类型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>OutletTemp</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>温度模式运行策略</td>
      <td>[开始时间, 供水温度]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"Temperature","Value":80,"Parameter type":"Real","Help":"","Condition":""}]</td>
      <td>[None, ℃]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>SettingParaType==0</td>
    </tr>
    <tr>
      <td>HeatPower</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>功率模式运行策略</td>
      <td>[开始时间, 加热功率]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"OperateParam","Value":{"default_value":["1","10"],"type":"table","value":[["1","10"]],"coldef":["挡位","台数"],"unit":["",""],"desc":"设备启停运行策略"},"Parametertype":"Table","Help":"","Condition":""}]</td>
      <td>[None, kW]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>SettingParaType==1</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OptimizationChoice</td>
      <td>choice</td>
      <td>1</td>
      <td>{'0': '否，使用仿真策略', '1': '是'}</td>
      <td></td>
      <td>是否优化该设备</td>
    </tr>
  </tbody>
</table>


### 热泵

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HeatPump</td>
      <td>热泵</td>
      <td>11001</td>
      <td>heatelec</td>
      <td>107</td>
      <td>0</td>
      <td>HeatPump</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==0)</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==1)</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>热泵</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CompType</td>
      <td>choice</td>
      <td>0</td>
      <td>元件类型</td>
      <td>{'0': '交流元件', '1': '直流元件'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>real</td>
      <td>1.0</td>
      <td>设备配置台数</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>20.0</td>
      <td>constant</td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
      <th>coldef</th>
      <th>colType</th>
      <th>unit</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SettingParaType</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '供水温度', '1': '制冷制热功率'}</td>
      <td></td>
      <td>设定参数类型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>OutletTemp</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>温度模式运行策略</td>
      <td>[开始时间, 供水温度]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"Temperature","Value":80,"Parameter type":"Real","Help":"","Condition":""}]</td>
      <td>[None, ℃]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>SettingParaType==0</td>
    </tr>
    <tr>
      <td>EnergySupply</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>功率模式运行策略</td>
      <td>[开始时间, 设备启停运行策略]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"OperateParam","Value":{"default_value":["1","1"],"type":"table","value":[["1","1"]],"coldef":["挡位","台数"],"unit":["",""]},"Parametertype":"Table","Help":"","Condition":""}]</td>
      <td>[None, ]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>SettingParaType==1</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OptimizationChoice</td>
      <td>choice</td>
      <td>1</td>
      <td>{'0': '否，使用仿真策略', '1': '是'}</td>
      <td></td>
      <td>是否优化该设备</td>
    </tr>
  </tbody>
</table>


### 燃气轮机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GasTurbine</td>
      <td>燃气轮机</td>
      <td>10001</td>
      <td>heatelec</td>
      <td>48</td>
      <td>0</td>
      <td>GasTurbine</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==0)</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==1)</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>燃气轮机</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CompType</td>
      <td>choice</td>
      <td>0</td>
      <td>元件类型</td>
      <td>{'0': '交流元件', '1': '直流元件'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>real</td>
      <td>1.0</td>
      <td>设备配置台数</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>20.0</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>FuelPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>燃料计价模型（支出）</td>
      <td>{'0': '无'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
      <th>coldef</th>
      <th>colType</th>
      <th>unit</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SettingParaType</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '供水温度', '1': '发电功率'}</td>
      <td></td>
      <td>设定参数类型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>OutletTemp</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>温度模式运行策略</td>
      <td>[开始时间, 供水温度]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"Temperature","Value":100,"Parameter type":"Real","Help":"","Condition":""}]</td>
      <td>[None, ℃]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>SettingParaType==0</td>
    </tr>
    <tr>
      <td>PowerGenerating</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>功率模式运行策略</td>
      <td>[开始时间, 设备启停运行策略]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"OperateParam","Value":{"default_value":[1,10],"type":"table","value":[[1,10]],"coldef":["挡位","台数"],"unit":["",""],"desc":"设备启停运行策略"},"Parametertype":"Table","Help":"","Condition":""}]</td>
      <td>[None, ]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>SettingParaType==1</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OptimizationChoice</td>
      <td>choice</td>
      <td>1</td>
      <td>{'0': '否，使用仿真策略', '1': '是'}</td>
      <td></td>
      <td>是否优化该设备</td>
    </tr>
  </tbody>
</table>


### 蓄电池

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Battery</td>
      <td>蓄电池</td>
      <td>14001</td>
      <td>electrical</td>
      <td>44</td>
      <td>0</td>
      <td>Battery</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==0)</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==1)</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>蓄电池</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CompType</td>
      <td>choice</td>
      <td>0</td>
      <td>元件类型</td>
      <td>{'0': '交流元件(含变流器)', '1': '直流元件'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>real</td>
      <td>1.0</td>
      <td>设备配置台数</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>20.0</td>
      <td>constant</td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
      <th>coldef</th>
      <th>colType</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>InitialPowerStorage</td>
      <td>real</td>
      <td>kWh</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>1000.0</td>
      <td>constant</td>
      <td>初始蓄电量</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>Power</td>
      <td>table</td>
      <td>[None, kW]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>[]</td>
      <td>NaN</td>
      <td>充放功率（正充负放）</td>
      <td>[开始时间, 充放功率(正充负放)]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"Power","Value":100,"Parameter type":"Real","Help":"","Condition":""}]</td>
      <td>0.0</td>
      <td>9999.0</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OptimizationChoice</td>
      <td>choice</td>
      <td>1.0</td>
      <td>{'0': '否，使用仿真策略', '1': '是'}</td>
      <td></td>
      <td>是否优化该设备</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MaxPowerStorageDiff</td>
      <td>real</td>
      <td>10.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>蓄电量始末最大偏差比例</td>
      <td>%</td>
      <td>0.0</td>
      <td>100.0</td>
      <td>constant</td>
      <td>OptimizationChoice==1</td>
    </tr>
  </tbody>
</table>


### 吸收式制冷机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AbsorptionChiller</td>
      <td>吸收式制冷机</td>
      <td>11001</td>
      <td>heatelec</td>
      <td>101</td>
      <td>0</td>
      <td>AbsorptionChiller</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==0)</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)</td>
      <td>42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)</td>
      <td>42</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)</td>
      <td>42</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==1)</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>吸收式制冷机</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CompType</td>
      <td>choice</td>
      <td>0</td>
      <td>元件类型</td>
      <td>{'0': '交流元件', '1': '直流元件'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>real</td>
      <td>1.0</td>
      <td>设备配置台数</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>20.0</td>
      <td>constant</td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
      <th>coldef</th>
      <th>colType</th>
      <th>unit</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SettingParaType</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '供水温度', '1': '制冷功率'}</td>
      <td></td>
      <td>设定参数类型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>OutletTemp</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>温度模式运行策略</td>
      <td>[开始时间, 冷水侧供水温度]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"Temperature","Value":10,"Parameter type":"Real","Help":"","Condition":""}]</td>
      <td>[None, ℃]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>SettingParaType==0</td>
    </tr>
    <tr>
      <td>CoolSupply</td>
      <td>table</td>
      <td>[]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>功率模式运行策略</td>
      <td>[开始时间, 设备启停运行策略]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"OperateParam","Value":{"default_value":[1,1],"type":"table","value":[[1,1]],"coldef":["挡位","台数"],"unit":["",""]},"Parametertype":"Table","Help":"","Condition":""}]</td>
      <td>[None, None]</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>SettingParaType==1</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OptimizationChoice</td>
      <td>choice</td>
      <td>1</td>
      <td>{'0': '否，使用仿真策略', '1': '是'}</td>
      <td></td>
      <td>是否优化该设备</td>
    </tr>
  </tbody>
</table>


### 柔性电负荷

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>FlexElectricalLoad</td>
      <td>柔性电负荷</td>
      <td>17001</td>
      <td>electrical</td>
      <td>86</td>
      <td>0</td>
      <td>FlexElectricalLoad</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>dimx</th>
      <th>dimy</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==0)</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(CompType==1)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>电负荷</td>
      <td>负荷名称</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CompType</td>
      <td>choice</td>
      <td>0</td>
      <td>元件类型</td>
      <td>{'0': '交流元件', '1': '直流元件'}</td>
      <td></td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>用电计价模型（收入）</td>
      <td>{'0': '无'}</td>
      <td></td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ElectircalLoad</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '无'}</td>
      <td></td>
      <td>电负荷</td>
    </tr>
  </tbody>
</table>

##### OptimizationParamters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OptimizationChoice</td>
      <td>choice</td>
      <td>1.0</td>
      <td>{'0': '否，使用仿真负荷', '1': '是'}</td>
      <td></td>
      <td>是否优化该负荷</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MaxLoad</td>
      <td>real</td>
      <td>1000.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>最大负荷</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>constant</td>
      <td>OptimizationChoice==1</td>
    </tr>
  </tbody>
</table>


### 建筑物冷热负荷围护模型

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HouseLoad</td>
      <td>建筑物冷热负荷围护模型</td>
      <td>17001</td>
      <td>heat</td>
      <td>91</td>
      <td>0</td>
      <td>HouseLoad</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)</td>
      <td>42</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)</td>
      <td>42</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>unit</th>
      <th>inputType</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>建筑物冷热负荷围护模型</td>
      <td>负荷名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>LocalPressureDropCoe</td>
      <td>real</td>
      <td>100.0</td>
      <td>局部压降系数</td>
      <td>kPa/(m³·s⁻¹)²</td>
      <td>constant</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HeatPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>采暖计价模型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>{'0': '无'}</td>
      <td></td>
    </tr>
    <tr>
      <td>CoolingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>用冷计价模型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>{'0': '无'}</td>
      <td></td>
    </tr>
  </tbody>
</table>

##### HouseParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HousePerimeter</td>
      <td>real</td>
      <td>m</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>70.00</td>
      <td>constant</td>
      <td>围护结构周长</td>
    </tr>
    <tr>
      <td>FloorArea</td>
      <td>real</td>
      <td>m²</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>80.00</td>
      <td>constant</td>
      <td>建筑占地面积</td>
    </tr>
    <tr>
      <td>HouseHeight</td>
      <td>real</td>
      <td>m</td>
      <td>0.0</td>
      <td>999.0</td>
      <td>8.00</td>
      <td>constant</td>
      <td>建筑高度</td>
    </tr>
    <tr>
      <td>PanelArea</td>
      <td>real</td>
      <td>m²</td>
      <td>0.0</td>
      <td>99999.0</td>
      <td>10.00</td>
      <td>constant</td>
      <td>冷/热媒与室内的有效换热面积</td>
    </tr>
    <tr>
      <td>WallThick</td>
      <td>real</td>
      <td>mm</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>200.00</td>
      <td>constant</td>
      <td>墙体厚度</td>
    </tr>
    <tr>
      <td>WallDensity</td>
      <td>real</td>
      <td>kg/m³</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>2400.00</td>
      <td>constant</td>
      <td>墙体密度</td>
    </tr>
    <tr>
      <td>WallHeatConductivity</td>
      <td>real</td>
      <td>W/(m·K)</td>
      <td>0.0</td>
      <td>99.0</td>
      <td>0.20</td>
      <td>constant</td>
      <td>墙体导热系数</td>
    </tr>
    <tr>
      <td>WallHeatCapacity</td>
      <td>real</td>
      <td>kJ/(kg·℃)</td>
      <td>0.0</td>
      <td>99.0</td>
      <td>1.00</td>
      <td>constant</td>
      <td>墙体比热容</td>
    </tr>
    <tr>
      <td>WallRadAbsorbCoe</td>
      <td>real</td>
      <td>None</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.65</td>
      <td>constant</td>
      <td>墙体辐射吸收系数</td>
    </tr>
    <tr>
      <td>WindowAreaRatio</td>
      <td>real</td>
      <td>%</td>
      <td>0.0</td>
      <td>100.0</td>
      <td>65.00</td>
      <td>constant</td>
      <td>窗面占比</td>
    </tr>
    <tr>
      <td>WindowHeatTransCoe</td>
      <td>real</td>
      <td>W/(m²·℃)</td>
      <td>0.0</td>
      <td>99.0</td>
      <td>2.00</td>
      <td>constant</td>
      <td>窗户传热系数</td>
    </tr>
    <tr>
      <td>FurnitureTotalHeatCapacity</td>
      <td>real</td>
      <td>kJ/℃</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>100.00</td>
      <td>constant</td>
      <td>家具总热容</td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>InitialTemperature</td>
      <td>real</td>
      <td>℃</td>
      <td>-50.0</td>
      <td>50.0</td>
      <td>25.0</td>
      <td>constant</td>
      <td>室内初始温度</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MiniIndoorTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>20.0</td>
      <td>constant</td>
      <td>最低室温</td>
    </tr>
    <tr>
      <td>MaxIndoorTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>28.0</td>
      <td>constant</td>
      <td>最高室温</td>
    </tr>
  </tbody>
</table>


### 直流变压器

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>FullBridgeConverter</td>
      <td>直流变压器</td>
      <td>15001</td>
      <td>electrical</td>
      <td>29</td>
      <td>0</td>
      <td>FullBridgeConverter</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>44</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>直流变压器</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>D</td>
      <td>real</td>
      <td>0.25</td>
      <td>占空比</td>
      <td>None</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>n</td>
      <td>real</td>
      <td>2.0</td>
      <td>隔离变压器变比</td>
      <td>None</td>
      <td>0.0</td>
      <td>99999.0</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>RT1</td>
      <td>real</td>
      <td>0.25</td>
      <td>隔离变压器1次侧漏电阻</td>
      <td>Ω</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>RT2</td>
      <td>real</td>
      <td>0.04</td>
      <td>隔离变压器2次侧漏电阻</td>
      <td>Ω</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>RD</td>
      <td>real</td>
      <td>0.075</td>
      <td>二极管导通电阻</td>
      <td>Ω</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>RL</td>
      <td>real</td>
      <td>0.72</td>
      <td>隔离变压器2次侧励磁电阻</td>
      <td>Ω</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>constant</td>
    </tr>
  </tbody>
</table>


### 管道

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Pipe</td>
      <td>管道</td>
      <td>16001</td>
      <td>heat</td>
      <td>13</td>
      <td>0</td>
      <td>Pipe</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>42</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>42</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>管道</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>Length</td>
      <td>real</td>
      <td>200.0</td>
      <td>管道长度</td>
      <td>m</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>constant</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>{}</td>
      <td></td>
    </tr>
  </tbody>
</table>


### 外部电源

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ExternalPowerSource</td>
      <td>外部电源</td>
      <td>10001</td>
      <td>electrical</td>
      <td>36</td>
      <td>0</td>
      <td>ExternalPowerSource-1</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>外部电源(参考节点)</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>PurchasePriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>购电计价模型（支出）</td>
      <td>{'0': '无'}</td>
      <td></td>
    </tr>
    <tr>
      <td>SalePriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>上网计价模型（收入）</td>
      <td>{'0': '无'}</td>
      <td></td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Voltage</td>
      <td>real</td>
      <td>kV</td>
      <td>110.0</td>
      <td>constant</td>
      <td>电压</td>
    </tr>
    <tr>
      <td>Angle</td>
      <td>real</td>
      <td>deg</td>
      <td>0.0</td>
      <td>constant</td>
      <td>相角</td>
    </tr>
  </tbody>
</table>


### 热管式太阳能集热器

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HPSolarCollector</td>
      <td>热管式太阳能集热器</td>
      <td>11001</td>
      <td>heat</td>
      <td>48</td>
      <td>0</td>
      <td>HPSolarCollector</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>42</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>42</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>热管式太阳能集热器</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备配置台数</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>100000000.0</td>
      <td>constant</td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>coldef</th>
      <th>colType</th>
      <th>unit</th>
      <th>minrowcount</th>
      <th>maxrowcount</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Strategy</td>
      <td>table</td>
      <td>[]</td>
      <td>[开始时间, 设备启动台数]</td>
      <td>[{"Key":"Time","Value":"2021-01-01 08:00:00","Parameter type":"Text","Help":"","Condition":""}, {"Key":"Unit","Value":1,"Parameter type":"Real","Help":"","Condition":""}]</td>
      <td>[, ]</td>
      <td>0</td>
      <td>10000</td>
      <td>启停策略</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>choiceSource</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OptimizationChoice</td>
      <td>choice</td>
      <td>1</td>
      <td>{'0': '否，使用仿真策略', '1': '是'}</td>
      <td></td>
      <td>是否优化该设备</td>
    </tr>
  </tbody>
</table>


### 储气罐

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AirTank</td>
      <td>储气罐</td>
      <td>14000</td>
      <td>heat</td>
      <td>11</td>
      <td>0</td>
      <td>AirTank</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>43</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>43</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>储气罐</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>InitialWaterLevel</td>
      <td>real</td>
      <td>m</td>
      <td>1.0</td>
      <td>99.0</td>
      <td>3.0</td>
      <td>constant</td>
      <td>初始水位高度</td>
    </tr>
    <tr>
      <td>InitialWaterTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>999.0</td>
      <td>25.0</td>
      <td>constant</td>
      <td>初始水温</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MaxLevelDifference</td>
      <td>real</td>
      <td>%</td>
      <td>0.0</td>
      <td>100.0</td>
      <td>20.0</td>
      <td>constant</td>
      <td>始末最大水位差</td>
    </tr>
    <tr>
      <td>MaxTemperatureDifference</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>100.0</td>
      <td>20.0</td>
      <td>constant</td>
      <td>始末最大水温差</td>
    </tr>
  </tbody>
</table>


### 压气机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Compressor</td>
      <td>压气机</td>
      <td>16000</td>
      <td>heatelec</td>
      <td>13</td>
      <td>0</td>
      <td>Compressor</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>43</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>压气机</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>InitialWaterLevel</td>
      <td>real</td>
      <td>m</td>
      <td>1.0</td>
      <td>99.0</td>
      <td>3.0</td>
      <td>constant</td>
      <td>初始水位高度</td>
    </tr>
    <tr>
      <td>InitialWaterTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>999.0</td>
      <td>25.0</td>
      <td>constant</td>
      <td>初始水温</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MaxLevelDifference</td>
      <td>real</td>
      <td>%</td>
      <td>0.0</td>
      <td>100.0</td>
      <td>20.0</td>
      <td>constant</td>
      <td>始末最大水位差</td>
    </tr>
    <tr>
      <td>MaxTemperatureDifference</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>100.0</td>
      <td>20.0</td>
      <td>constant</td>
      <td>始末最大水温差</td>
    </tr>
  </tbody>
</table>


### 透平发电机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>TurbineGenerator</td>
      <td>透平发电机</td>
      <td>10000</td>
      <td>heatelec</td>
      <td>14</td>
      <td>0</td>
      <td>TurbineGenerator</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>43</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### BasicParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>choiceSource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>透平发电机</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td></td>
    </tr>
  </tbody>
</table>

##### SimuParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>InitialWaterLevel</td>
      <td>real</td>
      <td>m</td>
      <td>1.0</td>
      <td>99.0</td>
      <td>3.0</td>
      <td>constant</td>
      <td>初始水位高度</td>
    </tr>
    <tr>
      <td>InitialWaterTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>999.0</td>
      <td>25.0</td>
      <td>constant</td>
      <td>初始水温</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MaxLevelDifference</td>
      <td>real</td>
      <td>%</td>
      <td>0.0</td>
      <td>100.0</td>
      <td>20.0</td>
      <td>constant</td>
      <td>始末最大水位差</td>
    </tr>
    <tr>
      <td>MaxTemperatureDifference</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>100.0</td>
      <td>20.0</td>
      <td>constant</td>
      <td>始末最大水温差</td>
    </tr>
  </tbody>
</table>



## 规划设计参数

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>参数分类</th>
      <th>中文名称</th>
      <th>有关设备</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>DeviceParameters</td>
      <td>机组参数, 设备参数, 母线参数</td>
      <td>母线, 吸收式制冷机, 蓄电池, 电容器, 电压缩制冷机, 尾气排放装置, 燃气锅炉, 余热锅炉, 换热器, 热泵, 蓄热电锅炉, 热管式太阳能集热器, 蓄冰空调, 光伏系统, 管道, 离心泵, 传输线, 变压器, 风机, 蒸汽轮机, 燃气轮机, 燃气内燃机, 外部电源</td>
    </tr>
    <tr>
      <td>OperationParameters</td>
      <td>运行参数组</td>
      <td>吸收式制冷机, 电压缩制冷机, 尾气排放装置, 燃气锅炉, 余热锅炉, 换热器, 热泵, 蓄热电锅炉, 热管式太阳能集热器, 蓄冰空调, 负荷, 蒸汽轮机, 燃气轮机, 燃气内燃机, 外部电源</td>
    </tr>
    <tr>
      <td>ComputingParameters</td>
      <td>计算参数组</td>
      <td>蓄电池, 电压缩制冷机, 燃气锅炉, 热泵, 蒸汽轮机, 燃气轮机, 燃气内燃机</td>
    </tr>
    <tr>
      <td>LoadSettings</td>
      <td>负荷设置</td>
      <td>负荷</td>
    </tr>
  </tbody>
</table>

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

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BusNode</td>
      <td>母线</td>
      <td>15000</td>
      <td>electrical</td>
      <td>1</td>
      <td>0</td>
      <td>BusNode</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>cond</th>
      <th>unit</th>
      <th>inputType</th>
      <th>choices</th>
      <th>help</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Name</td>
      <td>text</td>
      <td></td>
      <td>母线名称</td>
      <td>true</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>VBase</td>
      <td>real</td>
      <td>115.0</td>
      <td>额定电压</td>
      <td>true</td>
      <td>kV</td>
      <td>constant</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>V</td>
      <td>real</td>
      <td>1.0</td>
      <td>电压</td>
      <td>true</td>
      <td>pu</td>
      <td>constant</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>Angle</td>
      <td>real</td>
      <td>0.0</td>
      <td>相角</td>
      <td>true</td>
      <td>deg</td>
      <td>constant</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>NodeType</td>
      <td>choice</td>
      <td>1</td>
      <td>节点类型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>{'1': 'PQBus', '2': 'PVBus', '3': 'SlackBus'}</td>
      <td>节点类型</td>
    </tr>
  </tbody>
</table>


### 吸收式制冷机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AbsorptionChiller</td>
      <td>吸收式制冷机</td>
      <td>11000</td>
      <td>heatelec</td>
      <td>59</td>
      <td>0</td>
      <td>NewAbsorptionChiller</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(HeatSourceType==0)</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(HeatSourceType==1)</td>
      <td>41</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(HeatSourceType==2)</td>
      <td>43</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(HeatSourceType==2)</td>
      <td>43</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>44</td>
    </tr>
    <tr>
      <th>6</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>inputType</th>
      <th>cond</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>吸收式制冷机</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HeatSourceType</td>
      <td>choice</td>
      <td>0</td>
      <td>热源流体类型</td>
      <td>{'0': '热水', '1': '蒸汽', '2': '烟气'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '东星/dx-30wd'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniCoolSupply</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小制冷功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MaxCoolSupply</td>
      <td>real</td>
      <td>1000.0</td>
      <td>最大制冷功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniHeatSupply</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小制热功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>MaxHeatSupply</td>
      <td>real</td>
      <td>1000.0</td>
      <td>最大制热功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>HeatingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>热水用热计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>HeatSourceType==0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>SteamPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>蒸汽用热计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>HeatSourceType==1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CoolSupplyPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供冷过网计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HeatSupplyPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供热过网计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>desc</th>
      <th>cond</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>IsSourceReturnTempSpecified</td>
      <td>choice</td>
      <td>0.0</td>
      <td>{'0': '否', '1': '是'}</td>
      <td>热源流体出口温度是否指定</td>
      <td>HeatSourceType==2</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>SourceReturnTemp</td>
      <td>real</td>
      <td>50.0</td>
      <td>NaN</td>
      <td>热源流体出口温度</td>
      <td>HeatSourceType==0||(HeatSourceType==2&amp;&amp;IsSourceReturnTempSpecified==1)</td>
      <td>℃</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>IsSourcePressureSpecified</td>
      <td>choice</td>
      <td>0.0</td>
      <td>{'0': '否', '1': '是'}</td>
      <td>热源流体进口压力是否指定</td>
      <td>HeatSourceType==2</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>SourceInletPressure</td>
      <td>real</td>
      <td>0.5</td>
      <td>NaN</td>
      <td>热源流体进口压力</td>
      <td>(HeatSourceType==2&amp;&amp;IsSourcePressureSpecified==1)||HeatSourceType==1</td>
      <td>MPa</td>
      <td>0.0</td>
      <td>99.0</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>ColdWaterSupplyTemp</td>
      <td>real</td>
      <td>10.0</td>
      <td>NaN</td>
      <td>冷水出口温度</td>
      <td>NaN</td>
      <td>℃</td>
      <td>-20.0</td>
      <td>99.0</td>
      <td>constant</td>
    </tr>
    <tr>
      <td>HeatWaterSupplyTemp</td>
      <td>real</td>
      <td>60.0</td>
      <td>NaN</td>
      <td>热水出口温度</td>
      <td>NaN</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>constant</td>
    </tr>
  </tbody>
</table>


### 蓄电池

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Battery</td>
      <td>蓄电池</td>
      <td>14000</td>
      <td>electrical</td>
      <td>19</td>
      <td>0</td>
      <td>NewBattery</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
      <th>cond</th>
      <th>unit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>蓄电池</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '盛弘电气/PWS2-250K'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniPowerStorage</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小蓄电量</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kWh</td>
    </tr>
    <tr>
      <td>MaxPowerStorage</td>
      <td>real</td>
      <td>1000.0</td>
      <td>最大蓄电量</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kWh</td>
    </tr>
    <tr>
      <td>ChargingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>用电计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DischargingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供电上网计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### ComputingParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>IsSlackNode</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '否', '1': '是'}</td>
      <td>是否作为系统参考节点</td>
    </tr>
  </tbody>
</table>


### 电容器

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Capacitance</td>
      <td>电容器</td>
      <td>15000</td>
      <td>electrical</td>
      <td>11</td>
      <td>0</td>
      <td>NewCapacitance</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>电容器</td>
      <td>元件名称</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{}</td>
    </tr>
  </tbody>
</table>


### 电压缩制冷机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CompRefrg</td>
      <td>电压缩制冷机</td>
      <td>11000</td>
      <td>heatelec</td>
      <td>58</td>
      <td>0</td>
      <td>NewCompRefrg</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>inputType</th>
      <th>cond</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>电压缩制冷机</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '凯德利/KDSL02050P'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniCoolSupply</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小制冷量</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>99999999.0</td>
    </tr>
    <tr>
      <td>MaxCoolSupply</td>
      <td>real</td>
      <td>10000.0</td>
      <td>最大制冷量</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>99999999.0</td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>用电计价模型</td>
      <td>{'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CoolingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供冷过网计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>-20.0</td>
      <td>99.0</td>
      <td>15.0</td>
      <td>constant</td>
      <td>供水温度</td>
    </tr>
  </tbody>
</table>

##### ComputingParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>IsSlackNode</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '否', '1': '是'}</td>
      <td>是否作为系统参考节点</td>
    </tr>
  </tbody>
</table>


### 尾气排放装置

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ExhaustTreater</td>
      <td>尾气排放装置</td>
      <td>16000</td>
      <td>heat</td>
      <td>11</td>
      <td>0</td>
      <td>NewExhaustTreater</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>43</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>尾气排放装置</td>
      <td>元件名称</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>desc</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>IsExhaustPressureSpecified</td>
      <td>choice</td>
      <td>0.0</td>
      <td>{'0': '否', '1': '是'}</td>
      <td>进口烟气压力是否指定</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>ExhaustPressure</td>
      <td>real</td>
      <td>2.0</td>
      <td>NaN</td>
      <td>进口烟气压力</td>
      <td>MPa</td>
      <td>0.0</td>
      <td>99.0</td>
      <td>constant</td>
      <td>IsExhaustPressureSpecified==1</td>
    </tr>
  </tbody>
</table>


### 燃气锅炉

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GasBoiler</td>
      <td>燃气锅炉</td>
      <td>11000</td>
      <td>heat</td>
      <td>93</td>
      <td>0</td>
      <td>NewGasBoiler</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>BoilerType==0</td>
      <td>42</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>BoilerType==1</td>
      <td>41</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>inputType</th>
      <th>cond</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>燃气锅炉</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>BoilerType</td>
      <td>choice</td>
      <td>0</td>
      <td>锅炉类型</td>
      <td>{'0': '热水锅炉', '1': '蒸汽锅炉'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '泰康锅炉/SZS10-2.5-YQ', '2': '泰康锅炉/SZS40-2.5-YQ'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniHeatSupply</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小制热功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>MaxHeatSupply</td>
      <td>real</td>
      <td>1000.0</td>
      <td>最大制热功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>FuelPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>燃料计价模型</td>
      <td>{'0': '无', '1': '天然气-居民'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HeatingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供热过网计价模型</td>
      <td>{'0': '无', '1': '燃气电站供热价格'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SteamSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>500.0</td>
      <td>180.0</td>
      <td>constant</td>
      <td>蒸汽温度</td>
      <td>BoilerType==1</td>
    </tr>
    <tr>
      <td>WaterSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>80.0</td>
      <td>constant</td>
      <td>供水温度</td>
      <td>BoilerType==0</td>
    </tr>
  </tbody>
</table>

##### ComputingParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>IsSlackNode</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '否', '1': '是'}</td>
      <td>是否作为系统参考节点</td>
    </tr>
  </tbody>
</table>


### 余热锅炉

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HeatRecoveryBoiler</td>
      <td>余热锅炉</td>
      <td>11000</td>
      <td>heat</td>
      <td>24</td>
      <td>0</td>
      <td>NewHeatRecoveryBoiler</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>43</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>43</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>BoilerType==0</td>
      <td>42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>BoilerType==1&amp;&amp;PressureLevel==0</td>
      <td>41</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-1</td>
      <td></td>
      <td>BoilerType==1&amp;&amp;PressureLevel==1</td>
      <td>41</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-1</td>
      <td></td>
      <td>BoilerType==1&amp;&amp;PressureLevel==1</td>
      <td>41</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>cond</th>
      <th>min</th>
      <th>inputType</th>
      <th>unit</th>
      <th>max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>余热蒸汽锅炉</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>BoilerType</td>
      <td>choice</td>
      <td>0</td>
      <td>锅炉类型</td>
      <td>{'0': '热水锅炉', '1': '蒸汽锅炉'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>PressureLevel</td>
      <td>choice</td>
      <td>0</td>
      <td>压力等级</td>
      <td>{'0': '单压', '1': '双压'}</td>
      <td>BoilerType==1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '郑锅股份/QC110/625-22-3.82/450'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>DeviceSelection!=0</td>
      <td>1.0</td>
      <td>constant</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniHeatSupply</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小制热功率</td>
      <td>NaN</td>
      <td>DeviceSelection==0</td>
      <td>0.0</td>
      <td>constant</td>
      <td>kW</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>MaxHeatSupply</td>
      <td>real</td>
      <td>1000.0</td>
      <td>最大制热功率</td>
      <td>NaN</td>
      <td>DeviceSelection==0</td>
      <td>0.0</td>
      <td>constant</td>
      <td>kW</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>HeatingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供热过网计价模型</td>
      <td>{'0': '无', '1': '燃气电站供热价格'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
      <th>cond</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>WaterSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>80.0</td>
      <td>constant</td>
      <td>供水温度</td>
      <td>BoilerType==0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>SteamSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>500.0</td>
      <td>180.0</td>
      <td>constant</td>
      <td>蒸汽温度</td>
      <td>BoilerType==1&amp;&amp;PressureLevel==0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>SubSteamSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>500.0</td>
      <td>150.0</td>
      <td>constant</td>
      <td>次高压蒸汽温度</td>
      <td>BoilerType==1&amp;&amp;PressureLevel==1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HighSteamSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>500.0</td>
      <td>200.0</td>
      <td>constant</td>
      <td>高压蒸汽温度</td>
      <td>BoilerType==1&amp;&amp;PressureLevel==1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>IsExhaustOutletTempSpecified</td>
      <td>choice</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>烟气出口温度是否指定</td>
      <td>NaN</td>
      <td>{'0': '否', '1': '是'}</td>
    </tr>
    <tr>
      <td>ExhaustOutletTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>300.0</td>
      <td>constant</td>
      <td>烟气出口温度</td>
      <td>IsExhaustOutletTempSpecified==1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>IsExhaustPressureSepecified</td>
      <td>choice</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>烟气进口压力是否指定</td>
      <td>NaN</td>
      <td>{'0': '否', '1': '是'}</td>
    </tr>
    <tr>
      <td>InletExhaustPressure</td>
      <td>real</td>
      <td>MPa</td>
      <td>0.0</td>
      <td>99.0</td>
      <td>0.5</td>
      <td>constant</td>
      <td>烟气进口压力</td>
      <td>IsExhaustPressureSepecified==1</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>


### 换热器

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HeatExchanger</td>
      <td>换热器</td>
      <td>16000</td>
      <td>heat</td>
      <td>14</td>
      <td>0</td>
      <td>NewHeatExchanger</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>HeatFliudType==0</td>
      <td>43</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>HeatFliudType==0</td>
      <td>43</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>HeatFliudType==1</td>
      <td>42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>42</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>inputType</th>
      <th>cond</th>
      <th>unit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>换热器</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HeatFliudType</td>
      <td>choice</td>
      <td>0</td>
      <td>热流体类型</td>
      <td>{'0': '烟气', '1': '热水'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '无锡科技/BR1.0'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniHeatExchange</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小换热量</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
    </tr>
    <tr>
      <td>MaxHeatExchange</td>
      <td>real</td>
      <td>1000.0</td>
      <td>最大换热量</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
    </tr>
    <tr>
      <td>HeatFluidPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>用热计价模型</td>
      <td>{'0': '无', '1': '燃气电站供热价格'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>ColdFluidPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供热过网计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
      <th>cond</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HeatWaterOutletTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>70.0</td>
      <td>constant</td>
      <td>热流体(水)回水温度</td>
      <td>HeatFliudType==1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>IsExhaustOutletTempSpecified</td>
      <td>choice</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>热流体(烟气)出口温度是否指定</td>
      <td>HeatFliudType==0</td>
      <td>{'0': '否', '1': '是'}</td>
    </tr>
    <tr>
      <td>ExhaustOutletTemp</td>
      <td>real</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>200.0</td>
      <td>constant</td>
      <td>热流体(烟气)出口温度</td>
      <td>HeatFliudType==0&amp;&amp;IsExhaustOutletTempSpecified==1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>IsExhaustInletPressureSpecified</td>
      <td>choice</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>热流体(烟气)进口压力是否指定</td>
      <td>HeatFliudType==0</td>
      <td>{'0': '否', '1': '是'}</td>
    </tr>
    <tr>
      <td>ExhaustInletPressure</td>
      <td>real</td>
      <td>MPa</td>
      <td>0.0</td>
      <td>99.0</td>
      <td>2.0</td>
      <td>constant</td>
      <td>热流体(烟气)进口压力</td>
      <td>HeatFliudType==0&amp;&amp;IsExhaustInletPressureSpecified==1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>ColdFluidOutletTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>60.0</td>
      <td>constant</td>
      <td>冷流体(水)出口温度</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>


### 热泵

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HeatPump</td>
      <td>热泵</td>
      <td>11000</td>
      <td>heatelec</td>
      <td>78</td>
      <td>0</td>
      <td>NewHeatPump</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>inputType</th>
      <th>cond</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>热泵</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '华誉能源/R22'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniHeatSupply</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小制热功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>MaxHeatSupply</td>
      <td>real</td>
      <td>1000.0</td>
      <td>最大制热功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>MiniCoolSupply</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小制冷功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>MaxCoolSupply</td>
      <td>real</td>
      <td>1000.0</td>
      <td>最大制冷功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>用电计价模型</td>
      <td>{'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HeatingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供热过网计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CoolingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供冷过网计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HeatingSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>50.0</td>
      <td>constant</td>
      <td>热水出口温度</td>
    </tr>
    <tr>
      <td>CoolingSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>-10.0</td>
      <td>50.0</td>
      <td>5.0</td>
      <td>constant</td>
      <td>冷水出口温度</td>
    </tr>
  </tbody>
</table>

##### ComputingParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>IsHeatSlackNode</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '否', '1': '是'}</td>
      <td>供热时是否作为系统参考节点</td>
    </tr>
    <tr>
      <td>IsCoolSlackNode</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '否', '1': '是'}</td>
      <td>供冷时是否作为系统参考节点</td>
    </tr>
  </tbody>
</table>


### 蓄热电锅炉

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HeatStorageElectricalBoiler</td>
      <td>蓄热电锅炉</td>
      <td>14000</td>
      <td>heatelec</td>
      <td>13</td>
      <td>0</td>
      <td>NewHeatStorageElectricalBoile</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>inputType</th>
      <th>cond</th>
      <th>unit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>蓄热电锅炉</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniHeatStorage</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小蓄热量</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kWh</td>
    </tr>
    <tr>
      <td>MaxHeatStorage</td>
      <td>real</td>
      <td>1000.0</td>
      <td>最大蓄热量</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kWh</td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>用电计价模型</td>
      <td>{'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HeatingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供热过网计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>60.0</td>
      <td>constant</td>
      <td>供水温度</td>
    </tr>
  </tbody>
</table>


### 热管式太阳能集热器

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HPSolarCollector</td>
      <td>热管式太阳能集热器</td>
      <td>11000</td>
      <td>heat</td>
      <td>31</td>
      <td>0</td>
      <td>NewHPSolarCollector</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>42</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>unit</th>
      <th>inputType</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>热管式太阳能集热器</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': 'VITOSOL/222-T'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>real</td>
      <td>1.0</td>
      <td>安装台数</td>
      <td>NaN</td>
      <td>None</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
    </tr>
    <tr>
      <td>MiniInstallArea</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小安装面积</td>
      <td>NaN</td>
      <td>m2</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
    </tr>
    <tr>
      <td>MaxInstallArea</td>
      <td>real</td>
      <td>10000.0</td>
      <td>最大安装面积</td>
      <td>NaN</td>
      <td>None</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
    </tr>
    <tr>
      <td>HeatingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供热过网计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>60.0</td>
      <td>constant</td>
      <td>供水温度</td>
    </tr>
  </tbody>
</table>


### 蓄冰空调

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>IceStorageAC</td>
      <td>蓄冰空调</td>
      <td>14000</td>
      <td>heatelec</td>
      <td>68</td>
      <td>0</td>
      <td>NewIceStorageAC</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>inputType</th>
      <th>cond</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>蓄冰空调</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '光华创世/GC-ICU-587-P'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniCoolStorage</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小蓄冷量</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kWh</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>MaxCoolStorage</td>
      <td>real</td>
      <td>1000.0</td>
      <td>最大蓄冷量</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kWh</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>用电计价模型</td>
      <td>{'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CoolingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供冷过网计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>-20.0</td>
      <td>50.0</td>
      <td>15.0</td>
      <td>constant</td>
      <td>供水温度</td>
    </tr>
  </tbody>
</table>


### 负荷

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Load</td>
      <td>负荷</td>
      <td>17000</td>
      <td>heatelec</td>
      <td>62</td>
      <td>0</td>
      <td>NewLoad</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>dimx</th>
      <th>dimy</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==2)&amp;&amp;(ElectircalLoad!=0)</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(HeatingLoad!=0)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(CoolingLoad!=0)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>44</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(SteamLoad!=0)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>41</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### LoadSettings

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>负荷</td>
      <td>负荷名称</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>ElectircalLoad</td>
      <td>choice</td>
      <td>0</td>
      <td>电负荷</td>
      <td>{'0': '无', '1': '居住片区电负荷', '2': '滨湖核心服务区电负荷', '3': '食品生产工业片区电负荷', '4': '工业研发片区电负荷', '5': '装备制造工业片区电负荷'}</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>用电计价模型</td>
      <td>{'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'}</td>
      <td>ElectircalLoad!=0</td>
    </tr>
    <tr>
      <td>HeatingLoad</td>
      <td>choice</td>
      <td>0</td>
      <td>采暖负荷</td>
      <td>{'0': '无', '1': '沪苏产业联动集聚区管委会负荷', '2': '能源站内负荷'}</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HeatPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>采暖计价模型</td>
      <td>{'0': '无'}</td>
      <td>HeatingLoad!=0</td>
    </tr>
    <tr>
      <td>CoolingLoad</td>
      <td>choice</td>
      <td>0</td>
      <td>制冷负荷</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>CoolingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>制冷计价模型</td>
      <td>{'0': '无'}</td>
      <td>CoolingLoad!=0</td>
    </tr>
    <tr>
      <td>SteamLoad</td>
      <td>choice</td>
      <td>0</td>
      <td>蒸汽制热负荷</td>
      <td>{'0': '无', '1': '江苏人酒业', '2': '明珠重工', '3': '紫菜精深加工', '4': '思凯林家居', '5': '奥为节能科技', '6': '翔牛食品', '7': '电巴新能源', '8': '海丰米业', '9': '人民医院', '10': '世贸天阶制药', '11': '维德木业', '12': '久王（铵盐）', '13': '英伦倍健'}</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>SteamPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>蒸气计价模型</td>
      <td>{'0': '无', '1': '燃气电站供热价格'}</td>
      <td>SteamLoad!=0</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ReturnHeatWaterTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>40.0</td>
      <td>constant</td>
      <td>热水回水温度</td>
      <td>HeatingLoad!=0</td>
    </tr>
    <tr>
      <td>ReturnColdWaterTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>-10.0</td>
      <td>50.0</td>
      <td>15.0</td>
      <td>constant</td>
      <td>冷水回水温度</td>
      <td>CoolingLoad!=0</td>
    </tr>
  </tbody>
</table>


### 光伏系统

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>PhotovoltaicSys</td>
      <td>光伏系统</td>
      <td>10000</td>
      <td>electrical</td>
      <td>21</td>
      <td>0</td>
      <td>PhotovoltaicSys</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
      <th>cond</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>光伏系统</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>real</td>
      <td>100.0</td>
      <td>安装台数</td>
      <td>NaN</td>
      <td>m2</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
    </tr>
    <tr>
      <td>MiniInstallArea</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小安装面积</td>
      <td>NaN</td>
      <td>m2</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
    </tr>
    <tr>
      <td>MaxInstallArea</td>
      <td>real</td>
      <td>1000.0</td>
      <td>最大安装面积</td>
      <td>NaN</td>
      <td>m2</td>
      <td>0.0</td>
      <td>99999999.0</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>发电上网计价模型</td>
      <td>{'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>


### 管道

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Pipe</td>
      <td>管道</td>
      <td>16000</td>
      <td>heat</td>
      <td>8</td>
      <td>0</td>
      <td>NewPipe</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>MediaType==0</td>
      <td>42</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>MediaType==0</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>MediaType==1</td>
      <td>44</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>MediaType==1</td>
      <td>44</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-1</td>
      <td></td>
      <td>MediaType==2</td>
      <td>41</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-1</td>
      <td></td>
      <td>MediaType==2</td>
      <td>41</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>管道</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>Length</td>
      <td>real</td>
      <td>200.0</td>
      <td>管道长度</td>
      <td>m</td>
      <td>0.0</td>
      <td>999999.0</td>
      <td>constant</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MediaType</td>
      <td>choice</td>
      <td>0</td>
      <td>流通介质类型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>{'0': '热水', '1': '冷水', '2': '蒸汽'}</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>{}</td>
    </tr>
  </tbody>
</table>


### 离心泵

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Pump</td>
      <td>离心泵</td>
      <td>16000</td>
      <td>heatelec</td>
      <td>40</td>
      <td>0</td>
      <td>NewPump</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>desc</th>
      <th>dimx</th>
      <th>dimy</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td></td>
      <td></td>
      <td></td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(MediaType==0)</td>
      <td>泵入口</td>
      <td>1</td>
      <td>1</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(MediaType==0)</td>
      <td>泵出口</td>
      <td>1</td>
      <td>1</td>
      <td>42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(MediaType==1)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>44</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-1</td>
      <td></td>
      <td>(!show_pin||show_pin==3)&amp;&amp;(MediaType==1)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>44</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>离心泵</td>
      <td>元件名称</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{}</td>
    </tr>
    <tr>
      <td>MediaType</td>
      <td>choice</td>
      <td>0</td>
      <td>介质类型</td>
      <td>{'0': '热水', '1': '冷水'}</td>
    </tr>
  </tbody>
</table>


### 传输线

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>TransferLine</td>
      <td>传输线</td>
      <td>15000</td>
      <td>electrical</td>
      <td>18</td>
      <td>0</td>
      <td>TransferLine</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>inputType</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>传输线</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>Length</td>
      <td>real</td>
      <td>1.0</td>
      <td>传输线长度</td>
      <td>km</td>
      <td>0.0</td>
      <td>9999.0</td>
      <td>constant</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>{}</td>
    </tr>
  </tbody>
</table>


### 变压器

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Transformer</td>
      <td>变压器</td>
      <td>15000</td>
      <td>electrical</td>
      <td>13</td>
      <td>0</td>
      <td>Transformer</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>变压器</td>
      <td>元件名称</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{}</td>
    </tr>
  </tbody>
</table>


### 风机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>WindPowerGenerator</td>
      <td>风机</td>
      <td>10000</td>
      <td>electrical</td>
      <td>19</td>
      <td>0</td>
      <td>WindPowerGenerator</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>min</th>
      <th>inputType</th>
      <th>cond</th>
      <th>unit</th>
      <th>max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>风机</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniDeviceNumber</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小风机台数</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>NaN</td>
      <td>9999.0</td>
    </tr>
    <tr>
      <td>MaxDeviceNumber</td>
      <td>integer</td>
      <td>20</td>
      <td>最大风机台数</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>NaN</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>发电过网计价模型</td>
      <td>{'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>


### 蒸汽轮机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SteamTurbine</td>
      <td>蒸汽轮机</td>
      <td>10000</td>
      <td>heatelec</td>
      <td>22</td>
      <td>0</td>
      <td>NewSteamTurbine</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>41</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>inputType</th>
      <th>cond</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>蒸汽轮机</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '青能动力/QFW-8-4'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniPowerGenerate</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小发电功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>MaxPowerGenerate</td>
      <td>real</td>
      <td>10000.0</td>
      <td>最大发电功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>发电过网计价模型</td>
      <td>{'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>SteamUsePriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>蒸汽用热计价模型</td>
      <td>{'0': '无', '1': '燃气电站供热价格'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SteamPressure</td>
      <td>real</td>
      <td>MPa</td>
      <td>0.0</td>
      <td>99.0</td>
      <td>2.0</td>
      <td>constant</td>
      <td>蒸汽压力</td>
    </tr>
  </tbody>
</table>

##### ComputingParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>IsSlackNode</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '否', '1': '是'}</td>
      <td>是否作为系统参考节点</td>
    </tr>
  </tbody>
</table>


### 燃气轮机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GasTurbine</td>
      <td>燃气轮机</td>
      <td>10000</td>
      <td>heatelec</td>
      <td>24</td>
      <td>0</td>
      <td>GasTurbine</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>43</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>inputType</th>
      <th>cond</th>
      <th>unit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>燃气轮机</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '西门子/SGT-800', '2': '东汽日立/H-25(42)', '3': '南汽/PG6581B', '4': '南汽/GT-6F.01', '5': '华电/LM6000PF', '6': '普惠/FT8'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniPowerGenerate</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小发电功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
    </tr>
    <tr>
      <td>MaxPowerGenerate</td>
      <td>real</td>
      <td>100000.0</td>
      <td>最大发电功率</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
    </tr>
    <tr>
      <td>FuelPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>燃料计价模型</td>
      <td>{'0': '无', '1': '天然气-居民'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>发电过网计价模型</td>
      <td>{'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ExhaustTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>500.0</td>
      <td>constant</td>
      <td>烟气温度</td>
    </tr>
  </tbody>
</table>

##### ComputingParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SlackNodeMode</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '不是参考节点', '1': '电力系统参考节点', '2': '热力系统参考节点'}</td>
      <td>参考节点模式</td>
    </tr>
  </tbody>
</table>


### 燃气内燃机

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GasEngine</td>
      <td>燃气内燃机</td>
      <td>10000</td>
      <td>heatelec</td>
      <td>15</td>
      <td>0</td>
      <td>NewGasEngine</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1</td>
      <td></td>
      <td>!show_pin||show_pin==3</td>
      <td>43</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
      <th>inputType</th>
      <th>cond</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>燃气内燃机</td>
      <td>元件名称</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceSelection</td>
      <td>choice</td>
      <td>0</td>
      <td>设备选型</td>
      <td>{'0': '设备类型待选', '1': '杰瑞/J612'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>DeviceNumber</td>
      <td>integer</td>
      <td>1</td>
      <td>设备台数</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection!=0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>MiniPowerGenerate</td>
      <td>real</td>
      <td>0.0</td>
      <td>最小发电量</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>MaxPowerGenerate</td>
      <td>real</td>
      <td>1000.0</td>
      <td>最大发电量</td>
      <td>NaN</td>
      <td>constant</td>
      <td>DeviceSelection==0</td>
      <td>kW</td>
      <td>0.0</td>
      <td>999999.0</td>
    </tr>
    <tr>
      <td>FuelPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>燃料计价模型</td>
      <td>{'0': '无', '1': '天然气-居民'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>PowerPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>发电过网计价模型</td>
      <td>{'0': '无', '1': '燃气电站含税交易电价', '2': '燃气电站含税上网电价', '3': '农光互补光伏电站含税直接交易电价', '4': '农光互补光伏电站含税上网电价', '5': '分布式光伏电站含税直接交易电价', '6': '分布式光伏电站含税上网电价', '7': '风力发电含税直接交易电价', '8': '风力发电含税上网电价', '9': '公共电网购电价'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>HeatingPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供热过网计价模型</td>
      <td>{'0': '无'}</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>max</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>WaterSupplyTemp</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>200.0</td>
      <td>80.0</td>
      <td>constant</td>
      <td>供水温度</td>
    </tr>
    <tr>
      <td>ExhaustTemperature</td>
      <td>real</td>
      <td>℃</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>300.0</td>
      <td>constant</td>
      <td>烟气温度</td>
    </tr>
  </tbody>
</table>

##### ComputingParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>choices</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SlackNodeMode</td>
      <td>choice</td>
      <td>0</td>
      <td>{'0': '不是参考节点', '1': '电力系统参考节点', '2': '热力系统参考节点'}</td>
      <td>参考节点模式</td>
    </tr>
  </tbody>
</table>


### 外部电源

#### 设备信息

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>classname</th>
      <th>name</th>
      <th>type</th>
      <th>thutype</th>
      <th>ver</th>
      <th>id</th>
      <th>sym</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ExternalPowerSource</td>
      <td>外部电源</td>
      <td>10000</td>
      <td>electrical</td>
      <td>27</td>
      <td>0</td>
      <td>ExternalPowerSource</td>
    </tr>
  </tbody>
</table>

#### 针脚定义

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>node</th>
      <th>label</th>
      <th>cond</th>
      <th>conntype</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1</td>
      <td></td>
      <td>true</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

#### 参数填写

##### DeviceParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>value</th>
      <th>desc</th>
      <th>choices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CompName</td>
      <td>text</td>
      <td>外部电源(参考节点)</td>
      <td>元件名称</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>PowerConsumePriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>上网计价模型</td>
      <td>{'0': '无'}</td>
    </tr>
    <tr>
      <td>PowerSupplyPriceModel</td>
      <td>choice</td>
      <td>0</td>
      <td>供电计价模型</td>
      <td>{'0': '无'}</td>
    </tr>
    <tr>
      <td>FuelModel</td>
      <td>choice</td>
      <td>0</td>
      <td>电厂发电燃料模型</td>
      <td>{'0': '无'}</td>
    </tr>
  </tbody>
</table>

##### OperationParameters

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>ID</th>
      <th>type</th>
      <th>unit</th>
      <th>min</th>
      <th>value</th>
      <th>inputType</th>
      <th>desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>BasekV</td>
      <td>real</td>
      <td>kV</td>
      <td>0.0</td>
      <td>115.0</td>
      <td>constant</td>
      <td>基准电压</td>
    </tr>
    <tr>
      <td>Voltage</td>
      <td>real</td>
      <td>pu</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>constant</td>
      <td>电压</td>
    </tr>
    <tr>
      <td>Angle</td>
      <td>real</td>
      <td>deg</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>constant</td>
      <td>相角</td>
    </tr>
  </tbody>
</table>


