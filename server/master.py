#!/usr/bin/python           # This is server.py file

import socket, sys
import mraa
import json
import threading
import time
from datetime import date, datetime
from sqlite import saveData,saveJsonData,getData
BUFFER_SIZE = 1024

class ClientThread(threading.Thread):
   def __init__(self,ClientIp,connection):
      threading.Thread.__init__(self)
      self.ip = ClientIp
      self.connection = connection
   def run(self):
      print ('thread opened with ip ',self.ip)
      j = 0
      while 1:
         data = self.connection.recv(BUFFER_SIZE)
         print(j)
         j = j + 1
         print(data)
         data = json.loads(data)
         print ("recieved data:",data)
         if data == 'close':
            print('entered')
            break
         #saveData('test.db',date.today(),"mohamedPhone",140,150)
         saveJsonData(data,'test.db')
         print(getData('test.db'))

      print ("Connection Closed")

      self.connection.close()

s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
host = "192.168.1.2"
port = 123                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
i = 1
while i<10: # accept up to 10 connection and close the socket
   i = i+1
   print("try")
   c, addr = s.accept()     # Establish connection with client.
   print ('Got connection from', addr)
   thread  = ClientThread(addr,c)
   thread.start()
   c = 0

s.close()

