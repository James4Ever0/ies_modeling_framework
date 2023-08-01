input_file = "test_code.html"
from bs4 import BeautifulSoup

soup = BeautifulSoup(open(input_file, 'r').read())

import parse
line_range = range(10, 20+1)

for a in soup.find_all('a'):
    print(a)
    print(dir(a))
    span = a.next("span")
    print(span)
    # find next sibling of "span".