import socket, time, threading
from alarmcodes import *
from gpiozero import Button

alarmtrigger = Button(17) #button S1
resettrigger = Button(27) #Button S2

def triggerAlarm():
    global state, inTime
    inTime = True
    t = threading.Thread(target=timeout)
    t.start()
    state = alarmcodes['triggered']

    while inTime:
        sock.send(state.encode())
        inputState = resettrigger.is_pressed
        if not inputState:
            state = alarmcodes['ok']
            t.join()
            return
    state = alarmcodes['alarm']


def timeout():
    global inTime
    print('start timer')
    time.sleep(5)
    inTime = False


state = alarmcodes['ok']

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '192.168.1.100'
port = 12345

sock.connect((host, port))
sock.send(b'A')

while True:

    time.sleep(1)
    sock.send(state.encode())
    rMessage = sock.recv(2).decode()
    if not alarmtrigger.is_pressed:
        print('button is pressed')
        triggerAlarm()

    if rMessage == alarmcodes['alarm']:
        alarm = True
        state = alarmcodes['alarm']
    elif rMessage == alarmcodes['shutdown']:
        break
    elif rMessage == alarmcodes['ok']:
        print('Connection is stable')
        continue

    print('Connection is unstable')




sock.close()
