TYPE_SYSTEM_FILES = microgrid_v2_all_types_structured.json microgrid_v2_connectivity_matrix.json microgrid_v2_device_port_type_mapping.json

type_system.png ${microgrid_v2_connectivity_matrix}: type_system_v2.py
	python3 $< -p

microgrid_jinja_param_base.json: parse_units_and_names.py device_params_intermediate.json
	python3 $<

device_params_intermediate:parse_device_parameters_excel.py device_parameters_v3.3.xlsx