from kafka import KafkaConsumer
from time import sleep
from json import loads, dump
import sys
import os
from kafka.admin import KafkaAdminClient, NewTopic

# # Add the parent directory to the system path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from ..connection.connection import mongodb_connection
from connection import mongodb_connection


# def createTopic():
#     admin_client = KafkaAdminClient(bootstrap_servers=["broker:9092"])
#     try:
#         admin_client.create_topics(new_topics=, validate_only=False)
#         print("Topic Created Successfully")
#     except TopicAlreadyExistsError as e:
#         print("Topic Already Exist")
#     except  Exception as e:
#         print(e)

def consumer():

    collection = mongodb_connection("bitcoin_data")

    consumer = KafkaConsumer("BitcoinData",
                            bootstrap_servers = ["broker:9092"],
                            value_deserializer = lambda x: loads(x.decode("utf-8")))

    print("send data from consumer to MongoDB...")
    for data in consumer:
        print(data.value)
    # for data in consumer:
        collection.insert_one(data.value)
        # with open("IBM-stock-market.json", "a") as file:
        #     # print(data.value)
        #     dump(data.value, file)
consumer()