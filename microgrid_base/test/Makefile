main:
	pytest --capture=tee-sys --lfnf=all --lf test_model.py

test_model.py: test_model.py.j2 
	python3 generate_test_model.py

