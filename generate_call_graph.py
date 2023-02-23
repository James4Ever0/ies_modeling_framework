filepaths= ["cpExample.py","data_visualize_utils.py", "integratedEnergySystemPrototypes.py", "config.py"] 
import os
for filepath in filepaths:
    command = f"pyan3 {filepath} --uses --no-defines --colored --grouped --annotated --dot > myuses_{filepath.split('.')[0]}.dot"
    os.system(command)
