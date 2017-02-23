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

        self._red_frq = GPIO.PWM(self._red_gpio, 50)
        self._red_frq.start(0)
        self._green_frq = GPIO.PWM(self._green_gpio, 50)
        self._green_frq.start(0)
        self._blue_frq = GPIO.PWM(self._blue_gpio, 50)
        self._blue_frq.start(0)

    def change_colour(self, red=0, green=0, blue=0):
        self._red_frq.ChangeDutyCycle(red)
        self._green_frq.ChangeDutyCycle(green)
        self._blue_frq.ChangeDutyCycle(blue)

    def __del__(self):
        self._red_frq.stop()
        self._green_frq.stop()
        self._blue_frq.stop()

        GPIO.cleanup([self._red_gpio, self._green_gpio, self._blue_gpio])
