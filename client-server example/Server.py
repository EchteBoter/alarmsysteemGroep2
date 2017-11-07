import socket
from threading import Thread
from socketserver import ThreadingMixIn


class clientThread(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print('New server socket thread created for ' + ip + ':' + str(port))


    def run(self):
        print(self.ip)
        print(self.port)


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = 12345
serversocket.bind((host, port))

threads = []


while True:
    serversocket.listen(5)
    print('Waiting for connection...')

    (conn, (ip, port)) = serversocket.accept()
    ct = clientThread(ip,port)
    ct.start()
    threads.append(ct)