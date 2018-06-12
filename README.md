# Iot-Smart-Home
A smart home implementation using 9 intel Galileo boards.

The system described here is a simple smart home that collects various sensory data through different sensors and microprocessor-based boards installed and spread over several house rooms. Through GPS tracking, our system is also able to calculate how far the owner of the house is. Based on that, it takes the appropriate actions to prepare for the owner's arrival using 9 Galileo boards and various sensors. 


# Architecture

The architecture we used in this project is the client/server architecture. The server is responsible for controlling the start/stopping of the client applications and monitoring them. It also contains the location database which stores the location information of the owner when it is received and contains the service that allows map applications to get the location data available in the database. On the other hand, we have multiple clients; each client application runs on one of the devices mentioned before and communicates with the server.

![iod](https://user-images.githubusercontent.com/6074821/41300403-ed3f2676-6e65-11e8-81d6-918e25f4ef5e.jpg)


# Process Flowchart

As you can see, the clients (including phone clients) connect to the server and when the server receives location data from a phone client, it calculates the distance between the house and the owner‟s location. According to this distance, the server either sends a 'start'/'close' command to the other clients so that their applications can start/stop working. The location data can also be accessed from and shown on a map application that gets that data from the service running on the server.

![iod3](https://user-images.githubusercontent.com/6074821/41300494-2942b2be-6e66-11e8-95b1-5c2676e4e98a.jpg)


# Results

The following figures are screenshots of the results of the map application. The application got the user‟s location data from the database using the api running on the server and showed them on the map. The red marker represents the „home‟ while other markers represent the owners. The lines drawn represent the paths that the user moved along.


![iod4](https://user-images.githubusercontent.com/6074821/41300690-a8f613e8-6e66-11e8-85c3-50b6b31924cd.jpg)


# Additional Info

For more information please check our documentation for the project.
