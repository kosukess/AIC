cd ~

# install torch2trt
git clone https://github.com/NVIDIA-AI-IOT/torch2trt
cd torch2trt
sudo python3 setup.py install --plugins

cd ~

# install dependency libraries
sudo python3 -m pip install tqdm cython pycocotools
sudo apt-get install python3-matplotlib

# install trt_pose
git clone https://github.com/NVIDIA-AI-IOT/trt_pose
cd trt_pose
sudo python3 setup.py install

cd ~