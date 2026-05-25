from pymongo import MongoClient

client = MongoClient("mongodb://mongodb:27017")
mongo_db = client["my_mongo_db"]

def get_mongo():
    return mongo_db
