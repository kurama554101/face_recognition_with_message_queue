#!/usr/bin/env bash

# get kafka
wget http://ftp.jaist.ac.jp/pub/apache/kafka/2.3.0/kafka_2.12-2.3.0.tgz
tar -zxf kafka_2.12-2.3.0.tgz
rm -rf kafka_2.12-2.3.0.tgz

# install JDK
apt-get install -y openjdk-8-jdk

# install kafkacat to debug
apt-get install -y kafkacat
