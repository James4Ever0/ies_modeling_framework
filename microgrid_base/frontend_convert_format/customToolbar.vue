<template>
  <div class="customToolbarContainer">
    <!-- 左侧节点/放大缩小工具 菜单 -->
    <div class="toolbarContainer">
      <div class="aside-button-group"></div>
      <!-- 左侧节点 -->
      <el-tabs v-model="activeName" type="card" stretch>
        <el-tab-pane label="模型库" name="first">
          <el-collapse v-model="activeNames">
            <!-- 外部能源 -->
            <el-collapse-item name="1" class="custom-toolbar">
              <template slot="title">外部能源</template>
              <span v-for="(item, index) in externalEnergy" style
                :class="{ 'rectangle-node': item['nodeType'] === 'rectangle' }" class="custom-node" :key="item['title']"
                ref="externalEnergy">
                <el-popover placement="right" trigger="hover" :ref="`popoverExter${index}`">
                  <img :src="item['icon']" />
                  <img slot="reference" :src="item['icon']" @mouseenter="handlerMouseenter(index, (tip = 1))" />
                </el-popover>
                <br />
                <span class="node-title">{{ item["title"] }}</span>
              </span>
            </el-collapse-item>
            <!-- 负荷类型 -->
            <el-collapse-item name="2" class="custom-toolbar">
              <template slot="title">负荷类型</template>
              <span v-for="(item, index) in loadType" style
                :class="{ 'rectangle-node': item['nodeType'] === 'rectangle' }" class="custom-node" :key="item['title']"
                ref="loadType">
                <el-popover placement="right" trigger="hover" :ref="`popoverLoad${index}`">
                  <img :src="item['icon']" />
                  <img slot="reference" :src="item['icon']" @mouseenter="handlerMouseenter(index, (tip = 2))" />
                  <!-- <span>{{ item["title"] }}</span> -->
                </el-popover>
                <br />
                <span class="node-title">{{ item["title"] }}</span>
              </span>
            </el-collapse-item>

            <!-- 发电设备 -->
            <el-collapse-item name="3" class="custom-toolbar">
              <template slot="title">发电设备</template>
              <span v-for="(item, index) in electricItems" style
                :class="{ 'rectangle-node': item['nodeType'] === 'rectangle' }" class="custom-node" :key="item['title']"
                ref="electricItems">
                <el-popover placement="right" trigger="hover" :ref="`popoverEle${index}`">
                  <img :src="item['icon']" />
                  <img slot="reference" :src="item['icon']" @mouseenter="handlerMouseenter(index, (tip = 3))" />
                  <!-- <span>{{ item["title"] }}</span> -->
                </el-popover>
                <br />
                <span class="node-title">{{ item["title"] }}</span>
              </span>
            </el-collapse-item>

            <!-- 储能设备 -->
            <el-collapse-item name="4" class="custom-toolbar">
              <template slot="title">储能设备</template>
              <span v-for="(item, index) in energyStorage" style
                :class="{ 'rectangle-node': item['nodeType'] === 'rectangle' }" class="custom-node" :key="item['title']"
                ref="energyStorage">
                <el-popover placement="right" trigger="hover" :ref="`popoverStor${index}`">
                  <img :src="item['icon']" />
                  <img slot="reference" :src="item['icon']" @mouseenter="handlerMouseenter(index, (tip = 4))" />
                  <!-- <span>{{ item["title"] }}</span> -->
                </el-popover>
                <br />
                <span class="node-title">{{ item["title"] }}</span>
              </span>
            </el-collapse-item>
            <!-- 配电传输 -->
            <el-collapse-item name="5" class="custom-toolbar">
              <template slot="title">配电传输</template>
              <span v-for="(item, index) in distributionTransmission" style
                :class="{ 'rectangle-node': item['nodeType'] === 'rectangle' }" class="custom-node" :key="item['title']"
                ref="distributionTransmission">
                <el-popover placement="right" trigger="hover" :ref="`popoverTran${index}`">
                  <img :src="item['icon']" />
                  <img slot="reference" :src="item['icon']" @mouseenter="handlerMouseenter(index, (tip = 5))" />
                  <!-- <span>{{ item["title"] }}</span> -->
                </el-popover>
                <br />
                <span class="node-title">{{ item["title"] }}</span>
              </span>
            </el-collapse-item>
            <!-- 其他 -->
            <el-collapse-item name="6" class="custom-toolbar other">
              <template slot="title">其他</template>
              <span v-for="(item, index) in others" style :class="{ 'rectangle-node': item['nodeType'] === 'rectangle' }"
                class="custom-node" :key="item['title']" ref="others">
                <el-popover placement="right" trigger="hover" :ref="`popoverOth${index}`">
                  <img :src="item['icon']" />
                  <img slot="reference" :src="item['icon']" @mouseenter="handlerMouseenter(index, (tip = 6))" />
                  <!-- <span>{{ item["title"] }}</span> -->
                </el-popover>
                <br />
                <span class="node-title">{{ item["title"] }}</span>
              </span>
              <!-- <span v-for="item in generalToolbarItems" :style="item['style']" :class="item['class']" :key="item['index']"
                ref="generalToolItems">
                <span class="generalTooltitle">{{ item["text"] }}</span>
              </span> -->
            </el-collapse-item>
          </el-collapse>
        </el-tab-pane>
        <!-- <el-tab-pane label="资源库" name="second">
          <el-tree :data="treeData" :expand-on-click-node="false">
            <span class="custom-tree-node" slot-scope="{ node, data }">
              <span @click="appear(node)">{{ node.label }}</span>
              <span>
                <el-button type="text" size="small" @click="() => remove(node, data)">删除</el-button>
              </span>
            </span>
          </el-tree>
        </el-tab-pane>-->
        <el-tab-pane label="资源表" name="thirdly">
          <el-tree :data="resourceData" @node-click="handleNodeClick"></el-tree>
        </el-tab-pane>
      </el-tabs>
    </div>
    <!-- 画布的顶部工具栏 -->
    <div class="top-tools">
      <el-col :span="4">
        <div class="grid-content bg-purple" style="font-weight: 800; font-size: 22px; margin-left: 44px"></div>
      </el-col>
      <el-col :span="12" class="tools-group">
        <el-tooltip class="item" effect="dark" content="放大" placement="bottom">
          <el-button type="text" icon="el-icon-zoom-in" @click="zoomIn"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="缩小" placement="bottom">
          <el-button type="text" icon="el-icon-zoom-out" @click="zoomOut"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="等比缩放" placement="bottom">
          <el-button type="text" icon="el-icon-rank" @click="autoSize"></el-button>
        </el-tooltip>
        <!-- <el-tooltip class="item" effect="dark" content="保存" placement="bottom">
          <el-button type="text" icon="el-icon-check" @click="dialogFormVisible = true"></el-button>
        </el-tooltip> -->
        <el-tooltip class="item" effect="dark" content="组合" placement="bottom">
          <el-button type="text" icon="el-icon-document-copy" @click="enGroup"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="导入xml文件" placement="bottom">
          <el-button type="text" icon="el-icon-upload2" @click="inPutXml"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="导出xml文件" placement="bottom">
          <el-button type="text" icon="el-icon-download" @click="outPutXml"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" v-if="showBackground" content="隐藏网格背景" placement="bottom">
          <el-button type="text" icon="el-icon-s-grid" @click="showBackground = false"></el-button>
        </el-tooltip>
        <el-tooltip v-else class="item" effect="dark" content="显示网格背景" placement="bottom">
          <el-button type="text" icon="el-icon-full-screen" @click="showBackground = true"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="导出为图片" placement="bottom">
          <el-button type="text" icon="el-icon-picture-outline" @click="showImage"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" v-if="showBackground" content="隐藏网格背景" placement="bottom">
          <el-button type="text" icon="el-icon-s-grid" @click="showBackground = false"></el-button>
        </el-tooltip>
        <!-- <el-tooltip
          class="item"
          effect="dark"
          content="树形布局"
          placement="bottom"
        >
          <el-button
            type="text"
            @click="graphLayout(true, 'compactTreeLayout')"
            icon="iconfont icon-Directory-tree"
          ></el-button>
        </el-tooltip>-->
        <el-tooltip class="item" effect="dark" content="随机布局" placement="bottom">
          <el-button type="text" @click="graphLayout(true, 'randomLayout')" icon="el-icon-c-scale-to-original">
          </el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="撤销" placement="bottom">
          <el-button type="text" icon="el-icon-d-arrow-left" @click="goBack"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="前进" placement="bottom">
          <el-button type="text" icon="el-icon-d-arrow-right" @click="goForward"></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="删除" placement="bottom">
          <el-button type="text" icon="el-icon-delete-solid" @click="deleteNode"></el-button>
        </el-tooltip>
      </el-col>
      <el-col :span="3">
        <el-button size="small" @click="saveGraph">保存</el-button>
        <el-button size="small" @click="dialogFormVisible = true">保存至模板库</el-button>
      </el-col>
    </div>
    <!-- 中心画布 -->
    <div class="graphContainer" id="graphContainer" ref="container"
      :class="{ 'graphContainer-background': showBackground }"></div>
    <!-- 收缩小工具 -->
    <div class="show-map" ref="showMap"></div>
    <!-- 右侧栏 -->
    <div class="right-bar">
      <!-- 样式设置 -->
      <style-select @changeDashed="changeDashed" @changeStrokeColor="changeStrokeColor" :id="id"
        @changeStrokeWidth="changeStrokeWidth" @changeFontSize="changeFontSize" @changeFontColor="changeFontColor"
        @changeLabelBackgroundColor="changeLabelBackgroundColor" @changeConfigOrder="changeConfigOrder"
        @changeFillColor="changeFillColor" @changeShadow="changeShadow" @changeFontStyle="changeFontStyle"
        @changeNodeimage="changeNodeimage" @edgeChange="edgeChange" @textValueChange="textValueChange"
        :textValue="textValue" :isNode="isNode" :importData="importData" :cellStyle="cellStyle"
        :currentNormalType="currentNormalType" :graphX="graphX" :graphY="graphY" ref="styleSelect" :key="id"
        :modelnum="modelnum" :modelId="modelId" :modelName="modelName" @pinBlur="pinBlur" :loadSelects="loadSelects"
        :typeSelects="typeSelects" :costModels="costModels" :fuelModels="fuelModels" @saveRightParam="saveRightParam"
        :rightParams="rightParams" @startCompute="startCompute" :start="start" @checkResult="checkResult" />
    </div>
    <!-- XML数据导入/导出 -->
    <upload-data v-if="uploadDataVisible" @uploadPaintFlow="uploadPaintFlow" :graphXml="graphXml"
      :isOutputXml="isOutputXml"></upload-data>

    <!-- 点击保存出现的弹框 -->
    <el-dialog title="请输入模板名称" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="模板名称" label-width="120px">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveModel">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 仿真计算结果 -->
    <el-dialog :visible.sync="showResult" width="80%">
      <div class="down">
        <el-button type="success" @click="downResult">导出结果数据</el-button>
      </div>
      <el-table :data="resultTable" border>
        <el-table-column prop="id" align="center" label="元件标识符">
        </el-table-column>
        <el-table-column prop="name" align="center" label="元件自定义名称">
        </el-table-column>
        <el-table-column prop="powerSupply" align="center" label="供电量(kWh)">
        </el-table-column>
        <el-table-column prop="electricLoad" align="center" label="电负荷(kWh)">
        </el-table-column>
        <el-table-column prop="heatingLoad" align="center" label="供热量(kWh)">
        </el-table-column>
        <el-table-column prop="heatLoad" align="center" label="热负荷(kWh)">
        </el-table-column>
        <el-table-column prop="coolingCapacity" align="center" label="供冷量(kWh)">
        </el-table-column>
        <el-table-column prop="coolingLoad" align="center" label="冷负荷(kWh)">
        </el-table-column>
        <el-table-column prop="equipmentMaintenanceCosts" align="center" label="设备维护费用(万元)">
        </el-table-column>
        <el-table-column prop="electricitySalesRevenue" align="center" label="售电收入(万元)">
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 查看元件表 -->
    <ComponentList @changeDia="changeDia" :checkElementTable="checkElementTable" :componentTable="componentTable">
    </ComponentList>
  </div>
</template>

<script>
import ComponentList from './component/componentList.vue';
// 获取元件类型接口
import { lithiumBatteryList } from '@/api/devicenIformation/energy';
import { dieselOilList, draughtList, lightvList } from '@/api/devicenIformation/index';
import { rectifierList, transformerList, transmissionLineList } from '@/api/devicenIformation/powerDistribution';
import { dieselList } from '@/api/fuel/diesel';
import { electricalLoadList } from '@/api/loadInfo/electricityLoad'
import { saveTopInfo, searchElePrice } from '@/api/topInput/index';
// 导入自定义图标数组
import uploadData from "./component/uploadData";
import { generalToolbarItems } from "./general-shape";
import {
  distributionTransmission,
  electricItems,
  energyStorage,
  externalEnergy,
  loadType,
  others
} from "./toolbar";
// 组元素
import _ from "lodash";
import mx from "mxgraph";
import * as R from "ramda";
import X2JS from "x2js";
import XLSX from "xlsx";
import { grouptoolItems } from "./GroupToolbarItems";
import styleSelect from "./component/styleSelect";
const mxgraph = mx({});

const connectivity_rule = {
    "可连接电母线_双向变流器线路端输入输出": "不可连接电母线输入输出",

    "变流器输入_供电端输出": "不可连接供电端母线",
    "可连接供电端母线_可连接供电端母线": "可合并供电端母线",
    "变流器输入_可连接供电端母线": "不可连接供电端母线输出",
    "可连接供电端母线_供电端输出": "不可连接供电端母线输入",
    
    "变压器输出_负荷电输入": "不可连接负荷电母线",
    "可连接负荷电母线_可连接负荷电母线": "可合并负荷电母线",
    "可连接负荷电母线_负荷电输入": "不可连接负荷电母线输出",
    "变压器输出_可连接负荷电母线": "不可连接负荷电母线输入",

    "柴油输入_柴油输出": "不可连接柴油母线",
    "可连接柴油母线_可连接柴油母线": "可合并柴油母线",
    "柴油输入_可连接柴油母线": "不可连接柴油母线输出",
    "可连接柴油母线_柴油输出": "不可连接柴油母线输入",

    "电母线输出_电母线输入": "不可连接电母线",
    "可连接电母线_可连接电母线": "可合并电母线",
    "可连接电母线_电母线输入": "不可连接电母线输出",
    "电母线输出_可连接电母线": "不可连接电母线输入",

    "电储能端输入输出_双向变流器储能端输入输出": "不可连接电储能端母线",
    "可连接电储能端母线_可连接电储能端母线": "可合并电储能端母线",
    "电储能端输入输出_可连接电储能端母线": "不可连接电储能端母线输出",
    "可连接电储能端母线_双向变流器储能端输入输出": "不可连接电储能端母线输入"
};

const typeClasses = {
    "设备": {
        "电": [
            "变流器输入",
            "变压器输出",
            "供电端输出",
            "电母线输入",
            "电储能端输入输出",
            "双向变流器储能端输入输出",
            "电母线输出",
            "双向变流器线路端输入输出",
            "负荷电输入"
        ],
        "柴油": [
            "柴油输入",
            "柴油输出"
        ]
    },
    "母线": {
        "电": [
            "可连接电储能端母线",
            "可连接供电端母线",
            "可连接负荷电母线",
            "可连接电母线"
        ],
        "柴油": [
            "可连接柴油母线"
        ]
    },
    "连接线": {
        "电": [
            "不可连接电储能端母线输出",
            "不可连接负荷电母线",
            "不可连接电母线",
            "不可连接电母线输入输出",
            "不可连接供电端母线输入",
            "不可连接电储能端母线输入",
            "不可连接负荷电母线输入",
            "不可连接供电端母线输入输出",
            "不可连接负荷电母线输出",
            "不可连接电母线输出",
            "不可连接电储能端母线",
            "不可连接供电端母线输出",
            "不可连接负荷电母线输入输出",
            "不可连接电储能端母线输入输出",
            "不可连接电母线输入",
            "不可连接供电端母线"
        ],
        "柴油": [
            "不可连接柴油母线",
            "不可连接柴油母线输入输出",
            "不可连接柴油母线输出",
            "不可连接柴油母线输入"
        ]
    },
    "合并线": {
        "电": [
            "可合并供电端母线",
            "可合并电母线",
            "可合并电储能端母线",
            "可合并负荷电母线"
        ],
        "柴油": [
            "可合并柴油母线"
        ]
    }
};

var 母线类型创建规则 = {}

