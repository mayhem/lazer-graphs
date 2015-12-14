#!/usr/bin/env python

import sys
import serial
from time import sleep

BAUD_RATE = 9600

if len(sys.argv) < 2:
    print "Usage: %s <serial device>" % (sys.argv[0])
    sys.exit(-1)

device = sys.argv[1]

try:
    ser = serial.Serial(device, 
                        BAUD_RATE, 
                        bytesize=serial.EIGHTBITS, 
                        parity=serial.PARITY_NONE, 
                        stopbits=serial.STOPBITS_ONE,
                        timeout=.01)
except serial.serialutil.SerialException as e:
    print "Cannot open serial port: %s" % str(e)
    sys.exit(-1)

while True:
    ser.write("?C1;")

    while True:
        ch = ser.read(1)
        if ch == '\n':
            break

    sleep(1)
