# this dockerfile install below libraries
# TensorFlow 1.15.5
# PyTorch v1.9.0
# torchvision v0.10.0
# torchaudio v0.9.0
# onnx 1.8.0
# CuPy 9.2.0
# numpy 1.19.5
# numba 0.53.1
# OpenCV 4.5.0 (with CUDA)
# pandas 1.1.5
# scipy 1.5.4
# scikit-learn 0.23.2
# JupyterLab 2.2.9
ARG BASE_IMAGE=nvcr.io/nvidia/l4t-ml:r32.6.1-py3
FROM ${BASE_IMAGE}

RUN apt-get install python3-matplotlib
RUN python3 -m pip install tqdm cython pycocotools traitlets

WORKDIR /root