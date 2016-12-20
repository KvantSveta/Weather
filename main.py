__author__ = "Evgeny Goncharov"

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

app.run(host="192.168.1.102", port=5000, debug=True)
