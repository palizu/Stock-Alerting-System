# import imp
from ast import Str
import json
from kafka import KafkaConsumer
from pyspark.sql.functions import *
from pyspark.sql.types import *
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
            .load(file_path))

        streaming_query = (self.df.writeStream
                    .format("parquet")
                    .option("path", "src/ingestion/stream_processor/data/output")
                    .option("checkpointLocation", "src/ingestion/stream_processor/data/checkpoint_dir")
                    .start())

if __name__ == '__main__':
    processor = StreamProcessor()
    processor.consume_from_file("src/ingestion/stream_processor/data/data.json")