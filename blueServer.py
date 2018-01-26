import socket

hostMacAddress = '3C:A0:67:6D:F5:DE'
port = 65432
backlog = 1
sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.bind((hostMacAddress, port))
sock.listen(backlog)

try:
    client, address = sock.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data)

except:
    print("Closing socket")
    client.close()
    sock.close()
