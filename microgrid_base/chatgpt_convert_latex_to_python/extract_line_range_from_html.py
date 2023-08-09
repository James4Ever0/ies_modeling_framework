input_file = "test_code.html"
output_path = "test_code_line_10_to_20.html"

from bs4 import BeautifulSoup

soup = BeautifulSoup(open(input_file, "r").read())

line_range = range(10, 20 + 1)
# import rich

elements_to_delete = []
for a in soup.find_all("a"):
    # print(a)
    a_id = a.attrs["id"]
    id_no = int(a_id.split("-")[-1])
    if id_no not in line_range:
        print("removing line:", id_no)
        elements_to_delete.append(a)
        for elem in a.next_siblings:
            # print(elem, elem.name)
            if elem.name == "a":
                # if elem.name !='span':
                break
            else:
                elements_to_delete.append(elem)
    # span = a.next_sibling()
    # print(span)
    # print(dir(a))
    # find next sibling of "span".

for elem in elements_to_delete:
    elem.extract()

with open(output_path, "w+") as f:
    f.write(str(soup))
