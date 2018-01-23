import socket, time, threading, os
from gpiozero import Button

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '192.168.42.3'
    port = 12345
    sock.connect((host, port))
    sock.send(b'A')
except:
    print('Connection is unstable.')
    print('Please check the server')
    os._exit(0)

while True:
    time.sleep(0)
#    rMessage = sock.recv(2).decode()
    

sock.close()
