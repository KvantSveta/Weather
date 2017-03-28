from pymongo import MongoClient
from pymongo import errors

__author__ = "Evgeny Goncharov"


class Mongo():
    def __init__(self, log, db_name="Weather", collection_name="day",
                 ip_address="localhost", port=27017, server_timeout_ms=1000):
        self._log = log

        self._client = MongoClient(host=ip_address, port=port,
                                   serverSelectionTimeoutMS=server_timeout_ms)

        self._db = self._client[db_name]

        self._collection = self._db[collection_name]

    def decorator(function):
        def wrapper(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)
            except errors.ServerSelectionTimeoutError as e:
                self._log.error("Невозможно подключиться к БД {}".format(e))
            except Exception as e:
                self._log.error("Неизвестная ошибка {}".format(e))
        return wrapper

    @property
    @decorator
    def ping_mongodb(self):
        return bool(self._client.server_info())

    @decorator
    def find(self, query=None, _filter=None):
        return [i for i in self._collection.find(query, _filter)]

    @decorator
    def find_one(self, query=None, _filter=None):
        return self._collection.find_one(query, _filter)

    @decorator
    def find_one_and_replace(self, _filter, replacement):
        self._collection.find_one_and_replace(filter=_filter,
                                              replacement=replacement)

    @decorator
    def insert_one(self, document):
        self._collection.insert_one(document=document)

    @decorator
    def update_one(self, _filter, update):
        self._collection.update_one(filter=_filter,
                                    update={'$set': update})

    @decorator
    def remove(self, spec_or_id):
        self._collection.remove(spec_or_id=spec_or_id)
