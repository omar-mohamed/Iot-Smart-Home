import sys,sqlite3,json
from datetime import date, datetime

def createDatabase(databaseName):
     connection = sqlite3.connect(databaseName)
     cursor = connection.cursor()
     sql_command = """
     CREATE TABLE Location ( 
     ID INTEGER PRIMARY KEY, 
     Board_ID VARCHAR(10) NOT NULL,
     Latitude DOUBLE NOT NULL,
     Longitude DOUBLE NOT NULL,  
     Date DATE NOT NULL,
     Time TIME NOT NULL
     );
     """
     try:
            cursor.execute(sql_command)
     except:
            pass    
     connection.commit()
     connection.close()

def saveData(databaseName,date,boardID,longitude,latitude):
     connection = sqlite3.connect(databaseName)
     cursor = connection.cursor()
     format_str = """INSERT INTO Location (Board_ID, Longitude, Latitude, Date, Time)
     VALUES ("{BoardID}", "{Lon}", "{Lat}", "{Date}", time());"""
     sql_command = format_str.format(BoardID=boardID, Lon=longitude, Lat=latitude, Date = date)
     cursor.execute(sql_command)
     connection.commit()
     connection.close()

def saveJsonData(databaseName,locationData):
     connection = sqlite3.connect(databaseName)
     cursor = connection.cursor()
     format_str = """INSERT INTO Location (Board_ID, Longitude, Latitude, Date, Time)
     VALUES ("{BoardID}", "{Lon}", "{Lat}", "{Date}", time());"""
     sql_command = format_str.format(BoardID=locationData['source'], Lon=locationData['long'], Lat=locationData['lat'], Date = date.today())
     cursor.execute(sql_command)
     connection.commit()
     connection.close()

def insert_update(databaseName,data):
     connection = sqlite3.connect(databaseName)
     cursor = connection.cursor()
     locationData = json.loads(data)
     cursor.execute("SELECT * FROM Location WHERE Board_ID = \""+locationData['source']+"\"") 
     result = cursor.fetchone()
     if result == None:
         format_str = """INSERT INTO Location (Board_ID, Longitude, Latitude, Date, Time)
         VALUES ("{BoardID}" , "{Lon}", "{Lat}" , "{Date}", time());"""
     else:
         format_str = """UPDATE Location SET Latitude = "{Lat}", Longitude = "{Lon}", Date = "{Date}", Time = time() WHERE Board_ID = "{BoardID}";"""
     sql_command = format_str.format(BoardID=locationData['source'], Lon=locationData['long'], Lat=locationData['lat'], Date = date.today())   
     cursor.execute(sql_command)
     connection.commit()
     connection.close()
     
def deleteAllData(databaseName):
     connection = sqlite3.connect(databaseName)
     cursor = connection.cursor()
     sql_command = "DELETE FROM Location"
     cursor.execute(sql_command)
     connection.commit()
     connection.close()

def getAllData(databaseName):   # return data as list of dictionary
     connection = sqlite3.connect(databaseName)
     cursor = connection.cursor()
     cursor.execute("SELECT * FROM Location")
     data = [] 
     result = cursor.fetchall()
     if result == None:
        return None
     for r in result:
          obj = {}
          obj["source"] = r[1]
          obj["lat"] = r[2]
          obj["long"] = r[3]
          obj["date"] = r[4]
          data.append(obj)
     #print ("Data = ",data)
     cursor.close()
     connection.close()
     return data

def getMostRecentData(databaseName):   
     connection = sqlite3.connect(databaseName)
     cursor = connection.cursor()
     cursor.execute("SELECT * FROM Location ORDER BY Board_ID ASC, Time DESC")
     data = []
     result = cursor.fetchall()
     if result == None:
        return None
     i = -1
     for r in result:
          obj = {}
          obj["source"] = r[1]
          if i != -1 and obj["source"] == data[i]['source']:
               continue
          obj["lat"] = r[2]
          obj["long"] = r[3]
          data.append(obj)
          i += 1
     cursor.close()
     connection.close()
     return data

def get(databaseName,board_id):
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Location WHERE Board_ID = \""+board_id+"\"") 
    result = cursor.fetchone()
    if result == None:
        return None
    data = {}
    data["source"] = result[1]
    data["lat"] = result[2]
    data["long"] = result[3]
    data["date"] = result[4]
    #print ("Data = ",data)
    cursor.close()
    connection.close()
    return data
