apt-get update -y
apt-get -y install python3-tk
apt-get upgrade -y
python3 -m pip install setuptools tqdm cython pycocotools traitlets

pip3 uninstall scikit-learn -y
python3 -m pip install scikit-learn==0.23.2

mkdir /script
cd /script

# jupyter lab library
jupyter nbextension enable --py widgetsnbextension
wget https://nodejs.org/dist/v12.13.0/node-v12.13.0-linux-arm64.tar.xz
tar -xJf node-v12.13.0-linux-arm64.tar.xz
cd node-v12.13.0-linux-arm64 && cp -R * /usr/local/
node -v
jupyter labextension install @jupyter-widgets/jupyterlab-manager

# install torch2trt
git clone https://github.com/NVIDIA-AI-IOT/torch2trt
cd torch2trt
python3 setup.py install --plugins

cd /script

# install trt_pose
git clone https://github.com/NVIDIA-AI-IOT/trt_pose
cd trt_pose
python3 setup.py install

cd /script

git clone https://github.com/NVIDIA-AI-IOT/jetcam.git
cd jetcam
python3 setup.py install
