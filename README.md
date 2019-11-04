# Streaming Data with Object Detection

## introduction

sample object detection and face recognition function

## environment

* Docker
    * if you need to play face recognition codes, don't use docker container.

## install

### Create Docker Image

```
$ docker build -t streaming_data_with_object_detection:0.1 -f docker/DockerFile .
```

If you don't use cache, set "--no-cache=true".

### Run Docker Container

```
$ docker run -v `pwd`/script:/home/development/script -it --name sdwod_container streaming_data_with_object_detection:0.1 /bin/bash
```

## Usage

TODO
