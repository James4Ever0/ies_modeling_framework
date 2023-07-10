OS_TYPE = windows

ifeq (${OS_TYPE}, macos)
CONDA_ENV = base
else
CONDA_ENV = cplex
endif

CONDA = conda run -n ${CONDA_ENV} --live-stream --no-capture-output

main: run_test.sh test_model.py common_fixtures.py stepwise
	ifeq (${OS_TYPE}, macos)
	bash $<
	else
	${CONDA} pytest --lf --lfnf=all --capture=tee-sys test_model.py
	endif

test_model.py: generate_test_model.py test_model.py.j2 
	python3 $<

common_fixtures.py.tmp: dev_info_tmp_gen.py common_fixtures.py.j2 
	python3 $<

stepwise: runtime_override_stepwise.py
	/usr/bin/python3 $< -t
	${CONDA} python $< -t
