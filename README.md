# Streaming Data with Face Detection

## introduction

Face recognition function using messaging queue of kafka.
This function use following component.

* client(host)
    * this component run main script.
* kafka server(docker container)
    * this component run kafka message queue.
* zookeeper(docker container)
    * this component run zookeeper.

## environment

* Docker
    * if you need to play face recognition codes, don't use docker container.
* python3.6
    * because main script and faust framework use "async".
* [kafka](https://github.com/apache/kafka)
* python packages
    * [faust](https://github.com/robinhood/faust)
    * [aiostream](https://github.com/vxgmichel/aiostream)

## setup

### Create Docker Image

```
$ cd (root directory of this repository)
$ docker build -t streaming_data_with_object_detection:0.1 -f docker/DockerFile .
```

If you don't use cache, set "--no-cache=true".

### Create Docker Container

you need to create following docker container.

* kafka_server
* zookeeper

So you need to do following process.

1. run zookeeper container
2. run kafka server container
3. set up the config of kafka server container

#### Run zookeeper container

1. run zookeeper container

    ```
    $ docker run -v `pwd`/script:/home/development/script -it \
      --name zookeeper streaming_data_with_object_detection:0.1 /bin/bash
    ```

2. check ip address of zookeeper

    ```
    $ docker attach zookeeper
    $ hostname --i
    ```

    "hostname --i" command display private ip address of docker container.
    Suppose the ip address is A.

3. run zookeeper process
    
    ```
    $ cd kafka_2.12-2.3.0
    $ bin/zookeeper-server-start.sh config/zookeeper.properties
    ```
    
    if you start the process of zookeeper, you detach this container(not exit)

#### Run kafka server container

1. run kafka server container

    ```
    $ docker run -v `pwd`/script:/home/development/script -it -p 9092:9092 \
      --name kafka_server streaming_data_with_object_detection:0.1 /bin/bash
    ```
    
    if you run main script on host machine, 
    you need to link the host machine port to the this container port.

2. modify kafka server.properties

    ```
    $ docker attach kafka_server
    $ vim kafka_2.12-2.3.0/config/server.properties
    ```
    
    you need to modify the following parameters.
    * advertised.listeners=PLAINTEXT://localhost:9092
    * zookeeper.connect=A:2181 (A is the ip address of zookeeper container)

3. run kafka process

    ```
    $ cd kafka_2.12-2.3.0
    $ bin/kafka-server-start.sh config/server.properties
    ```
    
    if you have done these process, you detach this container(not exit)

### Run test script

1. run test script
    
    you should run test script on host machine because of check the setting.
    
    ```
    $ cd (root directory of this repository)/script
    $ python3 sample/hello_world.py worker -l info
    ```

    After waiting for a while, "[WARNING] b'hoge'" message is displayed on the console.

### Run main script of face recognition

1. run main script of face recognition
    
    ```
    $ cd (root directory of this repository)/script
    $ python3 main.py worker -l info
    ```
    
    After running the main script, face recognition result with capture image of camera is displayed.
