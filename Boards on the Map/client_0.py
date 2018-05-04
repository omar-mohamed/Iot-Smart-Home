import socket,json,time

BUFFER_SIZE = 1024
BOARD_ID = 0
ITERATIONS = 60/10 # send every 10 seconds for 1 minute

my_server = socket.socket()         
my_ip = "192.168.1.102"
my_port = 5001

server = socket.socket()
server_ip = "192.168.1.102"
server_port = 5002

text = raw_input('start / close: ')

if text == 'start':
    my_server.bind((my_ip,my_port))        
    my_server.listen(1)  

    phone_client,address = my_server.accept()
    my_server.close()
    print('Connected to phone:', address)

    server.connect((server_ip,server_port))

    i = 0
    while i < ITERATIONS: 
        print('Iteration #',i)
        phone_data = phone_client.recv(BUFFER_SIZE)
        phone_location = json.loads(phone_data)
        board_location = phone_location
        #board_location['source'] = BOARD_ID
        
        server.send(json.dumps(board_location))
        data = server.recv(BUFFER_SIZE)
        data = json.loads(data)
        print('Nearest board: ',data['nearest'])
        print('Distance: ',data['distance'])
        i += 1
        time.sleep(10)
        
    phone_client.close()
    server.close()
