__author__ = 'Harald'

import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

while 1:
    ser.write(b'1')
    time.sleep(60)