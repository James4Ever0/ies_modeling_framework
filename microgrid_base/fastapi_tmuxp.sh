ps aux | grep rabbitmq | grep -v grep | awk '{print $2}' | xargs -Iabc kill -s KILL abc
ps aux | grep redis | grep 6380 | grep -v grep | awk '{print $2}' | xargs -Iabc kill -s KILL abc
tmux kill-session -t fastapi_tmuxp
tmuxp load fastapi_tmuxp.yml