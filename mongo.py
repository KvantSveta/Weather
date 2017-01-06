from pymongo import MongoClient


__author__ = "Evgeny Goncharov"


class Mongo():
    def __init__(self, ip_address='localhost', port=27017, db_name='weather'):
        self._client = MongoClient(host=ip_address, port=port)

        self._db = self._client[db_name]

        self._collection_day = self._db['day']

    def find(self, query=None, _filter=None):
        return [i for i in self._collection_day.find(query, _filter)]

    def find_one(self, query=None, _filter=None):
        return self._collection_day.find_one(query, _filter)

    def insert_one(self, document):
        self._collection_day.insert_one(document=document)
