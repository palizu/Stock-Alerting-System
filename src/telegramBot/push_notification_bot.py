from concurrent.futures import thread
import logging
import bot_configs
from telegram import Update, Bot
from telegram.ext import *
import mysql.connector
from mysql.connector import Error
from kafka import KafkaConsumer
import redis
import threading

class PushNotificationBot():
    def __init__(self, consumer_configs=None) -> None:
        try: 
            connection = mysql.connector.connect(
                host=bot_configs.host,
                database=bot_configs.database,
                port=bot_configs.port,
                user=bot_configs.username,
                password=bot_configs.password
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
        self.bot = Bot(bot_configs.TOKEN)
        if consumer_configs is None:
            consumer_configs = {
                "bootstrap_servers" : ["127.0.0.1:9092"],
                "key_deserializer" : lambda x: x.decode("utf-8"),
                "value_deserializer" : lambda x: float(x)
            }
        self.consumer = KafkaConsumer(**consumer_configs)
        self.consumer.subscribe(['price', 'ma20', 'macd'])

    def consume(self):
        while True:
            raw_messages = self.consumer.poll(2000)

            for topic_partition, messages in raw_messages.items():
                if topic_partition.topic == "price":
                    self.process_price_info(messages)

    def process_price_info(self, messages):
        for message in messages:
            ticker = message.key
            cur_price = message.value
            print(f"ticker: {ticker} ---- price: {cur_price}")
            alert_chat_ids_lt = self.r.zrangebyscore(f"alert:{ticker}:lt", cur_price, '+inf')
            self.send_alerts(alert_chat_ids_lt, ticker, cur_price, 0)
            alert_chat_ids_gt = self.r.zrangebyscore(f"alert:{ticker}:gt", 0, cur_price)
            self.send_alerts(alert_chat_ids_gt, ticker, cur_price, 1)

    def send_alerts(self, chat_ids, ticker, threshold, direction):
        if direction == 0:
            msg = bot_configs.LT_MESSAGE
        else:
            msg = bot_configs.GT_MESSAGE
        for chat_id in chat_ids:
            bot.send_message(chat_id=chat_id, message=(msg, (ticker, threshold)))


if __name__ == "__main__":
    bot = PushNotificationBot()
    bot.consume()