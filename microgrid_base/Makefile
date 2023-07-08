TYPE_SYSTEM_FILES = microgrid_v2_all_types_structured.json microgrid_v2_connectivity_matrix.json microgrid_v2_device_port_type_mapping.json

type_system.png ${microgrid_v2_connectivity_matrix}: type_system_v2.py
	python3 $< -p

: microgrid_jinja_param_base.json