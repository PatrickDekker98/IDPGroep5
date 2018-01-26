import socket, time, threading, os, json
from gpiozero import Button
from joystick import *

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    host = '145.89.207.150'
#    host = '172.16.48.248'
    host = '192.168.42.7'
    port = 12347
    sock.connect((host, port))
#    sock.send(b'A')
    print('connection established')
except:
    print('Connection is unstable.')
    print('Please check the server')
    os._exit(0)

while True:
    time.sleep(0.1)
    dirs = str(directions[0].readDirection()) + "," + str( directions[1].readDirection()) + '\n' 
    sock.send(dirs.encode())
#    allInput = json.dumps(sendAllInput(directions, buttons))
#    sock.send(allInput.encode())

#    rMessage = sock.recv(6)
#    print(rMessage)
    

sock.close()
