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
        intChan = int(chan.value * 100)
        if intChan == 100:
            retVal = 10
        elif intChan < 45 :
            retVal = -1
        elif intChan > 55 :
            retVal = 1
        else :
            retVal = 0

        return retVal


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


def sendAllInput(directions, buttons):
    sendDic = {}
    for direction in directions:
#        print(direction.direction)
        sendDic[direction.direction] = direction.readDirection()
    
    for button in buttons:
#        print(button.collor)
        sendDic[button.collor] = button.pressButton()

    return sendDic

#while True:
#    print(sendAllInput(directions, buttons))
#    sleep(0.5)


#for direction in directions:
#    del direction
