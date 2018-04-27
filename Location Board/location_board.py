import socket, sys
import threading
import time


SEND_TCP_IP = '192.168.1.110' # your ip

SEND_TCP_PORT = 5005

RECV_TCP_IP = '192.168.1.110' # your ip

RECV_TCP_PORT = 5006

BUFFER_SIZE = 1024



class listen_to_port(threading.Thread):

    def __init__(self,thread_name,ip,port_number,buffer_size):
                threading.Thread.__init__(self)
                self.thread_name=thread_name
                self.ip=ip
                self.port_number=port_number
                self.buffer_size=buffer_size

    def run(self):
        print("opening thread: "+self.thread_name)




        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind((self.ip, self.port_number))
		
		
		     s.listen(1)

        while 1:
                conn, addr = s.accept()

                print ('Connection address:', addr)

                while 1:

                        data=conn.recv(self.buffer_size)

                        print ("received data:", data)

                        if data == 'close':
                               break
                        time.sleep(1)


                conn.close()
        s.close()
        s = none



class send_to_port(threading.Thread):

    def __init__(self,thread_name,ip,port_number,buffer_size):
                threading.Thread.__init__(self)
                self.thread_name=thread_name
                self.ip=ip
                self.port_number=port_number
                self.buffer_size=buffer_size

    def run(self):
        print("opening thread: "+self.thread_name)

		


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind((self.ip, self.port_number))

        s.listen(1)

        while 1:
                conn, addr = s.accept()

                print ('Connection address:', addr)

                while 1:
                        conn.send("sound board")
                        print ("Sent data")
                        time.sleep(4);

                conn.close()
        s.close()
        s = none



try:
    thread =listen_to_port("Thread"+str(RECV_TCP_PORT),RECV_TCP_IP,RECV_TCP_PORT,BUFFER_SIZE)
    thread.start()

    thread =send_to_port("Thread"+str(SEND_TCP_PORT),SEND_TCP_IP,SEND_TCP_PORT,BUFFER_SIZE)
    thread.start()
except:
    print("problem in starting thread")

