import gmplot
import webbrowser, os
import sqlite3
import json
from datetime import date, datetime


databaseName = "test.db"

# Connect to the database
connection = sqlite3.connect(databaseName)

#Set the cursor
cursor = connection.cursor()

# Fetch all the data returned by the database query as a list
cursor.execute("SELECT * FROM location")
lat_long = cursor.fetchall()

# Initialize two empty lists to hold the latitude and longitude values
latitude = []
longitude = [] 

# Transform the the fetched latitude and longitude data into two separate lists
for i in range(len(lat_long)):
	latitude.append(lat_long[i][3])
	longitude.append(lat_long[i][2])



# Initialize the map to the first location in the list
gmap = gmplot.GoogleMapPlotter(latitude[0],longitude[0],20)

# Draw the points on the map. I created my own marker for '#FF66666'. 
# You can use other markers from the available list of markers. 
# Another option is to place your own marker in the folder - 
# /usr/local/lib/python3.5/dist-packages/gmplot/markers/
# gmap.scatter(latitude, longitude, '#FF6666', edge_width=12)
gmap.plot(latitude,longitude,'cornflowerblue', edge_width=10)
# gmap.scatter(latitude, longitude, '#3B0B39', size=10)

for i in range(len(latitude)):
	gmap.marker(latitude[i], longitude[i], 'cornflowerblue')

# Write the map in an HTML file
gmap.draw('map.html')
webbrowser.open("map.html")


# Close the cursor and the database connection 
cursor.close()
connection.close()