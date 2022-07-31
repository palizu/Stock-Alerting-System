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


# spark = SparkSession.builder.appName("mnpl_data").getOrCreate()

# df = spark.read.parquet("src/ingestion/stream_processor/past_data")

# spark.read.parquet("src/ingestion/stream_processor/past_data").createOrReplaceTempView("df")
# windowSpec = Window.partitionBy(col("Symbol"), col())
# df = spark.sql("select *, Close - lag(Close, 1) over(partition by Symbol order by day) as price_changed from df order by Symbol, PARTITION_DATE")

# df = spark.sql("""select
#                     *,
#                     avg(close) over(
#                         partition by Symbol
#                         order by
#                             day ROWS BETWEEN 19 PRECEDING
#                             AND CURRENT ROW
#                     ) as MA20,
#                      avg(close) over(
#                         partition by Symbol
#                         order by
#                             day ROWS BETWEEN 49 PRECEDING
#                             AND CURRENT ROW
#                     ) as MA50
#                 from df """)

# df = spark.sql("select *, MA20 as EMA12, MA20 as EMA26 from df")

# k12 = 2 / 13
# k26 = 2 / 27

# windowSpec = Window.partitionBy(col("Symbol")).orderBy(col("day"))
# df = df.withColumn("Open", col("Open") / 1000)
# df = df.withColumn("High", col("High") / 1000)
# df = df.withColumn("Low", col("Low") / 1000)
# df = df.withColumn("Close", col("Close") / 1000)
# df = df.withColumn("MA20", col("MA20") / 1000)
# df = df.withColumn("MA50", col("MA50") / 1000)


# print(f"------------------00000-------------: {day}")

# df = df.withColumn("EMA12", col("Close") * k12 + lag("EMA12", 1).over(windowSpec) * (1 - k12))
# df = df.withColumn("EMA26", col("Close") * k26 + lag("EMA26", 1).over(windowSpec) * (1 - k26))
# df = df.withColumn("MACD", col("EMA12") - col("EMA26"))


# # df.write.mode("overwrite").partitionBy("PARTITION_DATE").parquet("src/ingestion/stream_processor/past_data_2")
# df.show()
# spark.read.parquet("src/ingestion/stream_processor/past_data").orderBy(["Symbol", "day"]).show()


spark = SparkSession.builder.master("spark://Van.local:7077").appName("mnpl_data").getOrCreate()
# df = spark.read.parquet("src/ingestion/stream_processor/past_data")
# df = df.toPandas()

# df['signal_line'] = df['PARTITION_DATE']
# df = df.rename(columns={"PARTITION_DATE":"signal_line", "signal_line" : "PARTITION_DATE"})
# df['signal_line'] = df['MACD']
# k9 = 2/10
# res = pd.DataFrame(columns=df.columns)
# for ticker in config.TICKERS:
#     temp_df = df.loc[df["Symbol"] == ticker].copy()
#     for i in range(61):
#         if i + 1 not in df[df.Symbol == ticker]['day'].values:
#             continue
#         prev_ema9 = temp_df.loc[temp_df['day'] == i + 1, 'signal_line'].values[0]
#         close = temp_df.loc[temp_df['day'] == i + 2, 'MACD'].values[0]
#         ema9 = close * k9 + prev_ema9 * (1-k9)
#         temp_df.loc[temp_df['day'] == i + 2, 'signal_line'] = ema9
#     res = pd.concat([res, temp_df])
    

# mapping = df.loc[df['Symbol'] == 'SJF'][['day', 'PARTITION_DATE']]
# day_mapping = {}
# for ind, row in mapping.iterrows():
#     key = row['PARTITION_DATE']
#     day = row['day']
#     day_mapping[key] = day

# for i in range(len(df)):
#     row = df.iloc[i]
#     day = day_mapping[row['PARTITION_DATE']]
#     df.loc[i, 'day'] = day

# df['EMA12'] = df['Close']
# df['EMA26'] = df['Close']
# res = pd.DataFrame(columns=df.columns)
# for ticker in config.TICKERS:
#     temp_df = df.loc[df["Symbol"] == ticker].copy()
#     for i in range(61):
#         if i == 0:
#             temp_df.loc[temp_df['day'] == 1, 'MACD'] = 0
#         if i + 1 not in df[df.Symbol == ticker]['day'].values:
#             continue
#         prev_ema12 = temp_df.loc[temp_df['day'] == i + 1, 'EMA12'].values[0]
#         prev_ema26 = temp_df.loc[temp_df['day'] == i + 1, 'EMA26'].values[0]
#         close = temp_df.loc[temp_df['day'] == i + 2, 'Close'].values[0]
#         ema12 = close * k12 + prev_ema12 * (1-k12)
#         ema26 = close * k26 + prev_ema26 * (1-k26)
#         temp_df.loc[temp_df['day'] == i + 2, 'EMA12'] = ema12
#         temp_df.loc[temp_df['day'] == i + 2, 'EMA26'] = ema26
#         temp_df.loc[temp_df['day'] == i + 2, 'MACD'] = ema12 - ema26
#     res = pd.concat([res, temp_df])


# -------------------------- RSI ------------------

# df.insert(loc=14, column='Up_Change', value=df['Close'])
# df.insert(loc=15, column='Down_Change', value=df['Close'])
# df.insert(loc=16, column='RSI', value=df['Close'])

