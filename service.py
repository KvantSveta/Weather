import signal
import time
from threading import Event

from mongo import Mongo
from weather import Weather
from logger import Logger

__author__ = "Evgeny Goncharov"


run_service = Event()
run_service.set()

log = Logger()
m = Mongo(log)


def handler(signum, frame):
    run_service.clear()
    log.info("Сигнал для остановки контейнера (%s)", signum)


signal.signal(signal.SIGTERM, handler)

log.info("Сервис запущен", 1)

while run_service.is_set():
    # запрос содержит текущую дату
    query = {"date": time.strftime("%d.%m.%y")}

    # сервер БД доступен
    if m.ping_mongodb:
        # записи нет в БД
        if not m.find_one(query):
            log.info("Записи нет в БД")
            w = Weather(log)
            # информация о погоде успешно получена
            if w.ok_response:
                m.insert_one(document=w.get_weather)
                log.info("Документ успешно записан")
            else:
                log.critical("Невозможно получить информацию о погоде")
        else:
            log.info("Запись уже существует")
    else:
        log.critical("Сервер с БД недоступен")

    start = time.time()
    # делать запрос каждый час
    try:
        while run_service.is_set() and time.time() - start < 3600:
            time.sleep(1)
    except Exception as e:
        log.critical("Неизвестная ошибка (%s)", e)

log.info("Сервис остановлен\n")
