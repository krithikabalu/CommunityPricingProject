import sys

from pyspark.sql import SparkSession

spark = SparkSession.builder. \
    appName("Pricing").getOrCreate()


def execute():
    data = spark.read.format("avro").load(sys.argv[1])
    data.withColumn("gross_price",
                    data["cost"] *
                    (1 + data["markup"] / 100) /
                    (1 - (data["base_discount"] + data["promotional_discount"]) / 100)) \
        .write \
        .csv(sys.argv[2], header=True)


execute()
