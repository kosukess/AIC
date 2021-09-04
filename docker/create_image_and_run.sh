PATH_DIR_SCRIPT="$(cd "$(dirname "${BASH_SOURCE:-$0}")" && pwd)"
sudo docker build -t aic_project:ver.1.0 "$PATH_DIR_SCRIPT"

PATH_DIR_PARENT="$(dirname "$(cd "$(dirname "${BASH_SOURCE:-$0}")" && pwd)")"
sudo docker run -it --runtime nvidia -p 8000:8000 -v "$PATH_DIR_PARENT":/root --name aic_project_run aic_project:ver.1.0