for (let e of connectivity_rule){
  let k0, k1 = e.split("_")
  let i= 0
 let  母线类型 = ""
 let  锚点类型 = ""
  if (k0.startsWith("可连接")){ i+=1; 锚点类型 = k1; 母线类型 = k0}
  if (k1.startsWith("可连接")){ i+=1; 锚点类型 = k0; 母线类型 = k1}

  let v = connectivity_rule[e]

  if (i == 1){
    母线类型创建规则[锚点类型] = [母线类型,v]
  }
}

const {
  mxStencilRegistry,
  mxStencil,
  mxEvent,
  mxGraph,
  mxEditor,
  mxUtils,
  mxRubberband,
  mxKeyHandler,
  mxGraphHandler,
  mxConstants,
  mxImage,
  mxCellState,
  mxConnectionHandler,
  mxCodec,
  mxRectangleShape,
  mxPoint,
  mxClipboard,
  mxUndoManager,
  mxClient,
  mxEdgeHandler,
  mxPerimeter,
  mxOutline,
  mxEventObject,
  mxGeometry,
  mxCell,
  mxShape,
  mxConstraintHandler,
  mxEllipse,
  mxFastOrganicLayout,
  mxHierarchicalLayout,
  mxCompactTreeLayout,
  mxMorphing,
  mxCircleLayout,
  mxSvgCanvas2D,
  mxImageExport,
  mxConnectionConstraint,
  mxPolyline,
  mxVertexHandler,
  mxRectangle,
  mxImageShape,
  ActiveXObject,
  mxGraphView,
  mxEdgeSegmentHandler,
  mxEdgeStyle,
  mxStyleRegistry,
  // mxCellHighlight
} = mxgraph;
const path = require("path");

