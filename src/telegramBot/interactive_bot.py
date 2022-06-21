from bdb import effective
from distutils.debug import DEBUG
import logging
import bot_configs
from telegram import Update
from telegram.ext import *
import mysql.connector
from mysql.connector import Error
import redis


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class InteractiveBot():
    def __init__(self) -> None:
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

        self.application = ApplicationBuilder().token(bot_configs.TOKEN).build()
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('list', self.list_condition))
        self.application.add_handler(CommandHandler('add', self.add_condition))
        self.application.add_handler(CommandHandler('remove', self.remove_condition))
        self.application.add_handler(MessageHandler(filters.COMMAND, self.unknown))


    async def start(self, update: Update, context: CallbackContext.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        logging.info(f"Start command at chat: {chat_id}")
        select_query = "SELECT * FROM user WHERE chat_id = %s"
        self.cursor.execute(select_query, (chat_id,))
        rows = self.cursor.fetchone()
        
        if rows is None:    
            insert_query = "INSERT INTO user (chat_id) VALUES (%s)"
            new_user_info = (chat_id,)
            self.cursor.execute(insert_query, new_user_info)
            self.connection.commit()
            logging.info(f"New user added with chat id: {chat_id}")
        await context.bot.send_message(chat_id=chat_id, text=bot_configs.WELCOME_MESSAGE)


    async def list_condition(self, update: Update, context: CallbackContext.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        logging.info(f"List condition command at chat: {chat_id}")
        select_query = "SELECT * FROM user_alert_condition WHERE chat_id = %s"
        self.cursor.execute(select_query, (chat_id,))
        row = self.cursor.fetchone()
        
        if row is None: 
            message = bot_configs.NO_CONDITION_MESSAGE
            logging.info(f"List condition at chat id {chat_id}: Did not find any condition")
        else:
            message = "Your alert condition: \n"
            symbol = row[1]
            price = row[2]
            direction = row[3]
            message = message + "\nTicker " + symbol.upper()
            if direction == 0: 
                message = message + " has lower boundary: " + str(price)
            if direction == 1: 
                message = message +  "has upper boundary: " + str(price)
            logging.info(f"List condition at chat id {chat_id}: Success")
        await context.bot.send_message(chat_id=chat_id, text=message)


    async def add_condition(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        args = context.args

        if len(args) != 3:
            message = "Invalid command arguments!\nThe syntax is: /add \{ticker\} \{threshold\} \{direction (0 or 1)\}"
            await context.bot.send_message(chat_id=chat_id, text=message)
            return

        ticker = args[0].upper()
        direction = int(args[2])
        threshold = float(args[1])

        if ticker.upper() not in bot_configs.TICKERS:
            message = bot_configs.UNSUPPORTED_TICKER_MSG + ticker
            logging.info(f"User update condition failed at chat id {chat_id} -- REASON -- Ticker is not supported: {ticker}")
        elif direction not in (0, 1):
            message = bot_configs.UNSUPPORTED_CONDITION_MSG + direction
            logging.info(f"User update condition failed at chat id {chat_id} -- REASON -- Wrong direction: {direction}")
        elif threshold < 0:
            message = bot_configs.NEGATIVE_THRESHOLD_MSG
            logging.info(f"User update condition failed at chat id {chat_id} -- REASON -- Negative threshold")
        else:
            select_query = "SELECT * FROM user_alert_condition WHERE chat_id = %s and ticker = %s and direction = %s"
            self.cursor.execute(select_query, (chat_id, ticker, direction))
            row = self.cursor.fetchone()
            if row is None:
                insert_query = f"INSERT INTO user_alert_condition (chat_id, ticker, price, direction) values (%s, %s, %s, %s)"
                self.cursor.execute(insert_query, (chat_id, ticker, threshold, direction))
                self.connection.commit()
            else:
                update_query = f"UPDATE user_alert_condition set price = %s where chat_id = %s and ticker = %s and direction = %s"
                self.cursor.execute(update_query, (threshold, chat_id, ticker, direction))
                self.connection.commit()
            if row is not None:
                if direction == 1:
                    self.r.zrem(f"alert:{ticker}:gt", chat_id)
                else:
                    self.r.zrem(f"alert:{ticker}:lt", chat_id)
            if direction == 1:
                self.r.zadd(f"alert:{ticker}:gt", {str(chat_id): threshold})
                # self.r.zadd(f"alert:{ticker}:gt", threshold, chat_id)
            else:
                self.r.zadd(f"alert:{ticker}:lt", {str(chat_id): threshold})
                #  self.r.zadd(f"alert:{ticker}:lt", threshold, chat_id)
            message = "Alert added successfully! Use /list to see all your alert"
            logging.info(f"User updated condition at chat id {chat_id}: {' '.join(args)} -- Success")
        await context.bot.send_message(chat_id=chat_id, text=message)


    async def remove_condition(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        args = context.args
        if len(args) != 2:
            message = "Invalid command arguments!\nThe syntax is: /remove \{ticker\} \{direction (0 or 1)\} "
            await context.bot.send_message(chat_id=chat_id, text=message)
            return

        ticker = args[0].upper()
        direction = int(args[2])

        if ticker.upper() not in bot_configs.TICKERS:
            message = bot_configs.UNSUPPORTED_TICKER_MSG + ticker
            logging.info(f"User remove condition failed at chat id {chat_id} -- REASON -- Ticker is not supported: {ticker}")
        elif type not in bot_configs.TYPE_LIST:
            message = bot_configs.UNSUPPORTED_CONDITION_MSG + type
            logging.info(f"User remove condition failed at chat id {chat_id} -- REASON -- Wrong direction: {direction}")
        else:
            select_query = "SELECT * FROM user_alert_condition WHERE chat_id = %s AND ticker = %s and direction = %s"
            self.cursor.execute(select_query, (chat_id, ticker, direction))
            row = self.cursor.fetchone()
            if row is None:
                message = (bot_configs.NO_CONDITION_OM_TICKER_MESSAGE, (ticker,))
                logging.info(f"User remove condition at chat id {chat_id} -- No condition on ticker")
            else:
                delete_query = "DELETE FROM user_alert_condition WHERE WHERE chat_id = %s AND ticker = %s and direction = %s"
                self.cursor.execute(delete_query, (chat_id, ticker, direction))
                self.connection.commit()
                message = "Alert removed successfully! Use /list to see all your alert"
                logging.info(f"User remove condition at chat id {chat_id}: {' '.join(args)} -- Success")
            if direction == 1:
                self.r.zrem(f"alert:{ticker}:gt", chat_id)
            else:
                self.r.zrem(f"alert:{ticker}:lt", chat_id)
        await context.bot.send_message(chat_id=chat_id, text=message)

    async def stop(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.chat_id
        logging.info(f"Stop receiving alert from chat: {chat_id}")
        select_query = f"SELECT * FROM user WHERE chat_id = {chat_id}"
        self.cursor.execute(select_query)
        row = self.cursor.fetchone()
        if row is not None:
            delete_user_query = f"DELETE FROM user WHERE chat_id = {chat_id}"
            self.cursor.execute(delete_user_query)
            self.connection.commit()
            delete_condition_query = f"DELETE FROM user_alert_condition WHERE chat_id = {chat_id}"
            self.cursor.execute(delete_condition_query)
            self.connection.commit()
            logging.info("Remove user info from db successfully")
        message = "Bye have a good time"
        await context.bot.send_message(chat_id=chat_id, text=message)

    async def unknown(self, update: Update, context: CallbackContext.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    interation_bot = InteractiveBot()
    interation_bot.application.run_polling()