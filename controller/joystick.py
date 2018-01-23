import os
from gpiozero import MCP3008, Button
from time import sleep

directions = []
buttons = []

#Y = MCP3008(0)
#X = MCP3008(1)
#for i in range(10):
#    print('Y value ', Y.value)
#    print('X value ', X.value)
#    sleep(1)

class joyStick:
    def __init__(self, channel, direction):
        self.direction = direction
        self.channel = MCP3008(channel)
        directions.append(self)

    def readDirection(self):
        chan = self.channel
#        print(chan.value)
        return chan.value 

class pushButton:
    def __init__(self, pin, collor):
        self.collor = collor
        self.pin = Button(pin)
        buttons.append(self)

    def pressButton(self):
        button = self.pin
        buttonState = button.is_pressed
        return buttonState

yDir = joyStick(0, 'Y')
xDir = joyStick(1, 'X')
gButton = pushButton(2, 'green')
while True:
    print(gButton.pressButton())
    if gButton.pressButton():
        print('X value ', xDir.readDirection())
    else :   
        print('Y value ', yDir.readDirection())
    sleep(0.1)


for direction in directions:
    del direction
