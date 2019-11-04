#!/usr/bin/env bash

# create docker image
docker build -t streaming_data_with_object_detection:0.1 -f docker/DockerFile .

# create each container(zookeeper, kafka server, client)
