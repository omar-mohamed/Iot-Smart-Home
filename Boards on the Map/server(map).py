import socket,threading,json,time,webbrowser
from math import radians,sin,cos,atan2,sqrt
from gmplot import gmplot
import sqliteDB

BUFFER_SIZE = 1024
DB_NAME = "Board_Location.db"
TOTAL_BOARDS = 3
ITERATIONS = 60/10
color_dict = {0:"red",1:"orange",2:"yellow",3:"green",4:"blue",5:"indigo",6:"violet",7:"pink",8:"purple"}
locations = [() for i in range(0,TOTAL_BOARDS)]

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
      global locations
      print('Thread opened with IP',self.ip)
      i = 0
      while i < ITERATIONS:
         data = self.connection.recv(BUFFER_SIZE)
         print("data-------      ",data)
         data = data.split("}")
         data = data[len(data)-2] + "}"
         print("new --------     ",data)
         #print(sqliteDB.getAllData(DB_NAME))
         try:
            data2 = data
            data = json.loads(data)
            sqliteDB.saveJsonData(DB_NAME,data2)
            print ('Message from ',self.ip,' : ',data)
            my_id = int(data['source'].split('_')[1])
            locations[my_id] = (data['lat'],data['long'])
            while locations.count(()) > TOTAL_BOARDS-2:
               time.sleep(0.5)
            # Calculate distance between other boards and me
            min_distance = float('Inf')
            nearest = -1
            for j in range(0,TOTAL_BOARDS):
               if j == my_id or locations[j] == ():
                  continue
               tmp_distance = calculate_distance(locations[my_id],locations[j])
               if tmp_distance < min_distance:
                  min_distance = tmp_distance
                  nearest = j
         except:
            print("moshkla...........") #########################################3
            nearest = -1
            min_distance = float('Inf')
         self.connection.send(json.dumps({'nearest':nearest,'distance':min_distance}))
         i += 1
      print (self.ip,'connection closed')
      self.connection.close()

#######################################################################

sqliteDB.createDatabase(DB_NAME)

my_server = socket.socket()         
my_server_ip = "192.168.43.68"
my_server_port = 5011

my_server.bind((my_server_ip,my_server_port))        
my_server.listen(9)  # wait for client connection

i = 0
while i < TOTAL_BOARDS:  
   client,address = my_server.accept()    # accept connection request from client
   print('Connected to client:', address)
   print('Thread #:', i)
   thread  = ClientThread(address,client)
   thread.start()
   i += 1

my_server.close()

while locations.count(()) == TOTAL_BOARDS:
   time.sleep(5)

i = 0
while i < ITERATIONS: # show locations on map every 10 seconds for 1 minute
   print("Iteration # ",i)
   # Place map
   gmap = gmplot.GoogleMapPlotter(30.0312506,31.21046320000005,19) # FCI
   #lats, longs = zip(*[loc for loc in locations if loc != ()])
   #gmap.scatter(lats, longs, 'red', size = 50, marker = False) # scatter points
   for j in range(0,TOTAL_BOARDS):
      if locations[j] != ():
         gmap.marker(locations[j][0],locations[j][1],color = color_dict[j])
   gmap.draw("map"+str(i)+".html") 
   webbrowser.open("map"+str(i)+".html")
   time.sleep(10)
   i += 1

#######################################################################
