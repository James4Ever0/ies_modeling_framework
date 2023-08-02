input_file = "test_code.html"
output_path = "test_code_highlight.html"

from bs4 import BeautifulSoup

soup = BeautifulSoup(open(input_file, "r").read())

# line_range = range(10, 20 + 1)
# import rich

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

for elem in elements_to_delete:
    elem.extract()

with open(output_path, "w+") as f:
    f.write(str(soup))
