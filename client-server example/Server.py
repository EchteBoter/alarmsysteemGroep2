import socket, time
from threading import *
from socketserver import ThreadingMixIn


class clientThread(Thread):

    def __init__(self, clientthread):
        Thread.__init__(self)
        self.ct = clientthread
        self.name = self.ct.recv(1).decode()
        #print('New server socket thread created for ' + ip + ':' + str(port))


    def run(self):
        while True:
            time.sleep(1)
            message = self.ct.recv(2).decode()
            if message == '00':
                print('Sensor ' + self.name + ': '+ 'Connection OK')


    def shutdown(self):
        self.ct.send(b'99')



serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = 12345
serversocket.bind((host, port))

threads = []


while True:
    serversocket.listen(5)

    print('Waiting for connection...')
    (conn, (ip, port)) = serversocket.accept()

    # Create new client thread
    ct = clientThread(conn)

    # Start new client Thread
    ct.start()