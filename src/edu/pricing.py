from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType
import sys

spark = SparkSession.builder. \
    appName("Pricing").getOrCreate()


def execute():
    data = spark.read.format("avro").load(sys.argv[1])
    result = data.withColumn("cost", data["cost"].cast(DoubleType()))
    agg_result = result.groupBy("elasticity").avg("cost")
    agg_result.write.csv(sys.argv[2])


execute()
