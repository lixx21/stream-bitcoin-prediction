from operator import ne
import pandas as pd
from kafka import KafkaProducer
from time import sleep
from json import dumps
import json

def readCsvData():
    dataCSV = "./dataset/Bitcoin_USD_(01-05.2024).csv"
    bitcoinData = pd.read_csv(dataCSV) 
    bitcoinData = bitcoinData.dropna()

    #change date type into timestamp
    bitcoinData['Date'] = pd.to_datetime(bitcoinData['Date'], format='%Y-%m-%d')

    newBitcoinData = bitcoinData[['Date','Close']]
    newBitcoinData['Close'] = newBitcoinData['Close'].round(2)

    # Feature engineering
    
    newBitcoinData['Day'] = newBitcoinData['Date'].dt.day
    newBitcoinData['Month'] = newBitcoinData['Date'].dt.month
    newBitcoinData['Year'] = newBitcoinData['Date'].dt.year

    return newBitcoinData.to_dict(orient='records')

def sendData():

    csvData = readCsvData()

    producer = KafkaProducer(bootstrap_servers= ["broker:9092"],
                            value_serializer = lambda x: dumps(x).encode("utf-8"))

    # #sending the data
    for data in csvData:
        finalData =  {
                    'Date': data['Date'].isoformat(),
                    'Day': data['Day'],
                    'Month': data['Month'],
                    'Year': data['Year'],
                    'Price': data['Close']
                }
        producer.send(
                'BitcoinData', 
                finalData
            )
        producer.flush()
        print(finalData)
        sleep(3) #wait for 3 seconds

sendData()