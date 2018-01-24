import socket, time, os
from threading import *

def shutdown():
    if False:
        time.sleep(2)
        serversocket.close()
        os._exit(0)



class clientThread(Thread):

    def __init__(self, clientthread, ip):
        Thread.__init__(self)
        self.ct = clientthread
        self.name = self.ct.recv(1).decode()
        self.ip = ip
        print('New server socket thread created for ' + self.ip + ': Sensor ' + self.name)

    def run(self):
        while True:
            time.sleep(0.1)
            self.state = 'OK'
            try:
                message = self.ct.recv(100).decode()
            except:
#                message = self.ct.recv(2).decode()
                message = 'not ok'
                self.ct.send(message.encode())
                print('someting went wrong')

#            self.state = message
            print(message)





serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 12345

serversocket.bind((host, port))

threads = []
t = Thread(target=shutdown)
t.start()
while True:
    serversocket.listen(5)

    print('Waiting for connection... ')
    (conn, (ip, port)) = serversocket.accept()

    ct = clientThread(conn, ip)

    ct.start()

    threads.append(ct)
