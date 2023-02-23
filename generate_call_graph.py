filepaths= ["cpExample.py","data_visualize_utils.py", "integratedEnergySystemPrototypes.py", "config.py"] 
import os
for filepath in filepaths:
    command = f"python D:\\ProgramFiles\\anaconda\\envs\\py37\\Scripts\\pyan {filepath} --uses --no-defines --colored --grouped --annotated --dot > myuses_{filepath.split('.')[0]}.dot"

