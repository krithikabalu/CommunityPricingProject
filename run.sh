docker cp src/WordCount-1.0-SNAPSHOT.jar hadoop-master:/root/
docker cp src/input/sample1.txt hadoop-master:/root/sample1.txt
docker exec -it hadoop-master hadoop fs -copyFromLocal /root/sample1.txt /sample1.txt
docker exec -it hadoop-master hadoop jar WordCount-1.0-SNAPSHOT.jar Driver /sample1.txt /output
