import pandas
from kafka import KafkaConsumer
from time import sleep
from json import loads, dump

consumer = KafkaConsumer("BitcoinData",
                         bootstrap_servers = ["localhost:9092"],
                         value_deserializer = lambda x: loads(x.decode("utf-8")))
for data in consumer:
# for data in consumer:
    with open("IBM-stock-market.json", "a") as file:
        # print(data.value)
        dump(data.value, file)