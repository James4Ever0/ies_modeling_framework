if which docker; [ "$?" -ne 0 ]; then
    echo "Docker not installed."
    echo "Setting up now."
    bash install_docker.sh
else
    echo "Docker already installed."
fi

pip3 install -r requirements_docker_launch.sh
