import socket, time, os
from threading import *
from alarmcodes import *
from gpiozero import Button, LED


shutdownButton = Button(24)
leds = []

def shutdown():
    while True:
        inputState = shutdownButton.is_pressed
        if not inputState:
            print('System will shut down in 2 seconds')
            greenLED.turnoff()
            time.sleep(2)
            serversocket.close()
            time.sleep(1)
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

            try:
                message = self.ct.recv(2).decode()
            except:
                print('Sensor ' + self.name + ': '+ 'Connection is NOT OK')
                print('Sensor ' + self.name + ': '+ 'Entering triggered state')
                self.setalarmTriggered()

            print(message)
            self.state = message

            if self.state == alarmcodes['ok']:
                turnoffallleds()
                greenLED.turnon()
            elif self.state == alarmcodes['triggered']:
                turnoffallleds()
                yellowLED.turnon()
            elif self.state == alarmcodes['alarm']:
                turnoffallleds()
                redLED.turnon()

            self.ct.send(self.state.encode())
            if message == alarmcodes['ok']:
                print('Sensor ' + self.name + ': ' + 'Connection OK')
            elif message == alarmcodes['triggered']:
                self.setalarmTriggered()


    def setalarmTriggered(self):
        t = Thread(target=self.timeout)
        t.start()

        while inTime:
            message = self.ct.recv(2).decode()
            if message != alarmcodes['ok']:
                self.state = message
                return
            elif message == '':
                self.ct.join()
                return
        self.state = alarmcodes['alarm']
        t.join()

    def timeout(self):
        global inTime
        inTime = True
        time.sleep(5)
        inTime = False

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
