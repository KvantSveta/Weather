import unittest2 as unittest

from weather import Weather
from logger import Logger


__author__ = "Evgeny Goncharov"


class TestWeather(unittest.TestCase):
    def test_good_connect(self):
        log = Logger(file_name='test_weather.log')
        w = Weather(log)
        self.assertTrue(w.flag)
        self.assertTrue(w.get_weather)

    def test_bad_connect(self):
        log = Logger(file_name='test_weather.log')
        w = Weather(log, page='https:/10.0.0.1/')
        self.assertFalse(w.flag)
        with self.assertRaises(AttributeError):
            log.logger.info(w.get_weather)


if __name__ == '__main__':
    unittest.main()
