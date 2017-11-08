import socket, time


def reportTriggered():
    errorcode = b'01'
    sock.send(errorcode)




sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '145.89.207.113'
port = 12345

sock.connect((host, port))
sock.send(b'C')

while True:
    sock.send(b'00')git




sock.close()
