# import imp
from ast import Str
import json
from kafka import KafkaConsumer
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import *
from pyspark.sql.streaming import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import first, last
import logging
import mysql.connector
from mysql.connector import Error
import configs


class StreamProcessor():
    def __init__(self) -> None:
        self.spark = (SparkSession
                    .builder
                    .master('local')
                    .appName("StreamStockPriceProcessor")
                    .getOrCreate())
            
        # self.past_data = self.spark.read.parquet('past_data')
        # print(self.past_data.schema)

        try: 
            connection = mysql.connector.connect(
                host=configs.host,
                database=configs.database,
                port=configs.port,
                user=configs.username,
                password=configs.password
            )
            if connection.is_connected():
                self.connection = connection
                logging.info(connection.get_server_info())
                self.cursor = connection.cursor()
                self.cursor.execute("select database();")
                record = self.cursor.fetchone()
                logging.info(f"You're connected to database: {record}")

        except Error as e:
            logging.error("Error while connecting to MySQL:\n" + e)

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
                    .withColumn("timestamp", to_timestamp(concat_ws(" ", "TradingDate", "Time"), 'dd/MM/yyyy HH:mm:ss'))
                    )
        price_table = (price_table
        #             .withWatermark("timestamp", "10 minutes") 
        #             .groupBy("Symbol")
        #             .agg(last("Close").alias("Last Close"), last("Volume").alias("Last Volume"), last("Time").alias("Time"))
                    .filter(col("Symbol") == 'FPT')
                    )
                    

        streaming_query = (price_table.writeStream
                    .format("console")
                    .outputMode("append")
                    # .trigger(processingTime = "60 second")
                    .option("checkpointLocation", "src/ingestion/stream_processor/checkpoint_dir")
                    .start())

        streaming_query.awaitTermination()
        streaming_query.stop()


if __name__ == '__main__':
    processor = StreamProcessor()
    processor.consume_from_file("src/ingestion/stream_processor/test_data/")