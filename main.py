import time
from subprocess import check_output

from flask import Flask, render_template, request

from mongo import Mongo
from logger import Logger
from pwm import Pwm_led, import_package

__author__ = "Evgeny Goncharov"

app = Flask(__name__, static_url_path="")

log = Logger("web.log")
m = Mongo(log)

pwm_led = Pwm_led()


@app.route("/", methods=["GET"])
def temperature():
    log.info("Запрос на получение температуры RPi", 3)

    temp = check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"])
    temp = temp.decode()
    temp = str(round(int(temp) / 1000, 1)) + "'C"
    current_time = str(time.strftime("%H:%M:%S - %d.%m.%y"))

    return render_template(
        "temperature.html", temperature=temp, current_time=current_time
    )


@app.route("/weather", methods=["GET"])
def weather():
    log.info("Запрос на получение информации о погоде", 3)

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


@app.route("/colours", methods=["GET", "POST"])
def colours():
    data = request.json
    if data:
        red = int(data["red"] / 255 * 100)
        green = int(data["green"] / 255 * 100)
        blue = int(data["blue"] / 255 * 100)
        if import_package:
            pwm_led.change_colour(red, green, blue)
    return render_template("colours.html")


app.config.from_json("config.json")

app.run(
    host=app.config.get("HOST"),
    port=app.config.get("PORT"),
    debug=app.config.get("DEBUG")
)
