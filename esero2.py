import threading
import pandas as pd
from lxml import etree as ET
from sense_hat import SenseHat
import time
from gpiozero import MotionSensor
import RPi.GPIO as GPIO

scanning = True
pir_sensor_pin = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_sensor_pin, GPIO.IN)
pir = MotionSensor(pin=14, pull_up=False)
lock = threading.Lock()

def scan_thread():
    global scanning
    scanning_time = 60
    time.sleep(scanning_time)
    with lock:
        scanning = False

def Temperature():
    temp = round(sense.get_temperature(),2)
    temp_value = temp / 2.5 + 16
    #stampaT = "T: " + str(round(temp_value,2))
    #sense.show_message(stampaT,back_colour=[0,100,0])
    time.sleep(.5)
    return temp

def printT(temp):
    stampaT = "T: " + str(round(temp,2))
    sense.show_message(stampaT,back_colour=[0,100,0])
    time.sleep(.5)

def Humidity():
    humidity = round(sense.humidity,2)
    humidity_value = 64 * humidity / 100
    #stampaH = "H:" + str(round(humidity_value,2)) + "%"
    #sense.show_message(stampaH,back_colour=[0,0,100])
    time.sleep(.5)
    return humidity

def printH(humi):
    stampaH = "H:" + str(round(humi,2)) + "%"
    sense.show_message(stampaH,back_colour=[0,0,100])
    time.sleep(.5)


def Pressure():
    pressure = round(sense.pressure)
    pressure_value = pressure / 20
    #stampaP = "P: " + str(round(pressure_value,2))
    #sense.show_message(stampaP,back_colour=[100,0,0])
    time.sleep(.5)
    return pressure

def printP(pressure):
    stampaP = "P: " + str(round(pressure,2))
    sense.show_message(stampaP,back_colour=[100,0,0])
    time.sleep(.5)

def Acceleration():
    speed = 0
    prev_accel = sense.get_accelerometer_raw()
    curr_accel = sense.get_accelerometer_raw()
    delta_accel = {axis: curr_accel[axis] - prev_accel[axis] for axis in ['x', 'y', 'z']}
    prev_accel = curr_accel
    speed += sum(delta_accel.values())
    #stampaA = "V: " + str(round(speed,2))
    #sense.show_message(stampaA,back_colour=[100,0,0])
    time.sleep(0.5)
    return round(speed,2)

def printA(acceleration):
    stampaA = "V: " + str(round(acceleration,2))
    sense.show_message(stampaA,back_colour=[100,0,0])
    time.sleep(0.5)

def addData(temperature,humidity,pressure,acceleration):
    measurement = ET.SubElement(root, 'measurement')
    t = ET.SubElement(measurement, 'temperature')
    t.text = str(temperature)
    h = ET.SubElement(measurement, 'humidity')
    h.text = str(humidity)
    p = ET.SubElement(measurement, 'pressure')
    p.text = str(pressure)
    p = ET.SubElement(measurement, 'acceleration')
    p.text = str(acceleration)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write('data.xml', encoding="utf-8")

def pir_thread():
    while True:
        pir.wait_for_motion()
        with lock:
            if scanning:
                print("Start pir_thread")
                tempe = Temperature()
                print("Temperature: " ,tempe, "°C;")
                printT(tempe)
                humi = Humidity()
                print("Humidity': " ,humi, "%;")
                printH(humi)
                pressu = Pressure()
                print("Pressure: " ,pressu, "hPa;")
                printP(pressu)
                acce = Acceleration()
                print("Acceleration" ,acce, "m/s;")
                printA(acce)
                addData(tempe,humi,pressu,acce)
                print("End pir_thread")
                time.sleep(5)

def tScan_loop():
    global scanning
    while scanning:
        print("Start tScan_loop")
        tempe = Temperature()
        print("Temperature: " ,tempe, "°C;")
        humi = Humidity()
        print("Humidity': " ,humi, "%;")
        pressu = Pressure()
        print("Pressure: " ,pressu, "hPa;")
        acce = Acceleration()
        print("Acceleration" ,acce, "m/s;")
        addData(tempe,humi,pressu,acce)
        print("End tScan_loop")
        time.sleep(10)

if __name__ == "__main__":
    sense = SenseHat()
    root = ET.Element('data')
    tScan = threading.Thread(target=tScan_loop)
    tPir = threading.Thread(target=pir_thread)

    tScan.start()
    tPir.start()

    tScan.join()
    tPir.join() 

    print("Scansione completata. Il programma si ferma.")