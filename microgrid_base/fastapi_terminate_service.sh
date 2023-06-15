ps aux | grep rabbitmq | grep -v grep | awk '{print $2}' | xargs -Iabc kill -s TERM abc
ps aux | grep redis | grep 6380 | grep -v grep | awk '{print $2}' | xargs -Iabc kill -s TERM abc
# shall you wait till terminated.
# you may use libtmux for better 'killing' experience.
# 
tmux kill-session -t fastapi_tmuxp
sleep 3