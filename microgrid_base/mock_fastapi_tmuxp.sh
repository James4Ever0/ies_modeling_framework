if [ "$1" != "macos" ] ; then
    if [ "$1" != "windows" ] ; then 
        echo "supports: [ macos | windows ]"
        echo "unknown platform: $1"
        exit 1
    fi
fi

echo "running under: $1"

bash fastapi_terminate_service.sh

if [ "$1" == "macos" ] ; then
    env CPLEX_DIR=":/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx/" CONDA_ENV_NAME="rosetta" MOCK='1' tmuxp load fastapi_tmuxp.yml
elif [ "$1" == "windows" ] ; then 
    env CPLEX_DIR="" CONDA_ENV_NAME="cplex" MOCK='1' tmuxp load fastapi_tmuxp.yml
fi
