import subprocess

import unittest2 as unittest

from main.weather import Weather
from main.logger import Logger

__author__ = "Evgeny Goncharov"


class TestWeather(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.weather_log = "test_weather.log"

    def test_good_connect(self):
        w = Weather(Logger(file_name=self.weather_log))

        self.assertTrue(w.ok_response)

        self.assertTrue(w.date)

        self.assertTrue(w.temperature)

        self.assertTrue(w.wind)

        self.assertTrue(w.pressure)

        self.assertTrue(w.humidity)

        self.assertTrue(w.precipitation)

        self.assertTrue(w.get_weather)

    def test_bad_connect(self):
        w = Weather(
            Logger(file_name=self.weather_log),
            page="https:/10.0.0.1/"
        )

        self.assertFalse(w.ok_response)

        with self.assertRaises(AttributeError):
            w.date

        with self.assertRaises(AttributeError):
            w.temperature

        with self.assertRaises(AttributeError):
            w.wind

        with self.assertRaises(AttributeError):
            w.pressure

        with self.assertRaises(AttributeError):
            w.humidity

        with self.assertRaises(AttributeError):
            w.precipitation

        with self.assertRaises(AttributeError):
            w.get_weather

    @classmethod
    def tearDownClass(cls):
        subprocess.call(["rm", cls.weather_log])


if __name__ == "__main__":
    unittest.main()
