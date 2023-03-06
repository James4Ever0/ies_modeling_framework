# IES modeling

## dependencies preparation

python==3.7

install `cplex` and `docplex` from IBM CPLEX Studio installation directory, run `python setup.py install` under the corresponding folders (total 2 folders)

install remaining dependencies via `pip install -r requirements.txt`

## current state

rudimentary IES modeling, or framework only IES modeling

## execute these commands for demo

```bash
python cpExample.py # a huge demo
python mini_ies_system.py # electricity only
python mini_heat_system.py # warm water heating
python mini_refrigeration_system.py # cold water cooling
```

## file contents

|filename | content|
|-- | -- |
|integratedEnergySystemPrototypes.py | prototypes of IES systems, define internal constraints, device IO and utils|
|system_topology_utils.py |visualize system topology|
|mini_data_log_utils.py| high level wrapper to check model validity, solve model, print parameters and save plots|
|jinan_changqing-hour.dat| first two columns for intensity of illumination, last two for wind speed|
|mini_ies_test.py| electricity only test |
|mini_heat_system.py | heating system test|
|mini_refrigeration_system.py | cooling system test|
|result_processlib.py| utils for extracting values from model solution|
|demo_utils.py|getting resource data and common devices from default parameters, for `cpExample.py`|
|data_visualize_utils.py|printing solution parameters, device count, and objectives, plotting and saving graphs|
|config.py| common model parameters|
|cpExample.py|a huge test|
