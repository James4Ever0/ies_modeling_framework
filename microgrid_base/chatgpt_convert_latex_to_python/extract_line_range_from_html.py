input_file = "test_code.html"
from bs4 import BeautifulSoup

soup = BeautifulSoup(open(input_file, 'r').read())

import parse
line_range = range(10, 20+1)
# import rich

for a in soup.find_all('a'):
    print(a)
    a_id = a.attrs['id']
    id_no = int(a_id.split("-")[-1])
    if id_no not in line_range:
        print('removing line:', id_no)
        # for elem in a.
    # rich.print(a.__dict__)
    print(dir(a))
    # span = a.next_sibling()
    # print(span)
    # find next sibling of "span".