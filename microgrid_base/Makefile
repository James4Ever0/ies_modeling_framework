# https://www.gnu.org/software/make/manual/html_node/Parallel-Output.html
# gmake -Oline

.PHONY: test

################ VARIABLES ################
PLATFORM := $(shell )

OS_TYPE = windows
# OS_TYPE = macos

PYTHON_ENV = -X utf8=1

ifeq (${OS_TYPE}, macos)
CONDA_ENV = base
PYTHON = /usr/bin/python3
else
CONDA_ENV = cplex
PYTHON = python ${PYTHON_ENV}
endif

CONDA = conda run -n ${CONDA_ENV} --live-stream --no-capture-output
# CONDA = conda run -n rosetta --live-stream --no-capture-output

MICROGRID_TYPESYS_JSONS = microgrid_v2_all_types_structured.json microgrid_v2_connectivity_matrix.json microgrid_v2_device_port_type_mapping.json

TYPESYS_PLOTS = type_system.png device_connectivity_matrix.png

RELEASE_DIR = microgrid_server_release

SERVER_RELEASE_DIR = ${RELEASE_DIR}/server

RELEASE_INIT_DIR = ${RELEASE_DIR}/init

# RELEASE_TEST_DIR = ${RELEASE_DIR}/test

SERVER_CODE = fastapi_celery_server.py fastapi_datamodel_template.py fastapi_server_template.py

SERVER_SCRIPT = fastapi_terminate_service.sh fastapi_tmuxp.sh fastapi_tmuxp.yml

RELEASE_ARCHIVE = release.7z

MODEL_CODE = topo_check.py ies_optim.py export_format_validate.py

EXTRA_CODE_DEPS = unit_utils.py passwords.py solve_model.py expr_utils.py

EXTRA_DATA_DEPS = export_format.json frontend_sim_param_translation.json

UNIT_DEFINITIONS = ../merged_units.txt ../constants_en.txt

INIT_FILES = requirements.txt init.sh

TEST_INPUT_FORMAT_FILES = template_input.json test_json_input_format.py

TEST_CODE = test_topo_check.py ${TEST_INPUT_FORMAT_FILES}

LOG_DIRS = logs ${SERVER_RELEASE_DIR}/logs

ifeq (${OS_TYPE}, macos)
MAIN_EXEC=${CONDA} bash cplex_test.sh
else
MAIN_EXEC=${PYTHON} test_topo_check.py -f
endif

################ META TARGETS ################

main: code test_code ${LOG_DIRS}
	${MAIN_EXEC}

${LOG_DIRS}:
	mkdir -p $@
	touch $@/.log

serve: release
	cd ${SERVER_RELEASE_DIR}
	bash fastapi_tmuxp.sh ${OS_TYPE}

test: release
	${MAKE} -C test

# packup all necessary files for the test.
release: code server ${LOG_DIRS}
	rm -rf ${RELEASE_DIR}
	rm -rf ${RELEASE_ARCHIVE}
	mkdir -p ${SERVER_RELEASE_DIR}
	mkdir -p ${RELEASE_INIT_DIR}
	cp ${INIT_FILES} ${RELEASE_INIT_DIR}
	cp ${UNIT_DEFINITIONS} ${RELEASE_DIR}
	cp ${MODEL_CODE} ${EXTRA_CODE_DEPS} ${EXTRA_DATA_DEPS} ${SERVER_CODE} ${SERVER_SCRIPT} ${TEST_CODE} ${SERVER_RELEASE_DIR}
	7z a ${RELEASE_ARCHIVE} ${RELEASE_DIR}

code: ${MODEL_CODE} ${TEST_CODE} ${EXTRA_CODE_DEPS} ${EXTRA_DATA_DEPS}

server: server_code server_script

server_code: ${SERVER_CODE}

server_script: ${SERVER_SCRIPT}

test_code: ${TEST_CODE}

docs: constraints.log

server_docs: openapi.json

templates: output_template.json template_input.json

################ IMPLEMENTATION ################

param_base.py: frontend_sim_param_translation.json microgrid_jinja_param_base.json ${MICROGRID_TYPESYS_JSONS} lib_parse_params.py

topo_check.py ies_optim.py: topo_check.py.j2 ies_optim.py.j2 jinja_template_model_generator.py jinja_utils.py param_base.py unit_utils.py ${UNIT_DEFINITIONS}
	${PYTHON} jinja_template_model_generator.py

export_format_validate.py export_format.json sim_param_export.xlsx: export_format_validate.py.j2 parse_export_format.py jinja_utils.py 设备信息库各参数.xlsx param_base.py unit_utils.py ${UNIT_DEFINITIONS}
	${PYTHON} parse_export_format.py

microgrid_jinja_param_base.json: device_params_intermediate.json microgrid_device_port_type_mapping.json parse_units_and_names.py unit_utils.py ${UNIT_DEFINITIONS}
	${PYTHON} parse_units_and_names.py

${MICROGRID_TYPESYS_JSONS} ${TYPESYS_PLOTS}: type_system_v2.py utils.py
	${PYTHON} type_system_v2.py -p

frontend_sim_param_translation.json: frontend_sim_param_translation.js parse_frontend_sim_param_translation.py
	${PYTHON} parse_frontend_sim_param_translation.py

device_params_intermediate.json microgrid_device_params_intermediate.json: parse_params.py 设备接口-微电网参数.csv 设备信息库各参数.xlsx
	${PYTHON} parse_params.py

constraints.log: parse_optim_constraints.py ies_optim.py
	${PYTHON} parse_optim_constraints.py > constraints.log