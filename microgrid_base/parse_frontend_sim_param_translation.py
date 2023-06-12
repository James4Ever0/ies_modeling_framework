filepath = "frontend_sim_param_translation.js"

import re

with open(filepath,'r') as f:
    data = f.read()
    lines = data.split("\n")
    print(lines)