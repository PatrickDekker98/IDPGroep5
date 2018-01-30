import socket

serverMACAddress = '3C:A0:67:6D:F5:DE'
#serverMACAddress = '3c:a0:67:6d:f5:de'
port = 15
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
while 1:
    text = input()
    if text == "quit":
        break
    s.send(bytes(text, 'UTF-8'))
s.close()

