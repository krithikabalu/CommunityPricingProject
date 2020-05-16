#!/bin/bash
docker rm -f hadoop-master 
docker rm -f hadoop-slave1
docker rm -f hadoop-slave2 
docker rm -f hadoop-slave3
docker rm elasticsearch -f
docker rm kibana -f
docker network rm hadoop


