import sys
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PricingErrorProcessing").getOrCreate()


def records_with_invalid_name(data):
    return data.filter((data.name == '') | data.name.isNull())


def records_with_invalid_base_discount(data):
    return data.filter((data.base_discount < 0) | (data.base_discount >= 99))


def execute():
    print("Starting the error processing")
    data = spark.read.format("avro").load(sys.argv[1])
    invalid_name_error_records = records_with_invalid_name(data)
    invalid_base_discount_error_records = records_with_invalid_base_discount(data)
    error_records = invalid_name_error_records.union(invalid_base_discount_error_records).distinct()
    result = data.exceptAll(error_records)
    result.write.format("avro").save(sys.argv[2])
    error_records.write.format("avro").save(sys.argv[3])


execute()
