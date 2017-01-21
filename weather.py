import time
from urllib.request import urlopen
from urllib.error import URLError

from bs4 import BeautifulSoup


__author__ = "Evgeny Goncharov"


class Weather():
    def __init__(
            self, log, page="https://www.gismeteo.ru/weather-stavropol-5141/"
    ):
        self._log = log

        self._flag = False

        try:
            response = urlopen(page).read()
            self._flag = True
        except URLError as e:
            self._log.logger.error("Невозможно отправить запрос (%s)", e)
            return
        except Exception as e:
            self._log.logger.error("Неизвестная ошибка (%s)", e)
            return

        soup = BeautifulSoup(response, "lxml")

        self.set_weather(soup)

    @property
    def ok_response(self):
        return self._flag

    def set_weather(self, soup):
        self.set_date()

        self.set_temperature(soup)

        self.set_wind(soup)

        self.set_pressure(soup)

        self.set_humidity(soup)

        self.set_precipitation(soup)

    def set_date(self):
        self._date = time.strftime("%d.%m.%y")

    def set_temperature(self, soup):
        # температура, градус Цельсия
        s = soup.find("div", "templine_inner")
        self._temperature = [
            t.text for t in s.find_all("span", "js_value val_to_convert")
        ]

    def set_wind(self, s):
        # скорость и направление ветра, м/с
        self._wind = [
            w.text for w in s.find_all("div", "wind_value js_meas_container")
        ]

    def set_pressure(self, soup):
        # давление, мм рт. ст.
        s = soup.find("div", "pressureline")
        self._pressure = [
            p.text for p in s.find_all("span", "js_value val_to_convert")
        ]

    def set_humidity(self, soup):
        # влажность, %
        self._humidity = [
            h.text for h in soup.find_all("div", "humidity_value")
        ]

    def set_precipitation(self, s):
        # атмосферные осадки, мм
        _s = s.find("div", "_line precipitationline js_precipitation clearfix")
        self._precipitation = [
            r.text.strip() for r in _s.find_all("div", "weather_item")
        ]
        if self._precipitation == []:
            self._precipitation = ["0"] * 9

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
            "precipitation": self.precipitation
        }
