import socket,threading,json,time,webbrowser
from math import radians,sin,cos,atan2,sqrt
import MapMaker
import sqliteDB

BUFFER_SIZE = 1024
DB_NAME = "Board_Location.db"
TOTAL_BOARDS = 3
PHONE_BOARDS = 2
ITERATIONS = 1000/10
HOME_LOCATION = ()
START = False
CLOSE = False
color_dict = {0:"red",1:"orange",2:"yellow",3:"green",4:"blue",5:"indigo",6:"violet",7:"pink",8:"purple"}

#######################################################################

def calculate_distance(loc1,loc2):
   R = 6373.0  # approximate radius of Earth in km
   lat1  = radians(loc1[0])
   long1  = radians(loc1[1])
   lat2  = radians(loc2[0])
   long2  = radians(loc2[1])
   dlong = long2 - long1
   dlat = lat2 - lat1
   a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
   c = 2 * atan2(sqrt(a),sqrt(1 - a))
   distance = R * c * 1000
   return distance

#######################################################################
   
class ClientThread(threading.Thread):
   def __init__(self,clientIP,connection):
      threading.Thread.__init__(self)
      self.ip = clientIP
      self.connection = connection
      
   def run(self):
      global START,CLOSE
      #print('Thread opened with IP',self.ip)
      i = 0
      while i < ITERATIONS:
         data = self.connection.recv(BUFFER_SIZE)
         data = data.split("}") # more than 1 json object
         data = data[len(data)-2] + "}"
         try:
            data = json.loads(data)
            print ('Message from ',self.ip,' ----- ',data)
            if data['source'] == 'temp' or data['source'] == 'light' or data['source'] == 'sound' or data['source'] == 'motion' or data['source'] == 'smoke':
               if not START:
                  while not START:
                     time.sleep(1)
                  self.connection.send('start')
                  #print(data)
               else:
                  time.sleep(2)
                  if CLOSE or i == ITERATIONS-1:
                     self.connection.send('close')
                     break
                  else:
                     self.connection.send('continue')
            else: # source = phone
               my_id = int(data['source'].split('_')[1])
               if my_id == 0: # home location
                  print(data)
                  global HOME_LOCATION
                  HOME_LOCATION = (data['lat'],data['long'])
                  MapMaker.initialize_map(HOME_LOCATION[0],HOME_LOCATION[1],20,color_dict[0],PHONE_BOARDS)
                  webbrowser.open("map.html")
                  break
               else:
                  sqliteDB.saveJsonData(DB_NAME,data)
                  # Calculate distance between home location and me
                  distance = calculate_distance((data['lat'],data['long']),HOME_LOCATION)
                  print('Distance from ',data['source'],'to home = ',distance)
                  self.connection.send(json.dumps({'distance':distance}))
                  if distance <= 10.0 and not START: # Turn on devices
                     START = True
                     print("Start devices -----")
                  if distance >= 10.0 and START: # Turn off devides
                     CLOSE = True
                     print("Close devices -----")
                  time.sleep(2)
         except:
            print("JSON ERROR!")
            self.connection.send('error')
         i += 1
      print (self.ip,' ----- connection closed')
      self.connection.close()

#######################################################################

sqliteDB.createDatabase(DB_NAME)

my_server = socket.socket()         
my_server_ip = "192.168.1.102"
my_server_port = 5009

my_server.bind((my_server_ip,my_server_port))        
my_server.listen(9)  # wait for client connection

i = 0
while i < TOTAL_BOARDS:  
   client,address = my_server.accept()    # accept connection request from client
   print('Thread # ',i,' ----- connected to client:', address)
   thread  = ClientThread(address,client)
   thread.start()
   i += 1

my_server.close()

#######################################################################
