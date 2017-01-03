from weather import Weather
from mongo import Mongo


__author__ = "Evgeny Goncharov"

w = Weather()
document = w.get()

m = Mongo()
m.write(document=document)
