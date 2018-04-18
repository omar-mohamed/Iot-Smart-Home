import socket               # Import socket module
import os
import json
from ctypes import *
lib = cdll.LoadLibrary('./lightsensor.so')
lib.return_string.restype = c_char_p
s = socket.socket()         # Create a socket object
host = "192.168.1.13"    # the ip address of the machine run the server
port = 5003              # Reserve a port for service.

s.connect((host, port))
last_inp=''
i = 0
clientData = {"room_no":1 }
while(1):
    inp = lib.return_string()

    if(inp != last_inp):

        if inp == "0":
            clientData["light"] = 0
        elif inp == "1":
            clientData["light"] = 1

        jsonObj = json.dumps(clientData)
        s.send(jsonObj)

    last_inp = inp
    i += 1

s.close()