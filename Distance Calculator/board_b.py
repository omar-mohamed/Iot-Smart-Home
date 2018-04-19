import socket,json

BUFFER_SIZE = 1024

my_server = socket.socket()         
my_server_ip = "192.168.1.102"
my_server_port = 5002

my_server.bind((my_server_ip,my_server_port))        
my_server.listen(1)  

phone_client,address = my_server.accept()
print('Connected to client (phone):', address)

my_client = socket.socket()
other_board_ip = "192.168.1.101"
other_board_port = 5001

my_client.connect((other_board_ip,other_board_port))

i = 0
while i < 2:
    print('Iteration #',i)
    phone_data = phone_client.recv(BUFFER_SIZE)
    phone_location = json.loads(phone_data)
    board_location = phone_location
    board_location['source'] = 'board'
    
    my_client.send(json.dumps(board_location))
    data = my_client.recv(BUFFER_SIZE)
    data = json.loads(data)
    print('Distance (received from server):',data['distance'])
    i += 1
    
phone_client.close()
my_client.close()
