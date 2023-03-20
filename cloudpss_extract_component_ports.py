source = "cloudpss_component_ports.json"
import json
from bs4 import BeautifulSoup

# keys = ['母线', '燃气内燃机', '负荷',]
# values = ['', '<text str=\"电接口\" x=\"15.983333333333334\" y=\"28.52569986979166\" align=\"center\" valign=\"middle\" vertical=\"0\" rotation=\"0\" localized=\"0\" align-shape=\"0\" />', '<text str=\"热水接口\" x=\"24.6356416004801\" y=\"44.88333333333334\" align=\"center\" valign=\"middle\" vertical=\"0\" rotation=\"0\" localized=\"0\" align-shape=\"0\" />',]

content = open(source, 'r', encoding='utf-8').read()
data = json.loads(content)
for element in data["cmp"]:
    value=element["typename"]
    print(value)
    print()
    shape = element['shape']
    xml_shape = BeautifulSoup(shape, features='xml')
    # breakpoint()
    # xml_shape.find_all("background")[0].find_all("text")[0]['str']
    for background in xml_shape.find_all("background"):
        for text in background.find_all("text"):
            string = text['str']
            print(string)
    print("_"*20)
# assert status == 0
# assert msg == ""

# totalPage is 4, we need to iterate.
# page start from 1
# cmp is the main data list.

# for key, value in data.items():
#     print("KEY?", key)
#     # print("VAL?", value)

# my_dict = dict(zip(keys, values))
# print(my_dict)
