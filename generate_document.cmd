@REM pdoc --http 0.0.0.0:8021 integratedEnergySystemPrototypes.py demo_utils.py cpExample.py
pdoc --html integratedEnergySystemPrototypes.py demo_utils.py cpExample.py config.py

7z a ies_planning.7z integratedEnergySystemPrototypes.py demo_utils.py cpExample.py config.py html