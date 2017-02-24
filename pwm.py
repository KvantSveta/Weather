import time
import threading
try:
    import RPi.GPIO as GPIO
    import_pwm = True
except RuntimeError:
    import_pwm = False

__author__ = "Evgeny Goncharov"


class Pwm_led():
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self._red_gpio = 17
        self._green_gpio = 27
        self._blue_gpio = 22

        GPIO.setup(self._red_gpio, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._green_gpio, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._blue_gpio, GPIO.OUT, initial=GPIO.LOW)

        self._red_pwm = GPIO.PWM(self._red_gpio, 50)
        self._green_pwm = GPIO.PWM(self._green_gpio, 50)
        self._blue_pwm = GPIO.PWM(self._blue_gpio, 50)

    def decorator(func):
        def wrapper(*args, **kwargs):
            threading.Thread(target=func, args=args, kwargs=kwargs).start()

        return wrapper

    @decorator
    def change_colour(self, red=0, green=0, blue=0, time_shine=60):
        self._red_pwm.start(red)
        self._green_pwm.start(green)
        self._blue_pwm.start(blue)

        time.sleep(time_shine)

        self._red_pwm.stop()
        self._green_pwm.stop()
        self._blue_pwm.stop()

    def __del__(self):
        GPIO.cleanup([self._red_gpio, self._green_gpio, self._blue_gpio])
