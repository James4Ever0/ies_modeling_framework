var path = "sample.json"

function pretty_print(obj){
    console.log(JSON.stringify(obj,null, 4))
}

const fs = require('fs')

var content = fs.readFileSync(path)

var obj = JSON.parse(content)

obj.graph = JSON.parse(obj.graph)
// console.log(obj)
// console.dir(obj)
pretty_print(obj)