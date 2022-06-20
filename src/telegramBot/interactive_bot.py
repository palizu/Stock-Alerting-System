import logging
import bot_configs
from telegram import Update
from telegram.ext import *
import mysql.connector
from mysql.connector import Error


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
            price_lower = row[2]
            price_upper = row[3]
            message = message + "\nTicker " + symbol.upper() + ":"
            if price_upper is not None: 
                message = message + "\n - Upper threshhold: " + str(price_upper)
            if price_lower is not None: 
                message = message + "\n - Lower threshhold: " + str(price_lower)
            logging.info(f"List condition at chat id {chat_id}: Success")
        await context.bot.send_message(chat_id=chat_id, text=message)


    async def add_condition(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        args = context.args

        if len(args) != 3:
            message = "Invalid command arguments!\nThe syntax is: /add \{ticker\} \{upper/lower\} \{threshold\}"
            await context.bot.send_message(chat_id=chat_id, text=message)
            return

        ticker = args[0].upper()
        type = args[1].upper()
        threshold = float(args[2])

        if ticker.upper() not in bot_configs.SYMBOL_LIST:
            message = bot_configs.UNSUPPORTED_TICKER_MSG + ticker
            logging.info(f"User update condition failed at chat id {chat_id} -- REASON -- Ticker is not supported: {ticker}")
        elif type not in bot_configs.TYPE_LIST:
            message = bot_configs.UNSUPPORTED_CONDITION_MSG + type
            logging.info(f"User update condition failed at chat id {chat_id} -- REASON -- Wrong condition rule: {type}")
        elif threshold < 0:
            message = bot_configs.NEGATIVE_THRESHOLD_MSG
            logging.info(f"User update condition failed at chat id {chat_id} -- REASON -- Negative threshold")
        else:
            select_query = "SELECT * FROM user_alert_condition WHERE chat_id = %s and ticker = %s"
            self.cursor.execute(select_query, (chat_id, ticker))
            row = self.cursor.fetchone()
            if row is None:
                insert_query = f"INSERT INTO user_alert_condition (chat_id, ticker, {type}) values (%s, %s, %s)"
                self.cursor.execute(insert_query, (chat_id, ticker, threshold))
                self.connection.commit()
            else:
                update_query = f"UPDATE user_alert_condition set {type} = %s where chat_id = %s and ticker = %s"
                self.cursor.execute(update_query, (threshold, chat_id, ticker))
                self.connection.commit()
            message = "Alert added successfully! Use /list to see all your alert"
            logging.info(f"User updated condition at chat id {chat_id}: {' '.join(args)} -- Success")
        await context.bot.send_message(chat_id=chat_id, text=message)


    async def remove_condition(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        args = context.args
        if len(args) != 2:
            message = "Invalid command arguments!\nThe syntax is: /remove \{ticker\} \{price_upper/price_lower\} "
            await context.bot.send_message(chat_id=chat_id, text=message)
            return

        ticker = args[0].upper()
        type = args[1].upper()

        if ticker.upper() not in bot_configs.SYMBOL_LIST:
            message = bot_configs.UNSUPPORTED_TICKER_MSG + ticker
            logging.info(f"User remove condition failed at chat id {chat_id} -- REASON -- Ticker is not supported: {ticker}")
        elif type not in bot_configs.TYPE_LIST:
            message = bot_configs.UNSUPPORTED_CONDITION_MSG + type
            logging.info(f"User remove condition failed at chat id {chat_id} -- REASON -- Wrong condition rule: {type}")
        else:
            select_query = "SELECT * FROM user_alert_condition WHERE chat_id = %s AND ticker = %s"
            self.cursor.execute(select_query, (chat_id, ticker))
            row = self.cursor.fetchone()
            if row is None:
                message = (bot_configs.NO_CONDITION_OM_TICKER_MESSAGE, (ticker,))
                logging.info(f"User remove condition at chat id {chat_id} -- No condition on ticker")
            else:
                update_query = f"UPDATE user_alert_condition SET {type} = NULL WHERE chat_id = %s and ticker = %s"
                self.cursor.execute(update_query, (chat_id, ticker))
                self.connection.commit()
                message = "Alert removed successfully! Use /list to see all your alert"
                logging.info(f"User remove condition at chat id {chat_id}: {' '.join(args)} -- Success")
        await context.bot.send_message(chat_id=chat_id, text=message)


    async def unknown(self, update: Update, context: CallbackContext.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    interation_bot = InteractiveBot()
    interation_bot.application.run_polling()