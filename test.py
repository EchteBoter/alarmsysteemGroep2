from gpiozero import Button
from gpiozero import LED
import time

button = Button(18)
red = LED(17)

#while True:
#    inputState = button.is_pressed 
#    if inputState:
#        print('Button Pressed')
#        time.sleep(0.2)

while True:
    inputState = button.is_pressed
    if inputState: 
        red.on()
        print('Bullshit!')
        time.sleep(1)
        red.off()