// 配置自定义事件
Object.assign(mxEvent, {
  NORMAL_TYPE_CLICKED: "NORMAL_TYPE_CLICKED",
});
// 导入流程图案例数据
const xmlData1 = path.join("data/data1.xml");
const xmlData2 = path.join("data/data2.xml");
const xmlData3 = path.join("data/data3.xml");
export default {

  components: {
    styleSelect,
    uploadData,
    ComponentList
  },
  watch: {
    elementData() {
      // if (this.isShowName) {
      //   this.showHiddenName();
      // }
    },
  },
  computed: {
    // 组元素
    grouptoolItems: () => grouptoolItems,
    toolbarItems: () => toolbarItems,
    generalToolbarItems: () => generalToolbarItems,
    externalEnergy: () => externalEnergy,
    loadType: () => loadType,
    electricItems: () => electricItems,
    energyStorage: () => energyStorage,
    distributionTransmission: () => distributionTransmission,
    others: () => others,
    componentTable() {
      let newUseData = JSON.parse(JSON.stringify(this.dataObj));
      return Object.keys(newUseData)
      // return this.dataObj
    },
  },
  data() {
    return {
      /**
       * 当前页面接口管理
       * @param {*} anchorPoint[index]type 连接类型 0黄色 1灰色 2蓝色
       * @param {*} basicParameters 基础运行参数
       * @param {*} pinObject 节点名称
       * @param {*} anchorPoint 修改或删除
       * @param {*} type text(输入框) choose(选择框)
       * @param {*} operationParameters 优化参数
       * @param {*} addType 0 为普通新增 1为复制新增 在新增节点时做出判断
       */
      typeSelects: [], //各设备的类型选择
      costModels: [], //发电上网计价模型
      loadSelects: [], //负荷选型
      fuelModels: [], //燃料计价模型
      mPoint: [], //储存锚点信息，验证每个锚点只能连接一条线
      lineId: '',
      start: '开始仿真计算',
      showResult: false, //展示仿真计算结果
      connectionsAnchors: [], //锚点信息展示
      // 计算结果表格数据
      resultTable: [
        {
          id: 'ele-1',
          name: '电负荷1',
          powerSupply: '5445',
          electricLoad: '0.45666',
          heatingLoad: '0',
          heatLoad: '0',
          coolingCapacity: '0',
          coolingLoad: '0',
          equipmentMaintenanceCosts: '45',
          electricitySalesRevenue: '89',
        }
      ],
      //数据模板
      dataSource: {
        //柴油
        dieselOil: {
          nodeType: 'dieselOil',
          type: 1,
          params: {
            // 机组参数
            unitParameters: {
              desc: "燃料设置",
              value: "unitParameters",
              params: {
                name: '柴油',
                fuelModel: '无'
              },
            },
            // 基础参数
            basicParameters: {
              desc: "基础参数",
              value: "basicParameters",
              params: {
                name: '柴油',
                fuelModel: '无'
              },
            },
          },
          pinObject: [{}],
          anchorPoint: [{
            type: 1,
            name: '柴油输出'
          }
          ],
        },
        //电负荷
        electricLoad: {
          nodeType: 'electricLoad',
          type: 1,
          params: {
            // 机组参数
            unitParameters: {
              desc: "负荷设置",
              value: "unitParameters",
              params: {
                loadSelect: '无',
                biggestLoad: '',
                payModel: '无',
              }
            },
            // 基础参数
            basicParameters: {
              desc: "基础参数",
              value: "basicParameters",
              params: {
                loadSelect: '0',
                payModel: '无',
              }
            },
          },
          pinObject: [{}, {}],
          anchorPoint: [{
            type: 2,
            name: '负荷电输入'
          },
          ],
        },
        //光伏发电
        photovoltaics: {
          nodeType: 'photovoltaics',
          type: 1,
          params: {
            // 机组参数
            unitParameters: {
              desc: "机组参数",
              value: "basicParameters",
              params: {
                name: '光伏发电',
                typeSelect: '设备类型待选',
                leastArea: '0',
                biggestArea: '1000',
                costModel: '无'
              }
            },
            // 基础参数
            basicParameters: {
              desc: "基础参数",
              value: "basicParameters",
              params: {
                name: '光伏发电',
                typeSelect: '设备类型待选',
                equiNum: '1',
                costModel: '无'
              }
            },
          },
          pinObject: [{}, {}],
          anchorPoint: [{
            type: 3,
            name: '供电端输出'
          },
          ],
        },
        //风力发电
        windPower: {
          nodeType: 'windPower',
          type: 1,
          params: {
            // 机组参数
            unitParameters: {
              desc: "机组参数",
              value: "unitParameters",
              params: {
                name: '风力发电',
                typeSelect: '设备类型待选',
                leastNum: '0',
                biggestNum: '20',
                costModel: '无'
              }
            },
            // 基础参数
            basicParameters: {
              desc: "基础参数",
              value: "basicParameters",
              params: {
                name: '风力发电',
                typeSelect: '设备类型待选',
                equiNum: '1',
                costModel: '无'
              }
            },
          },
          pinObject: [{}, {}],
          anchorPoint: [{
            type: 3,
            name: '供电端输出'
          }
          ],
        },
        //柴油发电
        dieselGenerator: {
          nodeType: 'dieselGenerator',
          type: 1,
          params: {
            // 机组参数
            unitParameters: {
              desc: "机组参数",
              value: "unitParameters",
              params: {
                name: '柴油发电',
                typeSelect: '设备类型待选',
                leastNum: '0',
                biggestNum: '20',
                costModel: '无'
              }
            },
            // 基础参数
            basicParameters: {
              desc: "基础参数",
              value: "basicParameters",
              params: {
                name: '柴油发电',
                typeSelect: '设备类型待选',
                equiNum: '1',
                costModel: '无'
              }
            },
          },
          pinObject: [{}, {}],
          anchorPoint: [{
            type: 1,
            name: '柴油输入'
          },
          {
            type: 3,
            name: '供电端输出'
          },
          ],
        },
        //锂电池
        lithiumCell: {
          nodeType: 'lithiumCell',
          type: 1,
          params: {
            // 燃料设置
            unitParameters: {
              desc: "机组参数",
              value: "unitParameters",
              params: {
                name: '锂电池',
                typeSelect: '设备类型待选',
                leastContain: '',
                biggestContain: '',
                soc: '',
                loop: '0',
              }
            },
            // 基础参数
            basicParameters: {
              desc: "基础参数",
              value: "basicParameters",
              params: {
                name: '锂电池',
                typeSelect: '设备类型待选',
                contain: '',
                soc: '',
              }
            },
          },
          pinObject: [{}],
          anchorPoint: [{
            type: 6,
            name: '电储能端输入输出'
          },],
        },
        //变压器
        transformer: {
          nodeType: 'transformer',
          type: 1,
          params: {
            // 机组参数
            unitParameters: {
              desc: "机组参数",
              value: "unitParameters",
              params: {
                name: '变压器',
                typeSelect: '设备类型待选',
                leastNum: '0',
                biggestNum: '20',
                powerFactor: '0.95',
                redundance: '',
              }
            },
            // 基础参数
            basicParameters: {
              desc: "基础参数",
              value: "basicParameters",
              params: {
                name: '变压器',
                typeSelect: '设备类型待选',
                equiNum: '1',
                powerFactor: '0.95',
              }
            },
          },
          pinObject: [{}, {}],
          anchorPoint: [{
            type: 7,
            name: '电母线输入'
          }, {
            type: 2,
            name: '变压器输出'
          },],
        },
        //变流器
        converter: {
          nodeType: 'converter',
          type: 1,
          params: {
            // 燃料设置
            unitParameters: {
              desc: "机组参数",
              value: "unitParameters",
              params: {
                name: '变流器',
                typeSelect: '设备类型待选',
                leastNum: '0',
                biggestNum: '20',
              }
            },
            // 基础参数
            basicParameters: {
              desc: "基础参数",
              value: "basicParameters",
              params: {
                name: '变流器',
                typeSelect: '设备类型待选',
                equiNum: '1',
              }
            },
          },

          pinObject: [{}, {}],
          anchorPoint: [{
            type: 3,
            name: '变流器输入'
          },
          {
            type: 7,
            name: '电母线输出'
          },
          ],
        },
        //双向变流器
        bidirectionalInverter: {
          nodeType: 'bidirectionalInverter',
          type: 1,
          params: {
            // 燃料设置
            unitParameters: {
              desc: "机组参数",
              value: "unitParameters",
              params: {
                name: '双向变流器',
                typeSelect: '设备类型待选',
                leastNum: '0',
                biggestNum: '20',
              }
            },
            // 基础参数
            basicParameters: {
              desc: "基础参数",
              value: "basicParameters",
              params: {
                name: '双向变流器',
                typeSelect: '设备类型待选',
                equiNum: '1',
              }
            },
          },
          pinObject: [{}, {}, {}],
          anchorPoint: [{
            type: 6,
            name: '双向变流器储能端输入输出'
          },
          {
            type: 7,
            name: '双向变流器线路端输入输出'
          },
          ],
        },
        //传输线
        transmissionLine: {
          nodeType: 'transmissionLine',
          type: 1,
          params: {
            // 机组参数
            unitParameters: {
              desc: "传输线设置",
              value: "unitParameters",
              params: {
                name: '传输线',
                typeSelect: '设备类型待选',
                length: '1',
              }
            },
            // 基础参数
            basicParameters: {
              desc: "基础参数",
              value: "basicParameters",
              params: {
                name: '传输线',
                typeSelect: '设备类型待选',
                length: '1',
              }
            },
          },
          pinObject: [{}, {}],
          anchorPoint: [{
            type: 7,
            name: '电母线输入'
          },
          {
            type: 7,
            name: '电母线输出'
          },
          ],
        },
        //母线
        bus: {
          nodeType: 'bus',
          type: 1,
          params: {
            // 机组参数
            unitParameters: {
              desc: "机组参数",
              value: "unitParameters",
              params: {
              },
            },
            // 基础参数
            basicParameters: {
              desc: "基础参数",
              value: "basicParameters",
              params: {
              },
            },
          },

          pinObject: [],
          anchorPoint: [],
          refname: "母线"
        },
      },
      // 收集整个页面右侧面板数据
      rightParams: [],
      //全局数据
      dataObj: {},
      //传入参数
      importData: {},
      cellId: "",
      cellObj: null, //cell大对象 鼠标点击时修改
      id: "",
      modelnum: "",
      modelId: "",
      modelName: "",
      name: "abc",
      dialogFormVisible: false,
      form: {
        name: "",
      },
      activeName: "first",
      treeData: [{
        id: 1,
        label: "锅炉余热",
        xml: this.xmlData1,
      },],
      graph: null,
      editor: null,
      palettes: {},
      graphXml: "",
      activeNames: ["1", "2", "3"],
      isNode: false,
      cellStyle: {},
      graphX: 100,
      graphY: 10,
      undoMng: "",
      textValue: "",
      uploadDataVisible: false,
      isOutputXml: false,
      edgeStyle: "orthogonalEdgeStyle",
      outline: "",
      idSeed: 0,
      normalIdSeed: 0,
      // configOrder: 0,
      jsonData: {
        cells: {
          nodes: [],
          groups: [],
        },
        edges: [],
      },
      showBackground: true,
      currentNormalType: {},
      normalTypePosition: {
        top: "0",
        left: "0",
      },
      // 保存的模板
      model: [],
      // 连线时锚点信息
      connectDotData: {
        data: [],
        edge: {},
      },
      // 资源表数据
      resourceData: [],
      // 模型类型
      modelType: {
        rectangle: "矩形",
      },
      elementData: [],
      // 复制元素
      selectionCells: [],
      // 显示隐藏
      isShow: {
        // 显示或者隐藏元件名称
        isShowName: false,
        // 隐藏或显示热原件
        isShowHot: false,
        // 隐藏或显示电原件
        isShowElectricity: false,
      },
      // 查看元件表
      checkElementTable: false,
      // 元件表数据
      elementTableData: [],
    };
  },
  methods: {
    // 根据子组件传过来的值，保存右侧面板数据
    saveRightParam(rightParam) {
      // 若传递过来的元件id已经存在，则进行替换
      let arr = this.rightParams.filter(item => {
        return item.id === rightParam.id
      })
      if (arr.length !== 0) {
        this.rightParams = this.rightParams.map(item => {
          return item = item.id === rightParam.id ? rightParam : item
        })
      } else {
        this.rightParams.push(rightParam)
      }
      console.log(this.rightParams);
    },
    // 开始仿真计算
    async startCompute(state) {
      this.start = state
      if (state === '开始仿真计算') {
        //调终止接口
        this.$message.error('已经终止计算')
        // this.start = '开始仿真计算'
      } else {
        let xml = this.encode(this.graph) //graph图的xml文件
        var x2js = new X2JS();
        let xml2json = x2js.xml2js(xml) + JSON.stringify(this.connectionsAnchors)
        // 开始计算
        const res = await saveTopInfo({ proId: 1, content: JSON.stringify(xml2json) })
        // console.log(res);
        if (res.code === 200) {
          this.start = '开始仿真计算'
        }
      }
    },
    // 查看评价结果
    checkResult() {
      this.showResult = true
    },
    // 导出结果数据
    downResult() {
      let bodyData = this.resultTable.map(item => {
        wscols.push({ wch: 18, });
        return {
          '元件标识符': item.id,
          '元件自定义名称': item.name,
          '供电量(kWh)': item.powerSupply,
          '电负荷(kWh)': item.electricLoad,
          '供热量(kWh)': item.heatingLoad,
          '热负荷(kWh)': item.heatLoad,
          '供冷量(kWh)': item.coolingCapacity,
          '冷负荷(kWh)': item.coolingLoad,
          '设备维护费用(万元)': item.equipmentMaintenanceCosts,
          '售电收入(万元)': item.electricitySalesRevenue,
        }
      })
      let workSheet = XLSX.utils.json_to_sheet(bodyData)
      const workBook = XLSX.utils.book_new()
      workSheet["!cols"] = wscols;
      XLSX.utils.book_append_sheet(workBook, workSheet, '数据报表')
      XLSX.writeFile(workBook, '计算结果.xlsx')
    },

    // 保存
    async saveGraph() {
      // 保存graph图
      let xml = this.encode(this.graph) //graph图的xml文件
      // 保存图元参数信息(自定义图元，母线)
      // console.log(JSON.stringify(this.graph));
      var x2js = new X2JS();
      let xml2json = x2js.xml2js(xml)
      console.log(JSON.stringify(xml2json));

      // 保存连线的锚点信息
      // let xml2jsonc = x2js.xml2js(this.connectionsAnchors)
      // console.log(this.connectionsAnchors);
      // console.log(this.rightParams);
      let arr = this.connectionsAnchors.map(item => {
        // console.log(item);
        let obj = {
          id: item.edge.id,
          sourceAnchors: item.data[0],
          targetAnchors: item.data[1],
        }
        return obj
      })
      // console.log(arr);

      let infos = { graph: JSON.stringify(xml2json), connectionsAnchors: arr, rightParams: this.rightParams }
      // console.log(JSON.stringify(infos));
      // // 保存全部graph图信息
      const res = await saveTopInfo({ proId: 1, content: JSON.stringify(infos) })
      console.log(res);
    },
    // 隐藏元件表
    changeDia(newVal) {
      this.checkElementTable = newVal
    },
    // 左侧图元位置
    handlerMouseenter(index, tip) {
      // 鼠标进入触发元素
      let popover;
      if (tip === 1) {
        popover = this.$refs[`popoverExter${index}`][0];
      } else if (tip === 2) {
        popover = this.$refs[`popoverLoad${index}`][0];
      } else if (tip === 3) {
        popover = this.$refs[`popoverEle${index}`][0];
      }
      else if (tip === 4) {
        popover = this.$refs[`popoverStor${index}`][0];
      }
      else if (tip === 5) {
        popover = this.$refs[`popoverTran${index}`][0];
      }
      else if (tip === 6) {
        popover = this.$refs[`popoverOth${index}`][0];
      }


      let timer = setTimeout(() => {
        const wid = document.querySelector(".custom-toolbar").offsetWidth;
        popover.popperElm.style.left = wid + "px";
        clearTimeout(timer);
      }, 5);
    },
    // 点击出现模板
    appear(newValue) {
      this.uploadPaintFlow(newValue.data.xml);
    },

    // 保存模板
    saveModel() {
      this.dialogFormVisible = false;
      this.treeData.push({
        id: this.treeData.length,
        label: this.form.name,
        xml: this.encode(this.graph),
      });
      this.$message.success("保存成功");
      this.form.name = "";
    },
    // 删除模板
    remove(node, data) {
      const parent = node.parent;
      const children = parent.data.children || parent.data;
      const index = children.findIndex((d) => d.id === data.id);
      children.splice(index, 1);
    },

    // 创建画布并进行初始化
    createGraph() {
      // 创建graph
      // 方式一：直接构建graph实例
      // this.graph = new mxGraph(this.$refs.container)
      this.editor = new mxEditor();
      this.graph = this.editor.graph;
      this.editor.setGraphContainer(this.$refs.container);
      // 配置默认全局样式
      this.configureStylesheet(this.graph);
      // 去锯齿效果
      mxRectangleShape.prototype.crisp = true;
      // 定义全局变量，如。用于触发建立新的连接的活动区域的最小尺寸（以像素为单位），该部分（100％）的小区区域被用于触发新的连接，以及一些窗口和“下拉菜菜单选择
      mxConstants.MIN_HOTSPOT_SIZE = 16;
      mxConstants.DEFAULT_HOTSPOT = 1;

      //cell创建支持传入html
      this.graph.setHtmlLabels(true);
      this.graph.setDropEnabled(true);
      this.graph.setSplitEnabled(false);
      // 有效的拖放操作，则返回true
      this.graph.isValidDropTarget = (target, cells, evt) => {
        if (
          this.graph.isSplitEnabled() &&
          this.graph.isSplitTarget(target, cells, evt)
        ) {
          console.log("拖放");
          return true;
        }
      };

      // mxEvent.addMouseWheelListener((evt, up) => {
      //   if (up) {
      //     this.graph.zoomIn();
      //   } else {
      //     this.graph.zoomOut();
      //   }
      //   mxEvent.consume(evt);
      // });

      // 禁用分组的收缩功能 方法1:
      // this.graph.isCellFoldable = (cell) => {
      //   return false
      // }
      // 禁用分组的收缩功能 方法2:
      this.graph.foldingEnabled = false;
      // 组内的子元素是否随父元素变化而变化
      this.graph.recursiveResize = true;

      // 设置连线时的预览路径及样式
      this.graph.connectionHandler.createEdgeState = () => {

        // 设置预览的连接线,第三个参数为连接成功后连接线上的label
        var edge = this.graph.createEdge(null, null, null, null, null);
        console.log(edge);
        // edge.style += `;edgeStyle=orthogonalEdgeStyle `
        return new mxCellState(
          this.graph.view,
          edge,
          this.graph.getCellStyle(edge)
        );
      };

      // 是否开启旋转
      mxVertexHandler.prototype.livePreview = true;
      mxVertexHandler.prototype.rotationEnabled = true;
      // 设置旋转按钮
      mxVertexHandler.prototype.createSizerShape = function (
        bounds,
        index,
        fillColor
      ) {
        if (this.handleImage != null) {
          bounds = new mxRectangle(
            bounds.x,
            bounds.y,
            this.handleImage.width,
            this.handleImage.height
          );
          let shape = new mxImageShape(bounds, this.handleImage.src);
          // Allows HTML rendering of the images
          shape.preserveImageAspect = true;
          return shape;
        } else if (index == mxEvent.ROTATION_HANDLE) {
          // return new mxDoubleEllipse(bounds, fillColor || mxConstants.HANDLE_FILLCOLOR, mxConstants.HANDLE_STROKECOLOR);
          // 设置旋转图标
          bounds = new mxRectangle(bounds.x, bounds.y, 15, 15);
          let rotationShape = new mxImageShape(bounds, "icon/rotate.svg");
          rotationShape.preserveImageAspect = true;
          return rotationShape;
        } else {
          return new mxRectangleShape(
            bounds,
            fillColor || mxConstants.HANDLE_FILLCOLOR,
            mxConstants.HANDLE_STROKECOLOR
          );
        }
      };
      // 设置旋转角度（解决默认旋转180度的bug）
      mxVertexHandler.prototype.getRotationHandlePosition = function () {
        let padding = this.getHandlePadding();
        return new mxPoint(
          this.bounds.x +
          this.bounds.width -
          this.rotationHandleVSpacing +
          padding.x / 2,
          this.bounds.y + this.rotationHandleVSpacing - padding.y / 2
        );
      };
      // 设置默认组
      // groupBorderSize 设置图形和它的子元素的边距
      let group = new mxCell(
        "Group",
        new mxGeometry(),
        "group;fontColor=white;"
      );
      group.setVertex(true);
      // 设置组可连接
      group.setConnectable(true);
      // group.setCellsResizable(false);
      this.editor.defaultGroup = group;
      this.editor.groupBorderSize = 80;

      // 是否根元素
      this.graph.isValidRoot = function (cell) {
        return this.isValidDropTarget(cell);
      };

      // // 是否可以被选中
      // this.graph.isCellSelectable = function (cell) {
      //   return !this.isCellLocked(cell);
      // };

      // 返回元素
      this.graph.getLabel = function (cell) {
        var tmp = mxGraph.prototype.getLabel.apply(this, arguments); // "supercall"
        if (this.isCellLocked(cell)) {
          // 如元素被锁定 返回空标签
          return "";
        } else if (this.isCellCollapsed(cell)) {
          var index = tmp.indexOf("</h1>");
          if (index > 0) {
            tmp = tmp.substring(0, index + 5);
          }
        }
        return tmp;
      };

      // 目标是否有效
      this.graph.isValidDropTarget = function (cell) {
        // console.log(cell, cells, evt);
        return this.isSwimlane(cell);
      };

      // 是否根元素
      this.graph.isValidRoot = function (cell) {
        return this.isValidDropTarget(cell);
      };

      // 是否可以被选中
      this.graph.isCellSelectable(true);

      // 允许重复连接
      this.graph.setMultigraph(false);
      // 禁止连接线晃动(即连线两端必须在节点上)
      this.graph.setAllowDanglingEdges(true);
      // 允许连线的目标和源是同一元素
      this.graph.setAllowLoops(false);
      //边被拖动时始终保持连接
      this.graph.setDisconnectOnMove(false);
      // 选择基本元素开启
      this.graph.setEnabled(true);
      // 动态改变样式
      this.graph.getView().updateStyle = true;
      // 鼠标框选
      this.rubberBand = new mxRubberband(this.graph);
      this.graph.setResizeContainer(true);
      // this.graph.setCellsEditable(false);

      // 开启画布平滑移动
      // this.graph.setPanning(true);
      this.graph.setPanning = true;
      // 开启提示
      this.graph.setTooltips(true);
      // 允许连线
      this.graph.setConnectable(true);
      this.graph.connectionHandler.waypointsEnabled = false; // 禁用锚点一样的连线
      console.log(this.graph.connectionHandler.waypointsEnabled, '===================w22222222222222222222');
      //移动元素的步长
      this.graph.gridSize = 3;
      this.graph.setBorder(160);

      // 开启方块上的文字编辑功能
      this.graph.setCellsEditable(true);
      // 禁止双击修改内容(弃用)
      // this.graph.dblClick = (evt, cell) => {
      //   var model = this.graph.getModel();
      //   if (model.isVertex(cell)) {
      //     return false;
      //   }
      // };
      // Disables synchronous loading of resources
      // 可用于禁用HTML的泳道标签，避免冲突(返回false即可)
      // 判断是否为泳道标签
      // this.graph.isHtmlLabel = function (cell) {
      //   return this.isSwimlane(cell);
      // };
      //准备撤销还原功能
      // 构造具有给定历史记录大小的新撤消管理器。默认100步
      this.undoMng = new mxUndoManager();
      let listener = (sender, evt) => {
        this.undoMng.undoableEditHappened(evt.getProperty("edit"));
      };
      this.graph.getModel().addListener(mxEvent.UNDO, listener);
      this.graph.getView().addListener(mxEvent.UNDO, listener);
      // 创建缩略图
      this.outline = new mxOutline(this.graph, this.$refs.showMap);
      if (this.graph == null || this.graph == undefined) {
        return;
      }
      // 从value中获取显示的内容(如果节点的value为空则显示节点的title)
      this.graph.convertValueToString = (cell) => {
        return cell["value"] ? cell["value"] : cell["title"];
      };
    },

    // 设置每个锚点只能连接一条线


    // 新增自定义节点
    addCustomCell(dropCell, toolItem, x, y) {
      // 判断是否是放在组元素上
      const drop = !R.isNil(dropCell); // drop && this.$message.info(`${toolItem['title']}节点进入${dropCell.title}`);
      // console.log(toolItem);
      const {
        width,
        height
      } = toolItem;
      const styleObj = toolItem.style;
      const style = Object.keys(styleObj).map((attr) => `${attr}=${styleObj[attr]}`)
        .join(";");
      // let style = "shape=image;image=./models/下载.svg"
      // let style = "shape=image;image=./models/光伏发电.svg"
      // console.log(style);
      const realX = drop ? x - dropCell.geometry.x : x;
      const realY = drop ? y - dropCell.geometry.y : y;
      const parent = drop ? dropCell : this.graph.getDefaultParent();
      this.graph.getModel().beginUpdate();
      try {
        let vertex = this.graph.insertVertex(
          parent,
          null,
          null,
          realX - width / 2,
          realY - height / 2,
          width,
          height,
          style,
          // `${style};'noSingleConnection;anchor=SingleConnectionAnchor'`
        );

        vertex.geometry.alternateBounds = new mxRectangle(0, 0, 100, 100);
        // vertex.title = toolItem["title"];
        vertex.modelnum = toolItem["modelnum"];
        vertex.id = toolItem["id"] + "-" + toolItem["idSeed"];
        vertex.ports = toolItem.ports;
        vertex.dropAble = toolItem["dropAble"];
        // 添加完节点后自动添加顺序图标
        // this.addPoint(vertex, toolItem["idSeed"]);
        toolItem["idSeed"]++;
        vertex["isGroup"] = toolItem["id"].includes("group") ? true : false;
        vertex.ports = toolItem.ports;
        vertex.isBasicElement = toolItem.isBasicElement;
        vertex.width = toolItem.width;
        vertex.height = toolItem.height;
        vertex.realX = realX;
        vertex.realY = realY;
        vertex.type = toolItem.type;
        let splitStr = vertex.id.split("-");
        this.dataObj[vertex.id] = JSON.parse(
          JSON.stringify(this.dataSource[splitStr[0]])
        );
        //nodeType 0 为节点新增 1为复制新增
        this.dataObj[vertex.id].addType = 0;
        // vertex.value = svgText;
      } finally {
        this.graph.getModel().endUpdate();
      }
    },
    // 布局
    graphLayout(animate, layoutType) {
      try {
        if (layoutType === "randomLayout") {
          // 随机布局
          mxFastOrganicLayout.prototype.minDistanceLimit = 100;
          // eslint-disable-next-line new-cap
          var layout = new mxFastOrganicLayout(this.graph);
          layout.forceConstant = 500;
          layout.execute(this.graph.getDefaultParent());
        } else if (layoutType === "hierarchicalLayout") {
          // 分层布局
          mxHierarchicalLayout.prototype.intraCellSpacing = 300;
          mxHierarchicalLayout.prototype.fineTuning = false;
          mxHierarchicalLayout.prototype.traverseAncestors = false;
          mxHierarchicalLayout.prototype.resizeParent = true;
          // 无关系实体之间的间距
          mxHierarchicalLayout.prototype.interHierarchySpacing = 200;
          // 层级之间的距离
          mxHierarchicalLayout.prototype.interRankCellSpacing = 800;

          // eslint-disable-next-line new-cap
          var hierarchicallayout = new mxHierarchicalLayout(
            this.graph,
            mxConstants.DIRECTION_NORTH
          );
          hierarchicallayout.execute(this.graph.getDefaultParent());
        } else if (layoutType === "compactTreeLayout") {
          // 树形布局
          // eslint-disable-next-line new-cap
          var compactTreelayout = new mxCompactTreeLayout(this.graph);
          compactTreelayout.execute(this.graph.getDefaultParent());
        } else if (layoutType === "circleLayout") {
          // 圆形布局
          // eslint-disable-next-line new-cap
          var circleLayout = new mxCircleLayout(this.graph, 400);
          circleLayout.execute(this.graph.getDefaultParent());
        }
      } finally {
        // 是否开启布局动画
        if (animate) {
          // eslint-disable-next-line new-cap
          var morph = new mxMorphing(this.graph, 20, 7.7, 40);
          morph.addListener(mxEvent.DONE, () => {
            this.graph.getModel().endUpdate();
          });
          morph.startAnimation();
        } else {
          this.graph.getModel().endUpdate();
        }
      }
    },
    // 初始化基础节点
    initGeneralTool() {
      var generalToolbarDomArray = this.$refs.generalToolItems;
      // 判断是否为数组且数组是否为空
      if (
        !(
          generalToolbarDomArray instanceof Array ||
          generalToolbarDomArray.length <= 0
        )
      ) {
        return;
      }

      generalToolbarDomArray.forEach((dom, domIndex) => {
        var toolItem = this.generalToolbarItems[domIndex];
        var {
          width,
          height
        } = toolItem;
        var itemClass = toolItem.class;
        //新增基础节点
        var generalDropHandler = (graph, evt, dropCell, x, y) => {
          const drop = !R.isNil(dropCell);
          // drop && this.$message.info(`${toolItem['title']}节点进入${dropCell.title}`);
          const realX = drop ? x - dropCell.geometry.x : x;
          const realY = drop ? y - dropCell.geometry.y : y;
          const {
            width,
            height
          } = toolItem;
          const styleObj = toolItem.style;
          const style = Object.keys(styleObj)
            .map((attr) => `${attr}=${styleObj[attr]}`)
            .join(";");
          const parent = drop ? dropCell : this.graph.getDefaultParent();
          this.graph.getModel().beginUpdate();
          try {
            let vertex = this.graph.insertVertex(
              parent,
              null,
              null,
              realX - width / 2,
              realY - height / 2,
              width,
              height,
              style + ";whiteSpace=wrap;word-break=break-all"
            );
            vertex.title =
              `<div style='word-break:break-all'>` +
              toolItem["title"] +
              "</div>";
            vertex.dropAble = toolItem["dropAble"];
            // vertex.modelnum = toolItem["modelnum"];
            vertex.id = toolItem["id"] + "-" + toolItem["idSeed"];
            toolItem["idSeed"]++;
            vertex["isGroup"] = toolItem["id"].includes("group") ? true : false;
            vertex.ports = toolItem.ports;
            vertex.isBasicElement = toolItem.isBasicElement;
            vertex.width = toolItem.width;
            vertex.height = toolItem.height;
          } finally {
            this.graph.getModel().endUpdate();
          }
        };
        // 设置节点被拖拽时的样式(预览)
        var generalcreateDragPreview = () => {
          var elt = document.createElement("div");
          elt.style.width = `${width}px`;
          elt.style.height = `${height}px`;
          elt.style.transform = "translate(-50%,-50%)";
          elt.className = itemClass;
          return elt;
        };
        // 允许拖拽
        let ds = mxUtils.makeDraggable(
          dom,
          this.graph,
          generalDropHandler,
          generalcreateDragPreview(),
          0,
          0,
          true,
          true
        );
        ds.setGuidesEnabled(true);
      });
    },
    // A为边到边连接添加椭圆标记。

    mxGetCellStyle() {
      let mxGraphGetCellStyle = mxGraph.prototype.getCellStyle;
      mxGraph.prototype.getCellStyle = function (cell) {
        var style = mxGraphGetCellStyle.apply(this, arguments);

        if (style != null && this.model.isEdge(cell)) {
          style = mxUtils.clone(style);

          if (this.model.isEdge(this.model.getTerminal(cell, true))) {
            style["startArrow"] = "oval";
          }

          if (this.model.isEdge(this.model.getTerminal(cell, false))) {
            style["endArrow"] = "oval";
          }
        }

        return style;
      };
    },
    // A 重写预览和创建新边的方法。
    preview() {
      // 设置边到边连接的源终端点。
      // Sets source terminal point for edge-to-edge connections.
      // this.graph.connectionHandler.createEdgeState = function (me) {
      //   var edge = graph.createEdge(null, null, null, null, null, 'edgeStyle=none'); // 创建一个隐藏的边线
      //   return new mxCellState(this.graph.view, edge, this.graph.getCellStyle(edge)); // 返回边线状态
      // };

      // 
      mxConnectionHandler.prototype.createEdgeState = function (me) {

        var edge = this.graph.createEdge(null, null, null, null, null, 'edgeStyle=none');

        if (this.sourceConstraint != null && this.previous != null) {
          edge.style =
            mxConstants.STYLE_EXIT_X +
            "=" +
            this.sourceConstraint.point.x +
            ";" +
            mxConstants.STYLE_EXIT_Y +
            "=" +
            this.sourceConstraint.point.y +
            ";";
        } else if (this.graph.model.isEdge(me.getCell())) {
          var scale = this.graph.view.scale;
          var tr = this.graph.view.translate;
          var pt = new mxPoint(
            this.graph.snap(me.getGraphX() / scale) - tr.x,
            this.graph.snap(me.getGraphY() / scale) - tr.y
          );
          edge.geometry.setTerminalPoint(pt, true);
        }
        this.graph.connectionHandler.connectPreview = false; // 禁用从线条上脱出的连线
        return this.graph.view.createState(edge);
      };

      // 使用鼠标右键在背景上创建边缘(另请参阅:第67行ff)
      // Uses right mouse button to create edges on background (see also: lines 67 ff)
      mxConnectionHandler.prototype.isStopEvent = function (me) {
        return (
          me.getState() != null || mxEvent.isRightMouseButton(me.getEvent())
        );
      };

      // 更新边到边连接的目标终端点。
      // Updates target terminal point for edge-to-edge connections.
      let mxConnectionHandlerUpdateCurrentState =
        mxConnectionHandler.prototype.updateCurrentState;
      mxConnectionHandler.prototype.updateCurrentState = function (me) {
        mxConnectionHandlerUpdateCurrentState.apply(this, arguments);

        if (this.edgeState != null) {
          this.edgeState.cell.geometry.setTerminalPoint(null, false);

          if (
            this.shape != null &&
            this.currentState != null &&
            this.currentState.view.graph.model.isEdge(this.currentState.cell)
          ) {
            var scale = this.graph.view.scale;
            var tr = this.graph.view.translate;
            var pt = new mxPoint(
              this.graph.snap(me.getGraphX() / scale) - tr.x,
              this.graph.snap(me.getGraphY() / scale) - tr.y
            );
            this.edgeState.cell.geometry.setTerminalPoint(pt, false);
          }
        }
      };

      // 更新克隆预览中的终端和控制点。
      mxEdgeSegmentHandler.prototype.clonePreviewState = function (
        point
        // terminal
      ) {
        var clone = mxEdgeHandler.prototype.clonePreviewState.apply(
          this,
          arguments
        );
        clone.cell = clone.cell.clone();

        if (this.isSource || this.isTarget) {
          clone.cell.geometry = clone.cell.geometry.clone();

          // 设置一条边的端点如果我们移动其中一个端点
          // Sets the terminal point of an edge if we're moving one of the endpoints
          if (this.graph.getModel().isEdge(clone.cell)) {
            // 注意事项:仅当目标或源终端是边时设置此选项
            // TODO: Only set this if the target or source terminal is an edge
            clone.cell.geometry.setTerminalPoint(point, this.isSource);
          } else {
            clone.cell.geometry.setTerminalPoint(null, this.isSource);
          }
        }

        return clone;
      };

      var mxEdgeHandlerConnect = mxEdgeHandler.prototype.connect;
      mxEdgeHandler.prototype.connect = function (
        edge,
        terminal,
        isSource
        // isClone,
        // me
      ) {
        var result = null;
        var model = this.graph.getModel();
        // var parent = model.getParent(edge);

        model.beginUpdate();
        try {
          result = mxEdgeHandlerConnect.apply(this, arguments);
          var geo = model.getGeometry(result);

          if (geo != null) {
            geo = geo.clone();
            var pt = null;

            if (model.isEdge(terminal)) {
              pt =
                this.abspoints[this.isSource ? 0 : this.abspoints.length - 1];
              pt.x = pt.x / this.graph.view.scale - this.graph.view.translate.x;
              pt.y = pt.y / this.graph.view.scale - this.graph.view.translate.y;

              var pstate = this.graph
                .getView()
                .getState(this.graph.getModel().getParent(edge));

              if (pstate != null) {
                pt.x -= pstate.origin.x;
                pt.y -= pstate.origin.y;
              }

              pt.x -= this.graph.panDx / this.graph.view.scale;
              pt.y -= this.graph.panDy / this.graph.view.scale;
            }

            geo.setTerminalPoint(pt, isSource);
            model.setGeometry(edge, geo);
          }
        } finally {
          model.endUpdate();
        }

        return result;
      };
    },
    // A 计算边到边连接点的位置
    ComputesLocation() {
      mxGraphView.prototype.updateFixedTerminalPoint = function (
        edge,
        terminal,
        source,
        constraint
      ) {
        var pt = null;

        if (constraint != null) {
          pt = this.graph.getConnectionPoint(terminal, constraint);
        }

        if (source) {
          edge.sourceSegment = null;
        } else {
          edge.targetSegment = null;
        }

        if (pt == null) {
          var s = this.scale;
          var tr = this.translate;
          var orig = edge.origin;
          var geo = this.graph.getCellGeometry(edge.cell);
          pt = geo.getTerminalPoint(source);

          // 计算边到边连接点
          // Computes edge-to-edge connection point
          if (pt != null) {
            pt = new mxPoint(
              s * (tr.x + pt.x + orig.x),
              s * (tr.y + pt.y + orig.y)
            );

            // 在边缘上找到最近的段并计算交点
            // Finds nearest segment on edge and computes intersection
            if (terminal != null && terminal.absolutePoints != null) {
              var seg = mxUtils.findNearestSegment(terminal, pt.x, pt.y);

              // 找到线段的方向
              // Finds orientation of the segment
              var p0 = terminal.absolutePoints[seg];
              var pe = terminal.absolutePoints[seg + 1];
              var horizontal = p0.x - pe.x == 0;

              // 将段存储在边缘状态
              // Stores the segment in the edge state
              var key = source ? "sourceConstraint" : "targetConstraint";
              var value = horizontal ? "horizontal" : "vertical";
              edge.style[key] = value;

              // 将坐标保持在段边界内
              // Keeps the coordinate within the segment bounds
              if (horizontal) {
                pt.x = p0.x;
                pt.y = Math.min(pt.y, Math.max(p0.y, pe.y));
                pt.y = Math.max(pt.y, Math.min(p0.y, pe.y));
              } else {
                pt.y = p0.y;
                pt.x = Math.min(pt.x, Math.max(p0.x, pe.x));
                pt.x = Math.max(pt.x, Math.min(p0.x, pe.x));
              }
            }
          }
          // 计算顶点和端口上的约束连接点
          // Computes constraint connection points on vertices and ports
          else if (terminal != null && terminal.cell.geometry.relative) {
            pt = new mxPoint(
              this.getRoutingCenterX(terminal),
              this.getRoutingCenterY(terminal)
            );
          }

          // Snaps point to grid
          /*if (pt != null)
                {
                    var tr = this.graph.view.translate;
                    var s = this.graph.view.scale;
 
                    pt.x = (this.graph.snap(pt.x / s - tr.x) + tr.x) * s;
                    pt.y = (this.graph.snap(pt.y / s - tr.y) + tr.y) * s;
                }*/
        }

        edge.setAbsoluteTerminalPoint(pt, source);
      };
    },

    // 初始化自定义图标
    initCustomToolbar(toolbarItems) {
      // 获取工具栏中的自定义节点的dom
      var toolbarDomArray;
      if (toolbarItems[0].id === "dieselOil") {
        toolbarDomArray = this.$refs.externalEnergy;
      } else if (toolbarItems[0].id === "electricLoad") {
        toolbarDomArray = this.$refs.loadType;
      } else if (toolbarItems[0].id === "photovoltaics") {
        toolbarDomArray = this.$refs.electricItems;
      } else if (toolbarItems[0].id === "lithiumCell") {
        toolbarDomArray = this.$refs.energyStorage;
      } else if (toolbarItems[0].id === "transformer") {
        toolbarDomArray = this.$refs.distributionTransmission;
      } else if (toolbarItems[0].id === "bus") {
        toolbarDomArray = this.$refs.others;
      }
      if (!(toolbarDomArray instanceof Array) || toolbarDomArray.length <= 0) {
        return;
      }

      toolbarDomArray.forEach((dom, domIndex) => {
        var toolItem = toolbarItems[domIndex];

        // var toolItem = this.toolbarItems[domIndex];
        var {
          width,
          height
        } = toolItem;
        var image = toolItem.style.image;
        //定义拖拽后的回调函数
        var dropHandler = (graph, evt, cell, x, y) => {
          this.addCustomCell(cell, toolItem, x, y);
        };
        // 设置节点被拖拽时的样式(预览)
        var createDragPreview = () => {
          var elt = document.createElement("div");
          elt.style.border = "2px dotted black";
          elt.style.width = `${width}px`;
          elt.style.height = `${height}px`;
          elt.style.backgroundImage = `url(${image})`;
          elt.style.backgroundSize = "cover";
          elt.style.transform = "translate(-50%,-50%)";
          elt.style.backgroundRepeat = "no-repeat";
          return elt;
        };
        // 允许拖拽
        let ds = mxUtils.makeDraggable(
          dom,
          this.graph,
          dropHandler,
          createDragPreview(),
          0,
          0,
          false,
          true,
          true
        );
        ds.setGuidesEnabled(true);
      });
    },
    // 拖拽组元素
    makeToolbarDraggable() {
      console.log(this.$refs.grouptoolItem);
      const grouptoolItem = this.$refs.grouptoolItem;
      if (!(grouptoolItem instanceof Array)) {
        return;
      }
      grouptoolItem.forEach((item, index) => {
        const toolItem = this.grouptoolItems[index];
        const {
          height,
          width
        } = toolItem;
        // 创建拖拽时的预览图形
        const createDragPreview = () => {
          const elt = document.createElement("div");
          elt.style.border = "2px dotted black";
          elt.style.width = `${width}px`;
          elt.style.height = `${height}px`;
          elt.style.transform = "translate(-50%,-50%)";
          elt.className = toolItem.class;
          return elt;
        };
        // drop的处理函数
        const dropHandler = (graph, evt, cell, x, y) => {
          this.instanceCell(cell, toolItem, x, y);
        };
        // 获取拖放的对象
        const getDropTarget = (graph, x, y) => {
          const cell = graph.getCellAt(x, y);
          return R.propOr(null, "dropAble", cell) ? cell : null;
        };
        mxUtils.makeDraggable(
          item,
          this.graph,
          dropHandler,
          createDragPreview(index),
          0,
          0,
          false,
          true,
          true,
          getDropTarget
        );
      });
    },
    // 调整颜色
    changeShape(edge, type) {
      console.log(edge, type);
      switch (type) {
        case 0:
          this.graph.setCellStyles(
            mxConstants.STYLE_STROKECOLOR,
            "#ffd54b",
            edge
          );
          break;
        case 1:
          this.graph.setCellStyles(
            mxConstants.STYLE_STROKECOLOR,
            "#ac7300",
            edge
          );
          break;
        case 2:
          this.graph.setCellStyles(
            mxConstants.STYLE_STROKECOLOR,
            "green",
            edge
          );
          break;
        case 3:
          this.graph.setCellStyles(mxConstants.STYLE_STROKECOLOR, "red", edge);
          break;
        case 4:
          this.graph.setCellStyles(mxConstants.STYLE_STROKECOLOR, "orange", edge);
          break;
        case 5:
          this.graph.setCellStyles(mxConstants.STYLE_STROKECOLOR, "skyblue", edge);
          break;
        case 6:
          this.graph.setCellStyles(mxConstants.STYLE_STROKECOLOR, "purple", edge);
          break;
        case 7:
          this.graph.setCellStyles(mxConstants.STYLE_STROKECOLOR, "yellow", edge);
          break;
      }
      this.graph.setCellStyles(mxConstants.STYLE_STROKEWIDTH, "2", edge);
    },
    // 新增组元素
    instanceCell(dropCell, toolItem, x, y) {
      const drop = !R.isNil(dropCell);
      // drop && this.$message.info(`${toolItem['title']}节点入${dropCell.title}`);
      const styleObj = toolItem["style"] || {};
      const style = Object.keys(styleObj)
        .map((key) => `${key}=${styleObj[key]}`)
        .join(";");
      const realX = drop ? x - dropCell.geometry.x : x;
      const realY = drop ? y - dropCell.geometry.y : y;
      const {
        height,
        width
      } = toolItem;
      const parent = drop ? dropCell : this.graph.getDefaultParent();
      const isHtml = Object.is("1", toolItem["style"]["html"]);
      const tmpIndex = Date.now();
      const value = isHtml ? toolItem["html"](tmpIndex) : null;
      this.graph.getModel().beginUpdate();
      try {
        const vertex = this.graph.insertVertex(
          parent,
          null,
          value,
          realX - width / 2,
          realY - height / 2,
          width,
          height,
          style + ";whiteSpace=wrap;word-break=break-all"
        );
        vertex["title"] = toolItem["title"];
        vertex["dropAble"] = toolItem["dropAble"];
        vertex.modelnum = toolItem["modelnum"];
        vertex["id"] = toolItem["id"];
        vertex["isGroup"] = toolItem["id"].includes("group") ? true : false;
        vertex.width = toolItem.width;
        vertex.height = toolItem.height;
        // 设置连接点
        // cell['constraints'] = toolItem['constraints']
        this.$nextTick(() => {
          const createdCallback = toolItem["created"];
          if (createdCallback instanceof Function) {
            createdCallback(this.graph, vertex, tmpIndex);
          }
        });
      } finally {
        this.graph.getModel().endUpdate();
      }
    },

    // 基础配置函数
    eventCenter() {
      // 给graph添加事件
      // 监听自定义事件
      this.graph.addListener(mxEvent.NORMAL_TYPE_CLICKED, (sender, evt) => {
        let cell = evt.properties.cell.state.cell;
        this.currentNormalType = cell;
      });
      this.graph.dblClick = function (evt, cell) {
        const model = this.graph.getModel();
        if (model.isVertex(cell)) {
          return false;
        }
      };
      // this.graph.addListener(mxEvent.VERTEX_START_MOVE, (sender, evt) => {
      //   console.log('VERTEX_START_MOVE', sender, evt);
      // });
      // 画布平移事件
      this.graph.addListener(mxEvent.PAN, (sender, evt) => {
        // console.log("画布平移了", sender, evt);
      });
      // 新增节点事件
      this.graph.addListener(mxEvent.ADD_CELLS, (sender, evt) => {
        console.log("======================新增节点事件");
        this.$nextTick(() => {
          const addCell = evt.properties.cells[0];
          if (addCell.vertex) {
            // 判断是否为组节点
            if (addCell.isGroup) {
              this.$message.info("添加了一个组");
              let groupObj = _.pick(addCell, [
                "id",
                "title",
                "parent",
                "geometry",
              ]);
              this.jsonData["cells"]["groups"].push(groupObj);
            } else {
              console.log(evt);
              if (evt.properties.cells[0].isBasicElement) {
                this.resourceDataAssembly(evt.properties.parent.children);
              }
              

              let nodeObj = _.pick(addCell, [
                "id",
                "title",
                "parent",
                "geometry",
                "modelnum",
              ]);
              // debugger

              this.jsonData["cells"]["nodes"].push(nodeObj);
              // this.$message.info("添加了一个节点");

              return;
            }
            //  向jsonData中更新数据
          } else if (addCell.edge) {
            console.log(
              this.connectDotData,
              "===this.connectDotData.data==="
            );
            if (
              !this.connectDotData.data[this.connectDotData.data.length - 1] || !this.connectDotData.edge
                .source.isBasicElement
            ) {
              this.graph.removeCells([addCell]);
              window.alert("与线条类型不匹配");
              return;
            }
            console.log(this.dataObj);

            // 检验连线类型
            let sourceIndex;
            let targetIndex;
            let sourceType;
            let targetType;
            if (this.connectDotData.data.length != 2) {
              // TODO: figure out what is this?
              // console.log(addCell.source.id);
              sourceIndex = this.connectDotData.data[0].portId;
              targetIndex = this.connectDotData.data[0].portId;
              sourceType = this.dataObj[addCell.source.id].anchorPoint[sourceIndex].name;
              targetType = this.dataObj[addCell.source.id].anchorPoint[targetIndex].name;
            } else {
              sourceIndex = this.connectDotData.data[this.connectDotData.data.length - 2].portId;
              targetIndex = this.connectDotData.data[this.connectDotData.data.length - 1].portId;
              // console.log(addCell.source.id, sourceIndex);
              // console.log(addCell.target.id, targetIndex);
              sourceType = this.dataObj[addCell.source.id].anchorPoint[sourceIndex].name;
              if (addCell.target.id.split('-')[0] === 'bus' && this.dataObj[addCell.target.id].anchorPoint.length === 0 && this.dataObj[addCell.target.id].refname == "母线") {
                // targetType = this.dataObj[addCell.source.id].anchorPoint[sourceIndex].name;
                targetType = 母线类型创建规则[sourceType][0];
                this.dataObj[addCell.target.id].refname = targetType
              } else {
                targetType = this.dataObj[addCell.target.id].refname
              }
            }

            let lookup_keys = [sourceType+"_"+targetType, targetType+"_"+sourceType]

            // 若目标不在锚点上，则删除这条线
            if (addCell.target === null) {
              this.graph.removeCells([addCell]);
              this.$message('目标不在锚点上')
              return
            }

            // 若连接母线，则母线所有锚点转换成和连接的锚点一样的类型
            if (this.dataObj[addCell.target.id].nodeType === 'bus') {
            // if (this.dataObj[addCell.target.id].nodeType === 'bus' && this.dataObj[addCell.target.id].anchorPoint.length === 0) {
              if (this.dataObj[addCell.target.id].anchorPoint.length >99){
                
              this.graph.removeCells([addCell]);
              this.$message('母线不能连接超过99条线') ;return }
              for (let i = 0; i < 100; i++) {
                this.dataObj[addCell.target.id].anchorPoint.push({ type:targetType })
              }
            }
            // 判断两个锚点的类型是否一致
            if (sourceType !== targetType) {
              window.alert("源连接类型为" + sourceType + "," + "目标连接类型为" + targetType
              );
              this.graph.removeCells([addCell]);
              return;
            } else {
              // 每个锚点只能连接一条线
              // if (this.mPoint.includes(addCell.source.id + sourceIndex) || this.mPoint.includes(addCell.target.id + targetIndex)) {
              //   this.graph.removeCells([addCell]);
              //   this.$message('每个锚点只能连接一条线')
              // } else {
              //   this.mPoint.push(addCell.source.id + sourceIndex, addCell.target.id + targetIndex)
              // }
              let arr = this.mPoint.map((item) => {
                return Object.values(item).join()
              })

              if (arr.includes(addCell.source.id + '-' + sourceIndex) || arr.includes(addCell.target.id + '-' + targetIndex)) {
                this.graph.removeCells([addCell]);
                this.$message('每个锚点只能连接一条线')
              } else {
                const lineId = addCell.mxObjectId
                this.mPoint.push({ [lineId + 'b']: addCell.source.id + '-' + sourceIndex }, { [lineId + 'a']: addCell.target.id + '-' + targetIndex })
              }
            }
            let cell = this.graph.getSelectionCells();
            // this.changeShape([...cell], Number(sourceType));
            this.changeShape([...cell], sourceType);
            let lineObj = _.pick(addCell, [
              "id",
              "edge",
              "source",
              "parent",
              "geometry",
              "value",
            ]);
            this.jsonData["edges"].push(lineObj);
          }
        });
        console.log(this.componentTable, '===新增===');
        console.log(this.dataObj);
        // this.dataObj = JSON.parse(JSON.stringify(this.dataObj))
        console.log(Object.keys(this.dataObj), '=====数据======');
        Object.keys(this.dataObj).forEach(item => {
          console.log(item);
        })
        let arr = []
        this.connectDotData.data = [];
      });
      //拖动节点的事件
      this.graph.addListener(mxEvent.CELLS_MOVED, (sender, evt) => {
        // console.log(this.graph, "graph");
        let cellsName = [];
        this.$nextTick(() => {
          evt.properties.cells.forEach((item) => {
            item.parent.id.includes("group") && cellsName.push(item.title);
          });
          evt.properties.cells[0].parent.id !== "1" &&
            this.$message.info(
              `${[...cellsName]}节点进入${evt.properties.cells[0].parent.title}`
            );
        });
      });

      // 删除节点触发事件
      this.graph.addListener(mxEvent.CELLS_REMOVED, (sender, evt) => {
        // console.log('=====删除=====');
        this.$nextTick(() => {
          this.resource(evt.properties.cells[0]);
          let removeCells = evt.properties.cells;
          // console.log(removeCells, "removeCells");
          removeCells.forEach((item) => {
            // 拿每一个cellId在jsonData中进行遍历,并进行移除
            if (item.vertex) {
              // 判断是否为组节点
              if (item.isGroup) {
                // this.$message.info(`移除了${item.id}组`);
                this.jsonData["cells"]["groups"].splice(
                  this.jsonData["cells"]["groups"].findIndex((jsonItem) => {
                    return jsonItem.id === item.id;
                  }),
                  1
                );
              } else {
                console.log(item.id);
                delete this.dataObj[item.id];
                // this.$message.info(`移除${item.id}节点`);
                this.jsonData["cells"]["nodes"].splice(
                  this.jsonData["cells"]["nodes"].findIndex((jsonItem) => {
                    return jsonItem.id === item.id;
                  }),
                  1
                );
                // console.log(this.dataObj);
              }
            } else if (item.edge) {
              // this.$message.info("移除了线");
              this.jsonData["edges"].splice(
                this.jsonData["edges"].findIndex((jsonItem) => {
                  return jsonItem.id === item.id;
                }),
                1
              );
            }
            // this.jsonData.forEach(item)
          });
        });
      });

      // A
      // 创建连线成功
      this.graph.connectionHandler.addListener(
        mxEvent.CONNECT,
        (sender, evt, b, c) => {
          console.log(this.connectDotData);
          // 连线的锚点信息
          this.connectionsAnchors.push(this.connectDotData)
          console.log('连线成功');
        }
      );
      // // this.graph.connectionHandler.createConnection(e => {
      // //   console.log(e);
      // // });
      this.graph.addListener(mxEvent.CHANGE, function (sender, evt) {
        console.log(evt, "mxEvent.CHANGE");
      });
      let that = this;
      // // 连线约束 获取到两个锚点的信息 将数据保存在connectDotData中
      this.graph.setConnectionConstraint = function (
        edge,
        terminal,
        source,
        constraint
      ) {
        console.log(constraint, "========setConnectionConstraint======");
        if (constraint != null) {
          this.model.beginUpdate();
          that.anchorInfo(edge, terminal, source, constraint);
          try {
            if (constraint == null || constraint.point == null) {
              this.setCellStyles(
                source ? mxConstants.STYLE_EXIT_X : mxConstants.STYLE_ENTRY_X,
                null,
                [edge]
              );
              this.setCellStyles(
                source ? mxConstants.STYLE_EXIT_Y : mxConstants.STYLE_ENTRY_Y,
                null,
                [edge]
              );
              this.setCellStyles(
                source ? mxConstants.STYLE_EXIT_DX : mxConstants.STYLE_ENTRY_DX,
                null,
                [edge]
              );
              this.setCellStyles(
                source ? mxConstants.STYLE_EXIT_DY : mxConstants.STYLE_ENTRY_DY,
                null,
                [edge]
              );
              this.setCellStyles(
                source ?
                  mxConstants.STYLE_EXIT_PERIMETER :
                  mxConstants.STYLE_ENTRY_PERIMETER,
                null,
                [edge]
              );
            } else if (constraint.point != null) {
              this.setCellStyles(
                source ? mxConstants.STYLE_EXIT_X : mxConstants.STYLE_ENTRY_X,
                constraint.point.x,
                [edge]
              );
              this.setCellStyles(
                source ? mxConstants.STYLE_EXIT_Y : mxConstants.STYLE_ENTRY_Y,
                constraint.point.y,
                [edge]
              );
              this.setCellStyles(
                source ? mxConstants.STYLE_EXIT_DX : mxConstants.STYLE_ENTRY_DX,
                constraint.dx,
                [edge]
              );
              this.setCellStyles(
                source ? mxConstants.STYLE_EXIT_DY : mxConstants.STYLE_ENTRY_DY,
                constraint.dy,
                [edge]
              );

              // Only writes 0 since 1 is default
              if (!constraint.perimeter) {
                this.setCellStyles(
                  source ?
                    mxConstants.STYLE_EXIT_PERIMETER :
                    mxConstants.STYLE_ENTRY_PERIMETER,
                  "0",
                  [edge]
                );
              } else {
                this.setCellStyles(
                  source ?
                    mxConstants.STYLE_EXIT_PERIMETER :
                    mxConstants.STYLE_ENTRY_PERIMETER,
                  null,
                  [edge]
                );
              }
            }
          } finally {
            this.model.endUpdate();
          }
        }
      };
    },
    // A 资源表数据组装
    resourceDataAssembly(data) {
      console.log(data);
      const map = new Map();
      data.forEach((item) => {
        if (item.vertex) {
          const prefix = item.id.split("-")[0];
          if (!map.has(prefix)) {
            map.set(prefix, {
              label: this.modelType[prefix],
              children: [],
            });
          }
          map.get(prefix).children.push({
            label: item.id,
            data: item,
          });
        }
      });
      this.elementData = data;
      if (this.isShow.isShowName) {
        this.showHiddenName();
      }
      this.resourceData = Array.from(map.values());
    },
    // A 资源表数据删除
    resource(cells) {
      delete this.elementData[
        this.elementData.map((item, index) => {
          if (cells.id === item.id) return index;
        })
      ];
      this.resourceDataAssembly(this.elementData);
    },

    // A点击资源树
    handleNodeClick(e) {
      if (e.data) {
        console.log(e, "点击了资源表");
        this.selectCell(e.data.id);
      }
    },
    // A选中节点方法
    SelectElement(id) {
      this.graph.selectAll();
      var cells = this.graph.getSelectionCells();
      this.graph.clearSelection();
      for (var i = 0; i < cells.length; i++) {
        if (cells[i].id == id) {
          return cells[i];
        }
      }
      return null;
    },
    // A 选中节点方法
    selectCell(id) {
      const cell = this.SelectElement(id);
      const dome = this.$refs.container.firstElementChild;
      // const num = this.graph.getView().getScale();
      // let magnification;
      if (cell) {
        // let obj = this.graph.view.getState(cell);
        this.graph.setSelectionCell(cell);
        this.transferData(cell);
        let x = -cell.geometry.x + (dome.clientWidth - cell.geometry.width) / 2 - 150;
        let y = -cell.geometry.y +
          (dome.clientHeight - cell.geometry.height) / 2 -
          50;
        this.graph.getView().setTranslate(x, y);
      } else {
        alert("您选择的图形不在画布中！");
      }
    },
    // A获取连线时锚点信息
    anchorInfo(edge, terminal, source, constraint) {
      // console.log(edge, terminal, source, constraint);
      console.log(constraint);
      if (constraint) {
        this.connectDotData.data.push(constraint);
        this.connectDotData.edge = edge;
      } else {
        this.connectDotData = {
          data: [],
          edge: [],
        };
      }
      console.log(this.connectDotData);
    },
    // 配置鼠标事件
    configMouseEvent() {
      this.graph.addMouseListener({
        currentState: null,
        previousStyle: null,

        // 鼠标按下
        mouseDown: (sender, evt) => {
          if (!evt.state) {
            // console.log("点击了画布");
            // console.log(this.graph);
            return;
          } else if (evt.state.cell.edge) {
            // console.log("点击了连线");
            return;
          }

          const cell = evt.state.cell;
          let clickNormalType = false;
          if (cell.style !== undefined) {
            clickNormalType = cell.style.includes("normalType");
          }
          if (clickNormalType) {
            // 使用 mxGraph 事件中心，注册自定义事件
            this.graph.fireEvent(
              new mxEventObject(mxEvent.NORMAL_TYPE_CLICKED, "cell", evt)
            );
          } else {
            return;
          }
        },

        mouseMove: (sender, me) => {
          this.graphX = Math.ceil(me.graphX);
          this.graphY = Math.ceil(me.graphY); // 创建缩略图
        },

        //鼠标弹起事件
        mouseUp: (sender, evt) => {
          this.id = "";
          if (this.cellId) {
            console.log(this.dataSource);
            console.log(
              this.$refs.styleSelect.useData,
              this.cellId,
              "==============="
            );
            this.dataObj[this.cellId].params = JSON.parse(
              JSON.stringify(this.$refs.styleSelect.useData)
            );
            this.cellId = "";
            console.log(this.dataObj);
          }

          if (!evt.sourceState) return false;
          else {
            const cell = evt.sourceState.cell;
            // console.log(cell);

            if (cell) {
              console.log(cell);
              if (!cell.edge) {
                this.transferData(cell, evt);
              }
              cell.vertex ? (this.isNode = true) : (this.isNode = false);
              var getcellStyle = cell.getStyle() ? cell.getStyle() : null;
              if (!this.isNode) {
                // 点击的不是节点
                getcellStyle
                  ?
                  (this.edgeStyle = getcellStyle) :
                  "orthogonalEdgeStyle";
              } else {
                // 点击的是节点
                // console.log('getcellStyle', getcellStyle);
                if (getcellStyle) {
                  let arr = getcellStyle.split(";");
                  // arr.pop()
                  let styleObject = {};
                  arr.forEach((item) => {
                    styleObject[item.split("=")[0]] = item.split("=")[1];
                  });
                  this.cellStyle = styleObject;
                }
              }
            } else {
              this.$message.error("请选择节点或者连线");
            }
          }
        },
      });
    },
    transferData(cell, evt) {
      console.log(cell);
      this.cellId = cell.id;
      console.log(this.cellId);
      this.cellObj = cell;
      this.textValue = cell["value"] ? cell["value"] : cell["title"];
      this.importData = this.dataObj[this.cellId].params;
      // console.log(this.importData);
      this.id = cell.id;
      this.modelnum = cell.modelnum;
      this.modelId = cell.id;
      this.modelName = cell.title;
      this.getTypeSelects(cell.id, 1)
    },
    // 获取右侧面板选项
    async getTypeSelects(cellId, proId) {
      let uname = cellId.split('-')[0]
      if (uname === 'dieselOil') {
        //柴油
        const { data: res1 } = await dieselList({ proId })
        this.fuelModels = res1
      } else if (uname === 'electricLoad') {
        //电负荷
        const { data: res } = await electricalLoadList({ loadModel: '1', proId, simulationTime: 0 })
        this.loadSelects = res
      } else if (uname === 'photovoltaics') {
        // 光伏发电
        const { data: res1 } = await lightvList({ proId })
        console.log(res1);
        this.typeSelects = res1
        // const { data: res2 } = await searchElePrice({ proId })
        // console.log(res2);
        // this.costModels = res2
      } else if (uname === 'windPower') {
        // 风力发电
        const { data: res1 } = await draughtList({ proId })
        this.typeSelects = res1
        // const { data: res2 } = await searchElePrice({ proId })
        // this.costModels = res2
      } else if (uname === 'dieselGenerator') {
        // 柴油发电
        const { data: res1 } = await dieselOilList({ proId })
        this.typeSelects = res1
        // const { data: res2 } = await searchElePrice({ proId })
        // this.costModels = res2
      } else if (uname === 'lithiumCell') {
        // 锂电池
        const { data } = await lithiumBatteryList({ proId })
        this.typeSelects = data
      } else if (uname === 'transformer') {
        // 变压器(待完成)
        const res = await transformerList({ proId })
        // console.log(res);
        this.typeSelects = res
      } else if (uname === 'converter') {
        // 变流器(待完成)
        const res = await rectifierList({ containerType: 1, proId })
        // console.log(res);
        this.typeSelects = res
      } else if (uname === 'bidirectionalInverter') {
        // 双向变流器(待完成)
        const res = await rectifierList({ containerType: 2, proId })
        // console.log(res);
        this.typeSelects = res
      } else if (uname === 'transmissionLine') {
        // 传输线(待完成)
        const res = await transmissionLineList({ proId })
        // console.log(res);
        this.typeSelects = res
      }
    },
    //配置键盘事件
    configKeyEvent() {
      // 启动盘事件键
      this.keyHandler = new mxKeyHandler(this.graph);
      // 键盘按下删除键绑定事件
      this.keyHandler.bindKey(46, () => {
        this.deleteNode();
      });
      this.keyHandler.bindControlKey(65, () => {
        this.graph.selectAll();
      });
      this.keyHandler.bindControlKey(67, () => {
        this.copy();
      });
      this.keyHandler.bindControlKey(88, () => {
        this.cut();
      });
      this.keyHandler.bindControlKey(86, () => {
        this.paste();
      });
      this.keyHandler.bindControlKey(89, () => {
        this.goForward();
      });
      this.keyHandler.bindControlKey(90, () => {
        this.goBack();
      });
    },
    //配置右键菜单栏
    configMenu() {
      // 禁用浏览器默认的右键菜单栏
      mxEvent.disableContextMenu(this.$refs.container);
      this.graph.popupMenuHandler.factoryMethod = (menu, cell, parameter) => {
        console.log("右键", menu);
        console.log(cell);
        console.log(parameter);
        if (!cell) {
          menu.addItem("撤销", null, () => {
            this.goBack();
          });
          menu.addSeparator();
          if (this.selectionCells[0]) {
            menu.addItem("粘贴在此处", null, () => {
              this.paste(menu.triggerX, menu.triggerY);
            });
            menu.addSeparator();
          }
          menu.addItem("查看元件表", null, () => {
            this.checkElementTable = true;
          });
          menu.addItem("全选", null, () => {
            this.graph.selectAll();
          });
          menu.addItem(
            this.isShow.isShowName ? "隐藏元件名称" : "显示元件名称",
            null,
            () => {
              if (this.elementData.length === 0) return;
              this.isShow.isShowName = !this.isShow.isShowName;
              this.showHiddenName();
            }
          );
          menu.addItem(
            this.isShow.isShowHot ? "显示热原件" : "隐藏热原件",
            null,
            () => {
              if (this.elementData.length === 0) return;
              this.showElement(this.isShow.isShowHot, "1");
              this.isShow.isShowHot = !this.isShow.isShowHot;
              this.graph.refresh();
            }
          );
          menu.addItem(
            this.isShow.isShowElectricity ? "显示电原件" : "隐藏电原件",
            null,
            () => {
              if (this.elementData.length !== 0) return;
              this.showElement(this.isShow.isShowElectricity, "2");
              this.isShow.isShowElectricity = !this.isShow.isShowElectricity;
            }
          );
        } else if (!cell.edge) {
          menu.addItem("删除", null, () => {
            this.rightParams = this.rightParams.filter(item => {
              return item.id !== this.graph.getSelectionCells()[0].id
            })
            // console.log(this.rightParams);
            this.graph.ungroupCells(this.graph.getSelectionCells());
            this.id = "";
            this.modelnum = "";
            this.modelId = "";
            this.modelName = "";
          });
          menu.addSeparator();
          menu.addItem("剪切", null, () => {
            this.cut();
          });
          menu.addItem("复制", null, () => {
            this.copy();
          });
          menu.addSeparator();
          menu.addItem("置于顶层", null, () => {
            this.toBack(cell);
          });
          menu.addItem("置于底层", null, () => {
            this.toFront(cell);
          });
        } else {
          menu.addItem("删除", null, () => {
            // 针对删除线，锚点不可连接，增加的
            let delLineId = this.graph.getSelectionCells()[0].mxObjectId;
            this.mPoint = this.mPoint.filter((item, i) => {
              return Object.keys(item).join().substring(0, Object.keys(item).join().length - 1) !== delLineId
            })
            // 本来的删除
            this.graph.ungroupCells(this.graph.getSelectionCells());
            this.id = "";
            this.modelnum = "";
            this.modelId = "";
            this.modelName = "";
          });
          menu.addSeparator();
          menu.addItem("剪切", null, () => {
            this.cut();
          });
          menu.addItem("复制", null, () => {
            this.copy();
          });
          menu.addSeparator();
          menu.addItem("置于顶层", null, () => {
            this.toFront(cell);
          });
          menu.addItem("置于底层", null, () => {
            this.toBack(cell);
          });
          menu.addSeparator();
          menu.addItem("添加拐点", null, () => {
            var cell = this.graph.getSelectionCell();

            if (cell != null && this.graph.getModel().isEdge(cell)) {
              var handler = this.editor.graph.selectionCellsHandler.getHandler(cell);

              if (handler instanceof mxEdgeHandler) {
                var t = this.graph.view.translate;
                var s = this.graph.view.scale;
                var dx = t.x;
                var dy = t.y;

                var parent = this.graph.getModel().getParent(cell);
                var pgeo = this.graph.getCellGeometry(parent);

                while (this.graph.getModel().isVertex(parent) && pgeo != null) {
                  dx += pgeo.x;
                  dy += pgeo.y;

                  parent = this.graph.getModel().getParent(parent);
                  pgeo = this.graph.getCellGeometry(parent);
                }

                var x = Math.round(this.graph.snap(this.graph.popupMenuHandler.triggerX / s - dx));
                var y = Math.round(this.graph.snap(this.graph.popupMenuHandler.triggerY / s - dy));

                handler.addPointAt(handler.state, x, y);
              }
            }
          });
          menu.addItem("删除拐点", null, () => {
            var cells = this.graph.getSelectionCells();

            if (cells != null) {
              cells = this.graph.addAllEdges(cells);

              this.graph.getModel().beginUpdate();
              try {
                for (var i = 0; i < cells.length; i++) {
                  var cell = cells[i];

                  if (this.graph.getModel().isEdge(cell)) {
                    var geo = this.graph.getCellGeometry(cell);

                    if (geo != null) {
                      geo = geo.clone();
                      geo.points = null;
                      this.graph.getModel().setGeometry(cell, geo);
                    }
                  }
                }
              } finally {
                this.graph.getModel().endUpdate();
              }
            }
          });
        }

        // menu.addItem("流动的线(测试)", null, () => {
        //   let cell = this.graph.getSelectionCell();
        //   if (cell && cell.edge) {
        //     let state = this.graph.view.getState(cell);
        //     state.shape.node
        //       .getElementsByTagName("path")[0]
        //       .removeAttribute("visibility");
        //     state.shape.node
        //       .getElementsByTagName("path")[0]
        //       .setAttribute("stroke-width", "6");
        //     state.shape.node
        //       .getElementsByTagName("path")[0]
        //       .setAttribute("stroke", "lightGray");
        //     state.shape.node
        //       .getElementsByTagName("path")[1]
        //       .setAttribute("class", "flow");
        //   } else {
        //     this.$message.error("请选择连线");
        //   }
        // });
        // menu.addSeparator();
        // menu.addItem('配置完成', null, () => {
        //   let cell = this.graph.getSelectionCell().children[0];
        //   let cellArrayStyle = cell.getStyle().split(';');
        //   cellArrayStyle.shift();
        //   let cellStyle = {};
        //   cellArrayStyle.forEach(item => {
        //     cellStyle[item.split('=')[0]] = item.split('=')[1];
        //   });
        //   let cellImage = cellStyle['image'].replace('unselect', 'selected');
        //   this.graph.setCellStyles(mxConstants.STYLE_IMAGE, cellImage, [cell]);
        //   this.graph.refresh(cell);
        // });

        // 分割符号
        // menu.addSeparator();
        // menu.addItem("修改样式", null, () => {
        //   var cell = this.graph.getSelectionCell();
        //   if (cell) {
        //     cell.vertex ? (this.isNode = true) : (this.isNode = false);
        //     var getcellStyle = cell.getStyle() ? cell.getStyle() : "";
        //     if (getcellStyle) {
        //       var arr = getcellStyle.split(";");
        //       //弹出最后一个空样式
        //       // arr.pop()
        //       var styleObject = {};
        //       arr.forEach(item => {
        //         styleObject[item.split("=")[0]] = item.split("=")[1];
        //       });
        //       this.cellStyle = styleObject;
        //       // if (this.isNode) {

        //       // }
        //     }
        //   } else {
        //     this.$message.error("请选择节点或者连线");
        //   }
        // });
      };
    },
    //  配置全局样式
    configureStylesheet(graph) {
      // 设置节点的文字可被移动
      // graph.vertexLabelsMovable = false;
      // 设置鼠标悬浮至节点或者连线时高亮显示的颜色
      // new mxCellTracker(graph, "#409eff");
      var style = new Object();
      style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_LABEL;
      style[mxConstants.STYLE_PERIMETER] = mxPerimeter.RectanglePerimeter;
      style[mxConstants.STYLE_VERTICAL_ALIGN] = mxConstants.ALIGN_MIDDLE;
      style[mxConstants.STYLE_ALIGN] = mxConstants.ALIGN_CENTER;
      style[mxConstants.STYLE_IMAGE_ALIGN] = mxConstants.ALIGN_CENTER;
      style[mxConstants.STYLE_IMAGE_VERTICAL_ALIGN] = mxConstants.ALIGN_CENTER;
      // style[mxConstants.STYLE_SPACING_TOP] = 6;
      style[mxConstants.STYLE_SPACING_LEFT] = 5;
      // style[mxConstants.STYLE_GRADIENTCOLOR] = 'skyblue'; // 渐变颜色
      style[mxConstants.STYLE_STROKECOLOR] = "#5d65df"; // 线条颜色
      style[mxConstants.STYLE_FILLCOLOR] = "#FFFFFF";
      style[mxConstants.STYLE_FONTCOLOR] = "#1d258f"; // 字体颜色
      style[mxConstants.STYLE_FONTFAMILY] = "Verdana"; // 字体风格
      style[mxConstants.STYLE_FONTSIZE] = "12"; // 字体大小
      style[mxConstants.STYLE_FONTSTYLE] = "0"; // 斜体字
      style[mxConstants.WORD_WRAP] = "normal"; // 文字换行    word-break: break-all;
      style[mxConstants["word-break"]] = "break-all"; // 文字换行
      style[mxConstants.STYLE_WHITE_SPACE] = "wrap"; // 文字换行
      // style[mxConstants.STYLE_ROUNDED] = false; // 圆角
      style[mxConstants.STYLE_IMAGE_WIDTH] = "28"; // 图片宽度
      style[mxConstants.STYLE_IMAGE_HEIGHT] = "28"; // 图片高度
      style[mxConstants.STYLE_OPACITY] = "100"; // 节点透明度(不包含字体)
      delete graph.getStylesheet().getDefaultEdgeStyle()["endArrow"]; //去掉箭头
      graph.getStylesheet().putDefaultVertexStyle(style);

      style = new Object();
      style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_SWIMLANE;
      style[mxConstants.STYLE_PERIMETER] = mxPerimeter.RectanglePerimeter;
      style[mxConstants.STYLE_ALIGN] = mxConstants.ALIGN_CENTER;
      style[mxConstants.STYLE_VERTICAL_ALIGN] = mxConstants.ALIGN_TOP;
      style[mxConstants.STYLE_FILLCOLOR] = "#409eff";
      // style[mxConstants.STYLE_GRADIENTCOLOR] = '#409eff';
      style[mxConstants.STYLE_STROKECOLOR] = "#409eff";
      style[mxConstants.STYLE_FONTCOLOR] = "#000000";
      // style[mxConstants.STYLE_ROUNDED] = false;
      style[mxConstants.STYLE_OPACITY] = "80";
      style[mxConstants.STYLE_STARTSIZE] = "30";
      style[mxConstants.STYLE_FONTSIZE] = "16";
      style[mxConstants.STYLE_FONTSTYLE] = 1;
      graph.getStylesheet().putCellStyle("group", style);

      style = new Object();
      style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_IMAGE;
      style[mxConstants.STYLE_FONTCOLOR] = "#774400";
      style[mxConstants.STYLE_PERIMETER] = mxPerimeter.RectanglePerimeter;
      style[mxConstants.STYLE_PERIMETER_SPACING] = "6";
      style[mxConstants.STYLE_ALIGN] = mxConstants.ALIGN_LEFT;
      style[mxConstants.STYLE_VERTICAL_ALIGN] = mxConstants.ALIGN_MIDDLE;
      style[mxConstants.STYLE_FONTSIZE] = "10";
      style[mxConstants.STYLE_FONTSTYLE] = 2;
      style[mxConstants.STYLE_IMAGE_WIDTH] = "16";
      style[mxConstants.STYLE_IMAGE_HEIGHT] = "16";
      style[mxConstants.STYLE_BACKGROUNDCOLOR] = "transparent";
      graph.getStylesheet().putCellStyle("port", style);

      style = graph.getStylesheet().getDefaultEdgeStyle();
      style[mxConstants.STYLE_LABEL_BACKGROUNDCOLOR] = "#FFFFFF";
      style[mxConstants.STYLE_STROKEWIDTH] = "";
      style[mxConstants.STYLE_ROUNDED] = false;
      style[mxConstants.STYLE_EDGESTYLE] = mxEdgeStyle.SegmentConnector;
      // 获取全局Edge、label样式
      var edgeStyle = this.graph.getStylesheet().getDefaultEdgeStyle();
      let labelStyle = this.graph.getStylesheet().getDefaultVertexStyle();
      // labelStyle[mxConstants.STYLE_WHITE_SPACE] = 'wrap'; //自动换行
      // console.log(labelStyle, "labelStyle");
      // 设置连线风格(设置为正交折线)
      edgeStyle["edgeStyle"] = "orthogonalEdgeStyle";

      // A=======================================================
      // 实验设置连线样式
      // 连线点击生成拐点
      mxConnectionHandler.prototype.movePreviewAway = false;
      mxConnectionHandler.prototype.waypointsEnabled = true;
      var invert = false;
      if (invert) {
        // container.style.backgroundColor = "black";

        // 白色就地编辑器文本颜色
        // White in-place editor text color
        // var mxCellEditorStartEditing = mxCellEditor.prototype.startEditing;
        // mxCellEditor.prototype.startEditing = function (cell, trigger) {

        var mxCellEditorStartEditing = mxEditor.prototype.startEditing;
        mxEditor.prototype.startEditing = function () {
          mxCellEditorStartEditing.apply(this, arguments);

          if (this.textarea != null) {
            this.textarea.style.color = "#FFFFFF";
          }
        };

        mxGraphHandler.prototype.previewColor = "white";
      }
      var labelBackground = invert ? "#000000" : "#FFFFFF";
      var fontColor = invert ? "#FFFFFF" : "#000000";
      var strokeColor = invert ? "#C0C0C0" : "#000000";
      // var fillColor = invert ? "none" : "#FFFFFF";
      var strokeWidth = 2;
      var joinNodeSize = 7;

      style = graph.getStylesheet().getDefaultEdgeStyle();
      delete style["endArrow"];
      style["strokeColor"] = strokeColor;
      style["labelBackgroundColor"] = labelBackground;
      // style["edgeStyle"] = "wireEdgeStyle"; //线条类型  设置为直线
      style["fontColor"] = fontColor;
      style["fontSize"] = "9";
      style["movable"] = "0";
      style["strokeWidth"] = strokeWidth;
      //style['rounded'] = '1';

      // Sets join node size
      style["startSize"] = joinNodeSize;
      style["endSize"] = joinNodeSize;

      style = graph.getStylesheet().getDefaultVertexStyle();
      style["gradientDirection"] = "south";
      //style['gradientColor'] = '#909090';
      style["strokeColor"] = strokeColor;
      //style['fillColor'] = '#e0e0e0';
      style["fillColor"] = "none";
      style["fontColor"] = fontColor;
      style["fontStyle"] = "1";
      style["fontSize"] = "12";
      // style["resizable"] = "0"; //设置图源是否可以缩放
      // style["rounded"] = "1";
      style["strokeWidth"] = strokeWidth;

      // =======================================================

      // 选中 cell/edge 后的伸缩大小的点/拖动连线位置的点的颜色
      // style[mxConstants.STYLE_WHITE_SPACE] = 'wrap'

      mxConstants.HANDLE_FILLCOLOR = "#409eff";
      mxConstants.HANDLE_STROKECOLOR = "transparent";
      mxConstants.STYLE_ANCHOR_POINT_DIRECTION = "anchorPointDirection";
      mxConstants.STYLE_STYLE_ROTATION = "rotation";
      // 是否缩放网格
      mxGraphHandler.prototype.scaleGrid = true;
      mxGraph.prototype.pageBreakDashed = false;

      // 指定是否应使用其他单元格对齐当前所选内容的右侧，中间或左侧。默认为false。
      mxGraphHandler.prototype.guidesEnabled = true;
      mxGraphHandler.prototype.htmlPreview = false;
      mxGraphHandler.prototype.allowLivePreview = true;
      // 指定预览形状的颜色。默认为黑色。
      mxGraphHandler.prototype.previewColor = "red";
      // 应该使用实时预览的最大单元数。默认值为0，表示没有实时预览。
      mxGraphHandler.prototype.maxLivePreview = 100;

      // Alt 按下禁用导航线
      mxGraphHandler.prototype.useGuidesForEvent = function (me) {
        return !mxEvent.isAltDown(me.getEvent());
      };
      // 导航线颜色
      mxConstants.GUIDE_COLOR = "#1a73e8";
      // 导航线宽度
      mxConstants.GUIDE_STROKEWIDTH = 2;
      // 导航线自动连接到目标
      mxEdgeHandler.prototype.snapToTerminals = true;
      // mxEdgeHandler.prototype.connect = function (
      //   edge,
      //   terminal,
      //   isSource,
      //   isClone,
      //   me
      // ) {
      //   console.log(edge, terminal, isSource, isClone, me, "===========");
      // };
      // 选中线条时的虚线颜色
      mxConstants.EDGE_SELECTION_COLOR = "#99ccff";
      // mxConstants.DEFAULT_INVALID_COLOR = 'yellow';
      // mxConstants.INVALID_CONNECT_TARGET_COLOR = 'yellow';
      // 连线(未满足连线要求)时预览的颜色
      mxConstants.INVALID_COLOR = "#99ccff";
      // 连线(满足连线要求)时预览的颜色
      mxConstants.VALID_COLOR = "blue";
      // mxConstants.GUIDE_COLOR = 'yellow';
      // mxConstants.LOCKED_HANDLE_FILLCOLOR = '#24bcab';
      // 选中节点时选中框的颜色
      mxConstants.VERTEX_SELECTION_COLOR = "#99ccff";

      //折叠-/展开+图标大小
      // mxGraph.prototype.collapsedImage = new mxImage('images/collapsed.gif', 15, 15);
      // mxGraph.prototype.expandedImage = new mxImage('images/expanded.gif', 15, 15);

      // 配置节点中心的连接图标(注釋掉即可指定錨點連接到另一個節點的錨點上)
      // mxConnectionHandler.prototype.connectImage = new mxImage(
      //   "./icon/connectionpoint.png",
      //   14,
      //   14
      // );
      // 显示中心端口图标
      graph.connectionHandler.targetConnectImage = false;
      // 是否开启浮动自动连接
      this.graph.connectionHandler.isConnectableCell = function (cell) {
        return true;
      };
      // 设定锚点的位置、可编辑状态和图标
      mxConstraintHandler.prototype.pointImage = new mxImage(
        "icon/dot.gif",
        10,
        10
      );
      // 设置锚点上的高亮颜色
      mxConstraintHandler.prototype.createHighlightShape = function () {
        return new mxEllipse(null, "#409eff99", "#409eff99", 15);
      };

      mxShape.prototype.constraints = [];
      mxPolyline.prototype.constraints = null;

      // A 设置锚点连接线条
      graph.view.scale = 1;
      graph.setPanning(true);
      graph.setConnectable(true);
      graph.setConnectableEdges(true);
      graph.setDisconnectOnMove(false);
      graph.foldingEnabled = false;
      style[mxConstants.STYLE_EDGE] = mxEdgeStyle.ElbowConnector;
      style[mxConstants.STYLE_EDGESTYLE] = mxEdgeStyle.SegmentConnector;

      // 确保非相对单元格只能通过约束进行连接
      graph.connectionHandler.isConnectableCell = function (cell) {
        if (this.graph.getModel().isEdge(cell)) {
          return true;
        } else {
          var geo = cell != null ? this.graph.getCellGeometry(cell) : null;

          return geo != null ? geo.relative : false;
        }
      };
      mxEdgeHandler.prototype.isConnectableCell = function (cell) {
        return graph.connectionHandler.isConnectableCell(cell);
      };
    },

    //设置连线样式
    changeDashed(value) {
      var cell = this.graph.getSelectionCells();
      this.graph.setCellStyles(mxConstants.STYLE_DASHED, value, [...cell]);
      // this.graph.refresh(cell)
    },

    //设置线条颜色样式
    changeStrokeColor(value) {
      var cell = this.graph.getSelectionCells();
      this.graph.setCellStyles(mxConstants.STYLE_STROKECOLOR, value, [...cell]);
      // this.graph.refresh(cell)
    },

    //设置线条宽度
    changeStrokeWidth(value) {
      var cell = this.graph.getSelectionCells();
      this.graph.setCellStyles(mxConstants.STYLE_STROKEWIDTH, value, [...cell]);
      // this.graph.refresh(cell)
    },

    //设置字体大小
    changeFontSize(value) {
      var cell = this.graph.getSelectionCells();
      this.graph.setCellStyles(mxConstants.STYLE_FONTSIZE, value, [...cell]);
      // this.graph.refresh(cell)
    },

    //设置字体颜色
    changeFontColor(value) {
      var cell = this.graph.getSelectionCells();
      this.graph.setCellStyles(mxConstants.STYLE_FONTCOLOR, value, [...cell]);
      // this.graph.refresh(cell)
    },

    //设置线条说明的背景颜色
    changeLabelBackgroundColor(value) {
      var cell = this.graph.getSelectionCells();
      this.graph.setCellStyles(mxConstants.STYLE_LABEL_BACKGROUNDCOLOR, value, [
        ...cell,
      ]);
      // this.graph.refresh(cell)
    },

    changeFillColor(value) {
      var cell = this.graph.getSelectionCells();
      this.graph.setCellStyles(mxConstants.STYLE_FILLCOLOR, value, [...cell]);
    },

    changeShadow(value) {
      var cell = this.graph.getSelectionCells();
      this.graph.setCellStyles(mxConstants.STYLE_SHADOW, +value, [...cell]);
    },

    changeFontStyle(value) {
      var cell = this.graph.getSelectionCells();
      this.graph.setCellStyles(mxConstants.STYLE_FONTSTYLE, value, [...cell]);
    },

    changeNodeimage(value) {
      var cell = this.graph.getSelectionCells();
      this.graph.setCellStyles(mxConstants.STYLE_IMAGE, value, [...cell]);
    },

    // 删除节点
    deleteNode() {
      this.rightParams = this.rightParams.filter(item => {
        return item.id !== this.graph.getSelectionCells()[0].id
      })
      var cells = this.graph.getSelectionCells();
      this.graph.removeCells([...cells]);
      this.id = "";
      this.modelnum = "";
      this.modelId = "";
      this.modelName = "";
    },

    // 修改连线样式
    edgeChange(value) {
      try {
        var cell = this.graph.getSelectionCells();
        this.graph.setCellStyles("edgeStyle", value, [...cell]);
        let style = cell[0].style;
        let valStr = cell[0].value;
        this.graph.removeCells(cell);
        let parent = this.graph.getDefaultParent();
        let v1 = "";
        let v2 = "";
        // 获取ID单元
        parent["children"].forEach((item) => {
          item["id"] === cell[0].source.id ? (v1 = item) : false;
          item["id"] === cell[0].target.id ? (v2 = item) : false;
        });
        this.graph.getModel().beginUpdate();
        this.graph.insertEdge(parent, null, valStr, v1, v2, style);

        // if (source.isVertex()) { // 如果起始点是元素
        //   var sourceAnchor = getAnchorByLocation(source, edge.getGeometry().getPoints().first()); // 获取连接起点的锚点
        //   edge.setTerminal(source, sourceAnchor.index); // 设置起始点和锚点
        // }

        // if (target.isVertex()) { // 如果终点是元素
        //   var targetAnchor = getAnchorByLocation(target, edge.getGeometry().getPoints().last()); // 获取连接终点的锚点
        //   edge.setTerminal(target, targetAnchor.index); // 设置终点和锚点
        // }
        this.graph.getModel().endUpdate();
        this.$message.success("切换连线样式成功");
      } catch (error) {
        this.$message.error("切换连线样式失败");
        console.log(error);
      }
    },

    // 修改节点文本内容
    textValueChange(value) {
      var cell = this.graph.getSelectionCells();
      console.log(value, "节点文本新内容", this.graph);
      console.log(cell[0]);
      this.graph.cellLabelChanged(cell[0], value);
    },

    changeConfigOrder(val) {
      // 获取当前的normalType元素,并更新他的title
      this.currentNormalType.title = val.newConfigOrder;
      // 修改指定cell的背景图片
      this.graph.setCellStyles(
        mxConstants.STYLE_IMAGE,
        `./images/order/unselect-${val.newConfigOrder}.png`,
        [this.currentNormalType]
      );
      this.graph.refresh(this.currentNormalType);
    },

    //复制
    copy() {
      this.selectionCells = this.graph.getSelectionCells();
      mxClipboard.copy(this.graph, this.selectionCells);
    },
    //粘贴
    paste(x, y) {
      const id = this.selectionCells[0].id.split("-")[0];
      const copyId = this.selectionCells[0].id
      const toolItem =
        this.externalEnergy.find((item) => item.id === id) ||
        this.loadType.find((item) => item.id === id) ||
        this.electricItems.find((item) => item.id === id) ||
        this.energyStorage.find((item) => item.id === id) ||
        this.distributionTransmission.find((item) => item.id === id) ||

        this.others.find((item) => item.id === id)

      console.log(toolItem, '粘贴在此处');
      const sourceId = toolItem["id"] + "-" + toolItem["idSeed"]
      this.dataObj[sourceId] = JSON.parse(JSON.stringify(this.dataObj[copyId]))
      this.dataObj[sourceId].addType = 1;
      this.dataObj[sourceId].copyId = copyId;
      this.addCustomCell(null, toolItem, x, y);
    },
    //剪切
    cut() {
      this.selectionCells = this.graph.getSelectionCells();
      mxClipboard.cut(this.graph, this.selectionCells);
    },
    // 前进
    goForward() {
      this.undoMng.redo();
    },

    // 撤退
    goBack() {
      this.undoMng.undo();
    },

    // 放大
    zoomIn() {
      this.graph.zoomIn();
    },

    // 缩小
    zoomOut() {
      this.graph.zoomOut();
    },

    //  将元素置于最底层
    toBack(cell) {
      this.graph.orderCells(false, [cell]); // 将元素置于最底层
    },

    // 将元素置于最顶层
    toFront(cell) {
      this.graph.orderCells(true, [cell]); // 将元素置于最顶层
    },

    // 等比例缩放
    autoSize() {
      // 方法一
      // this.editor.execute('actualSize');
      //方法二：
      this.graph.zoomActual();
      this.graph.fit(); //自适应
      this.graph.center(); //将画布放到容器中间
    },

    // 生成图片
    showImage() {
      this.editor.execute("show"); //直接页面跳转,并以svg流程图
      // 下载svg流程图
      console.log("this.gtaph", this.graph);
      const svg = this.exportModelSvg();
      const blob = new Blob([svg], {
        type: "image/svg+xml"
      });
      const url = URL.createObjectURL(blob);
      let link = document.createElement("a");
      link.href = url;
      link.download = "model.svg";
      link.click();
    },

    // 导出svg
    exportModelSvg() {
      let scale = this.graph.view.scale;
      let bounds = this.graph.getGraphBounds();
      let border = 10;

      // Prepares SVG document that holds the output
      let svgDoc = mxUtils.createXmlDocument();
      let root =
        svgDoc.createElementNS != null ?
          svgDoc.createElementNS(mxConstants.NS_SVG, "svg") :
          svgDoc.createElement("svg");

      if (root.style != null) {
        root.style.backgroundColor = "#FFFFFF";
      } else {
        root.setAttribute("style", "background-color:#FFFFFF");
      }

      if (svgDoc.createElementNS == null) {
        root.setAttribute("xmlns", mxConstants.NS_SVG);
      }
      let width = Math.ceil((bounds.width * scale) / scale + 2 * border);
      let height = Math.ceil((bounds.height * scale) / scale + 2 * border);
      root.setAttribute("class", "svg-container");
      root.setAttribute("width", width + "px");
      root.setAttribute("height", height + "px");
      root.setAttribute("viewBox", "0 0 " + width + " " + height);
      root.setAttribute("xmlns:xlink", mxConstants.NS_XLINK);
      root.setAttribute("version", "1.1");

      // Adds group for anti-aliasing via transform
      let group =
        svgDoc.createElementNS != null ?
          svgDoc.createElementNS(mxConstants.NS_SVG, "g") :
          svgDoc.createElement("g");
      group.setAttribute("transform", "translate(0.5,0.5)");
      root.appendChild(group);
      svgDoc.appendChild(root);

      // Renders graph. Offset will be multiplied with state's scale when painting state.
      let svgCanvas = new mxSvgCanvas2D(group);
      svgCanvas.translate(
        Math.floor(border / scale - bounds.x),
        Math.floor(border / scale - bounds.y)
      );
      svgCanvas.scale(scale);

      let imgExport = new mxImageExport();
      imgExport.drawState(
        this.graph.getView().getState(this.graph.model.root),
        svgCanvas
      );

      //let xml = encodeURIComponent(mxUtils.getXml(root)); //no need
      let xml = mxUtils.getXml(root);
      return xml;
    },
    // 组合
    enGroup() {
      this.editor.graph.setSelectionCell(this.editor.groupCells());
      this.$message.success("组合成功");
      // this.editor.groupCells(null, 0, this.graph.getSelectionCells());
    },

    // 开始导入xml文件
    inPutXml() {
      this.isOutputXml = false;
      this.uploadDataVisible = true;
      this.graphXml = "";
    },

    // 导入xml文件后更新视图
    uploadPaintFlow(newvalue) {
      this.graph.selectAll();
      this.graph.removeCells(this.graph.getSelectionCells());
      setTimeout(() => {
        this.decode(newvalue, this.graph);
        this.$message.success("渲染成功");
      }, 1000);
    },

    createXmlDom(str) {
      if (document.all) {
        //判断浏览器是否是IE
        var xmlDom = new ActiveXObject("Microsoft.XMLDOM");
        xmlDom.loadXML(str);
        return xmlDom;
      } else {
        return new DOMParser().parseFromString(str, "text/xml");
      }
    },

    // 渲染xml流程图
    decode(graphXml, graph) {
      this.graph.getModel().beginUpdate();
      try {
        // 渲染流程图 方法一:
        const xmlDocument = mxUtils.parseXml(graphXml);
        const decoder = new mxCodec(xmlDocument);
        console.log(decoder);
        console.log(xmlDocument.documentElement);
        decoder.decode(xmlDocument.documentElement, graph.getModel());
        // 渲染流程图 方法二:
        // var xmlDoc = this.createXmlDom(graphXml);
        // var node = xmlDoc.documentElement;
        // console.log(node);
        // console.log(graph.getModel());
        // var dec = new mxCodec(node.ownerDocument);
        // dec.decode(node, graph.getModel());
      } finally {
        this.graph.getModel().endUpdate();
        // 渲染完成调整位置
        this.autoSize();
      }
    },

    // 导出xml文件
    outPutXml() {
      this.isOutputXml = true;
      this.uploadDataVisible = true;
      this.graphXml = this.encode(this.graph);
    },

    // 导出xml数据
    encode(graph) {
      const encoder = new mxCodec();
      const result = encoder.encode(graph.getModel());
      console.log(result);
      return mxUtils.getPrettyXml(result);
    },
    //添加箭头组函数
    addStencilPalette(title, name, file) {
      let req = mxUtils.load(file);
      let root = req.getDocumentElement();
      let shape = root.firstChild;
      this.$set(this.palettes, name, {
        title,
        name,
        shapes: []
      });
      while (shape != null) {
        if (shape.nodeType === mxConstants.NODETYPE_ELEMENT) {
          const shapeName = shape.getAttribute("name");
          const h = shape.getAttribute("h");
          // shape.querySelector('path').setAttribute('fill', 'transparent')
          const w = shape.getAttribute("w");
          mxStencilRegistry.addStencil(shapeName, new mxStencil(shape));
          this.palettes[name]["shapes"].push({
            name: shape.getAttribute("name"),
            width: w / 2,
            height: h / 2,
            fill: "transparent",
          });
        }
        shape = shape.nextSibling;
      }
    },

    // 初始化箭头节点组的工具栏
    initStencilToolBar() {
      var stencilDomArray = this.$refs.stencilDragItem;
      if (
        !(stencilDomArray instanceof Array) ||
        stencilDomArray.length <= 0 ||
        this.graph == null ||
        this.graph == undefined
      ) {
        return;
      }
      stencilDomArray.forEach((dom) => {
        const shapeIndex = dom.getAttribute("shapeIndex");
        const paletteIndex = dom.getAttribute("paletteIndex");
        const shapeItem = Object.values(this.palettes)[paletteIndex]["shapes"][
          shapeIndex
        ];
        const shapeWidth = shapeItem["width"];
        const shapeHeight = shapeItem["height"];
        const stencilDragHandler = (graph, evt, cell, x, y) => {
          this.instanceGraph(
            this.graph,
            shapeItem,
            x,
            y,
            shapeWidth,
            shapeHeight,
            cell
          );
        };
        var createDragPreview = () => {
          //设置鼠标拖拽箭头节点时的样式
          const elt = document.createElement("div");
          elt.style.border = "2px dotted black";
          elt.style.cursor = "pointer";
          elt.style.width = `${shapeWidth}px`;
          elt.style.height = `${shapeHeight}px`;
          elt.style.transform = "translate(-50%,-50%)";
          return elt;
        };
        dom.appendChild(this.createThumb(shapeItem, shapeWidth, shapeHeight));
        mxUtils.makeDraggable(
          dom,
          this.graph,
          stencilDragHandler,
          createDragPreview(),
          0,
          0,
          false,
          true
        );
      });
    },

    // 新增箭头节点
    // instanceGraph(graph, shapeItem, x, y, width, height, dropCell) {
    //   const drop = !R.isNil(dropCell);
    //   // drop && this.$message.info(`箭头节点入${dropCell.title}`);
    //   const realX = drop ? x - dropCell.geometry.x : x;
    //   const realY = drop ? y - dropCell.geometry.y : y;
    //   const parent = drop ? dropCell : graph.getDefaultParent();
    //   graph.getModel().beginUpdate();
    //   try {
    //     let cell = graph.insertVertex(
    //       parent,
    //       null,
    //       null,
    //       realX - width / 2,
    //       realY - height / 2,
    //       width,
    //       height,
    //       `shape=${shapeItem["name"]};whiteSpace=wrap;word-break=break-all;`
    //     );
    //     cell["isGroup"] = false;
    //     cell.customer = true;
    //   } finally {
    //     graph.getModel().endUpdate();
    //   }
    // },

    // 拖拽结束时新增的箭头节点
    // createThumb(item, width, height) {
    //   const tmpGraph = new mxGraph(document.createElement("div"));
    //   const thumbBorder = 2;
    //   tmpGraph.labelsVisible = false;
    //   tmpGraph.view.scaleAndTranslate(1, 0, 0);
    //   this.instanceGraph(tmpGraph, item, 0, 0, width, height);
    //   const bounds = tmpGraph.getGraphBounds();
    //   const s =
    //     Math.floor(
    //       Math.min(
    //         (width - 2 * thumbBorder) / bounds.width,
    //         (height - 2 * thumbBorder) / bounds.height
    //       ) * 100
    //     ) / 100;

    //   tmpGraph.view.scaleAndTranslate(
    //     s,
    //     Math.floor((width - bounds.width * s) / 2 / s - bounds.x),
    //     Math.floor((height - bounds.height * s) / 2 / s - bounds.y)
    //   );

    //   const node = tmpGraph.view.getCanvas().ownerSVGElement.cloneNode(true);

    //   node.style.position = "relative";
    //   node.style.overflow = "hidden";
    //   node.style.cursor = "pointer";
    //   node.style.width = `${width}px`;
    //   node.style.height = `${height}px`;
    //   node.style.left = `${thumbBorder}px`;
    //   node.style.top = `${thumbBorder}px`;
    //   node.style.display = "inline-block";
    //   return node;
    // },

    // 添加序号图标
    addPoint(cell, number) {
      const normalTypeVertex = this.graph.insertVertex(
        cell,
        null,
        null,
        null,
        null,
        30,
        30,
        `port;normalType;orderPoint=true;fillColor=none;image=./images/order/unselect-${number}.png;spacingLeft=-45px;spacingBottom=-45px`
      );
      // 固定序号图标的位置.不随节点变大而改变位置
      // normalTypeVertex.geometry.offset = new mxPoint(45, 45);
      // 序号图标无法连接
      // normalTypeVertex.setConnectable(false);
      // normalTypeVertex.id = cell.id.split("-")[0] + `-unselect-${number}`;
      // normalTypeVertex.value = number;
      // normalTypeVertex.geometry.relative = true;
      // 将新增的图标鼠标悬浮换成手势的图案
      // const oldGetCursorForCell = mxGraph.prototype.getCursorForCell;
      // this.graph.getCursorForCell = function (...args) {
      //   const [cell] = args;
      //   if (cell.edge || cell.style == undefined) {
      //     return;
      //   }
      //   return cell.style.includes('normalType') ?
      //     'pointer' :
      //     oldGetCursorForCell.apply(this, args);
      // };
    },

    // 加载案例流程图
    // loadFlowCase(index) {
    //   // console.log(node);
    //   this.$confirm("请确认您当前流程图数据已保存至本地 ?", "提示", {
    //     confirmButtonText: "我已保存",
    //     cancelButtonText: "取消加载",
    //     type: "warning",
    //   })
    //     .then(() => {
    //       let loadData = "";
    //       switch (index) {
    //         case 1:
    //           loadData = xmlData1;
    //           break;
    //         case 2:
    //           loadData = xmlData2;
    //           // loadData = this.model
    //           break;
    //         case 3:
    //           loadData = xmlData3;
    //           break;
    //       }
    //       console.log("loadData", loadData);
    //       let newXml = mxUtils.load(loadData).request.response;
    //       this.graph.selectAll();
    //       this.graph.removeCells(this.graph.getSelectionCells());
    //       setTimeout(() => {
    //         this.decode(newXml, this.graph);

    //         this.$message.success("加载流程图案例成功");
    //       }, 1000);
    //     })
    //     .catch(() => {
    //       this.$message({
    //         type: "info",
    //         message: "已取消加载流程图案例",
    //       });
    //     });
    // },

    handleScroll(e) {
      if (e.wheelDelta > 0) {
        this.graph.zoomIn();
      } else {
        this.graph.zoomOut();
      }
    },
    // 引脚
    pinBlur(obj) {
      const {
        index,
        value
      } = obj;
      const positionData = [{
        x: 40,
        y: 0,
      },
      {
        x: 0,
        y: 40,
      },
      {
        x: 90,
        y: 40,
      },
      ];
      let data = this.dataObj[this.cellId].pinObject[index];
      if (data.id) {
        this.graph.getModel().remove(data);
        if (!value && data) return this.graph.getModel().remove(data);
        else if (!value && !data) return;
      }
      const normalTypeVertey = this.graph.insertVertex(
        this.cellObj,
        null,
        value,
        positionData[index].x,
        positionData[index].y,
        0,
        0,
        true,
        null
      );
      // normalTypeVertey.isBasicElement = true;
      this.dataObj[this.cellId].pinObject.splice(index, 1, normalTypeVertey);
    },
    // A 显示隐藏元件名称
    // showHiddenName() {
    //   if (this.isShow.isShowName) {
    //     this.elementData.forEach((item) => {
    //       const hasChildWithName = item.children?.some(
    //         (child) => child.isElementName
    //       );
    //       if (!hasChildWithName) {
    //         const obj = this.graph.insertVertex(
    //           item,
    //           null,
    //           item.id,
    //           0,
    //           item.height,
    //           item.width,
    //           0,
    //           // "align=left;verticalAlign=top;labelBackgroundColor=red;labelBorderColor=black",
    //           true
    //         );
    //         console.log(this.graph.insertVertex);
    //         obj.isElementName = true;
    //         obj.style = "pointer-events=none;"; //设置名字不可选中
    //       }
    //     });
    //   } else {
    //     this.elementData.forEach((item) => {
    //       item.children
    //         ?.filter((child) => child.isElementName)
    //         .forEach((child) => {
    //           this.graph.getModel().remove(child);
    //         });
    //     });
    //   }
    // },
    // A 隐藏或显示元件
    showElement(isShow, type) {
      this.elementData.forEach((item) => {
        if (item.type == type) {
          this.graph.toggleCells(isShow, [item], true);
        }
      });
    },
    // 查看元件表
    elementTableClick(e) {
      console.log(e);
    },
  },
  mounted() {
    // 检测浏览器兼容性
    if (!mxClient.isBrowserSupported()) {
      this.$message.error(
        "当前浏览器不支持拓扑图功能，请更换浏览器访问，建议使用Chrome浏览器访问!"
      );
    } else {
      // Overridden to define per-shape connection points
      mxGraph.prototype.getAllConnectionConstraints = function (terminal) {
        if (terminal != null && terminal.shape != null) {
          if (terminal.shape.stencil != null) {
            console.log("===============");
            if (terminal.shape.stencil.constraints != null) {
              return terminal.shape.stencil.constraints;
            }
          } else if (terminal.shape.constraints != null) {
            let ports = terminal.cell.ports;
            let cstrs = [];
            for (let key in ports) {
              let port = ports[key];
              let cstr = new mxConnectionConstraint(
                new mxPoint(port.x, port.y),
                port.perimeter
              );
              cstr.portId = port.portId;
              cstrs.push(cstr);
            }
            return cstrs;
          }
        }
        return null;
      };
      this.createGraph();
      this.eventCenter();
      this.configMouseEvent();
      this.configMenu();
      this.addStencilPalette(
        "箭头组",
        "arrows",
        path.join("./stencil/arrows.xml")
      );
      this.$nextTick(() => {
        this.initCustomToolbar(this.externalEnergy);
        this.initCustomToolbar(this.loadType);
        this.initCustomToolbar(this.electricItems);
        this.initCustomToolbar(this.energyStorage);
        this.initCustomToolbar(this.distributionTransmission);
        this.initCustomToolbar(this.others);
        // this.initGeneralTool();
        this.initStencilToolBar();
        this.makeToolbarDraggable();
        this.configKeyEvent();
        this.mxGetCellStyle();
        this.preview();
        this.ComputesLocation();
      });
    }

    document
      .getElementById("graphContainer")
      .addEventListener("mousewheel", this.handleScroll, true); // 监听（绑定）滚轮滚动事件
  },
  destroyed() {
    document
      .getElementById("graphContainer")
      .removeEventListener("mousewheel", this.handleScroll); //  离开页面清除（移除）滚轮滚动事件
    this.graph.destroy();
  },
};

