sudo apt install -y redis rabbitmq-server tmux tmuxp
conda run -n cplex --live-stream --no-capture-output pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
conda run -n cplex --live-stream --no-capture-output pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt