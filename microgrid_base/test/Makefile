OS_TYPE = windows

PYTHON_ENV = -X utf8=1

ifeq (${OS_TYPE}, macos)
CONDA_ENV = base
PYTHON = /usr/bin/python3
else
CONDA_ENV = cplex
PYTHON = python ${PYTHON_ENV}
endif

CONDA = conda run -n ${CONDA_ENV} --live-stream --no-capture-output


main: run_test.sh test_model.py common_fixtures.py stepwise
	ifeq (${OS_TYPE}, macos)
	bash $<
	else
	${CONDA} python ${PYTHON_ENV} -m pytest --lf --lfnf=all --capture=tee-sys test_model.py
	endif

test_model.py: generate_test_model.py test_model.py.j2 
	${PYTHON} $<

common_fixtures.py.tmp: dev_info_tmp_gen.py common_fixtures.py.j2 
	${PYTHON} $<

stepwise: runtime_override_stepwise.py
	${PYTHON} $< -t
	${CONDA} python ${PYTHON_ENV} $< -t
