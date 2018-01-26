import socket

hostMacAddress = '3C:A0:67:6D:F5:DE'
hostMacAddress = '3C:A0:67:6D:F5:DE'
port = 54321
sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.connect((hostMacAddress, port))

while True:
    text = input('vul text in: ')
    if text == 'guit':
        break
    sock.send(text.encode())
sock.close
