import socket
import json
from ctypes import *
lib = cdll.LoadLibrary('./sensor.out')
lib.return_string.restype = c_char_p
s = socket.socket()
host = "192.168.1.3"
port = 5003

s.connect((host, port))
jsonData = {"room_no": 1, "motion": 0}
i = 0
while i < 10:

    jsonData["motion"] = int(lib.return_string())
    print jsonData
    s.send(json.dumps(jsonData))
    i+=1
s.send('close')
s.close()