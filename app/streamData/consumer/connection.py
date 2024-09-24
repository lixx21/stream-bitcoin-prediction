import pymongo

def mongodb_connection(collection):
    client = pymongo.MongoClient("mongodb://admin:admin@mongodb:27017/")
    db = client["crypto_data"]
    collection = db["bitcoin_price"]

    return collection