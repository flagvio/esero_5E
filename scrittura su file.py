import pandas as pd
from lxml import etree as ET

def addData(i,temperature,humidity,pressure):
    measurement = ET.SubElement(root, 'measurement')
    measurement.attrib['id'] = str(i)
    t = ET.SubElement(measurement, 'temperature')
    t.text = temperature
    h = ET.SubElement(measurement, 'nome')
    h.text = humidity
    p = ET.SubElement(measurement, 'cognome')
    p.text = pressure
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write('data.xml', encoding="utf-8")

if __name__ == "__main__":
    root = ET.Element('data')
    i = 1
    while i<10:
        temperature = ""
        humidity = ""
        pressure = ""
        temperature = input('Inserisci temperatura: ')
        humidity = input('Inserisci umidita: ')
        pressure = input('Inserisci pressione: ')
        addData(i,temperature,humidity,pressure)
        i = i+1