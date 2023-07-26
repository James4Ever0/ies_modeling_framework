from log_utils import logger_print

filepath = "frontend_sim_param_translation.js"

output_path = "frontend_sim_param_translation.json"

MAKEFILE = dict(inputs=[filepath], outputs=[output_path], args=[])

import parse

with open(filepath, "r") as f:
    data = f.read()
    lines = data.split("\n")
    # print(lines)

resultMap = {}
for line in lines:
    line = line.replace(":", ": ").replace(",", " , ").strip()
    while True:
        if " :" in line:
            line = line.replace(" :", ":")
        else:
            break
    result = parse.parse(
        "{englishName}:{space_1}'{sampleData}'{space_2},{space_3}//{chineseName}", line
    )
    if result:
        print(result)
        resultMap[result["chineseName"].upper()] = result["englishName"]

import json

print("writing to:", output_path)
with open(output_path, "w+") as f:
    f.write(json.dumps(resultMap, ensure_ascii=False, indent=4))
