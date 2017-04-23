import os
import signal
import time
from datetime import datetime
from threading import Event

try:
    from logger import Logger
    from weather import Weather
    from mongo import Mongo
except ImportError:
    from main.logger import Logger
    from main.weather import Weather
    from main.mongo import Mongo

__author__ = "Evgeny Goncharov"

run_service = Event()
run_service.set()

log = Logger("weather.log")

m = Mongo(
    log, ip_address=os.environ['DB'] if os.environ.get('DB') else "localhost"
)


def handler(signum, frame):
    run_service.clear()
    log.info("Сигнал для остановки контейнера {}".format(signum))


signal.signal(signal.SIGTERM, handler)

log.info("Сервис запущен", 1)

while run_service.is_set():
    # запрос содержит текущую дату
    query = {"date": time.strftime("%d.%m.%y")}

    # сервер БД доступен
    if m.ping_mongodb:
        q = m.find_one(query)
        # записи нет в БД
        if not q:
            log.info("Записи нет в БД")
            w = Weather(log)
            # информация о погоде успешно получена
            if w.ok_response:
                m.insert_one(document=w.get_weather)
                log.info("Документ успешно записан")
                time.sleep(60)
            else:
                log.critical("Невозможно получить информацию о погоде")

        # запись уже имеется в БД
        else:
            w = Weather(log)
            # информация о погоде успешно получена
            if w.ok_response:
                q = m.find_one(query, {'_id': 0})
                if q != w.get_weather:
                    m.find_one_and_replace(_filter=query,
                                           replacement=w.get_weather)
                    log.info("Документ успешно перезаписан")
                    time.sleep(60)
            else:
                log.critical("Невозможно получить информацию о погоде")

    else:
        log.critical("Сервер с БД недоступен")

    # делать запрос каждый час
    try:
        while run_service.is_set() and datetime.now().minute:
            time.sleep(1)
    except Exception as e:
        log.critical("Неизвестная ошибка {}".format(e))
        del e

log.info("Сервис остановлен\n")
