cd ~

# install torch2trt
git clone https://github.com/NVIDIA-AI-IOT/torch2trt
cd torch2trt
python3 setup.py install --plugins

cd ~

# install trt_pose
git clone https://github.com/NVIDIA-AI-IOT/trt_pose
cd trt_pose
python3 setup.py install

cd ~

git clone https://github.com/NVIDIA-AI-IOT/jetcam.git
cd jetcam
python3 setup.py install