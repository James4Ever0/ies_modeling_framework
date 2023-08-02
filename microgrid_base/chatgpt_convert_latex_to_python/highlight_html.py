input_file = "test_code.html"
output_path = "test_code_highlight.html"

from bs4 import BeautifulSoup

soup = BeautifulSoup(open(input_file, "r").read())

# line_range = range(10, 20 + 1)
# import rich

# insert into head
css = """
.highlight_line{
  background-color: green !important;
}

"""
js = """
const span = 10

setInterval(function() {
    if(document.readyState=='complete'){
        var url_hash = window.location.hash
          var line_number = Number(url_hash.split("-")[1])
          if (!Number.isNaN(line_number)){
            for (var i=line_number-span; i<=line_number+span; i++){
            var div_id = 'div-line-'+i
            var div = document.getElementById(div_id)
            if 
            (div !== null){
            div.setAttribute("class","highlight_line");
            }
    }
  }
  }
}, 500);

"""

css_tag = soup.new_tag('style', type="text/css")
css_tag.append(css)

js_tag = soup.new_tag('script')
js_tag.append(js)

head = soup.find('head')
head.append(js_tag)
head.append(css_tag)

elements_to_wrap = {}
for a in soup.find_all("a"):
    # print(a)
    a_id = a.attrs["id"]
    id_no = int(a_id.split("-")[-1])
    elements_to_wrap[id_no] = []
    # if id_no not in line_range:
    print("changing line:", id_no)
    elements_to_wrap[id_no].append(a)
    for elem in a.next_siblings:
        # print(elem, elem.name)
        if elem.name == "a":
            # if elem.name !='span':
            break
        else:
            elements_to_wrap[id_no].append(elem)
    # span = a.next_sibling()
    # print(span)
    # print(dir(a))
    # find next sibling of "span".
pre = soup.find('pre')

for key, elems in elements_to_wrap.items():
    div = soup.new_tag('div',id=f'div-line-{key}')
    for elem in elems:
        # print(elem)
        elem.extract()
        div.append(elem)
    pre.append(div)
        #
        # # Find the tag you wish to append to.
        # original_tag = content.find("body")
        #
        # # Create & append new tags.
        # new_tag = content.new_tag("button",
        #
        #
        # class ="accordion")
        # original_tag.append(new_tag)
        #
        # new_tag = content.new_tag("div", class ="panel")
        # original_tag.append(new_tag)
        #
        # new_tag = content.new_tag("p")
        # original_tag.append(new_tag)

with open(output_path, "w+") as f:
    f.write(str(soup))
