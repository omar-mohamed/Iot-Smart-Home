#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import time
import json
import os
from ctypes import *
lib = cdll.LoadLibrary('./example.so')
lib.getLightSensorVal.restype = c_char_p
print(lib.getLightSensorVal())
val = lib.getLightSensorVal();
buffer_size = 1024
s = socket.socket()         # Create a socket object
#host = socket.gethostname() # if you run it on your local machine name
host = "192.168.43.69" # the ip address of the machine that you run the server
port = 5010                # Reserve a port for your service.
s.connect((host, port))
data = s.recv(buffersize)
while 1:
    val = lib.getLightSensorVal();
    data = {"room_no":1}
    data['light'] = 1
    if val < '100':
        data['light'] = 0
    jsondata = json.dumps(data)
    s.send(jsondata)
    time.sleep(3)
    data = s.recv(buffer_size)
    print data
    if  data == 'close':
         break
s.close
