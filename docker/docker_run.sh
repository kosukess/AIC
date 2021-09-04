PATH_DIR_PARENT="$(dirname "$(cd "$(dirname "${BASH_SOURCE:-$0}")" && pwd)")"
sudo docker run -it --runtime nvidia -p 8000:8000 -v "$PATH_DIR_PARENT":/home --name aic_project_run aic_project:develop