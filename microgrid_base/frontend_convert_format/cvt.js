var path="sample.json"

function pretty_print(obj,output_path) {
    let data=JSON.stringify(obj,null,4)
    console.log(data)
    fs.writeFileSync(output_path,data)
    console.log("write to:",output_path)
}

const fs=require('fs')

var content=fs.readFileSync(path)

var obj=JSON.parse(content)

obj.graph=JSON.parse(obj.graph)
// console.log(obj)
// console.dir(obj)
pretty_print(obj,'sample_parse.json')

const port_type_mapping={
    "外部能源": {
        "柴油": {
            "燃料接口": "柴油输出"
        }
    },
    "负荷类型": {
        "电负荷": {
            "电接口": "负荷电输入"
        }
    },
    "发电设备": {
        "光伏发电": {
            "电接口": "供电端输出"
        },
        "风力发电": {
            "电接口": "供电端输出"
        },
        "柴油发电": {
            "燃料接口": "柴油输入",
            "电接口": "供电端输出"
        }
    },
    "储能设备": {
        "锂电池": {
            "电接口": "电储能端输入输出"
        }
    },
    "配电传输": {
        "变压器": {
            "电输入": "电母线输入",
            "电输出": "变压器输出"
        },
        "变流器": {
            "电输入": "变流器输入",
            "电输出": "电母线输出"
        },
        "双向变流器": {
            "储能端": "双向变流器储能端输入输出",
            "线路端": "双向变流器线路端输入输出"
        },
        "传输线": {
            "电输入": "电母线输入",
            "电输出": "电母线输出"
        }
    }
}

var translate_port_type_and_dev_name_to_port_name={}

for(var i in port_type_mapping) {
    for(var j in port_type_mapping[i]) {
        for(var k in port_type_mapping[i][j]) {
            console.log(i,j,k)
            port_type=port_type_mapping[i][j][k]
            port_name=k
            translate_port_type_and_dev_name_to_port_name[`${j}_${port_type}`]=port_name
        }
    }
}

var graph_data={
    "典型日ID": null,
    "计算步长": "小时",
    "典型日": false,
    "典型日权重": 0,
    "计算类型": "设计规划",
    "风速": [],"光照": [],"气温": [],"年利率": 0.1
}

var input_template={
    "directed": false,
    "multigraph": false,
    "graph": graph_data,"nodes": [],"links": []
}

var anchorLUT={}
var connLUT={}
var node_id_cursor=0
var idLUT={}
var devLUT={}

var nodes_list=[]
var links_list=[]

// const myRe = /.+models\/(.+)\.svg.+/g;

for(var e of obj.graph.mxGraphModel.root.mxCell) {
    let id=e._id
    if(e.vertex) {
        let node_id=id
        // devType = myRe.exec(e._style)[0];
        let val=e._style;
        let devType=val.split("models/")[1].split(".svg")[0]

        dev_id_digit=node_id_cursor
        devLUT[`${node_id}`].id=node_id_cursor
        idLUT[`${node_id}`]=node_id_cursor++;
        if(devType!="母线") {
            devLUT[`${node_id}`].type='设备'
            devLUT[`${node_id}`].subtype=devType;
            if(e.Array.Object.length===undefined) {
                e.Array.Object=[e.Array.Object]
            }
            for(let o of e.Array.Object) {
                anchor_id=o._portId
                anchor_title=o._title
                anchor_k=`${node_id}_${anchor_id}`
                anchorLUT[anchor_k]=node_id_cursor
                // anchorLUT[anchor_k]=anchor_title
                port_type=anchor_title
                port_name=translate_port_type_and_dev_name_to_port_name[`${devType}_${port_type}`]
                nodes_list.append(
                    {
                        "type": "锚点",
                        "port_name": port_name,
                        "subtype": anchor_title,
                        "device_id": dev_id_digit,
                        "id": node_id_cursor
                    })
                links_list.append({source: dev_id_digit,target: node_id_cursor})
                idLUT[anchor_k]=node_id_cursor++;
            }
        } else {
            //母线

            devLUT[`${node_id}`].type='母线'
            devLUT[`${node_id}`].subtype=e._refname;

            conn=e._conn; // list of connected types.

            nodes_list.append(
                {
                    "type": "母线",
                    "subtype": e._refname,
                    "id": dev_id_digit,
                    "conn": conn
                })
        }

    } else if(e.edge) {
        connLUT[id].source_id=e.source
        connLUT[id].target_id=e.target
        connLUT[id].connType=e.connType
        nodes_list.append({
            "type": e.connType.startsWith("不可连接")? "连接线":"合并线",
            "subtype": e.connType,
            "id": node_id_cursor
        })
        idLUT[`${id}`]=node_id_cursor++;

    }
}

console.log(connLUT)

for(var e of obj.connectionsAnchors) {
    let conn_id=e.id
    let conn=connLUT[conn_id]
    let source_anchor_id=e.sourceAnchors.port_id
    let target_anchor_id=e.targetAnchors.port_id
    let sourceAnchorDigitId=anchorLUT[`${conn.source_id}_${source_anchor_id}`]
    let targetAnchorDigitId=anchorLUT[`${conn.target_id}_${target_anchor_id}`]
    links_list.append({source: sourceAnchorDigitId,target: idLUT[conn_id]})
    links_list.append({source: targetAnchorDigitId,target: idLUT[conn_id]})
}

for(var e of obj.rightParams) {
    let node_id=e.id
    devLUT[`${node_id}`].params=e
    // console.assert()
}

input_template.nodes=nodes_list
input_template.links=links_list

pretty_print(input_template,"input_template_processed.json")