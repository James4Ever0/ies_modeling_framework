# mkdir history_logs
# mv microgrid_server_release/server/logs history_logs
# rm -rf microgrid_server_release
# 7z x release.7z
# cd microgrid_server_release
# cd init
# bash init.sh
# cd ..
# cd server
# # mkdir logs
# mv /root/history_logs logs
# env MOCK='1' bash fastapi_tmuxp.sh windows
# env MOCK='1' bash reload.sh
# switch to config.py
env MOCK_TEST='1' bash reload.sh