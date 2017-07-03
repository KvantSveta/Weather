import time
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

__author__ = "Evgeny Goncharov"


class Weather():
    def __init__(
            self, log, page="https://www.gismeteo.ru/weather-stavropol-5141/"
    ):
        self._log = log

        self._flag = False

        self._date = time.strftime("%d.%m.%y")

        try:
            response = urlopen(page).read()
            self._flag = True
        except URLError as e:
            self._log.error("Невозможно отправить запрос {}".format(e))
            return
        except Exception as e:
            self._log.error("Неизвестная ошибка {}".format(e))
            return

        soup = BeautifulSoup(response, "lxml")

        self.set_weather(soup)

    def decorator(function):
        def wrapper(self, *args, **kwargs):
            try:
                function(self, *args, **kwargs)
            except Exception as e:
                self._log.error("Ошибка при прассинге html-файла {}".format(e))
                self._flag = False
        return wrapper

    @property
    def ok_response(self):
        return self._flag

    def set_weather(self, soup):
        self.set_temperature(soup)

        self.set_wind(soup)

        self.set_pressure(soup)

        self.set_humidity(soup)

        # self.set_precipitation(soup)

    @decorator
    def set_temperature(self, soup):
        # температура, градус Цельсия
        s = soup.find("div", "templine_inner")

        args = "div", "weather_item js_temp_graph"
        temperature = [
            t["data-value"] for t in s.find_all(*args)
        ]

        self._temperature = [int(i) for i in temperature]

        if not self._temperature:
            self._flag = False

    @decorator
    def set_wind(self, s):
        # скорость и направление ветра, м/с
        wind = [
            w.text for w in s.find_all("div", "widget__row widget__row_table")
        ]

        wind = wind[0]
        wind = wind.split()
        wind = [c.replace('штиль', '0') for c in wind]

        self._wind = [(wind[i], wind[i+1]) for i in range(0, 16, 2)]

        if not self._wind:
            self._flag = False

    @decorator
    def set_pressure(self, soup):
        # давление, мм рт. ст.
        s = soup.find("div", "pressureline")
        args = "div", "weather_item js_pressure_graph"
        self._pressure = [
            int(p["data-value"]) for p in s.find_all(*args)
        ]

        if not self._pressure:
            self._flag = False

    @decorator
    def set_humidity(self, soup):
        # влажность, %
        humidity = [
            h for h in soup.find_all("div", "widget__row widget__row_table")
        ]

        soup = humidity[2]

        self._humidity = [
            h.text for h in soup.find_all("div", "widget__item")
        ]

        if not self._humidity:
            self._flag = False

    @decorator
    def set_precipitation(self, s):
        # атмосферные осадки, мм
        _s = s.find("div", "_line precipitationline js_precipitation clearfix")
        precipitation = [
            r.text.strip() for r in _s.find_all("div", "weather_item")
        ]

        # if precipitation == []
        if not precipitation:
            self._precipitation = [0.0] * 8
        else:
            precipitation = [c.replace("н/д", "0") for c in precipitation]

            precipitation = [c.replace(",", ".") for c in precipitation]

            self._precipitation = list(map(float, precipitation))

    @property
    def date(self):
        return self._date

    @property
    def temperature(self):
        return self._temperature

    @property
    def wind(self):
        return self._wind

    @property
    def pressure(self):
        return self._pressure

    @property
    def humidity(self):
        return self._humidity

    @property
    def precipitation(self):
        return self._precipitation

    @property
    def get_weather(self):
        return {
            "date": self.date,
            "temperature": self.temperature,
            "wind": self.wind,
            "pressure": self.pressure,
            "humidity": self.humidity,
            # "precipitation": self.precipitation
        }


if __name__ == "__main__":
    import subprocess

    try:
        from logger import Logger
    except ImportError:
        from main.logger import Logger

    start = time.time()
    log_file = "main.log"
    log = Logger(log_file)
    w = Weather(log)
    if w.ok_response:
        print(w.get_weather)
        print("Время работы:", round(time.time() - start, 3), "с")
    else:
        print('Error')

    subprocess.call(["rm", log_file])
