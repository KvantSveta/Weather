import logging

from main.led import import_led, Led, GREEN, YELLOW, RED

__author__ = "Evgeny Goncharov"


class Logger():
    def __init__(self, file_name="weather.log"):
        file_handler = logging.FileHandler(file_name, "a")
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(message)s",
            datefmt="%e %b %y %H:%M:%S"
        )
        file_handler.setFormatter(fmt=formatter)
        self.logger = logging.getLogger()
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)

        # только для RPi
        if import_led:
            self._led = Led()

    def info(self, msg, time_shine=3):
        if import_led:
            self._led.led_shine(GREEN, time_shine)

        self.logger.info(msg=msg)

    def error(self, msg, time_shine=600):
        if import_led:
            self._led.led_shine(YELLOW, time_shine)

        self.logger.error(msg=msg)

    def critical(self, msg, time_shine=600):
        if import_led:
            self._led.led_shine(RED, time_shine)

        self.logger.critical(msg=msg)
