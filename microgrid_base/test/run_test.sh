# env PATH="/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx:$PATH" conda run -n rosetta --live-stream --no-capture-output python -m pytest --lf --lfnf=all --capture=tee-sys .
env PATH="/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx:$PATH" pytest --lf --lfnf=all --capture=tee-sys .
# pytest --lf --lfnf=all --capture=tee-sys .
# pytest --lf --lfnf=all --rootdir=../ .