# https://www.gnu.org/software/make/manual/html_node/Parallel-Output.html
# gmake -Oline

.PHONY: test

################ ENVIRONMENT VARIABLES ################

PLATFORM := $(shell python -c "import os; print(os.name)")
ifeq (${PLATFORM}, )
PLATFORM := $(shell python3 -c "import os; print(os.name)") # executed on macos
endif

ifeq (${PLATFORM}, nt)
OS_TYPE = windows
else
OS_TYPE = macos
endif

PYTHON_ENV = -X utf8=1

ifeq (${OS_TYPE}, macos)
CONDA_ENV = rosetta
PYTHON = /usr/bin/python3
GSUDO = 
else
CONDA_ENV = cplex
PYTHON = python ${PYTHON_ENV}
GSUDO = gsudo
endif

CONDA = conda run -n ${CONDA_ENV} --live-stream --no-capture-output

run_in_conda_env := conda run -n $(1) --live-stream --no-capture-output


# CONDA = conda run -n rosetta --live-stream --no-capture-output

export OS_TYPE PLATFORM PYTHON PYTHON_ENV CONDA_ENV

################ VARIABLES ################


MICROGRID_TYPESYS_JSONS = microgrid_v2_all_types_structured.json microgrid_v2_connectivity_matrix.json microgrid_v2_device_port_type_mapping.json

TYPESYS_PLOTS = type_system.png device_connectivity_matrix.png

RELEASE_DIR = microgrid_server_release

SERVER_RELEASE_DIR = ${RELEASE_DIR}/server

RELEASE_INIT_DIR = ${RELEASE_DIR}/init

# RELEASE_TEST_DIR = ${RELEASE_DIR}/test

SERVER_CODE = fastapi_celery_server.py fastapi_datamodel_template.py fastapi_server_template.py fastapi_celery_functions.py

SERVER_SCRIPT = fastapi_terminate_service.sh fastapi_tmuxp.sh fastapi_tmuxp.yml

RELEASE_ARCHIVE = release.7z

EXPORT_FORMAT_CODE = export_format_validate.py export_format_units.py

MODEL_CODE = topo_check.py ies_optim.py ${EXPORT_FORMAT_CODE}

# use $(wildcard <pattern>) to precompute the pattern.

FILTERED_UTILS = $(wildcard csv* pyright* jinja* json*)

# UTILS = $(filter-out ${FILTERED_UTILS}, *_utils.py)
UTILS = $(filter-out ${FILTERED_UTILS}, $(wildcard *_utils.py))

EXTRA_CODE_DEPS = passwords.py solve_model.py constants.py pyomo_patch.py ${UTILS}
# EXTRA_CODE_DEPS = unit_utils.py passwords.py solve_model.py expr_utils.py constants.py log_utils.py pyomo_patch.py debug_utils.py conflict_utils.py json_utils.py error_utils.py

EXPORT_FORMAT_SCHEMA = export_format.json planning_export_format.json

EXTRA_DATA_DEPS = frontend_sim_param_translation.json test_output_full_mock_reduced.json ${EXPORT_FORMAT_SCHEMA}

UNIT_DEFINITIONS = ../merged_units.txt ../constants_en.txt

PYTHON_REQUIREMENTS = requirements.txt requirements_docplex.txt

INIT_FILES = ${PYTHON_REQUIREMENTS} init.sh conda_init.sh

TEST_INPUT_FORMAT_FILES = template_input.json test_json_input_format.py

TEST_CODE = test_topo_check.py ${TEST_INPUT_FORMAT_FILES}

LOG_DIRS = logs ${SERVER_RELEASE_DIR}/logs

PARAM_BASE_REQUIREMENTS = frontend_sim_param_translation.json microgrid_jinja_param_base.json ${MICROGRID_TYPESYS_JSONS} lib_parse_params.py

ifeq (${OS_TYPE}, macos)
MAIN_EXEC=bash cplex_test.sh
# MAIN_EXEC=${CONDA} bash cplex_test.sh
else
MAIN_EXEC=env BETTER_EXCEPTIONS=1 ${PYTHON} test_topo_check.py -f
endif

################ META TARGETS ################

main: release
	${MAIN_EXEC}

requirements: ${PYTHON_REQUIREMENTS}
	${GSUDO} ${PYTHON} -m pip install -r requirements.txt
	${GSUDO} $(call run_in_conda_env, docplex) -m pip install -r requirements_docplex.txt

