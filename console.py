import socket, time, os
from threading import *

serversocket = socket.socket(socket.AF_INET, socket,SOCK_STREAM)
host = ''
port = 12345

serversocket.bind((host, port))

threads = []
t = Thread(target=shutdown)

while True:
    serversocket.listen(5)

    print('Waiting for connection... ')
    (conn, (IP, port)) = serversocket.accept()

    ct = clientThread(conn, ip)
