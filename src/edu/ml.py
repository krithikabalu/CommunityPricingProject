from pyspark.ml.feature import VectorAssembler, Normalizer
from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Demo").getOrCreate()


def execute():
    input_data = spark.read.csv('hdfs://hadoop-master:9000/kc_house_data.csv', header=True, inferSchema=True)
    # input_data = spark.read.csv('/Users/krithikab/Desktop/PRACT/SparkML/kc_house_data.csv', header=True, inferSchema=True)

    data = input_data\
        .filter(input_data.price > 0)\
        .withColumn("age", 2020-input_data.yr_built)\
        .drop_duplicates()

    assembler = VectorAssembler() \
        .setInputCols(
        ["bedrooms", "bathrooms", "sqft_living", "floors", "condition", "sqft_lot",
         "waterfront", "view", "grade", "sqft_above", "sqft_basement", "age",
         "zipcode", "lat", "long", "sqft_living15", "sqft_lot15"]) \
        .setOutputCol("features") \
        .transform(data)

    normalizer = Normalizer() \
        .setInputCol("features") \
        .setOutputCol("normFeatures") \
        .transform(assembler)

    linear_regression = LinearRegression() \
        .setLabelCol("price") \
        .setFeaturesCol("normFeatures") \
        .setMaxIter(10) \
        .setRegParam(1.0) \
        .setElasticNetParam(1.0)

    result_array = normalizer.randomSplit([0.7, 0.3])
    lr_model = linear_regression.fit(result_array[0])

    predicted_data = lr_model.transform(result_array[1]).select("features", "normFeatures", "price", "prediction")
    # predicted_data.select("price", "prediction").write.csv("result.csv")
    predicted_data.select("price", "prediction").write.csv("hdfs://hadoop-master:9000/prediction.csv")


execute()
