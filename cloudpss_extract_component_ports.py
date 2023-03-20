source = "cloudpss_component_ports.json"
import json
from bs4 import BeautifulSoup

keys = ['母线', '燃气内燃机', '负荷',]
values = ['', '<text str=\"电接口\" x=\"15.983333333333334\" y=\"28.52569986979166\" align=\"center\" valign=\"middle\" vertical=\"0\" rotation=\"0\" localized=\"0\" align-shape=\"0\" />', '<text str=\"热水接口\" x=\"24.6356416004801\" y=\"44.88333333333334\" align=\"center\" valign=\"middle\" vertical=\"0\" rotation=\"0\" localized=\"0\" align-shape=\"0\" />',]
my_dict = dict(zip(keys, values))
print(my_dict)
