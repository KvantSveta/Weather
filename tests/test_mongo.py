import subprocess
import time

import unittest2 as unittest

from main.logger import Logger
from main.mongo import Mongo
from main.weather import Weather

__author__ = "Evgeny Goncharov"

mongo_available = Mongo(
    Logger(file_name="test_mongo.log"),
    ip_address="127.0.0.1",
    port=27017
).ping_mongodb


class TestMongo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mongo_log = "test_mongo.log"
        cls.weather_log = "test_weather.log"
        cls.mongo_local = Mongo(Logger(file_name=cls.mongo_log),
                                ip_address="127.0.0.1",
                                port=27017)

        if cls.mongo_local.ping_mongodb:
            w = Weather(Logger(file_name=cls.weather_log))
            if w.ok_response:
                cls.mongo_local.insert_one(document=w.get_weather)

        cls.mongo_host = Mongo(Logger(file_name=cls.mongo_log),
                               ip_address="192.168.1.102",
                               port=27017)

    @unittest.skipUnless(mongo_available, "Mongo DB not available")
    def test_find(self):
        answer = self.mongo_local.find()
        self.assertTrue(answer)

        query = {"date": time.strftime("%d.%m.%y")}
        answer = self.mongo_local.find(query=query)
        self.assertTrue(answer)

        _filter = {"temperature": 1}
        answer = self.mongo_local.find(query=query, _filter=_filter)
        self.assertTrue(answer)

        answer = self.mongo_host.find()
        self.assertFalse(answer)

        answer = self.mongo_host.find(query=query)
        self.assertFalse(answer)

        answer = self.mongo_host.find(query=query, _filter=_filter)
        self.assertFalse(answer)

    @unittest.skipUnless(mongo_available, "Mongo DB not available")
    def test_find_one(self):
        answer = self.mongo_local.find()
        self.assertTrue(answer)

        query = {"date": time.strftime("%d.%m.%y")}
        answer = self.mongo_local.find(query=query)
        self.assertTrue(answer)

        _filter = {"temperature": 1}
        answer = self.mongo_local.find(query=query, _filter=_filter)
        self.assertTrue(answer)

        answer = self.mongo_host.find()
        self.assertFalse(answer)

        answer = self.mongo_host.find(query=query)
        self.assertFalse(answer)

        answer = self.mongo_host.find(query=query, _filter=_filter)
        self.assertFalse(answer)

    @unittest.skipUnless(mongo_available, "Mongo DB not available")
    def test_insert(self):
        count = self.mongo_local._collection_day.count()
        document = {"temp": 123456}
        self.mongo_local.insert_one(document=document)
        new_count = self.mongo_local._collection_day.count()
        self.assertEqual(new_count, count + 1)

        self.mongo_local._collection_day.remove(document)
        new_count = self.mongo_local._collection_day.count()
        self.assertEqual(new_count, count)

        self.mongo_host.insert_one(document=document)
        new_count = self.mongo_local._collection_day.count()
        self.assertEqual(new_count, count)

    @unittest.skipUnless(mongo_available, "Mongo DB not available")
    def test_connect(self):
        self.assertTrue(self.mongo_local.ping_mongodb)

        self.assertFalse(self.mongo_host.ping_mongodb)

    @unittest.skipUnless(mongo_available, "Mongo DB not available")
    def test_update_one(self):
        document = {"temp": 123456}
        self.mongo_local.insert_one(document=document)
        new_document = {"temp": 654321}
        self.mongo_local.update_one(_filter=document, update=new_document)
        document = self.mongo_local.find_one(query=new_document,
                                             _filter={"_id": 0})
        self.assertEqual(document, new_document)

    @unittest.skipUnless(mongo_available, "Mongo DB not available")
    def test_find_one_and_replace(self):
        document = {"temp": 123456}
        self.assertFalse(self.mongo_local.find_one(query=document))
        self.mongo_local.insert_one(document=document)
        self.assertTrue(self.mongo_local.find_one(query=document))
        new_document = {"temp": 654321}
        self.mongo_local.find_one_and_replace(_filter=document,
                                              replacement=new_document)
        self.assertTrue(self.mongo_local.find_one(query=new_document))
        self.assertFalse(self.mongo_local.find_one(query=document))
        self.mongo_local._collection_day.remove(new_document)
        self.assertFalse(self.mongo_local.find_one(query=document))

    @classmethod
    def tearDownClass(cls):
        subprocess.call(["rm", cls.mongo_log])

        if mongo_available:
            subprocess.call(["rm", cls.weather_log])


if __name__ == "__main__":
    unittest.main()
