from ast import Call
import logging
from gevent import config
from telegram import Update
import bot_configs
from telegram.ext import *
import mysql.connector
from mysql.connector import Error


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class InterationBot():
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
        self.application.add_handler(MessageHandler(filters.COMMAND, self.unknown))
        self.application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.echo))

    async def start(self, update: Update, context: CallbackContext.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        logging.info(f"Start command at chat: {chat_id}")
        select_query = "SELECT * from USER where chat_id = %s"
        self.cursor.execute(select_query, (chat_id,))
        rows = self.cursor.fetchone()
        if rows is None:    
            insert_query = "INSERT into USER (chat_id) values (%s)"
            new_user_info = (chat_id,)
            self.cursor.execute(insert_query, new_user_info)
            self.connection.commit()
            logging.info(f"New user added with chat id: {chat_id}")
        await context.bot.send_message(chat_id=chat_id, text=bot_configs.welcome_message)

    async def list_condition(self, update: Update, context: CallbackContext.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        logging.info(f"List condition command at chat: {chat_id}")
        select_query = "SELECT * from USER_ALERT_CONDITION where chat_id = %s"
        self.cursor.execute(select_query, (chat_id,))
        rows = self.cursor.fetchone()
        if rows is None: 
            message = bot_configs.NO_CONDITION_MESSAGE
        else:
            message = "Your alert condition: \n"
            for row in rows:
                print(row)
                symbol = row[1]
                price_lower = row[2]
                price_upper = row[3]
                message = message + "\nsymbol: " + symbol
                if price_upper is not None: 
                    message = message + "\n - Upper threshhold: " + price_upper
                if price_lower is not None: 
                    message = message + "\n - Lower threshhold: " + price_lower
        await context.bot.send_message(chat_id=chat_id, text=message)

    async def add_condition(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


    async def unknown(update: Update, context: CallbackContext.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

    async def echo(self, update: Update, context: CallbackContext.DEFAULT_TYPE):
        print(type(update.effective_chat.id))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


if __name__ == '__main__':
    interation_bot = InterationBot()
    interation_bot.application.run_polling()