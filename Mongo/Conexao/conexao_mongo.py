import os
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import quote_plus
from Mongo.comum import ComumMongo


class ConexaoMongoDB:
    load_dotenv(rf'{ComumMongo.PATH_MONGO}/.env_mongo')

    def __init__(self):
        self.__host = os.getenv('MONGO_HOST')
        self.__port = os.getenv('MONGO_PORT')
        self.__user = quote_plus(os.environ['MONGO_USER'])
        self.__password = quote_plus(os.environ['MONGO_PASSWORD'])
        self.__database = os.getenv('MONGO_DB')
        self.__client = MongoClient(
            f"mongodb://{self.__user}:{self.__password}@{self.__host}:{self.__port}/{self.__database}"
            f"?authSource={self.__database}",
            serverSelectionTimeoutMS=5000,
        )
        self.__client.admin.command('ping')

    @property
    def client(self):
        return self.__client
