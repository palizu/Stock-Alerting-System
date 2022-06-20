# import imp
from ast import Str
import json
from kafka import KafkaConsumer
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import *
from pyspark.sql.streaming import *
from pyspark.sql import SparkSession

class StreamProcessor():
    def __init__(self) -> None:
        self.spark = (SparkSession
                    .builder
                    .appName("StreamStockPriceProcessor")
                    .getOrCreate())

    def consume_from_file(self, file_path):
        file_schema = (StructType()
                    .add(StructField("RType", StringType()))
                    .add(StructField("TradingDate", StringType()))
                    .add(StructField("Time", StringType()))
                    .add(StructField("Symbol", StringType()))
                    .add(StructField("Open", DoubleType()))
                    .add(StructField("High", DoubleType()))
                    .add(StructField("Low", DoubleType()))
                    .add(StructField("Close", DoubleType()))
                    .add(StructField("Volume", DoubleType()))
                    .add(StructField("Value", DoubleType()))
                    )

        self.df = (self.spark
            .readStream
            .format('json')
            .schema(file_schema)
            .option('maxFilesPerTrigger', 1)
            .load(file_path))
        
        price_table = (self.df
                    .withColumn("timestamp", to_timestamp(to_date(concat_ws(" ", "TradingDate", "Time"), 'dd/MM/yyyy HH:mm:ss'))))
        price_table = (price_table
                    .withWatermark("timestamp", "10 minutes") 
                    .groupBy("Symbol")
                    .agg(last("Close").alias("Last Close"), last("Volume").alias("Last Volume"), last("Time").alias("Time"))
                    )

        streaming_query = (price_table.writeStream
                    .format("console")
                    .outputMode("complete")
                    .trigger(processingTime = "60 second")
                    .option("checkpointLocation", "src/ingestion/stream_processor/checkpoint_dir")
                    .start())

        streaming_query.awaitTermination()

if __name__ == '__main__':
    processor = StreamProcessor()
    processor.consume_from_file("src/ingestion/stream_processor/test_data/")