import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '145.89.207.113'
port = 12345

sock.connect((host, port))
print(sock.recv(1024).decode())
sock.close()