</script>
<style lang="less">
@import "./general-shap.css";
// // 左侧节点
// ::v-deep .el-tabs__item {
//   width: 71px !important;
// }

.customToolbarContainer {
  width: 100%;
  height: 95vh;
  // height: 100%;
  display: flex;
  position: relative;
  // overflow: hidden;

  .show-map {
    position: absolute;
    bottom: 50px;
    right: 320px;
    border: 3px solid #ededed;
    box-shadow: 9px 9px 12px -4px #cdc7c7;
    width: 160px;
    height: 120px;
    background: rgba(255, 255, 255, 0.5);
  }

  .toolbarContainer {
    height: 100% !important;
    padding-top: 50px;
    font-size: 20px;
    background: #efefef;
    text-align: center;
    background-color: #fff;
    border-right: 1px solid #ededed;
    width: 14%;
    position: relative;
    box-sizing: border-box;
    overflow-y: scroll;

    .general-toolbar {
      .el-collapse-item__wrap .el-collapse-item__content {
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        justify-content: start;
        align-content: center;

        .common {
          width: 30%;
          cursor: pointer;
          // padding: 10px;
          height: 50px;
          white-space: wrap;
          text-align: center;
          position: relative;

          .generalTooltitle {
            position: absolute;
            bottom: -10px;
            left: 0;
            width: 100%;
            transform: translateX(-50%);
          }
        }
      }
    }

    .custom-toolbar {
      .custom-node {
        display: inline-block;
        margin: 10px 0 0 0;
        width: 32%;
        height: 60px;
        padding: 5px 0;

        img {
          height: 34px;
        }
      }

      .rectangle-node {
        width: 45%;
        height: 40px;
        margin: 10px 0 0 0;
        background-color: #ffff;
        position: relative;
        border: 1px solid #000000;
        padding: none;

        img {
          position: absolute;
          left: 0;
          height: 35px;
          top: 50%;
          // transform: translateY(-50%);
        }

        .node-title {
          position: absolute;
          left: 60%;
          top: 50%;
          transform: translate(-50%, -50%);
        }
      }

      .el-collapse-item__content {
        display: flex;
        flex-wrap: wrap;
        justify-content: start;
        align-content: space-around;

        span {
          word-break: keep-all;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          cursor: pointer;
          font-size: 12px;
        }
      }
    }
  }

  .toolbarContainer::-webkit-scrollbar {
    display: none;
  }

  .graphContainer {
    // margin-top: 50px;
    height: 100% !important;
    line-height: 100%;
    position: relative;
    overflow: hidden;
    background-color: #fff !important;
    flex: 1;
  }

  .graphContainer-background {
    background-image: url("../../assets/grid.gif");
  }

  .top-tools {
    position: absolute;
    display: flex;
    align-items: center;
    box-sizing: border-box;
    top: 0;
    left: 0;
    padding: 0 20px 0 20px;
    width: 100%;
    z-index: 1000;
    background-color: #fff;
    height: 50px;
    // border-bottom: 1px solid #ededed;
    box-shadow: 0px 2px 8px -4px #c4c7c1;

    .select-edgetype {
      width: 100px;
      margin-right: 10px;
    }
  }

  .mxRubberband {
    background-color: rgb(58, 58, 207);
    position: absolute;
  }

  .el-collapse-item__header {
    padding-left: 30px;
  }

  .right-bar {
    width: 300px;
    background-color: #fff;
    height: 100%;
    position: absolute;
    right: 0;
    top: 0;
    border-left: 1px solid #ededed;
    padding-top: 50px;
    box-sizing: border-box;

    .json-viewer {
      overflow: auto;
      position: absolute;
      top: 35%;
      width: 260px;
      height: 70%;
      bottom: 0;
      right: 0;
    }
  }

  .tools-group {
    display: flex;
    justify-content: center;

    button {
      margin-left: 17px;
      font-size: 16px;
    }
  }

  .aside-button-group {
    width: 100%;
    position: sticky;
    top: 0px;
    background: #ffffff;
    box-sizing: border-box;
    z-index: 1000;
    border: 1px solid #ededed;
    border-left: none;
  }
}

