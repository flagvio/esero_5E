import pandas as pd
from lxml import etree as ET
from sense_hat import SenseHat
import time
import RPi.GPIO as GPIO

def Temperature():
    temp = round(sense.get_temperature(),2)
    temp_value = temp / 2.5 + 16
    stampaT = "T: " + str(round(temp_value,2))
    sense.show_message(stampaT,back_colour=[0,100,0])
    time.sleep(.5)
    return temp

def Humidity():
    humidity = round(sense.humidity,2)
    humidity_value = 64 * humidity / 100
    stampaH = "H:" + str(round(humidity_value,2)) + "%"
    sense.show_message(stampaH,back_colour=[0,0,100])
    time.sleep(.5)
    return humidity

def Pressure():
    pressure = round(sense.pressure)
    pressure_value = pressure / 20
    stampaP = "P: " + str(round(pressure_value,2))
    sense.show_message(stampaP,back_colour=[100,0,0])
    time.sleep(.5)
    return pressure

def addData(temperature,humidity,pressure):
    measurement = ET.SubElement(root, 'measurement')
    t = ET.SubElement(measurement, 'temperature')
    t.text = str(temperature)
    h = ET.SubElement(measurement, 'humidity')
    h.text = str(humidity)
    p = ET.SubElement(measurement, 'pressure')
    p.text = str(pressure)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write('data.xml', encoding="utf-8")

if __name__ == "__main__":
    sense = SenseHat()
    root = ET.Element('data')
    while True:
        tempe = Temperature()
        humi = Humidity()
        pressu = Pressure()
        addData(tempe,humi,pressu)
        print("scansione")