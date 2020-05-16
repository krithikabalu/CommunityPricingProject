#!/bin/bash
sh yarn-cluster/stop.sh

docker network create --driver=bridge hadoop

N=${1:-4}

# start hadoop master container
echo "start hadoop-master container..."
docker run -itd \
                --net=hadoop \
                -p 50070:50070 \
                -p 8088:8088 \
                -p 7077:7077 \
                -p 16010:16010 \
                -p 18080:18080 \
                -p 4040:4040 \
                --name hadoop-master \
                --hostname hadoop-master \
                spark-hadoop:latest &> /dev/null


# start hadoop slave container
i=1
while [ $i -lt $N ]
do
	echo "start hadoop-slave$i container..."
	port=$(( 8040 + $i ))
	docker run -itd \
			-p $port:8042 \
	                --net=hadoop \
	                --name hadoop-slave$i \
	                --hostname hadoop-slave$i \
	                spark-hadoop:latest &> /dev/null
	i=$(( $i + 1 ))
done 

docker exec -it hadoop-master /root/start-hadoop.sh
docker exec -it hadoop-master hadoop fs -mkdir /spark-logs
docker exec -it hadoop-master /usr/local/spark/sbin/start-history-server.sh

echo -e "🔎 run elasticsearch"
docker run --init --network hadoop -d --name elasticsearch -p 9200:9200 blacktop/elasticsearch

echo -e "🎃 run kibana"
docker run --init --network hadoop -d --name kibana --link elasticsearch -p 5601:5601 blacktop/kibana

echo -e "run hive init"
docker exec -it hadoop-master schematool -initSchema -dbType derby
echo ""