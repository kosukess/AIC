# this dockerfile install below libraries
# TensorFlow 1.15
# PyTorch v1.7.0
# torchvision v0.8.0
# torchaudio v0.7.0
# onnx 1.8.0
# CuPy 8.0.0
# numpy 1.19.4
# numba 0.52.0
# OpenCV 4.1.1
# pandas 1.1.5
# scipy 1.5.4
# scikit-learn 0.23.2
# JupyterLab 2.2.9
ARG BASE_IMAGE=nvcr.io/nvidia/l4t-ml:r32.5.0-py3
FROM ${BASE_IMAGE}

RUN apt-get install python3-matplotlib
RUN python3 -m pip install tqdm cython pycocotools traitlets

WORKDIR /root