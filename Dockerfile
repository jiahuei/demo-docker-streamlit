FROM python:3.9

# RUN cat /usr/include/cudnn.h | grep CUDNN_MAJOR -A 2
# ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/extras/CUPTI/lib64


### Time Zone ###
ARG TZ=Asia/Kuala_Lumpur
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y tzdata
RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

## Install Linux packages
# libgl1 is for OpenCV : https://stackoverflow.com/a/68666500
RUN apt-get update && apt-get install -y \
    apt-utils \
    curl \
    git \
    git-lfs \
    libxext6 \
    libxrender1 \
    libgl1 \
    nano \
    protobuf-compiler \
    software-properties-common \
    ssh \
    sudo \
    unzip \
    wget \
    zip

RUN git lfs install


# # Install / Update Python ##
# RUN apt-get update && apt-get install -y \
#     python3-dev \
#     python3-pip
# RUN apt-get update && apt-get install -y \
#     python3-cryptography \
#     python3-lxml \
#     python3-openssl \
#     python3-pil \
#     python3-setuptools \
#     python3-socks \
#     python3-tk \
#     python3-venv
# RUN pip3 --version
# RUN pip3 install --upgrade pip
# RUN pip3 install --upgrade setuptools wheel
# RUN ln -s /usr/bin/python3 /usr/bin/python & \
#     ln -s /usr/bin/pip3 /usr/bin/pip


### Python Packages ###
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade --no-cache-dir -r requirements.txt


### Clean-up ###
RUN apt-get clean


### Create a non-root user
# https://github.com/facebookresearch/detectron2/blob/v0.3/docker/Dockerfile
# https://code.visualstudio.com/docs/remote/containers-advanced#_creating-a-nonroot-user
ARG USER_ID=1000
RUN useradd -m --no-log-init --system  --uid ${USER_ID} appuser -g sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER appuser
ENV PATH="/home/appuser/.local/bin:${PATH}"


CMD bash
