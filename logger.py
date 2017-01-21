import logging


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
