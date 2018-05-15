import socket               # Import socket module
import os
import json

from ctypes import *
lib = cdll.LoadLibrary('./LDR_Sensor.so')
lib.get_sensor_reading.restype = c_char_p
s = socket.socket()         # Create a socket object
host = "192.168.1.100"    # the ip address of the machine that you run the serve
port = 5007               # Reserve a port for your service.
ROOM_NO = 1

s.connect((host, port))

state = 0
while 1:
    inp = lib.get_sensor_reading()
    if(inp == "1"):
        state = int(not state)
        dictionary = {'room_no':ROOM_NO,'light':state}
        json_obj = json.dumps(dictionary)
        print("light " + str(state))
        print(json_obj)
        s.send(json_obj)

s.close
