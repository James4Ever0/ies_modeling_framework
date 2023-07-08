main:
	pytest --capture=tee-sys --lfnf=all --lf test_model.py

test_model.py: test_model.py.j2 
	python3 generate_test_model.py

common_fixtures.py.tmp: common_fixtures.py.j2 dev_info_tmp_gen.py
	python3 dev_info_tmp_gen.py