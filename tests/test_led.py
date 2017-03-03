import time
import unittest2 as unittest
from subprocess import check_output

from main.led import Led, BLUE, GREEN, TURQUOISE, RED, PURPLE, YELLOW, WHITE
try:
    import RPi.GPIO as GPIO
    import_gpio = True
except RuntimeError:
    import_gpio = False

__author__ = "Evgeny Goncharov"


class TestLed(unittest.TestCase):
    @classmethod
    @unittest.skipUnless(import_gpio, "Not RPi")
    def setUpClass(cls):
        cls.led = Led()

    @unittest.skipUnless(import_gpio, "Not RPi")
    def test_gpio_type(self):
        self.assertEqual(GPIO.getmode(), GPIO.BCM)

    @unittest.skipUnless(import_gpio, "Not RPi")
    def test_gpio_out(self):
        self.assertEqual(GPIO.gpio_function(self.led.red_gpio), GPIO.OUT)
        self.assertEqual(GPIO.gpio_function(self.led.green_gpio), GPIO.OUT)
        self.assertEqual(GPIO.gpio_function(self.led.blue_gpio), GPIO.OUT)

    @unittest.skipUnless(import_gpio, "Not RPi")
    def test_led_shine(self):
        def convert_bin_dec():
            array = [
                check_output(["gpio", "-g", "read", str(self.led.red_gpio)]),
                check_output(["gpio", "-g", "read", str(self.led.green_gpio)]),
                check_output(["gpio", "-g", "read", str(self.led.blue_gpio)])
            ]
            array = [i.decode() for i in array]
            array = [i.strip() for i in array]

            string = 'ob' + ''.join(array)
            return int(string, base=2)

        time_shine = 3
        time_wait = 0.5

        # синий
        self.led.led_shine(colour=BLUE, time_shine=time_shine)
        time.sleep(time_wait)
        self.assertEqual(BLUE, convert_bin_dec())
        time.sleep(time_shine)

        # зеленый
        self.led.led_shine(colour=GREEN, time_shine=time_shine)
        time.sleep(time_wait)
        self.assertEqual(GREEN, convert_bin_dec())
        time.sleep(time_shine)

        # бирюзовый
        self.led.led_shine(colour=TURQUOISE, time_shine=time_shine)
        time.sleep(time_wait)
        self.assertEqual(TURQUOISE, convert_bin_dec())
        time.sleep(time_shine)

        # красный
        self.led.led_shine(colour=RED, time_shine=time_shine)
        time.sleep(time_wait)
        self.assertEqual(RED, convert_bin_dec())
        time.sleep(time_shine)

        # пурпурный
        self.led.led_shine(colour=PURPLE, time_shine=time_shine)
        time.sleep(time_wait)
        self.assertEqual(PURPLE, convert_bin_dec())
        time.sleep(time_shine)

        # желтый
        self.led.led_shine(colour=YELLOW, time_shine=time_shine)
        time.sleep(time_wait)
        self.assertEqual(YELLOW, convert_bin_dec())
        time.sleep(time_shine)

        # белый
        self.led.led_shine(colour=WHITE, time_shine=time_shine)
        time.sleep(time_wait)
        self.assertEqual(WHITE, convert_bin_dec())
        time.sleep(time_shine)

    @classmethod
    @unittest.skipUnless(import_gpio, "Not RPi")
    def tearDownClass(cls):
        del cls.led


if __name__ == "__main__":
    unittest.main()
