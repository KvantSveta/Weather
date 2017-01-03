from urllib.request import urlopen
from bs4 import BeautifulSoup
import time


__author__ = "Evgeny Goncharov"


class Weather():
    def __init__(self):
        page = "https://www.gismeteo.ru/weather-stavropol-5141/"

        response = urlopen(page).read()

        s = BeautifulSoup(response, 'lxml')

        # температура, градус Цельсия
        _s = s.find('div', 'templine_inner')
        self._temperature = [
            t.text for t in _s.find_all('span', 'js_value val_to_convert')
        ]

        # скорость и направление ветра, м/с
        self._wind = [
            w.text for w in s.find_all('div', 'wind_value js_meas_container')
        ]

        # давление, мм рт. ст.
        _s = s.find('div', 'pressureline')
        self._pressure = [
            p.text for p in _s.find_all('span', 'js_value val_to_convert')
        ]

        # влажность, %
        self._humidity = [
            h.text for h in s.find_all('div', 'humidity_value')
        ]

        # атмосферные осадки, мм
        _s = s.find('div', '_line precipitationline js_precipitation clearfix')
        self._precipitation = [
            r.text.strip() for r in _s.find_all('div', 'weather_item')
        ]
        if self._precipitation == []:
            self._precipitation = ['0'] * 9

    def get(self):
        return {
            'date': time.strftime("%d.%m.%y"),
            'temperature': self._temperature,
            'wind': self._wind,
            'pressure': self._pressure,
            'humidity': self._humidity,
            'precipitation': self._precipitation
        }
