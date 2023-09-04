# write a custom loader instead.
# or use pyomo?
# import lxml
from bs4 import BeautifulSoup
sol_file = "feasopt.sol"

with open(sol_file, 'r') as f:
	file = f.read()

# 'xml' is the parser used. For html files, which BeautifulSoup is typically used for, it would be 'html.parser'.
soup = BeautifulSoup(file, 'xml')
