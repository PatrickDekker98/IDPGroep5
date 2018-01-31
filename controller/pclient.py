import socket, time, threading, os, json
from gpiozero import Button
from joystick import *
from LCD import *
initLCD()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    host = '145.89.155.196'
#    host = '172.16.48.248'
    host = '192.168.42.7'
    port = 12345
    sock.connect((host, port))
#    sock.send(b'A')
    print('connection established')
except:
    print('Connection is unstable.')
    print('Please check the server')
    os._exit(0)

sendDict = {}
score0 = '0'
score('0')
number = ['0.', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '1']
while True:
    time.sleep(0.1)
#    dirs = str(directions[0].readDirection()) + "," + str( directions[1].readDirection()) + '\n' 
#    sock.send(dirs.encode())
    allInput = sendAllInput(directions, buttons)

#    lcdString(str(allInput['X']), LCD_LINE_1)
#    lcdString(str(allInput['Y']), LCD_LINE_2)
    if sendDict != allInput:
        sendDict = allInput
        jsonAllInput = json.dumps(allInput)
        sock.send(jsonAllInput.encode())
    else :
        sock.send('.'.encode())

    rMessage = sock.recv(16)
    message = rMessage.decode()
    if message != '.':
        newMessage = message.strip('.')
        if newMessage.isdigit():
            score(newMessage)
            score0 = newMessage
        elif message == 'gameover':
            gameOver(score0)
#            lcdString('score: ', LCD_LINE_2)
    

sock.close()
