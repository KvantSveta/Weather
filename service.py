import time
import signal
from threading import Event

from weather import Weather
from mongo import Mongo
from logger import Logger


__author__ = "Evgeny Goncharov"


run_service = Event()
run_service.set()

log = Logger()
m = Mongo(log)


def handler(signum, frame):
    run_service.clear()
    log.logger.info("Сигнал для остановки контейнера (%s)", signum)


signal.signal(signal.SIGTERM, handler)

log.logger.info("Сервис запущен")

while run_service.is_set():
    # запрос содержит текущую дату
    query = {"date": time.strftime("%d.%m.%y")}

    # сервер БД доступен
    if m.ping_mongodb:
        # записи нет в БД
        if not m.find_one(query):
            log.logger.info("Записи нет в БД")
            w = Weather(log)
            # информация о погоде успешно получена
            if w.ok_response:
                m.insert_one(document=w.get_weather)
                log.logger.info("Документ успешно записан")
            else:
                log.logger.critical("Невозможно получить информацию о погоде")
        else:
            log.logger.info("Запись уже существует")
    else:
        log.logger.critical("Сервер с БД недоступен")

    start = time.time()
    # делать запрос каждый час
    while run_service.is_set() and time.time() - start < 3600:
        time.sleep(1)

log.logger.info("Сервис остановлен\n")
