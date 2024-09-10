from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
from pyspark.sql.functions import from_json, col, window, count


# Define schema for the log data
log_schema = StructType(
    [
        StructField("client_ip", StringType()),
        StructField("rfc_id", StringType()),
        StructField("user_id", StringType()),
        StructField("@timestamp", TimestampType()),
        StructField("http_method", StringType()),
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

# Parse JSON data using the log_schema
parsed_df = df.select(
    from_json(col("value").cast("string"), log_schema).alias("data")
).select("data.*")

# Perform analytics
requests_per_minute = parsed_df \
    .withWatermark("`@timestamp`", "1 minute") \
    .groupBy(window("`@timestamp`", "1 minute")) \
    .agg(count("*").alias("request_count"))

# Write results to console
query = requests_per_minute \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()


# Debug to console
# debug_query = parsed_df \
#     .writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .start()

# debug_query.awaitTermination()
