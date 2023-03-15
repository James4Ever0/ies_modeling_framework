import re

source = "额定发电功率(kW)"
source_2 = "生产厂商"

pattern = r'(\w+)\((\w+)\)'
result = re.findall(pattern, source_2)
if len(result) > 0:
    a, b = result[0]
    print(f"a={a}\nb={b}")
else:
    print(f"a={source_2}")
#a = "额定发电功率"
#b = "kW"

