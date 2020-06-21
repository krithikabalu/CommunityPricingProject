docker exec -it hadoop-master hadoop fs -rm -r /Output
docker cp src/edu/pricing.py hadoop-master:/root/
docker cp src/edu/error_processing.py hadoop-master:/root/
docker exec -it hadoop-master spark-submit \
 --packages org.apache.spark:spark-avro_2.11:2.4.5 \
 --deploy-mode cluster \
  --num-executors 3 \
   /root/error_processing.py hdfs://hadoop-master:9000/user/root/product/ hdfs://hadoop-master:9000/user/root/processed/product
docker exec -it hadoop-master spark-submit \
 --packages org.apache.spark:spark-avro_2.11:2.4.5 \
 --deploy-mode cluster \
  --num-executors 3 \
   /root/pricing.py hdfs://hadoop-master:9000/user/root/processed/product/ hdfs://hadoop-master:9000/Output/