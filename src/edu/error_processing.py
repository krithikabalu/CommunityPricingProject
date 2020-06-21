import sys

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PricingErrorProcessing").getOrCreate()


def execute():
    data = spark.read.format("avro").load(sys.argv[1])
    result = data.filter(data.name != '')
    result.write.format("avro").save(sys.argv[2])


execute()