body div.mxPopupMenu {
  -webkit-box-shadow: 3px 3px 6px #c0c0c0;
  -moz-box-shadow: 3px 3px 6px #c0c0c0;
  box-shadow: 3px 3px 6px #c0c0c0;
  background: white;
  position: absolute;
  border: 3px solid #e7e7e7;
  padding: 3px;
}

body table.mxPopupMenu {
  border-collapse: collapse;
  margin: 0px;
}

body tr.mxPopupMenuItem {
  color: black;
  cursor: default;
}

body td.mxPopupMenuItem {
  padding: 6px 60px 6px 30px;
  font-family: Arial;
  font-size: 10pt;
}

body td.mxPopupMenuIcon {
  background-color: white;
  padding: 0px;
}

body tr.mxPopupMenuItemHover {
  background-color: #eeeeee;
  color: black;
}

table.mxPopupMenu hr {
  border-top: solid 1px #cccccc;
}

table.mxPopupMenu tr {
  font-size: 4pt;
}

.shapgroud {
  .el-collapse-item__content {
    display: flex;
    flex-wrap: wrap;
  }

  svg g path {
    fill: transparent;
  }

  .stencil-node {
    width: 20%;
  }

  svg g path {
    stroke: #515151;
    -webkit-text-fill-color: #515151;
  }
}