# res = pd.DataFrame(columns=df.columns)
# for ticker in config.TICKERS:
#     temp_df = df.loc[df["Symbol"] == ticker].copy()
#     for i in range(62):
#         if i == 0:
#             temp_df.loc[temp_df['day'] == 1, "Down_Change"] = 0
#             temp_df.loc[temp_df['day'] == 1, "Up_Change"] = 0
#         if i not in df[df.Symbol == ticker]['day'].values:
#             continue
#         prev_close = temp_df.loc[temp_df['day'] == i, "Close"].values[0]
#         cur_close = temp_df.loc[temp_df['day'] == i + 1, "Close"].values[0]
#         if prev_close < cur_close:
#             temp_df.loc[temp_df['day'] == i + 1, "Down_Change"] = 0
#             temp_df.loc[temp_df['day'] == i + 1, "Up_Change"] = cur_close - prev_close
#         else:
#             temp_df.loc[temp_df['day'] == i + 1, "Down_Change"] = prev_close - cur_close
#             temp_df.loc[temp_df['day'] == i + 1, "Up_Change"] =  0
#     res = pd.concat([res, temp_df])

# df = res

# res = pd.DataFrame(columns=df.columns)
# for ticker in config.TICKERS:
#     temp_df = df.loc[df["Symbol"] == ticker].copy()
#     temp_df = temp_df.sort_values(by="day")
#     temp_df["RSI"] = 100 - 100 / (1 + temp_df["Up_Change"].rolling(14).mean() / (temp_df["Down_Change"].rolling(14).mean() + 1e-6))
#     res = pd.concat([res, temp_df])



# schema = (StructType()
#             .add(StructField("Symbol", StringType()))
#             .add(StructField("Open", StringType()))
#             .add(StructField("High", StringType()))
#             .add(StructField("Low", StringType()))
#             .add(StructField("Close", StringType()))
#             .add(StructField("Volume", StringType()))
#             .add(StructField("Value", StringType()))
#             .add(StructField("day", StringType()))
#             .add(StructField("MA20", StringType()))
#             .add(StructField("MA50", StringType()))
#             .add(StructField("EMA12", StringType()))
#             .add(StructField("EMA26", StringType()))
#             .add(StructField("MACD", StringType()))
#             .add(StructField("SIGNAL_LINE", StringType()))
#             .add(StructField("Up_Change", StringType()))
#             .add(StructField("Down_Change", StringType()))
#             .add(StructField("RSI", StringType()))
#             .add(StructField("PARTITION_DATE", StringType()))    
#         )
# spark_df = spark.createDataFrame(res, schema=schema)
# spark_df.show()
# spark_df.write.mode('overwrite').partitionBy('PARTITION_DATE').parquet("src/ingestion/stream_processor/past_data_2")
# spark_df.show()

# ------------------------------ cast to double --------------------
# df = spark.read.parquet("src/ingestion/stream_processor/past_data_2")
# # df.filter(col("Symbol") == 'FPT').select("day",'MA20', 'MA50', 'MACD', 'EMA12', 'EMA26', 'Close').orderBy("day").show()
# cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Value', 'MA20', 'MA50', 'MACD', 'EMA12', 'EMA26', 'SIGNAL_LINE', 'Up_Change', 'Down_Change', 'RSI']
# for c in cols:
#     df = df.withColumn(c, col(c).cast('double'))
# df = df.withColumn('day', col('day').cast('int'))
# df.printSchema()
# df.show()
# df.write.mode('overwrite').partitionBy('PARTITION_DATE').parquet("src/ingestion/stream_processor/past_data")


#----------------------- write to influx ----------------------------
df = spark.read.parquet("src/ingestion/stream_processor/past_data")
df.printSchema()
df = df.toPandas()

# print(df.columns)
client = InfluxDBClient(url="http://127.0.0.1:8086", token=config.influx_token, org=config.influx_org)
write_api = client.write_api(write_options=SYNCHRONOUS)
points = []

for ind, row in df.iterrows():
    (symbol, open, high, low, close, volume, value, _, ma20, ma50, ema12, ema26, macd, signal_line, up_change, down_change, rsi, date) = row
    time = int(datetime.strptime(str(date),'%Y%m%d').timestamp()) * 1000000000
    # data = f"market_data,ticker={symbol} Open={open},High={high},Low={low},Close={close},Volume={volume},Value={value},\
    #         MA20={ma20},MA50={ma50},EMA12={ema12},EMA26={ema26},MACD={macd} {time*1000000}"
    p = Point("stock_info").tag("ticker", symbol) \
            .field("open", open) \
            .field("high", high) \
            .field("low", low) \
            .field("close", close) \
            .field("volume", volume) \
            .field("value", value) \
            .field("MA20", ma20) \
            .field("MA50", ma50) \
            .field("EMA12", ema12) \
            .field("EMA26", ema26) \
            .field("MACD", macd) \
            .field("SIGNAL_LINE", signal_line) \
            .field("Up_change", up_change) \
            .field("Down_change", down_change) \
            .field("RSI", rsi) \
            .time(time)
    points.append(p)
    if len(points) == 5000:
        write_api.write(config.influx_bucket, config.influx_org, points)
        points = []
        print("Writen...." + str(p.to_line_protocol()))

write_api.write(config.influx_bucket, config.influx_org, points)