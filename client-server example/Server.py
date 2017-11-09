import socket, time, os
from threading import *
from alarmcodes import *
from gpiozero import Button, LED


shutdownButton = Button(24)
resetButton = Button(17)
leds = []

def shutdown():
    while True:
        inputState = shutdownButton.is_pressed
        if not inputState:
            print('System will shut down in 2 seconds')
            for t in threads:
                print('1')
                #t.join()
                print('2')
                t.shutdownclient()
                print('3')
            time.sleep(2)
            serversocket.close()
            turnoffallleds()
            os._exit(0)

def turnoffallleds():
    for led in leds:
        led.turnoff()

class clientThread(Thread):

    def __init__(self, clientthread, ip):
        Thread.__init__(self)
        self.ct = clientthread
        self.name = self.ct.recv(1).decode()
        self.ip = ip
        print('New server socket thread created for ' + self.ip + ': Sensor ' + self.name)



    def run(self):
        while True:
            time.sleep(1)
            print('1')
            try:
                message = self.ct.recv(2).decode()
            except:
                print('Sensor ' + self.name + ': '+ 'Connection is NOT OK')
                print('Sensor ' + self.name + ': '+ 'Entering triggered state')
                self.setalarmTriggered()
            print('2')
            print(message)
            self.state = message
            print('3')
            if self.state == alarmcodes['ok']:
                turnoffallleds()
                greenLED.turnon()
            elif self.state == alarmcodes['triggered']:
                print('alarm has been triggered')
                turnoffallleds()
                yellowLED.turnon()
                self.setalarmTriggered()
            elif self.state == alarmcodes['alarm']:
                turnoffallleds()
                redLED.turnon()
                print('Sensor ' + self.name + ': ' + 'Connection OK')
            print('4')
            self.ct.send(self.state.encode())



    def setalarmTriggered(self):
        #t = Thread(target=self.timeout)
        #t.start()
        #message = self.ct.recv(2).decode()
        #while inTime:
        #    print('inTime')
        #    print('message is' + message)
        #    if message != alarmcodes['ok']:
        #        self.state = message
        #        print(self.state)
        #        return
        #    elif message == '':
        #        self.ct.join()
        #        return
        #self.state = alarmcodes['alarm']
        #t.join()
        time.sleep(5)
        message = self.ct.recv(2).decode()
        print('message is ' + message)


    def timeout(self):
        global inTime
        inTime = True
        time.sleep(5)
        inTime = False

    def shutdownclient(self):
        self.ct.send(alarmcodes['shutdown'].encode())
        self.join()
        self.ct.close()

class led:
    def __init__(self, color, gpiolocation):
        self.color = color
        self.LED = LED(gpiolocation)
        leds.append(self)

    def turnon(self):
        self.LED.on()

    def turnoff(self):
        self.LED.off()



redLED = led('red', 18)
yellowLED = led('yellow', 23)
greenLED = led('green', 25)


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 12345

serversocket.bind((host, port))


threads = []
t = Thread(target=shutdown)
t.start()

while True:
    greenLED.turnon()
    serversocket.listen(5)

    print('Waiting for connection...')
    (conn, (ip, port)) = serversocket.accept()

    # Create new client thread
    ct = clientThread(conn, ip)

    # Start new client Thread
    ct.start()

    # Add new thread to list of all threads(alarmsystemen)
    threads.append(ct)
