import socket, time, threading
from alarmcodes import *

def triggerAlarm():
    state = triggered
    t = threading.Thread(target=timeout)
    t.start()
    while True:
        if button == 'pressed' and inTime == True:
            state = ok
            t.join()
            break
        elif inTime == True:
            continue
        elif inTime == False:
            t.join()
            break


def timeout():
    global inTime
    inTime = True
    time.sleep(5)
    inTime = False


state = ok
alarm = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 12345

sock.connect((host, port))
sock.send(b'B')

while True:
    try:
        time.sleep(1)
        sock.send(state.encode())
        rMessage = sock.recv(2).decode()
        if alarm:
            triggerAlarm()

    except:
        print('Connection is unstable')




sock.close()
