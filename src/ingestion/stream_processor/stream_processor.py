# import imp
from ast import Str
import json
from os import truncate
from kafka import KafkaConsumer
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import *
from pyspark.sql.streaming import *
from pyspark.sql import SparkSession
import logging
import mysql.connector
from mysql.connector import Error
import config
import redis

class StreamProcessor():
    def __init__(self) -> None:
        self.spark = (SparkSession
                    .builder
                    .master('local')
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

        self.r = redis.Redis()
        self.loadMySQLTableToRedis

    def loadMySQLTableToRedis(self):
        pass

    # def getAlert(self, df, epoch_id):
    #     for ticker in config.TICKERS:
    #         price = df.filter(col("Symbol") == ticker).select("Last Close")
    #         print(price)
  

    def consume_from_file(self, file_path):
        file_schema = (StructType()
                .add(StructField("Symbol", StringType()))
                .add(StructField("Open", DoubleType()))
                .add(StructField("High", DoubleType()))
                .add(StructField("Low", DoubleType()))
                .add(StructField("Close", DoubleType()))
                .add(StructField("Volume", DoubleType()))
                .add(StructField("Value", DoubleType()))
                .add(StructField("Time", StringType()))
                .add(StructField("PARTITION_M", StringType()))
                .add(StructField("PARTITION_DATE", StringType()))
            )
        self.df = (self.spark
            .readStream
            .format('parquet')
            .schema(file_schema)
            .option('maxFilesPerTrigger', 1)
            .load(file_path))
        
        # price_table = (self.df
        #             .withColumn("timestamp", to_timestamp(to_date(concat_ws(" ", "TradingDate", "Time"), 'dd/MM/yyyy HH:mm:ss'))))
        self.df = self.df.filter(col("Symbol") == "AAA")
        
        price_table = (self.df
                    .groupBy("Symbol")
                    .agg(last("Close").alias("Last Close"), last("Volume").alias("Last Volume"), last("Time").alias("Time"))
                    )
                    
        streaming_query = (price_table.writeStream
                    .foreachBatch(self.getAlert)
                    .format("console")
                    .outputMode("complete")
                    .trigger(processingTime = "30 second")
                    .option("checkpointLocation", "src/ingestion/stream_processor/checkpoint_dir")
                    .start())

        streaming_query.awaitTermination()

if __name__ == '__main__':
    processor = StreamProcessor()
    processor.consume_from_file("src/ingestion/stream_processor/intra_day/PARTITION_DATE=04042022")