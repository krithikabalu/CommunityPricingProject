from pyspark.ml.feature import VectorAssembler, Normalizer
from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Demo").getOrCreate()


def execute():
    # data = spark.read.csv('/Users/krithikab/Desktop/PRACT/SparkML/kc_house_data.csv', header=True, inferSchema=True)
    data = spark.read.csv('hdfs://hadoop-master:9000/user/root/kc_house_data.csv', header=True, inferSchema=True)
    assembler = VectorAssembler() \
        .setInputCols(["bedrooms", "bathrooms"]) \
        .setOutputCol("features") \
        .transform(data)
    assembler.show()

    normalizer = Normalizer() \
        .setInputCol("features") \
        .setOutputCol("normFeatures") \
        .setP(2.0) \
        .transform(assembler)
    normalizer.show()

    linear_regression = LinearRegression() \
        .setLabelCol("price") \
        .setFeaturesCol("normFeatures") \
        .setMaxIter(10) \
        .setRegParam(1.0) \
        .setElasticNetParam(1.0)

    result_array = normalizer.randomSplit([0.7, 0.3])
    lr_model = linear_regression.fit(result_array[0])
    predicted_data = lr_model.transform(result_array[1]).select("features", "normFeatures", "price", "prediction")
    predicted_data.show()

execute()
