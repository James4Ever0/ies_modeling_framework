main: test_model.py common_fixtures.py
	pytest --capture=tee-sys --lfnf=all --lf $<

test_model.py: generate_test_model.py test_model.py.j2 
	python3 $<

common_fixtures.py.tmp: dev_info_tmp_gen.py common_fixtures.py.j2 
	python3 $<