import socket

s = socket.socket()
host = '145.89.167.38'
port = 12345
s.bind((host, port))


while True:
    s.listen(500)
    c, addr = s.accept()
    print ('Got connection from',addr)
    c.send('Thank you for connecting')
c.close()