ps aux | grep rabbitmq | grep -v grep | awk '{print $2}' | xargs -Iabc kill -s TERM abc
ps aux | grep redis | grep 6380 | grep -v grep | awk '{print $2}' | xargs -Iabc kill -s TERM abc
tmux kill-session -t fastapi_tmuxp
sleep 3
if [ "$1" -eq "macos" ] ; then
echo macos
elif [ "$1" -eq "windows" ] ; then 
echo windows
else 
echo unknown
exit 1
fi
# env CPLEX_DIR=":/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx/" CONDA_ENV_NAME="rosetta" tmuxp load fastapi_tmuxp.yml
# env CPLEX_DIR="" CONDA_ENV_NAME="cplex" tmuxp load fastapi_tmuxp.yml