.flow {
  stroke-dasharray: 8;
  animation: dash 0.5s linear;
  animation-iteration-count: infinite;
}

@keyframes dash {
  to {
    stroke-dashoffset: -16;
  }
}

.group-item {
  cursor: pointer;
  height: 40px;
  margin: 5px 0;
  line-height: 40px;
  width: 80%;
  display: inline-block;
  border: 1px solid #eeee;
}

.custom-tree-node {
  width: 100%;
  padding: 10px 10px 10px 0;
  display: flex;
  justify-content: space-between;
}

.mxPlainTextEditor {
  position: relative;
}

.mxPlainTextEditor::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 20px;
  height: 20px;
  background-color: #fbc117;
}

#graphContainer {
  overflow-y: scroll;
}

.mxTooltip {
  display: none;
}

// 查看元件表
.checkElementTable {
  // overflow: hidden;

  .el-dialog {
    height: 600px;
  }

  .el-tree {
    height: 500px;
    border: 1px solid rgb(204, 204, 204);
    float: left;
    width: 25%;
    margin-right: 8px;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.12), 0 0 6px 0 rgba(0, 0, 0, 0.04);
  }

  .el-tabs {
    height: 500px;
    float: left;
    width: 73%;
  }
}

.customToolbarContainer .toolbarContainer .other .custom-node img {
  height: 12px;
}

.down {
  display: flex;
  justify-content: end;
  margin-bottom: 10px;
}
</style>
