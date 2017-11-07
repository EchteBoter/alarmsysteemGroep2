import socket, time


def reportTriggered():
    errorcode = b'01'
    sock.send(errorcode)




sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '145.89.207.113'
port = 12345

sock.connect((host, port))
sock.send(b'A')

while True:
    sock.send(b'00')
    rMessage = sock.recv(1024).decode()
    print(rMessage)




sock.close()
