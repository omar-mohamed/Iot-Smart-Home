import socket,subprocess,time,json

buffer_size = 1024
server_ip = ""    
port = 5001             
iterations = 5

s = socket.socket() 
s.connect((server_ip, port))

my_data = {"source":"smoke","room_no":1,"smoke":0}
s.send(json.dumps(my_data))
data = s.recv(buffer_size)
print data

if data == 'start':
    fire_alarm_process = subprocess.Popen("./a.out")
    data_file = open("fire_alarm_data.txt",'r')
    while 1:
        data_file.seek(0)
        my_data["smoke"] = int(data_file.read())
        print my_data
        s.send(json.dumps(my_data))
        data = s.recv(buffer_size)
        print data
        if  data == 'close':
            break
        i += 1
    fire_alarm_process.kill()   
    data_file.close()

s.close()
