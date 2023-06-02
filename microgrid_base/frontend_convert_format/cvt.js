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

var graph_data = {}

var input_template={
    "directed": false,
    "multigraph": false,
    "graph": graph_data,"nodes": [],"links": []
}