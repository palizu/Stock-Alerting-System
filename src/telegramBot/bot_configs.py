TOKEN = '5386965479:AAFjT0giz4iIoyRIylfAF4Qci9ijjkPCTw8'

# db configs
host = '127.0.0.1'
database = 'StockAlertingSystem'
username = 'root'
password = 'FbpD@2926[]'
port = 3306

SYMBOL_LIST = ['SJF', 'AAA']
TYPE_LIST = ['PRICE_UPPER', 'PRICE_LOWER']
WRONG_RULE_CONDITION_MSG = "Wrong command format!\nTo add an alert, please use this command: /add \{ticker\} \{upper/lower\} \{threshold\}" 
NEGATIVE_THRESHOLD_MSG = "Hmmm... kind of stupid if a threshold is negative right? Please enter a positive threshold"

##
WELCOME_MESSAGE = "Welcome message, to be edited"
NO_CONDITION_MESSAGE = "You did not create any alert"
