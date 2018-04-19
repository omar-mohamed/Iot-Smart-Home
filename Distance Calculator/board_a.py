import socket,threading,json,time,mraa
from math import sin, cos, sqrt, atan2, radians
BUFFER_SIZE = 1024
phone_location = {}
other_board_location = {}

#######################################################################

def calculate_distance():
   
   R = 6373.0  # approximate radius of earth in km
   lon1  = radians(phone_location['long'])
   lon2  = radians(other_board_location['long'])
   lat1  = radians(phone_location['lat'])
   lat2  = radians(other_board_location['lat'])
   dlon = lon2 - lon1
   dlat = lat2 - lat1
   a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
   c = 2 * atan2(sqrt(a), sqrt(1 - a))
   distance = (R * c)*1000
   print("distance is: ", distance,"M");
   return distance

#######################################################################

def blink_LED(pin):
   LED = mraa.Gpio(pin)
   LED.dir(mraa.DIR_OUT)
   LED.write(1)
   time.sleep(1)
   LED.write(0)
   
#######################################################################

class ClientThread(threading.Thread):
   def __init__(self,clientIP,connection):
      threading.Thread.__init__(self)
      self.ip = clientIP
      self.connection = connection
      
   def run(self):
      global phone_location
      global other_board_location
      print ('Thread opened with IP',self.ip)
      i = 0
      while i < 2:
         data = self.connection.recv(BUFFER_SIZE)
         data = json.loads(data)
         print ('Message from ',self.ip,' : ',data)
         if data['source'] == 'phone':
            while phone_location:
               time.sleep(0.5) # wait until last phone_location is processed
            phone_location = data
         else:
            other_board_location = data
            while not phone_location:
               time.sleep(0.5) # wait until phone_location is received
            distance = calculate_distance()
            phone_location = {} 
            print('Distance:',distance)
            self.connection.send(json.dumps({'distance':distance}))
            if distance <= 5:
               print('LED')
               blink_LED(3)
         i += 1
      print (self.ip,'connection closed')
      self.connection.close()

#######################################################################
      
my_server = socket.socket()         
my_server_ip = "192.168.1.101"
my_server_port = 5001

my_server.bind((my_server_ip,my_server_port))        
my_server.listen(5)  # wait for client connection

i = 0
while i < 2:   # accept up to 2 connections
   i += 1
   client,address = my_server.accept()    # accept connection request from client
   print ('Connected to client:', address)
   print ('Thread #:', i)
   thread  = ClientThread(address,client)
   thread.start()

#######################################################################
