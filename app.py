from pyspark.sql import SparkSession
from pyspark import SparkConf

spark_master_url = 'spark://abantony-mac:7077'
conf = SparkConf().setAppName("Access Log Analysis").setMaster(spark_master_url)

spark = SparkSession.builder.config(conf=conf).getOrCreate()

file_name = "data/access.log"

rdd = spark.sparkContext.textFile(file_name)
first_5_lines = rdd.take(5)

for line in first_5_lines:
    print(line)

spark.stop()

