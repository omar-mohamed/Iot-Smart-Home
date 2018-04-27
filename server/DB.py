import sys
import sqlite3
import json
from datetime import date, datetime


def createDatabase(databaseName):
	connection = sqlite3.connect(databaseName)
	cursor = connection.cursor()

	sql_command = """
	CREATE TABLE location ( 
	id INTEGER PRIMARY KEY, 
	board_id VARCHAR(10),
	longitude DOUBLE, 
	latitude DOUBLE, 
	the_date DATE);"""
	try:
		cursor.execute(sql_command)
	except:
		pass	
	connection.commit()
	connection.close()


def saveData(databaseName,date,boardID,longitude,latitude):
	connection = sqlite3.connect(databaseName)
	cursor = connection.cursor()
	format_str = """INSERT INTO location (board_id, longitude, latitude, the_date)
	VALUES (  "{BoardID}" , "{Lon}", "{Lat}" , "{Date}" );"""
	sql_command = format_str.format(BoardID=boardID, Lon=longitude, Lat=latitude, Date = date)
	cursor.execute(sql_command)
	connection.commit()
	connection.close()

def saveJsonData(data,databaseName):
	connection = sqlite3.connect(databaseName)
	cursor = connection.cursor()
	locationData = json.loads(data)
	format_str = """INSERT INTO location (board_id, longitude, latitude, the_date)
	VALUES (  "{BoardID}" , "{Lon}", "{Lat}" , "{Date}" );"""
	sql_command = format_str.format(BoardID=locationData['source'], Lon=locationData['long'], Lat=locationData['lat'], Date = date.today())
	cursor.execute(sql_command)
	connection.commit()
	connection.close()

def deleteAllData(databaseName):
	connection = sqlite3.connect(databaseName)
	cursor = connection.cursor()
	sql_command = "DELETE FROM location"
	cursor.execute(sql_command)
	connection.commit()
	connection.close()


def getData(databaseName):   # return data as list of dictionary
	connection = sqlite3.connect(databaseName)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM location")
	data = [] 
	result = cursor.fetchall() 
	for r in result:
		obj = {"BoardID": "", "Latitude": "", "Longitude":"","Date": ""}
		obj["BoardID"] = r[1]
		obj["Latitude"] = r[3]
		obj["Longitude"] = r[2]
		obj["Date"] = r[4]
		data.append(obj)
	print ("Data = ",data)
	cursor.close()
	connection.close()



#createDatabase("test.db")
#deleteAllData("test.db")
#clientData = {"long":31.30774444444444445, "lat": 33.2544444444444, "source": "Phone1" } #Example 
#jsonObj = json.dumps(clientData)
#saveJsonData(jsonObj,"test.db")
#saveData( "test.db",date.today(),"Phone52",12.2,13.4)
#saveData( "test.db", date.today(),"Phone53",1.2,1.4)
#saveData( "test.db", date.today(),"Phone54",12.222,11.4)
getData("test.db")



