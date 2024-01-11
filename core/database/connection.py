from pymongo import MongoClient
from .config import database_settings


class DataBase:
    client: MongoClient = None


db = DataBase()


def connect_to_mongo():
    db.client = MongoClient(database_settings.mongo_url)
    print("Connected to MongoDB")


def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")
