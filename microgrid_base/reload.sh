# mkdir history_logs
cp -R microgrid_server_release/server/logs history_logs
rm -rf microgrid_server_release
7z x release.7z
cd microgrid_server_release
cd init
# pip3 install -r requirements_docker_launch.txt
# bash init.sh
bash init_docker_launch.sh
# cd ..
cd server
python3 docker_launch.py
# mkdir logs
cp -R /root/history_logs logs
rm -rf logs
bash fastapi_tmuxp.sh windows
