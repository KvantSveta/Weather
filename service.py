import time

from weather import Weather
from mongo import Mongo


__author__ = "Evgeny Goncharov"

w = Weather()
document = w.get()

m = Mongo()

# запрос содержит текущую дату
query = {'date': time.strftime("%d.%m.%y")}

if not m.read(query):
    print('Записи нет в БД')
    m.write(document=document)
    print('Документ успешно записан')
else:
    print('Запись уже существует')
