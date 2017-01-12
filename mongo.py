from pymongo import MongoClient
from pymongo import errors

__author__ = "Evgeny Goncharov"


class Mongo():
    def __init__(self, log, ip_address='localhost', port=27017):
        self._log = log

        self._client = MongoClient(host=ip_address, port=port)

        self._db = self._client['weather']

        self._collection_day = self._db['day']

    def decorator(function):
        def wrapper(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)
            except errors.ServerSelectionTimeoutError as e:
                self._log.logger.error('Невозможно подключиться к БД (%s)', e)
            except Exception as e:
                self._log.logger.error('Неизвестная ошибка (%s)', e)
        return wrapper

    @decorator
    def find(self, query=None, _filter=None):
        return [i for i in self._collection_day.find(query, _filter)]

    @decorator
    def find_one(self, query=None, _filter=None):
        return self._collection_day.find_one(query, _filter)

    @decorator
    def insert_one(self, document):
        self._collection_day.insert_one(document=document)
