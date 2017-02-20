import time
import threading
import RPi.GPIO as GPIO

__author__ = "Evgeny Goncharov"

# синий
BLUE = 1
# зеленый
GREEN = 2
# бирюзовый
TURQUOISE = 3
# красный
RED = 4
# пурпурный
PURPLE = 5
# желтый
YELLOW = 6
# белый
WHITE = 7


class Led():
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # синяя составляющая
        self.blue_gpio = 13

        # зеленая составляющая
        self.green_gpio = 26

        # красная составляющая
        self.red_gpio = 19

        GPIO.setup(self.blue_gpio, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.green_gpio, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.red_gpio, GPIO.OUT, initial=GPIO.LOW)

    def decorator(func):
        def wrapper(*args, **kwargs):
            threading.Thread(target=func, args=args, kwargs=kwargs).start()

        return wrapper

    @decorator
    def led_shine(self, colour, time_shine):
        # синяя составляющая
        if colour in (1, 3, 5, 7):
            GPIO.output(self.blue_gpio, GPIO.HIGH)

        # зеленая составляющая
        if colour in (2, 3, 6, 7):
            GPIO.output(self.green_gpio, GPIO.HIGH)

        # красная составляющая
        if colour in (4, 5, 6, 7):
            GPIO.output(self.red_gpio, GPIO.HIGH)

        time.sleep(time_shine)

        GPIO.output(self.blue_gpio, GPIO.LOW)
        GPIO.output(self.green_gpio, GPIO.LOW)
        GPIO.output(self.red_gpio, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()


'''
    R  G  B
(0, 0, 0, 0)
(1, 0, 0, 1)
(2, 0, 1, 0)
(3, 0, 1, 1)
(4, 1, 0, 0)
(5, 1, 0, 1)
(6, 1, 1, 0)
(7, 1, 1, 1)
'''
