var path = "sample.json"

const fs = require('fs')

var content = fs.readFileSync(path)

var obj = JSON.parse(content)

obj.graph = JSON.parse(obj.graph)
// console.log(obj)
console.dir(obj)