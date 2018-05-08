
import socket               # Import socket module
import os
import json

from ctypes import *
lib = cdll.LoadLibrary('./sound_sensor.so')
lib.get_sensor_reading.restype = c_char_p
s = socket.socket()         # Create a socket object
host = "192.168.1.100"    # the ip address of the machine that you run the serve
port = 5008               # Reserve a port for your service.
ROOM_NO = 1

s.connect((host, port))
my_data = {"source":"sound","room_no":ROOM_NO,"sound":0}
s.send(json.dumps(my_data))
data = s.recv(buffer_size)
print data
state = 0
if data == 'start':
	while 1:
		inp = lib.get_sensor_reading()
		if(inp == "1"):
			state = int(not state)
			my_data["sound"] = state
			json_obj = json.dumps(my_data)
			print("sound " + str(state))
			print(json_obj)
			s.send(json_obj)
			data = s.recv(buffer_size)
            print("received data: "+ data)
            if  data == 'close':
				break

s.close()
