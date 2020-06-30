docker cp src/edu/ml.py hadoop-master:/root/
docker exec -it hadoop-master spark-submit --deploy-mode cluster /root/ml.py