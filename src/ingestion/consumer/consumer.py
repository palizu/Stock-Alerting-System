# import imp
import json
from kafka import KafkaConsumer

consumer_configs = {
    'bootstrap_servers':['localhost:9092'],
    'group_id':'market_data_consumers',
    'value_deserializer':lambda x: json.loads(x.decode('utf-8')),
    'auto_offset_reset':'earliest',
    'enable_auto_commit':True
}
consumer = KafkaConsumer(**consumer_configs)
consumer.subscribe('market_data')

if __name__ == '__main__':
    for msg in consumer:
        print(msg)