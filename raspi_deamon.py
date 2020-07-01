import os
import serial
import time
import urllib
from time import sleep

baseURL = 'http://api.thingspeak.com/update?api_key=ELO0PS5JA8RX73B5&field1={}&field2={}&field3={}'


def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return float(temp.replace("temp=","").strip()[:-2])


while True:
    while True:
        for i in range(10):
            try:
                ser = serial.Serial('/dev/ttyUSB' + str(i), 9600)
            except Exception as e:
                print(e)
                sleep(1)
            else:
                break

        if ser and ser.is_open:
            break

    while True:
        try:
            for _ in range(20):
                line = ser.readline()
                arduino_temp, volts = line.strip().split()
                volts = float(volts)
                arduino_temp = float(arduino_temp)
                raspi_temp = measure_temp()
                
            print(volts, arduino_temp, raspi_temp)

            s = baseURL.format(volts, arduino_temp, raspi_temp)
            f = urllib.urlopen(s)
            f.read()
            f.close()
        except Exception as e:
            print(e)
            sleep(1)
            break

    sleep(10)
