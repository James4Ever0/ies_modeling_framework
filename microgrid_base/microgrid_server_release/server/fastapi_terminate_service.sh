ps aux | grep rabbitmq | grep -v grep | awk '{print $2}' | xargs -Iabc kill -s TERM abc
ps aux | grep redis | grep 6380 | grep -v grep | awk '{print $2}' | xargs -Iabc kill -s TERM abc
# shall you wait till terminated.
# you may use libtmux for better 'killing' experience.
# session name -> pane pids -> send SIGTERM -> kill session by name
# check if it is really killed. if not, send SIGKILL
# tmux kill-session -t fastapi_tmuxp
tmux kill-server # no other panes running anyway.
sleep 3