# httpbin.org сайт для проверки корректности запросов
# page = 'http://httpbin.org'

import urllib.request

page = "https://www.gismeteo.ru/weather-stavropol-5141/"

response = urllib.request.urlopen(page)
response = response.read()#.decode("utf-8")

from bs4 import BeautifulSoup

soup = BeautifulSoup(response, 'lxml')

minus = chr(8722)

array = [int(s.text.replace(minus, '-')) for s in soup.find_all('span', 'js_value val_to_convert')]

middle = int(len(array) / 2)
# массивы с температурой и давлением за сутки
temperature, pressure = array[:middle], array[middle:]

