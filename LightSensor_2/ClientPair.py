import socket
import json
from ctypes import *
lib = cdll.LoadLibrary('./lightSensor.out')
lib.return_string.restype = c_char_p
s = socket.socket()
host = "192.168.43.70"
port = 5013
buffer_size = 1024
s.connect((host, port))
jsonData = {"source":"light", "room_no": 1, "light": 0}
s.send(json.dumps(jsonData))
data = s.recv(buffer_size)
print data

if data == 'start':
        while 1:
                jsonData["light"] = int(lib.return_string())
                print jsonData
                s.send(json.dumps(jsonData))
                data = s.recv(buffer_size)
                print data
                if  data == 'close':
                        break

s.close()
