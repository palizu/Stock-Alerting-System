import ssi_fc_data
import json
import ssi_config as config
from kafka import KafkaProducer
import logging 
import pandas as pd
import time

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class MarketDataProducer():

    def __init__(self, configs=None) -> None:
        if configs is not None:
            producer_configs = configs 
        else:
            producer_configs = {
                'bootstrap_servers': ['localhost:9092'],
                'value_serializer': lambda x: json.dumps(x).encode('utf-8'),
                'key_serializer': str.encode,
                'client_id': 'producer-001'
            }
        self.producer = KafkaProducer(**producer_configs)

    def process_message(self, message):
        print(message)
        data = json.loads(message['Content'])
        if data['Close'] != 0:
            row = {
                'Symbol':data['Symbol'],
                'TradingDate':data['TradingDate'],
                'Time':data['Time'],
                'Open':data['Open'],
                'High':data['High'],
                'Low':data['Low'],
                'Close':data['Close'],
                'Volume':data['TotalVol'],
                'Change':data['Change'],
            }
            if row['Symbol'] not in config.TICKER:
                return
            logging.info("Sending: " + str(row))
            self.producer.send('market_data', value=row, key=row['Symbol'])

    def process_error(self, error):
        print(error)

    def produce_from_api(self):
        token = ssi_fc_data.access_token(config=config)
        config.access_jwt = token['data']['accessToken']
        channel = "X:ALL"
        ssi_fc_data.Market_Data_Stream(config, self.process_message, self.process_error, channel)

    # testing
    def produce_from_file(self, file_path):
        print("here")
        df_data = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                data = json.loads(line)
                row = [data['Symbol'], data['TradingDate'], data['Time'], data['Open'], \
                        data['High'], data['Low'], data['Close'], data['Volume'], data['TotalVol'], data['Change']]
                df_data.append(row)
        
        df = pd.DataFrame(columns=['Symbol', 'TradingDate', 'Time', 'Open', 'High', 'Low', 
                        'Close', 'Volume', 'TotalVol', 'Change'], data=df_data)
        df = df.sort_values('Time')
        print("Start producing")
        for index, row in df.iterrows():
            data_row = {
                'Symbol':row['Symbol'],
                'TradingDate':row['TradingDate'],
                'Time':row['Time'],
                'Open':row['Open'],
                'High':row['High'],
                'Low':row['Low'],
                'Close':row['Close'],
                'Volume':row['TotalVol'],
                'Change':row['Change'],
            }
            logging.info("Sending: " + str(data_row))
            self.producer.send('market_data', value=data_row, key=data_row['Symbol'])
            if index % 100 == 0:
                time.sleep(1)

    def __del__(self):
        self.producer.close()

if __name__ == '__main__':
    producer = MarketDataProducer()
    # producer.produce_from_api()
    producer.produce_from_file('src/ingestion/producer/test_data.json')


