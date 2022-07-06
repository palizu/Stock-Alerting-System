# import imp
from ast import Str
import json
from os import truncate
from tokenize import Double
from xml.dom.minicompat import StringTypes
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
import config

import os

class StreamProcessor():
    def __init__(self) -> None:
        self.spark = (SparkSession
                    .builder
                    .master('spark://vds-vanhta2:7077')
                    .appName("StreamStockPriceProcessor")
                    .getOrCreate())
            
        # self.past_data = self.spark.read.parquet('src/ingestion/stream_processor/past_data')
        # window_spec = Window.partitionBy('Symbol').orderBy(col('PARTITION_DATE').desc())
        # self.past_data = self.past_data.withColumn("rn", row_number().over(window_spec))
        # self.past_data = self.past_data.select(self.past_data.columns[:-1]).where("rn <= 20").orderBy("PARTITION_DATE", "Symbol")
        # print(self.past_data.schema)
        # self.past_data.show(truncate=False)
        # self.past_data.createOrReplaceTempView("past_data")

        try: 
            connection = mysql.connector.connect(
                host=config.host,
                database=config.database,
                port=config.port,
                user=config.username,
                password=config.password
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

    def process(self):
        schema = (StructType()
                .add(StructField("Symbol", StringType()))
                .add(StructField("TradingDate", StringType()))
                .add(StructField("Time", StringType()))
                .add(StructField("Open", StringType()))
                .add(StructField("High", StringType()))
                .add(StructField("Low", StringType()))
                .add(StructField("Close", StringType()))
                .add(StructField("Volume", StringType()))
            )

        self.df = (self.spark
            .readStream
            .format('kafka')
            .option("kafka.bootstrap.servers", "127.0.0.1:9092")
            .option("subscribe", "market_data")
            .option("startingOffsets", "latest")
            .load()
        )

        tbl = self.df.select(
            from_json(col("value") 
            .cast("string"), schema) 
            .alias("data")
        ).select("data.*")

        tbl = (tbl
            .withColumn("timestamp", to_timestamp(to_date(concat_ws(" ", "TradingDate", "Time"), 'dd/MM/yyyy HH:mm:ss')))
            .withWatermark("timestamp", "5 minutes")
            .groupBy("Symbol")
            .agg(last("Close").alias("last_close"), last("Volume").alias("last_volume"), last("Time").alias("last_time"))
        )

        tbl = tbl.withColumn("topic", lit("price"))

        # streaming_query = (tbl.selectExpr("CAST(Symbol as STRING) AS key", "CAST((last_close || ':' || Symbol || ':' || timestamp) as STRING) as value")
        #             .writeStream
        #             .format("console")
        #             .outputMode("complete")
        #             # .option("kafka.bootstrap.servers", "127.0.0.1:9092")
        #             .trigger(processingTime = "10 second")
        #             .option("checkpointLocation", "src/ingestion/stream_processor/checkpoint_dir")
        #             .start())
                    
        streaming_query = (tbl.selectExpr("topic", "CAST(Symbol as STRING) AS key", "CAST(last_close as STRING) as value")
                    .writeStream
                    .format("kafka")
                    .outputMode("Complete")
                    .option("kafka.bootstrap.servers", "127.0.0.1:9092")
                    .trigger(processingTime = "10 second")
                    .option("checkpointLocation", "src/ingestion/stream_processor/checkpoint_dir")
                    .start())

        streaming_query.awaitTermination()
        streaming_query.stop()


if __name__ == '__main__':
    processor = StreamProcessor()
    processor.process()