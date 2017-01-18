import time

from weather import Weather
from mongo import Mongo
from logger import Logger


__author__ = "Evgeny Goncharov"

log = Logger()
m = Mongo(log)

log.logger.info('Сервис запущен')

while True:
    # запрос содержит текущую дату
    query = {'date': time.strftime("%d.%m.%y")}

    # сервер БД доступен
    if m.ping_mongodb:
        # записи нет в БД
        if not m.find_one(query):
            log.logger.info('Записи нет в БД')
            w = Weather(log)
            # информация о погоде успешно получена
            if w.ok_response:
                m.insert_one(document=w.get_weather)
                log.logger.info('Документ успешно записан')
            else:
                log.logger.critical('Невозможно получить информацию о погоде')
        else:
            log.logger.info('Запись уже существует')
    else:
        log.logger.critical('Сервер с БД недоступен')

    try:
        # делать запрос каждый час
        time.sleep(3600)
    except:
        break

log.logger.info('Сервис остановлен\n')
