import subprocess
import unittest2 as unittest

from weather import Weather
from logger import Logger


__author__ = "Evgeny Goncharov"


class TestWeather(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.file_name = 'test_weather.log'

    def test_good_connect(self):
        w = Weather(Logger(file_name=self.file_name))
        self.assertTrue(w.flag)
        self.assertTrue(w.get_weather)

    def test_bad_connect(self):
        w = Weather(Logger(file_name=self.file_name), page='https:/10.0.0.1/')
        self.assertFalse(w.flag)
        with self.assertRaises(AttributeError):
            w.get_weather

    @classmethod
    def tearDownClass(self):
        subprocess.call(['rm', self.file_name])


if __name__ == '__main__':
    unittest.main()
