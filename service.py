import time

from weather import Weather
from mongo import Mongo


__author__ = "Evgeny Goncharov"

m = Mongo()

while True:
    # запрос содержит текущую дату
    query = {'date': time.strftime("%d.%m.%y")}

    if not m.read(query):
        print('Записи нет в БД')
        w = Weather()
        document = w.get()
        m.write(document=document)
        print('Документ успешно записан')
    else:
        print('Запись уже существует')

    # делать запрос каждый час
    time.sleep(3600)
