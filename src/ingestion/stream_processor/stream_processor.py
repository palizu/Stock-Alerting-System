import json
from os import truncate
from sqlite3 import Time
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
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import pandas as pd
from dateutil.tz import gettz


import os

class StreamProcessor():
    def __init__(self) -> None:
        self.spark = (SparkSession
                    .builder
                    .master(config.SPARK_SERVER)
                    .appName("StreamStockPriceProcessor")
                    .getOrCreate())
        self.spark.sparkContext.setLogLevel("WARN")
            
        self.past_data = self.spark.read.parquet('src/ingestion/stream_processor/past_data')
        self.new_day = self.past_data.agg(max("day")).collect()[0]["max(day)"] + 1
        self.prev_20_close_df = self.past_data.filter(col("day") == self.new_day - 20).selectExpr("Symbol", "Close as prev_20_close")
        self.prev_50_close_df = self.past_data.filter(col("day") == self.new_day - 50).selectExpr("Symbol", "Close as prev_50_close")
        self.prev_avg_changes_df = self.past_data.filter(col("day") >= self.new_day - 13).groupBy("Symbol").agg(
            sum("Up_Change").alias("sum_13_UpChange"),
            sum("Down_Change").alias("sum_13_DownChange"),
        )
        self.k12 = 2/13
        self.k26 = 2/27
        self.k9 = 2/10
        self.prev_day_df =  self.past_data.filter(col("day") == self.new_day - 1) \
                                .selectExpr("Symbol", "MA20 as prev_MA20", "MA50 as prev_MA50", "EMA12 as prev_EMA12", "EMA26 as prev_EMA26", "SIGNAL_LINE as prev_SIGNAL_LINE")
        self.prev_day_df = self.prev_day_df \
                                .join(self.prev_20_close_df, ["Symbol"], "inner") \
                                .join(self.prev_50_close_df, ["Symbol"], "inner") \
                                .join(self.prev_avg_changes_df, ["Symbol"], "inner")
        # self.today_timestamp = int(datetime.strptime(datetime.strftime(datetime.today(),"%d/%m/%Y"), "%d/%m/%Y").timestamp())
        self.today_timestamp = int(datetime.strptime("01/08/2022", "%d/%m/%Y").replace(tzinfo=gettz('Asia/Ho_Chi_Minh')).timestamp())
    
        # try: 
        #     connection = mysql.connector.connect(
        #         host=config.host,
        #         database=config.database,
        #         port=config.port,
        #         user=config.username,
        #         password=config.password
        #     )
        #     if connection.is_connected():
        #         self.connection = connection
        #         logging.info(connection.get_server_info())
        #         self.cursor = connection.cursor()
        #         self.cursor.execute("select database();")
        #         record = self.cursor.fetchone()
        #         logging.info(f"You're connected to database: {record}")
        # except Error as e:
        #     logging.error("Error while connecting to MySQL:\n" + e)

        self.influx_client = InfluxDBClient(url=config.influx_server, token=config.influx_token, org=config.influx_org)
        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
        

    def process_batch(self, df, epoch_id):
        df = df.join(self.prev_day_df, ["Symbol"], "inner")
        df = df.withColumn("MA20", (col("prev_MA20") * 20 - col("prev_20_close") + col("Close")) / 20) \
                .withColumn("MA50", (col("prev_MA50") * 50 - col("prev_50_close") + col("Close")) / 50) \
                .withColumn("EMA12", col("Close") * self.k12 + col("prev_EMA12") * (1- self.k12)) \
                .withColumn("EMA26", col("Close") * self.k26 + col("prev_EMA26") * (1- self.k26)) \
                .withColumn("RSI", 100 - 100 / (
                    1 + (col("sum_13_UpChange") + col("Up_Change")) / (col("sum_13_DownChange") + col("Down_Change") + 1e-6)
                    )) 
        df = df.withColumn("MACD", col("EMA12") - col("EMA26"))
        df = df.withColumn("SIGNAL_LINE", col("MACD") * self.k9 + col("prev_SIGNAL_LINE") * (1- self.k9))
        df.show()

        df.persist()
        kafka_df = df.selectExpr("'price' as topic", "CAST(Symbol as STRING) as key", "CAST(Close as STRING) as value") \
                    .unionAll(df.selectExpr("'MA20' as topic", "CAST(Symbol as STRING) as key", "CAST(MA20 as STRING) as value")) \
                    .unionAll(df.selectExpr("'MA50' as topic", "CAST(Symbol as STRING) as key", "CAST(MA50 as STRING) as value")) \
                    .unionAll(df.selectExpr("'EMA12' as topic", "CAST(Symbol as STRING) as key", "CAST(EMA12 as STRING) as value")) \
                    .unionAll(df.selectExpr("'EMA26' as topic", "CAST(Symbol as STRING) as key", "CAST(EMA26 as STRING) as value", )) \
                    .unionAll(df.selectExpr("'MACD' as topic", "CAST(Symbol as STRING) as key", "CAST(MACD as STRING) as value" ))  \
                    .unionAll(df.selectExpr("'RSI' as topic", "CAST(Symbol as STRING) as key", "CAST(RSI as STRING) as value")) 
        kafka_df.write \
                .format("kafka") \
                .option("kafka.bootstrap.servers", "127.0.0.1:9092") \
                .save()
        
        influx_df = df.toPandas()
        points = []
        for ind, row in influx_df.iterrows():
            p = Point("stock_info").tag("ticker", row['Symbol']) \
                    .field("open", row['Open']) \
                    .field("high", row['High']) \
                    .field("low", row['Low']) \
                    .field("close", row['Close']) \
                    .field("volume", row['Volume']) \
                    .field("MA20", row['MA20']) \
                    .field("MA50", row['MA50']) \
                    .field("EMA12", row['EMA12']) \
                    .field("EMA26", row['EMA26']) \
                    .field("MACD", row['MACD']) \
                    .field("SIGNAL_LINE", row['SIGNAL_LINE']) \
                    .field("RSI", row['RSI']) \
                    .time(self.today_timestamp * 1000000000)
            points.append(p)
            if len(points) == 5000:
                self.write_api.write(config.influx_bucket, config.influx_org, points)
                points = []
                print(f"Writen {len(points)} data points to influxdb")
        self.write_api.write(config.influx_bucket, config.influx_org, points)
        print(f"Writen {len(points)} data points to influxdb")
        df.unpersist()


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
                .add(StructField("Change", StringType()))
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

        tbl = tbl.withColumn("Open", col("Open").cast(DoubleType()) / 1000) \
                .withColumn("High", col("High").cast(DoubleType()) / 1000) \
                .withColumn("Low", col("Low").cast(DoubleType()) / 1000) \
                .withColumn("Close", col("Close").cast(DoubleType()) / 1000) \
                .withColumn("Volume", col("Volume").cast(DoubleType())) \
                .withColumn("Up_Change", expr("CASE WHEN Change > 0 then Change / 1000 else 0 end")) \
                .withColumn("Down_Change", expr("CASE WHEN Change < 0 then 0 - Change / 1000 else 0 end"))\
                .withColumn("Change", col("Change").cast(DoubleType()) / 1000) 
                
            

        tbl = (tbl
            .withColumn("timestamp", to_timestamp(to_date(concat_ws(" ", "TradingDate", "Time"), 'dd/MM/yyyy HH:mm:ss')))
            .withWatermark("timestamp", "30 seconds")
            .groupBy("Symbol")
            .agg(
                last("Open").alias("Open"),
                last("High").alias("High"),
                last("Low").alias("Low"),
                last("Close").alias("Close"), 
                last("Volume").alias("Volume"), 
                last("Up_Change").alias("Up_Change"), 
                last("Down_Change").alias("Down_Change"), 
            )
        )

        streaming_query = (tbl.writeStream
                            .outputMode("Complete")
                            .foreachBatch(self.process_batch)
                            .trigger(processingTime = "30 seconds")
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