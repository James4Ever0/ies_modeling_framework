# source ~/.bashrc
apt install -y redis rabbitmq-server tmux tmuxp openjdk-8-jdk htop
conda run -n cplex --live-stream --no-capture-output pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
conda run -n cplex --live-stream --no-capture-output pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
conda run -n docplex --live-stream --no-capture-output pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements_docplex.txt
# cannot install cbc from conda on windows.
conda install -n cplex -c conda-forge coin-or-cbc scip ipopt
# you can still use executables outside conda environments, but you may need to pass some environment variables to differentiate.