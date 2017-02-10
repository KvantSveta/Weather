import time
from subprocess import check_output

from flask import Flask, render_template

from mongo import Mongo
from logger import Logger

__author__ = "Evgeny Goncharov"

app = Flask(__name__, static_url_path="")

log = Logger("web.log")
m = Mongo(log)


@app.route("/", methods=["GET"])
def temperature():
    temp = check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"])
    temp = temp.decode()
    temp = str(round(int(temp) / 1000, 1)) + "'C"
    current_time = str(time.strftime("%H:%M:%S - %d.%m.%y"))
    return render_template(
        "temperature.html", temperature=temp, current_time=current_time
    )


@app.route("/index", methods=["GET"])
def index():
    query = {"date": time.strftime("%d.%m.%y")}
    current_time = str(time.strftime("%H:%M:%S - %d.%m.%y"))
    return current_time + "<br>" + str(m.find_one(query))


app.run(host="localhost", port=5000, debug=True)
