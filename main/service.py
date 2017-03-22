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
m = Mongo(log)


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
            else:
                log.critical("Невозможно получить информацию о погоде")

        # запись уже имеется в БД
        else:
            w = Weather(log)
            # информация о погоде успешно получена
            if w.ok_response:
                q = m.find_one(query, {'_id': 0, 'temperature': 1})
                if q['temperature'] != w.temperature:
                    m.update_one(_filter=query,
                                 update={'temperature': w.temperature})
                    log.info("Документ успешно перезаписан")
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

log.info("Сервис остановлен\n")
