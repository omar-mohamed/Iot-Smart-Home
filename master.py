#!/usr/bin/python           # This is server.py file

import socket, sys
import mraa
import json
import threading
import time
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
         print('data of light = ',data['light'])
         if 'temp' in data:
                 led = mraa.Gpio(5)
                 led.dir(mraa.DIR_OUT)
                 if data['temp'] == 1:
                         led.write(1)
                 else:
                         led.write(0)
         if 'sound' in data:
                 led = mraa.Gpio(6)
                 led.dir(mraa.DIR_OUT)
                 if data['sound'] == 1:
                         led.write(1)
                 else:
                         led.write(0)
         if 'light' in data:
                 led = mraa.Gpio(7)
                 led.dir(mraa.DIR_OUT)
                 if data['light'] == 1:
                         led.write(1)
                 else:
                         led.write(0)
         if 'motion' in data:
                 led = mraa.Gpio(4)
                 led.dir(mraa.DIR_OUT)
                 if data['motion'] == 1:
                         led.write(1)
                 else:
                         led.write(0)
         if 'smoke' in data:
                 led = mraa.Gpio(3)
                 led.dir(mraa.DIR_OUT)
                 if data['smoke'] == 1:
                         led.write(1)
                 else:
                         led.write(0)



      print ("Connection Closed")

      self.connection.close()

s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
host = "169.254.210.71"
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

