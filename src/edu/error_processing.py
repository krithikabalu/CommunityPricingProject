import sys

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PricingErrorProcessing").getOrCreate()


def execute():
    data = spark.read.format("avro").load(sys.argv[1])
    error_records = data.filter(data.name == '')
    result = data.exceptAll(error_records)
    result.write.format("avro").save(sys.argv[2])
    error_records.write.format("avro").save(sys.argv[3])

execute()
