from os import preadv
from gevent import config
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import *
from pyspark.sql.streaming import *
from pyspark.sql import SparkSession
import pandas as pd
import config
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import json
import time


#----------------------- write to influx ----------------------------
# data = []
# with open("src/ingestion/stream_processor/processed_past_data.json", 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         line = json.loads(line)
#         row = [line['Symbol'], line['Open'], line['High'], line['Low'],
#                 line['Close'], line['Volume'], line['Value'], line['day'], 
#                 line['MA20'], line['MA50'], line['EMA12'], line['EMA26'], line['MACD'], 
#                 line['SIGNAL_LINE'], line['Up_Change'], line['Down_Change'], line['RSI'], line['PARTITION_DATE']
#             ]
#         data.append(row)

# cols = ['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Value', 
#                 'day', 'MA20', 'MA50', 'EMA12', 'EMA26', 
#                 'MACD', 'SIGNAL_LINE','Up_Change', 'Down_Change', 'RSI', 'PARTITION_DATE', 
#         ]
# new_df = pd.DataFrame(columns=cols, data = data)

# c = ['Open', 'High', 'Low', 'Close', 'MA20', 'MA50', 'EMA12', 'EMA26', 
#      'MACD', 'SIGNAL_LINE','Up_Change', 'Down_Change']

# for c in c:
#     new_df[c] = new_df[c] / 1000

# df = new_df

# # print(df.columns)
# client = InfluxDBClient(url="http://127.0.0.1:8086", token=config.influx_token, org=config.influx_org)
# write_api = client.write_api(write_options=SYNCHRONOUS)
# points = []

# for ind, row in df.iterrows():
#     (symbol, open, high, low, close, volume, value, _, ma20, ma50, ema12, ema26, macd, signal_line, up_change, down_change, rsi, date) = row
#     time = int(datetime.strptime(str(date),'%Y%m%d').timestamp()) * 1000000000
#     # data = f"market_data,ticker={symbol} Open={open},High={high},Low={low},Close={close},Volume={volume},Value={value},\
#     #         MA20={ma20},MA50={ma50},EMA12={ema12},EMA26={ema26},MACD={macd} {time*1000000}"
#     p = Point("stock_info").tag("ticker", symbol) \
#             .field("open", open) \
#             .field("high", high) \
#             .field("low", low) \
#             .field("close", close) \
#             .field("volume", volume) \
#             .field("value", value) \
#             .field("MA20", ma20) \
#             .field("MA50", ma50) \
#             .field("EMA12", ema12) \
#             .field("EMA26", ema26) \
#             .field("MACD", macd) \
#             .field("SIGNAL_LINE", signal_line) \
#             .field("Up_change", up_change) \
#             .field("Down_change", down_change) \
#             .field("RSI", rsi) \
#             .time(time)
#     points.append(p)
#     if len(points) == 5000: 
#         write_api.write(config.influx_bucket, config.influx_org, points)
#         points = []
#         print("Writen...." + str(p.to_line_protocol()))

# write_api.write(config.influx_bucket, config.influx_org, points)

# ---------------------------- gen past data -----------------------------------
# data = []
# with open("src/ingestion/stream_processor/processed_past_data.json", 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         line = json.loads(line)
#         row = [line['Symbol'], line['Open'], line['High'], line['Low'],
#                 line['Close'], line['Volume'], line['Value'], line['day'], 
#                 line['MA20'], line['MA50'], line['EMA12'], line['EMA26'], line['MACD'], 
#                 line['SIGNAL_LINE'], line['Up_Change'], line['Down_Change'], line['RSI'], line['PARTITION_DATE']
#             ]
#         data.append(row)

# cols = ['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Value', 
#                 'day', 'MA20', 'MA50', 'EMA12', 'EMA26', 
#                 'MACD', 'SIGNAL_LINE','Up_Change', 'Down_Change', 'RSI', 'PARTITION_DATE', 
#         ]
# new_df = pd.DataFrame(columns=cols, data = data)

# c = ['Open', 'High', 'Low', 'Close', 'MA20', 'MA50', 'EMA12', 'EMA26', 
#      'MACD', 'SIGNAL_LINE','Up_Change', 'Down_Change']

# for c in c:
#     new_df[c] = new_df[c] / 1000

# df = new_df

# schema = (StructType()
#                 .add(StructField("Symbol", StringType()))
#                 .add(StructField("Open", FloatType()))
#                 .add(StructField("High", FloatType()))
#                 .add(StructField("Low", FloatType()))
#                 .add(StructField("Close", FloatType()))
#                 .add(StructField("Volume", FloatType()))
#                 .add(StructField("Value", FloatType()))
#                 .add(StructField("day", IntegerType()))
#                 .add(StructField("MA20", FloatType()))
#                 .add(StructField("MA50", FloatType()))
#                 .add(StructField("EMA12", FloatType()))
#                 .add(StructField("EMA26", FloatType()))
#                 .add(StructField("MACD", FloatType()))
#                 .add(StructField("SIGNAL_LINE", FloatType()))
#                 .add(StructField("Up_Change", FloatType()))
#                 .add(StructField("Down_Change", FloatType()))
#                 .add(StructField("RSI", FloatType()))
#                 .add(StructField("PARTITION_DATE", StringType()))
#             )

spark = (SparkSession
                    .builder
                    .master(config.SPARK_SERVER)
                    .appName("mpl_data")
                    .getOrCreate())

# spark_df = spark.createDataFrame(schema=schema, data=df)
# spark_df.show()
# spark_df.write.mode('overwrite').partitionBy("PARTITION_DATE").parquet('src/ingestion/stream_processor/past_data')

spark.read.parquet('src/ingestion/stream_processor/past_data').show()