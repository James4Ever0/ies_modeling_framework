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

var graph_data={}

var input_template={
    "directed": false,
    "multigraph": false,
    "graph": graph_data,"nodes": [],"links": []
}

var anchorLUT={}
var connLUT={}
var node_id_cursor=0

for(var e of obj.graph.mxGraphModel.root.mxCell) {
    let id=e._id
    if(e.vertex) {
        let node_id=id
    } else if(e.edge) {
        connLUT[id].source_id=e.source
        connLUT[id].target_id=e.target
    }
}

for(var e of obj.connectionsAnchors) {
    let conn_id=e.id
    let source_anchor_id=e.sourceAnchors.port_id
    let target_anchor_id=e.targetAnchors.port_id
}

for(var e of obj.rightParams) {
    let node_id=e.id
}