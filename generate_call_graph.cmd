@REM filepaths= ["cpExample.py","data_visualize_utils.py", "integratedEnergySystemPrototypes.py", "config.py"] 
@REM import os
@REM for filepath in filepaths:
@REM     command = f"pyan3 {filepath} --uses --no-defines --colored --grouped --annotated --dot > myuses_{filepath.split('.')[0]}.dot"
@REM     os.system(command)
pycallgraph graphviz -- cpExample.py
