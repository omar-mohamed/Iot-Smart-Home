import socket               # Import socket module
import os
import json
from ctypes import *

lib = cdll.LoadLibrary('./lightSensor.so')
lib.get_lightsensor_reading.restype = c_char_p
s = socket.socket()       # Create a socket object
server_ip = ""    # the ip address of the machine run the server
server_port = 5002               # Reserve a port for your service.
ROOM_NO = 1
buffer_size = 1024

s.connect((server_ip, server_port))
lightSensorData = {"source":"light","room_no":ROOM_NO,"light":0}
s.send(json.dumps(my_data))
receivedData = s.recv(buffer_size)

if receivedData == 'start':
	while 1:
		lightSensorData["light"] = int(lib.get_lightsensor_reading())
		json_obj = json.dumps(lightSensorData)
		print(json_obj)
		s.send(json_obj)
		receivedData = s.recv(buffer_size)
        print("received data: "+ receivedData)
        if  receivedData == 'close':
			break

s.close()
