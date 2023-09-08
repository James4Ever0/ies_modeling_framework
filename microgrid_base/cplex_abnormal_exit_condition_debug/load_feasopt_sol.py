# write a custom loader instead.
# or use pyomo?
# import lxml
from bs4 import BeautifulSoup

sol_file = "feasopt.xml"
# sol_file = "feasopt.sol"

with open(sol_file, "r") as f:
    file = f.read()

# 'xml' is the parser used. For html files, which BeautifulSoup is typically used for, it would be 'html.parser'.
soup = BeautifulSoup(file, "xml")
# breakpoint()
data = {}
for var in soup.find_all("variable"):
    name = var["name"]
    value = float(var["value"])
    data[name] = value
    print(f"%s: %s" % (name, value))
import json

with open(output_path:="feasopt.json", "w+") as f:
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
print("write to: %s" % output_path)