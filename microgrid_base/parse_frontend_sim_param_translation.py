filepath = "frontend_sim_param_translation.js"

import parse

with open(filepath,'r') as f:
    data = f.read()
    lines = data.split("\n")
    print(lines)

for line in lines:
    line = line.strip()
    parse.parse("{englishName}:{space_1}'{sampleData}',{space_2}//{chineseName}",line)