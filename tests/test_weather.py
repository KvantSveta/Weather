import subprocess

import unittest2 as unittest

from main.weather import Weather
from main.logger import Logger

__author__ = "Evgeny Goncharov"


class TestWeather(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.weather_log = "test_weather.log"

    def test_good_connect(self):
        w = Weather(Logger(file_name=self.weather_log))
        self.assertTrue(w.ok_response)
        self.assertTrue(w.get_weather)

    def test_bad_connect(self):
        w = Weather(
            Logger(file_name=self.weather_log),
            page="https:/10.0.0.1/"
        )
        self.assertFalse(w.ok_response)
        with self.assertRaises(AttributeError):
            w.get_weather

    @classmethod
    def tearDownClass(self):
        subprocess.call(["rm", self.weather_log])


if __name__ == "__main__":
    unittest.main()
