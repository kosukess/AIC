PATH_DIR_SCRIPT="$(cd "$(dirname "${BASH_SOURCE:-$0}")" && pwd)"
sudo docker build --no-cache --pull --force-rm -t aic_project:ver.1.0 "$PATH_DIR_SCRIPT"