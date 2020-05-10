#!/bin/bash

echo ""

echo -e "\nbuild docker hadoop & spark image\n"
docker build -t spark-hadoop:latest -f yarn-cluster/Dockerfile .

echo ""