${LOG_DIRS}:
	mkdir -p $@
	touch $@/.log

serve: release
	cd ${SERVER_RELEASE_DIR}
	bash fastapi_tmuxp.sh ${OS_TYPE}

# ref: https://www.gnu.org/software/make/manual/html_node/Variables_002fRecursion.html

code_check: code_checker.py
	${PYTHON} code_checker.py -- ${MAKE} ${MAKECMDGOALS}

test: release
	${MAKE} -e -C test

dsl:
	${MAKE} -e -C dsl_parser

# packup all necessary files for the test.

release: code test_code ${LOG_DIRS} server code_check release_prepare requirements

release_prepare:
	rm -rf ${RELEASE_DIR}
	rm -rf ${RELEASE_ARCHIVE}
	mkdir -p ${SERVER_RELEASE_DIR}
	mkdir -p ${RELEASE_INIT_DIR}
	cp ${INIT_FILES} ${RELEASE_INIT_DIR}
	cp ${UNIT_DEFINITIONS} ${RELEASE_DIR}
	cp ${MODEL_CODE} ${EXTRA_CODE_DEPS} ${EXTRA_DATA_DEPS} ${SERVER_CODE} ${SERVER_SCRIPT} ${TEST_CODE} ${SERVER_RELEASE_DIR}
	7z a ${RELEASE_ARCHIVE} ${RELEASE_DIR}

code: ${EXTRA_CODE_DEPS} ${EXTRA_DATA_DEPS} ${MODEL_CODE} ${TEST_CODE}

server: server_code server_script

server_code: ${SERVER_CODE}

server_script: ${SERVER_SCRIPT}

test_code: ${TEST_CODE}

docs: constraints.log

server_docs: openapi.json

templates: output_template.json template_input.json

################ IMPLEMENTATION ################

topo_check.py ies_optim.py: topo_check.py.j2 ies_optim.py.j2 jinja_template_model_generator.py jinja_utils.py param_base.py unit_utils.py ${UNIT_DEFINITIONS} ${PARAM_BASE_REQUIREMENTS}
	${PYTHON} jinja_template_model_generator.py

# pyright_regex_check:
# 	${PYTHON} pyright_utils.py

${EXPORT_FORMAT_CODE} ${EXPORT_FORMAT_SCHEMA} sim_param_export.xlsx: export_format_validate.py.j2 export_format_units.py.j2 parse_export_format.py jinja_utils.py 设备信息库各参数.xlsx param_base.py unit_utils.py ${UNIT_DEFINITIONS}
	${PYTHON} parse_export_format.py

microgrid_jinja_param_base.json: device_params_intermediate.json microgrid_device_port_type_mapping.json parse_units_and_names.py unit_utils.py ${UNIT_DEFINITIONS}
	${PYTHON} parse_units_and_names.py

${MICROGRID_TYPESYS_JSONS} ${TYPESYS_PLOTS}: type_system_v2.py csv_utils.py
	${PYTHON} type_system_v2.py -p

frontend_sim_param_translation.json: frontend_sim_param_translation.js parse_frontend_sim_param_translation.py
	${PYTHON} parse_frontend_sim_param_translation.py

# device_params_intermediate.json microgrid_device_params_intermediate.json: parse_params.py 设备接口-微电网参数.csv 设备信息库各参数.xlsx
device_params_intermediate.json microgrid_device_params_intermediate.json: parse_params.py 设备接口-微电网参数.csv 设备信息库各参数_23_7_24.xlsx
	${PYTHON} parse_params.py

constraints.log: parse_optim_constraints.py ies_optim.py
	${PYTHON} parse_optim_constraints.py > constraints.log

passwords.py: passwords_template.py
	cp passwords_template.py passwords.py

test_output_full_mock.json: test_output_full.json
	cp test_output_full.json test_output_full_mock.json

test_output_full_mock_reduced.json: test_output_full_mock.json reduce_demo_data_size.py json_utils.py
	${PYTHON} reduce_demo_data_size.py

# great.
# test_make_args:
# 	# echo ${MAKEFLAGS}
# 	echo ${MAKECMDGOALS}

# test_utils_wildcard:
#	echo ${UTILS}
#	echo ${FILTERED_UTILS}