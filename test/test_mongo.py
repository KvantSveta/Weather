import time
import subprocess
import unittest2 as unittest

from mongo import Mongo
from logger import Logger


__author__ = "Evgeny Goncharov"


class TestMongo(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.file_name = 'test_mongo.log'
        self.mongo_local = Mongo(Logger(file_name=self.file_name),
                                 ip_address='127.0.0.1', port=27017)
        self.mongo_host = Mongo(Logger(file_name=self.file_name),
                                ip_address='192.168.1.102', port=27017)

    def test_find(self):
        answer = self.mongo_local.find()
        self.assertTrue(answer)

        query = {'date': time.strftime("%d.%m.%y")}
        answer = self.mongo_local.find(query=query)
        self.assertTrue(answer)

        _filter = {'temperature': 1}
        answer = self.mongo_local.find(query=query, _filter=_filter)
        self.assertTrue(answer)

        answer = self.mongo_host.find()
        self.assertFalse(answer)

        answer = self.mongo_host.find(query=query)
        self.assertFalse(answer)

        answer = self.mongo_host.find(query=query, _filter=_filter)
        self.assertFalse(answer)

    def test_find_one(self):
        answer = self.mongo_local.find()
        self.assertTrue(answer)

        query = {'date': time.strftime("%d.%m.%y")}
        answer = self.mongo_local.find(query=query)
        self.assertTrue(answer)

        _filter = {'temperature': 1}
        answer = self.mongo_local.find(query=query, _filter=_filter)
        self.assertTrue(answer)

        answer = self.mongo_host.find()
        self.assertFalse(answer)

        answer = self.mongo_host.find(query=query)
        self.assertFalse(answer)

        answer = self.mongo_host.find(query=query, _filter=_filter)
        self.assertFalse(answer)

    def test_insert(self):
        count = self.mongo_local._collection_day.count()
        document = {'temp': 123456}
        self.mongo_local.insert_one(document=document)
        new_count = self.mongo_local._collection_day.count()
        self.assertEqual(new_count, count + 1)

        self.mongo_local._collection_day.remove(document)
        new_count = self.mongo_local._collection_day.count()
        self.assertEqual(new_count, count)

        self.mongo_host.insert_one(document=document)
        new_count = self.mongo_local._collection_day.count()
        self.assertEqual(new_count, count)

    def test_connect(self):
        self.assertTrue(self.mongo_local.ping_mongodb)

        self.assertFalse(self.mongo_host.ping_mongodb)

    @classmethod
    def tearDownClass(self):
        subprocess.call(['rm', self.file_name])


if __name__ == '__main__':
    unittest.main()
