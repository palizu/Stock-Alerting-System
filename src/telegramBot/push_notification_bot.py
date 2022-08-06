from concurrent.futures import thread
import logging
import bot_configs
import telegram
from telegram.ext import *
import mysql.connector
from mysql.connector import Error
from kafka import KafkaConsumer
import redis
import threading
import json
import asyncio
from influxdb import InfluxDBClient
from datetime import datetime, time


class PushNotificationBot():
    def __init__(self, consumer_configs=None) -> None:
        try: 
            connection = mysql.connector.connect(
                host=bot_configs.mysql_host,
                database=bot_configs.mysql_database,
                port=bot_configs.mysql_port,
                user=bot_configs.mysql_username,
                password=bot_configs.mysql_password
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
        self.influx_client = InfluxDBClient(
            host=bot_configs.influx_host, 
            port=bot_configs.influx_port,
            username=bot_configs.influx_username,
            password=bot_configs.influx_password
        )
        self.influx_client.switch_database('stock_info')
        self.bot = telegram.Bot(token=bot_configs.TOKEN)
        if consumer_configs is None:
            consumer_configs = {
                "bootstrap_servers" : ["127.0.0.1:9092"],
                "key_deserializer" : lambda x: x.decode("utf-8"),
                # "value_deserializer" : lambda x: float(x),
                "group_id" : "group-1"
            }
        self.consumer = KafkaConsumer(**consumer_configs)
        self.consumer.subscribe(['price', 'MA50', 'MA20', 'EMA12', 'RSI', 'EMA26', 'MACD'])

    async def consume(self):
        while True:
            raw_messages = self.consumer.poll(2000)

            for topic_partition, messages in raw_messages.items():
                print(messages)
                await self.process_messages(messages, topic_partition.topic)

    async def process_messages(self, messages, topic):
        for message in messages:
            ticker = message.key
            cur = message.value
            prev = self.r.get(f"{topic}:{ticker}")

            if prev is None:
                self.r.set(f"{topic}:{ticker}", cur)
                return

            prev = float(prev)
            alert_chat_ids_lt = self.r.zrangebyscore(f"{topic}:{ticker}:lt", cur, '+inf')
            if len(alert_chat_ids_lt) > 0 and cur < prev:
                await self.send_alerts(alert_chat_ids_lt, ticker, topic, cur, 0)
            alert_chat_ids_gt = self.r.zrangebyscore(f"{topic}:{ticker}:gt", cur, '+inf')
            if len(alert_chat_ids_gt) > 0 and cur > prev:
                await self.send_alerts(alert_chat_ids_gt, ticker, topic, cur, 1)
            
            self.r.set(f"{topic}:{ticker}", cur)


    async def send_alerts(self, chat_ids, ticker, cur_value, indicator, direction):
        if direction == 0:
            msg = bot_configs.LT_MESSAGE
        else:
            msg = bot_configs.GT_MESSAGE
        print(chat_ids)
        for chat_id in chat_ids:
            text_msg = msg.format(ticker, indicator, cur_value)
            await self.bot.send_message(chat_id=chat_id.decode('utf-8'), text=text_msg)

    def __del__(self):
        self.r.quit()

if __name__ == "__main__":
    bot = PushNotificationBot()
    asyncio.run(bot.consume())