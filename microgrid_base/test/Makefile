main: run_test.sh test_model.py common_fixtures.py stepwise
	bash $<

test_model.py: generate_test_model.py test_model.py.j2 
	python3 $<

common_fixtures.py.tmp: dev_info_tmp_gen.py common_fixtures.py.j2 
	python3 $<

stepwise: runtime_override_stepwise.py
	/usr/bin/python3 $< -t
	conda run -n base --live-stream --no-capture-output python $< -t
