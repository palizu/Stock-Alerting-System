import ssi_fc_data
import json
import ssi_config
from kafka import KafkaProducer


producer_configs = {
    'bootstrap_servers': ['localhost:9092'],
    'value_serializer': lambda x: json.dumps(x).encode('utf-8'),
    'key_serializer': str.encode,
    'client_id': 'producer-001'
}
producer = KafkaProducer(**producer_configs)

def process_message(message):
    data = json.loads(message['Content'])
    symbol = data['Symbol']
    price = data['Close']
    avg_price = data['AvgPrice']
    time = data['Time']
    tot_volume =data['TotalVol']
    row = {
        'symbol':symbol,
        'price':price,
        'avg_price':avg_price,
        'tot_volume':tot_volume,
        'time':time
    }
    print(row)
    producer.send('market_data', value=row, key=row['symbol'])

def process_error(error):
    print(error)

if __name__ == '__main__':
    token = ssi_fc_data.access_token(config=ssi_config)
    ssi_config.access_jwt = token['data']['accessToken']
    channel = "X:ALL"

    ssi_fc_data.Market_Data_Stream(ssi_config, process_message, process_error, channel)
    producer.close()


