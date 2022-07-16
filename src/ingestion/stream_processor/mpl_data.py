from os import preadv
from gevent import config
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import *
from pyspark.sql.streaming import *
from pyspark.sql import SparkSession
import time
import pandas as pd
import config

spark = SparkSession.builder.appName("mnpl_data").master("spark://vds-vanhta2:7077").getOrCreate()

df = spark.read.parquet("src/ingestion/stream_processor/past_data")

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

k12 = 2 / 13
k26 = 2 / 27

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


pd_df = df.toPandas()
pd_df['EMA12'] = pd_df['Close']
pd_df['EMA26'] = pd_df['Close']
res = pd.DataFrame(columns=pd_df.columns)

print(pd_df.loc[pd_df['Symbol'] == 'CACB2203']['PARTITION_DATE'].max())

# for ticker in config.TICKERS:
#     temp_df = pd_df.loc[pd_df["Symbol"] == ticker]
#     temp_df.loc[temp_df['day'] == 1, 'MACD'] = 0
#     for i in range(61):
#         print(f"{ticker} -- {i}")
#         prev_ema12 = temp_df.loc[temp_df['day'] == i + 1, 'EMA12'].values[0]
#         prev_ema26 = temp_df.loc[temp_df['day'] == i + 1, 'EMA26'].values[0]
#         close = temp_df.loc[temp_df['day'] == i + 2, 'Close'].values[0]
#         ema12 = close * k12 + prev_ema12 * (1-k12)
#         ema26 = close * k26 + prev_ema26 * (1-k26)
#         temp_df.loc[temp_df['day'] == i + 2, 'EMA12'] = ema12
#         temp_df.loc[temp_df['day'] == i + 2, 'EMA26'] = ema26
#         temp_df.loc[temp_df['day'] == i + 2, 'MACD'] = ema12 - ema26

#     res = pd.concat([res, temp_df])

print(res)

