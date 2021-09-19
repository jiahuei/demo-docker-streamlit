#!/usr/bin/env bash

#    -p 6006:6006 \
#    -v /home/USERNAME/datasets:/datasets \

docker run -it --rm \
    --gpus all \
    -u "$(id -u)":"$(id -g)" \
    -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
    demo-docker/python:3.9
