import socket, time, threading, os
from alarmcodes import *
from gpiozero import Button

alarmtrigger = Button(17) #button S1
resettrigger = Button(27) #Button S2

def triggerAlarm():
    global state, inTime
    inTime = True
    t = threading.Thread(target=timeout)
    t.start()
    print('Alarm is triggered')
    state = alarmcodes['triggered']
    sock.send(state.encode())
    #print(sock.recv(2).decode())
    while inTime:
        inputState = resettrigger.is_pressed
        if not inputState:
            state = alarmcodes['ok']
            print(state)
            t.join()
            return
    print('not inTime')
    state = alarmcodes['alarm']
    sock.send(state.encode())


def timeout():
    global inTime
    time.sleep(5)
    inTime = False


state = alarmcodes['ok']
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '192.168.1.100'
    port = 12345
    sock.connect((host, port))
    sock.send(b'B')
    print('Connection is stable')
except:
    print('Connection is unstable.')
    print('Please check the server.')
    os._exit(0)

while True:

    time.sleep(1)
    sock.send(state.encode())
    rMessage = sock.recv(2).decode()
    if not alarmtrigger.is_pressed:
        triggerAlarm()
        continue

    if rMessage == alarmcodes['alarm']:
        print('ALARM! ALARM!')
        continue
    elif rMessage == alarmcodes['shutdown']:
        print('System is going down')
        break
    elif rMessage == alarmcodes['ok']:
        print('System is ready')
        continue
    elif rMessage == alarmcodes['triggered']:
        print('alarm is triggered')
        continue
    elif rMessage == alarmcodes['resetalarm']:
        state = alarmcodes['ok']
        continue

    print(rMessage)
    print('Connection is unstable')




sock.close()
