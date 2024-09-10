from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType


# Define schema for the log data
log_schema = StructType(
    [
        StructField("client_ip", StringType()),
        StructField("user_id", StringType()),
        StructField("user", StringType()),
        StructField("timestamp", TimestampType()),
        StructField("request_method", StringType()),
        StructField("request", StringType()),
        StructField("http_version", StringType()),
        StructField("response_code", IntegerType()),
        StructField("bytes", IntegerType()),
        StructField("referrer", StringType()),
        StructField("user_agent", StringType()),
    ]
)


spark_master_url = "spark://abantony-mac:7077"
conf = SparkConf().setAppName("AccessLogAnalysis").setMaster(spark_master_url)

# Create SparkSession
builder = SparkSession.Builder()
spark = builder.config(conf=conf).getOrCreate()


# Read data from Kafka
df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "access_logs")
    .option("startingOffsets", "earliest")
    .load()
)
