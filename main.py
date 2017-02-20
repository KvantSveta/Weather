import time
import RPi.GPIO as GPIO
import threading
from subprocess import check_output

from flask import Flask, render_template

from mongo import Mongo
from logger import Logger

__author__ = "Evgeny Goncharov"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

app = Flask(__name__, static_url_path="")

log = Logger("web.log")
m = Mongo(log)

RED = 19
GREEN = 26
BLUE = 13

GPIO.setup(RED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GREEN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BLUE, GPIO.OUT, initial=GPIO.LOW)


def decorator(func):
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper


@decorator
def led_shine(colour, time_shine):
    GPIO.output(colour, GPIO.HIGH)
    time.sleep(time_shine)
    GPIO.output(colour, GPIO.LOW)


@app.route("/", methods=["GET"])
def temperature():
    led_shine(GREEN, 3)

    temp = check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"])
    temp = temp.decode()
    temp = str(round(int(temp) / 1000, 1)) + "'C"
    current_time = str(time.strftime("%H:%M:%S - %d.%m.%y"))

    return render_template(
        "temperature.html", temperature=temp, current_time=current_time
    )


@app.route("/weather", methods=["GET"])
def weather():
    led_shine(BLUE, 3)

    query = {"date": time.strftime("%d.%m.%y")}
    current_time = str(time.strftime("%H:%M:%S - %d.%m.%y"))
    weather = m.find_one(query)

    # температура, градус Цельсия
    temperature = weather["temperature"]
    # влажность, %
    humidity = weather["humidity"]
    # давление, мм рт. ст.
    pressure = weather["pressure"]
    # скорость и направление ветра, м/с
    wind = weather["wind"]
    # атмосферные осадки, мм
    precipitation = weather["precipitation"]

    return render_template(
        "weather.html",
        temperature=temperature,
        humidity=humidity,
        pressure=pressure,
        wind=wind,
        precipitation=precipitation,
        current_time=current_time
    )


app.config.from_json("config.json")

app.run(
    host=app.config.get("HOST"),
    port=app.config.get("PORT"),
    debug=app.config.get("DEBUG")
)
