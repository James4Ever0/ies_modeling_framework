mkdir history_logs
mv microgrid_server_release/server/logs history_logs/
rm -rf microgrid_server_release
7z x release.7z
cd microgrid_server_release
cd init
bash init.sh
cd ..
cd server
mkdir logs
bash fastapi_tmuxp.sh windows