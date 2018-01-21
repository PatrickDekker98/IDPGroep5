import os
from gpiozero import MCP3008
from time import sleep

directions = []

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

yDir = joyStick(0, 'Y')
xDir = joyStick(1, 'X')
for i in range(10):
#    xDir.readDirection()
#    yDir.readDirection()
    print('X value ', xDir.readDirection())
    print('Y value ', yDir.readDirection())
    sleep(0.5)
