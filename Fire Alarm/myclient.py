import socket,subprocess,time,json

buffer_size = 1024
server_ip = "192.168.1.100"    
port = 5007             

s = socket.socket() 
s.connect((server_ip, port))

start_process = 1 ###################
"""while 1:
    data = s.recv(buffer_size)
    if data == 'start':
        start_process = 1
        break
    elif data == 'close':
        break
"""        
if start_process:
    fire_alarm_process = subprocess.Popen("./a.out")
    data_file = open("fire_alarm_data.txt",'r')
    my_data = {"room_no":1,"smoke":0}
    i = 0
    while i<5:
        data_file.seek(0)
        my_data["smoke"] = int(data_file.read())
        print my_data
        s.send(json.dumps(my_data))
        time.sleep(5)
        i += 1
       #if s.recv(buffer_size) == 'close':
            #break
    fire_alarm_process.kill()   
    data_file.close()

s.close()
