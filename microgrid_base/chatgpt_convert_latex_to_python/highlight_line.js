
const span = 5
var previous_url_hash;

setInterval(function () {
    if (document.readyState == 'complete') {

        var url_hash = window.location.hash
        if (previous_url_hash == url_hash) {
            return
        }
        previous_url_hash = url_hash
        var line_number = Number(url_hash.split("-")[1])
        if (!Number.isNaN(line_number)) {
            var elemList = []
            for (let elem of document.getElementsByClassName('highlight_line')){
                elemList.push(elem)
            }
            for (let elem of elemList){
                elem.setAttribute("class","")
            }
            for (var i = line_number - span; i <= line_number + span; i++) {
                var div_id = 'div-line-' + i
                var div = document.getElementById(div_id)
                if
                    (div !== null) {
                    div.setAttribute("class", "highlight_line");
                }
            }
        }
    }
}, 500);
