#!/bin/bash

echo ""

echo -e "💥 build docker hadoop & spark image"
docker build -t spark-hadoop:latest -f yarn-cluster/Dockerfile .
