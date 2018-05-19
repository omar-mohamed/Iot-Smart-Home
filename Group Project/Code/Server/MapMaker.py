import gmplot,webbrowser

MAP_NAME = "map.html"
color_dict = {0:"red",1:"orange",2:"yellow",3:"green",4:"blue",5:"indigo",6:"violet",7:"pink",8:"purple"}
img = "http://maps.google.com/mapfiles/ms/micons/"
move_marker_fn = """function moveMarker(map, marker, latlng) {
			marker.setPosition(latlng);
			//map.panTo(latlng);
	}"""

def define_routes(num):
    routes = "\tvar routes = [\n\t\t"
    for i in range(0,num):
        routes += """\tnew google.maps.Polyline({
                path: [],
                geodesic : true,
                strokeColor: '""" + color_dict[i+1] + """',
                strokeOpacity: 1.0,
                strokeWeight: 2,
                editable: false,
                map:map
            })"""
        if i != num-1:
            routes += ",\n\t\t"
    return routes + "\n\t\t];\n\t"

def define_markers(num):
    markers = "\tvar markers = [\n\t\t"
    for i in range(0,num):
        markers += """\tnew google.maps.Marker({
                title: "no implementation",
                icon: \"""" + img + color_dict[i+1] + """.png\"
            })"""
        if i != num-1:
            markers += ",\n\t\t"             
    return markers + "\n\t\t];\n\t"

def initialize_map(center_lat,center_long,zoom,color,num_markers):
    gmap = gmplot.GoogleMapPlotter(center_lat,center_long,zoom)
    gmap.marker(center_lat,center_long,color = color)
    gmap.draw(MAP_NAME)
    
    map_file = open(MAP_NAME,'r')
    map_data = map_file.read()
    map_file.close()

    i = len(map_data)-1-map_data[::-1].index('}')
    first_part = map_data[0:i] + define_routes(num_markers) + define_markers(num_markers) + """\tfor (i = 0; i < markers.length; i++) markers[i].setMap(map);
		
		update(map,routes,markers);\n\t}\n\t""" + move_marker_fn + "\n\tfunction update(map,routes,markers) {\n\t\t"
    last_part = map_data[i+1:]

    i = first_part.index('script')
    i = first_part.index('script>',i)
    first_part = first_part[0:i] + """script>
<script   src="https://code.jquery.com/jquery-2.2.4.js"   integrity="sha256-iT6Q9iMJYuQiMWNd9lDyBUStIq/8PuOW33aOqmvFpqI="   crossorigin="anonymous"></script>
""" + first_part[i+8:]
    
    i = first_part.index('img')
    first_part = first_part[0:i] + "img = new google.maps.MarkerImage(\"" + img + color_dict[0]+".png\""+ first_part[first_part.index(')',i):]
    print("test")
    first_part += """var latlng;
		$.getJSON("http://193.227.14.15:2017/recent_locations" , function(locations) 
		{
			for (j = 0; j < locations.length; j++){
				//console.log(j)
				latlng = new google.maps.LatLng(locations[j]["lat"], locations[j]["long"]);
				id = parseInt(locations[j]["source"].split('_')[1])-1;
				routes[id].getPath().push(latlng);
				moveMarker(map, markers[id], latlng);
			}
		}).fail(function(){console.log("GET failed");});
		setTimeout(update,2000,map,routes,markers);
	}""" 

    map_file= open(MAP_NAME,'w')
    map_file.write(first_part + last_part)
    map_file.close()
    
    #webbrowser.open(MAP_NAME) #

    
initialize_map(30.0312506,31.21046320000005,15,'red',2)
