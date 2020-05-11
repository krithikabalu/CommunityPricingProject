#!/bin/bash

echo ""

echo -e "💥 build docker hadoop & spark image"
docker build -t spark-hadoop:latest -f yarn-cluster/Dockerfile .

echo -e "🔎 build elasticsearch"
docker rm elasticsearch -f
docker run --init --network hadoop -d --name elasticsearch -p 9200:9200 blacktop/elasticsearch

echo -e "🎃 build kibana"
docker rm kibana -f
docker run --init --network hadoop -d --name kibana --link elasticsearch -p 5601:5601 blacktop/kibana

echo ""
