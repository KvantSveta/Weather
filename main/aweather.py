import asyncio
import re
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
        self._page = page
        self._flag = False

    async def init(self):
        try:
            response = urlopen(self._page).read()
            self._flag = True
        except URLError as e:
            self._log.error("Невозможно отправить запрос {}".format(e))
            return
        except Exception as e:
            self._log.error("Неизвестная ошибка {}".format(e))
            return

        soup = BeautifulSoup(response, "lxml")

        await self.set_weather(soup)

    @property
    def ok_response(self):
        return self._flag

    async def set_weather(self, soup):
        await self.set_date()

        await self.set_temperature(soup)

        await self.set_wind(soup)

        await self.set_pressure(soup)

        await self.set_humidity(soup)

        await self.set_precipitation(soup)

    async def set_date(self):
        self._date = time.strftime("%d.%m.%y")

    async def set_temperature(self, soup):
        # температура, градус Цельсия
        s = soup.find("div", "templine_inner")

        args = "div", "weather_item js_temp_graph"
        temperature = [
            t["data-value"] for t in s.find_all(*args)
        ]

        self._temperature = [int(i) for i in temperature]

        if not self._temperature:
            self._flag = False

    async def set_wind(self, s):
        # скорость и направление ветра, м/с
        wind = [
            w.text for w in s.find_all("div", "wind_value js_meas_container")
        ]

        wind = [c.replace('штиль', '0') for c in wind]

        r = re.compile("(\d*)(\w*)")

        wind = [r.match(m) for m in wind]
        self._wind = [(int(m.group(1)), m.group(2)) for m in wind]

        if not self._wind:
            self._flag = False

    async def set_pressure(self, soup):
        # давление, мм рт. ст.
        s = soup.find("div", "pressureline")
        args = "div", "weather_item js_pressure_graph"
        self._pressure = [
            int(p["data-value"]) for p in s.find_all(*args)
        ]

        if not self._pressure:
            self._flag = False

    async def set_humidity(self, soup):
        # влажность, %
        self._humidity = [
            int(h.text) for h in soup.find_all("div", "humidity_value")
        ]

        if not self._humidity:
            self._flag = False

    async def set_precipitation(self, s):
        # атмосферные осадки, мм
        _s = s.find("div", "_line precipitationline js_precipitation clearfix")
        precipitation = [
            r.text.strip() for r in _s.find_all("div", "weather_item")
        ]

        if precipitation == []:
            self._precipitation = [0.0] * 9
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
            "precipitation": self.precipitation
        }


if __name__ == "__main__":
    import subprocess

    # import uvloop

    from main.logger import Logger

    start = time.time()
    # раскомментировать если нужен другой event loop (uvloop)
    # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    log_file = "main.log"
    log = Logger(log_file)
    w = Weather(log)
    # loop.set_debug(True)
    loop.run_until_complete(
        w.init()
    )
    loop.close()
    # print(w.get_weather)
    print("Время работы:", round(time.time() - start, 3), "с")

    subprocess.call(["rm", log_file])
