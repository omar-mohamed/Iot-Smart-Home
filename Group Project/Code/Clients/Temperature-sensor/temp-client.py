import mraa
import time
import socket
import json 

ROOM_NO=1


HOST='192.168.1.100' #master board IP
PORT=5010

# init socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
except:
    print ("Error with connection")


yellow= mraa.Gpio(12)
red = mraa.Gpio(13)

x = mraa.Aio(0)

#init led
yellow.dir(mraa.DIR_OUT)
red.dir(mraa.DIR_OUT)

yellow.write(0)
red.write(0)



while True:
    
    volt= x.read() * 2.0/ 1023
    temp = volt / 0.01
    
    dic={'room_no':ROOM_NO, 'temp':temp}
    sock.send(json.dumps(dic))

    print ("temp= %.2f C"%(temp))

    if temp >= 26:
        red.write(1)
        yellow.write(0)
    else :
        red.write(0)
        yellow.write(1)


    time.sleep(1)

