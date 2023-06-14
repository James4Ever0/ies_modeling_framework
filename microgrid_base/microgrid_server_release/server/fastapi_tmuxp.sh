ps aux | grep rabbitmq | grep -v grep | awk '{print $2}' | xargs -Iabc kill -s TERM abc
ps aux | grep redis | grep 6380 | grep -v grep | awk '{print $2}' | xargs -Iabc kill -s TERM abc
tmux kill-session -t fastapi_tmuxp
sleep 3
tmuxp load fastapi_tmuxp.yml
