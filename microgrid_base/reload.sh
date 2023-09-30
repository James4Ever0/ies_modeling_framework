APT_UPDATED=~/.apt_updated
# you can use makefile instead.
if test -f "$APT_UPDATED"; then
    echo "$APT_UPDATED exists."
else
    echo "$APT_UPDATED does not exist."
    apt update && touch $APT_UPDATED
fi
if [ "$(find $APT_UPDATED -mtime +7)" ]; then
    echo "Haven't update apt for at least 7 days"
    rm $APT_UPDATED && apt update && touch $APT_UPDATED
else
    echo "Apt is updated"
fi
if which docker; [ "$?" -ne 0 ]; then
    echo "7z not installed."
    echo "Setting up now."
    apt install -y p7zip-full
else
    echo "7z already installed."
fi

# cp -R microgrid_server_release/server/logs history_logs
rm -rf microgrid_server_release
7z x release.7z
cd microgrid_server_release
cd init
# pip3 install -r requirements_docker_launch.txt
# bash init.sh
bash init_docker_launch.sh
cd ..
cd server
# mkdir logs
# cp -R /root/history_logs logs
# rm -rf logs
# bash fastapi_tmuxp.sh windows
python3 docker_launch.py
