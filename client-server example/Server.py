import socket

s = socket.socket()
port = 12345
s.bind(("localhost", port))

def client_thread(clientsocket):
    c.send(b'send')
    c.close()

while True:
    s.listen(5)
    c, addr = s.accept()
    ct = client_thread(c)
    ct.run()
    print('Got connection from', addr)
    c.send(b'test')