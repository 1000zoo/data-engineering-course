from pyspark.sql import SparkSession
from pyspark.sql.functions import *


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Streaming Word Count") \
        .master("local[3]") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .config("spark.sql.shuffle.partitions", 3) \
        .getOrCreate()

    # READ
    lines_df = spark.readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", "9998") \
        .load()

    # TRANSFORM
    lines_df.createOrReplaceTempView("lines")
    words_df = spark.sql("SELECT explode(split(value, ' ')) as word FROM lines")
    words_df.createOrReplaceTempView("words")
    counts_df = spark.sql("SELECT word, count(*) as count FROM words GROUP BY word")

    # SINK
    word_count_query = counts_df.writeStream \
        .format("console") \
        .outputMode("complete") \
        .option("checkpointLocation", "chk-point-dir") \
        .start()

    print("Listening to localhost:9998")
    word_count_query.awaitTermination()