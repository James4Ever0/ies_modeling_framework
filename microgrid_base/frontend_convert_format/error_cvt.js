const error_mapping={
    "不满足负荷": ['infeasible'],"拓扑错误": ["相邻","节点"]
}
const reserved_error_msg='其他错误'

function convertErrorMsg(error_msg) {
    var splited_lines=error_msg.split("\n")
    var error_last_line=splited_lines[splited_lines.length-1]
    for(var k in error_mapping) {
        var vlist=error_mapping[k]
        for(var v of vlist) {
            if(error_last_line.includes(v)) {
                return k
            }
        }
    }
    return reserved_error_msg
}