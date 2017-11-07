import socket, time
from threading import *
from alarmcodes import *


print(ok, triggered, shutdown)

class clientThread(Thread):

    def __init__(self, clientthread):
        Thread.__init__(self)
        self.ct = clientthread
        self.name = self.ct.recv(1).decode()
        #print('New server socket thread created for ' + ip + ':' + str(port))


    def run(self):
        while True:
            time.sleep(1)

            try:
                message = self.ct.recv(2).decode()
            except:
                print('Sensor ' + self.name + ': '+ 'Connection is NOT OK')
                print('Sensor ' + self.name + ': '+ 'Entering triggered state')
                self.setalarmTriggered()

            self.state = message

            if message == ok:
                print('Sensor ' + self.name + ': ' + 'Connection OK')
                self.ct.send(b'Connection OK')
            elif message == triggered:
                self.setalarmTriggered()



    def setalarmTriggered(self):
        t = threading.Thread(target=timeout)
        t.start()

        while inTime:
            message = self.ct.recv(2).decode()
            if message != ok:
                self.state = message
                return
        self.state = alarm
        t.join()


    def timeout(self):
        global inTime
        inTime = True
        time.sleep(5)
        inTime = False




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

    # Add new thread to list of all threads(alarmsystemen)
    threads.append(ct)