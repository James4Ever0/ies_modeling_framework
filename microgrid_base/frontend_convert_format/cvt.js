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

var nodes_list = []
var links_list = []

// const myRe = /.+models\/(.+)\.svg.+/g;

for(var e of obj.graph.mxGraphModel.root.mxCell) {
    let id=e._id
    if(e.vertex) {
        let node_id=id
        // devType = myRe.exec(e._style)[0];
        let val=e._style;
        let devType=val.split("models/")[1].split(".svg")[0]
        idLUT[`${node_id}`]=node_id_cursor++;
        devLUT[`${node_id}`]=devType;
        if(e.Array.Object.length===undefined) {
            e.Array.Object=[e.Array.Object]
        }
        for(let o of e.Array.Object) {
            anchor_id=o._portId
            anchor_title=o._title
            anchor_k=`${node_id}_${anchor_id}`
            anchorLUT[anchor_k]=anchor_title
            idLUT[anchor_k]=node_id_cursor++;
        }
    } else if(e.edge) {
        connLUT[id].source_id=e.source
        connLUT[id].target_id=e.target
        connLUT[id].connType=e.connType
        idLUT[`${id}`]=node_id_cursor++;
    }
}

for(var e of obj.connectionsAnchors) {
    let conn_id=e.id
    let conn=connLUT[conn_id]
    let source_anchor_id=e.sourceAnchors.port_id
    let target_anchor_id=e.targetAnchors.port_id
    let sourceAnchorType=anchorLUT[`${conn.source_id}_${source_anchor_id}`]
    let targetAnchorType=anchorLUT[`${conn.target_id}_${target_anchor_id}`]
}

for(var e of obj.rightParams) {
    let node_id=e.id
    // console.assert()
}

input_template.nodes = nodes_list
input_template.links = links_list

pretty_print(input_template, "input_template_processed.json")