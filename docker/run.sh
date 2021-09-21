PATH_DIR_PARENT="$(dirname "$(cd "$(dirname "${BASH_SOURCE:-$0}")" && pwd)")"
sudo docker run -it --runtime nvidia --gpus all --network host --device /dev/video0:/dev/video0:mwr \
    -v /tmp/.X11-unix/:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
    -v /tmp/argus_socket:/tmp/argus_socket \
    -v "$PATH_DIR_PARENT":/home --name aic_project_run aic_project:ver.1.0