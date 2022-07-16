import json
from os import truncate
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
from influxdb import InfluxDBClient
from datetime import datetime, time

import os

class StreamProcessor():
    def __init__(self) -> None:
        self.spark = (SparkSession
                    .builder
                    .master('spark://vds-vanhta2:7077')
                    .appName("StreamStockPriceProcessor")
                    .getOrCreate())
            
        self.past_data = self.spark.read.parquet('src/ingestion/stream_processor/past_data')
        self.new_day = self.past_data.agg(max("day")).collect()[0]["max(day)"] + 1
        self.prev_20_close_df = self.past_data.filter(col("day") == self.new_day - 20).selectExpr("Symbol", "Close as prev_20_close")
        self.prev_50_close_df = self.past_data.filter(col("day") == self.new_day - 50).selectExpr("Symbol", "Close as prev_50_close")
        self.k12 = 2/13
        self.k26 = 2/27
        self.prev_day_df =  self.past_data.filter(col("day") == self.new_day - 1) \
                                .selectExpr("Symbol", "MA20 as prev_MA20", "MA50 as prev_MA50", "EMA12 as prev_EMA12", "EMA26 as prev_EMA26")
        self.prev_day_df = self.prev_day_df \
                                .join(self.prev_20_close_df, ["Symbol"], "inner") \
                                .join(self.prev_50_close_df, ["Symbol"], "inner")

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

        self.influx_client =  self.influx_client = InfluxDBClient(
            host=config.influx_host, 
            port=config.influx_port,
            username=config.influx_username,
            password=config.influx_password
        )
        

    def process_batch(self, df, epoch_id):
        df = df.join(self.prev_day_df, ["Symbol"], "inner")
        df = df.withColumn("MA20", (col("prev_MA20") * 20 - col("prev_20_close") + col("Close")) / 20) \
                .withColumn("MA50", (col("prev_MA50") * 50 - col("prev_50_close") + col("Close")) / 50) \
                .withColumn("EMA12", col("Close") * self.k12 + col("prev_EMA12") * (1- self.k12)) \
                .withColumn("EMA26", col("Close") * self.k26 + col("prev_EMA26") * (1- self.k26)) 
        df = df.withColumn("MACD", col("EMA12") - col("EMA26"))

        df.persist()
        kafka_df = df.selectExpr("CAST(Symbol as STRING) as key", "CAST(Close as STRING) as value", "'price' as topic") \
                    .unionAll(df.selectExpr("CAST(Symbol as STRING) as key", "CAST(MA20 as STRING) as value", "'MA20' as topic")) \
                    .unionAll(df.selectExpr("CAST(Symbol as STRING) as key", "CAST(MA50 as STRING) as value", "'MA50' as topic")) \
                    .unionAll(df.selectExpr("CAST(Symbol as STRING) as key", "CAST(EMA12 as STRING) as value", "'EMA12' as topic")) \
                    .unionAll(df.selectExpr("CAST(Symbol as STRING) as key", "CAST(EMA26 as STRING) as value", "'EMA26' as topic")) \
                    .unionAll(df.selectExpr("CAST(Symbol as STRING) as key", "CAST(MACD as STRING) as value", "'MACD' as topic"))  
        kafka_df.write \
                .format("kafka") \
                .option("kafka.bootstrap.servers", "127.0.0.1:9092") \
                .save()
        
        influx_df = df.withColumn("Time", lit(int(datetime.combine(datetime.now(), time.min).timestamp())))
        influx_df.write \
                .format("console") \
                .mode("overwrite") \
                .save()


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
            .agg(last("Close").alias("Close"), 
                last("Volume").alias("Volume"), 
                last("Time").alias("Time"),
                last("Open").alias("Open"),
                last("High").alias("High"),
                last("Low").alias("Low"),
            )
        )

        streaming_query = (tbl.writeStream
                            .outputMode("Complete")
                            .foreachBatch(self.process_batch)
                            .trigger(processingTime = "10 second")
                            .option("checkpointLocation", "src/ingestion/stream_processor/checkpoint_dir")
                            .start()    
                        )
                    
        # streaming_query = (tbl.selectExpr("topic", "CAST(Symbol as STRING) AS key", "CAST(last_close as STRING) as value")
        #             .writeStream
        #             .format("kafka")
        #             .outputMode("Complete")
        #             .option("kafka.bootstrap.servers", "127.0.0.1:9092")
        #             .trigger(processingTime = "10 second")
        #             .option("checkpointLocation", "src/ingestion/stream_processor/checkpoint_dir")
        #             .start())

        streaming_query.awaitTermination()
        streaming_query.stop()


if __name__ == '__main__':
    processor = StreamProcessor()
    processor.process()