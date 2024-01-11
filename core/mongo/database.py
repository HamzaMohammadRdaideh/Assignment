from pymongo import MongoClient

from core.mongo.config import settings

client = MongoClient(settings.MONGO_URL)
db = client[settings.MONGO_DB_NAME]
