__author__ = "Evgeny Goncharov"

from urllib.request import urlopen
from bs4 import BeautifulSoup

page = "https://www.gismeteo.ru/weather-stavropol-5141/"

response = urlopen(page).read() #.decode("utf-8")

soup = BeautifulSoup(response, 'lxml')
# выбор всех значений о погоде
# [s.text for s in soup.find_all('div', 'weather_item')]

# температура, градус Цельсия
temperature = [s.text for s in soup.find_all('div', 'weather_item js_temp_graph')]
# скорость и направление ветра, м/с
wind = [s.text for s in soup.find_all('div', 'wind_value js_meas_container')]
# давление, мм рт.ст.
pressure = [s.text for s in soup.find_all('div', 'weather_item js_pressure_graph')]
# влажность, %
humidity = [s.text for s in soup.find_all('div', 'humidity_value')]
# осадки, мм
rainfall = [s.text.strip() for s in soup.find_all('div', 'weather_item')][-9:]
