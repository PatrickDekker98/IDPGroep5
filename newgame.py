#!/usr/bin/env python

import random, os.path

#import basic pygame modules
import pygame
from pygame.locals import *

#game constants
MAX_SHOTS      = 2      #most player bullets onscreen
BOMB_ODDS      = 60    #chances a new bomb will drop
SCREENRECT     = Rect(0, 0, 1024, 1024)
SCORE          = 0
walls = []

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'assets', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

winstyle = 0
# Initialize pygame
pygame.init()

# Set the display mode
winstyle = 0  # |FULLSCREEN
bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
#decorate the game window

#create the background, tile the bgd image
background = pygame.Surface(SCREENRECT.size)
screen.blit(background, (0,0))
pygame.display.flip()

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


# each type of game object gets an init and an
# update function. the update function is called
# once per frame, and it is when each object should
# change it's current position and state. the Player
# object actually gets a "move" function instead of
# update, since it is passed extra information about
# the keyboard
class wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 64, 64)

class player(pygame.sprite.Sprite):
#    speed = 10
    bounce = 24
    gun_offset = -11
    images = []
    def __init__(self, pos, speed=5):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.speed = speed
        self.xDir = 0
        self.yDir = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, xDir, yDir):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if xDir < 0:
#                    self.rect.left = wall.rect.right + 
                    self.rect.left = wall.rect.right
                    return
                if xDir > 0:
                    self.rect.right = wall.rect.left
                    return
                if yDir > 0:
                    self.rect.bottom = wall.rect.top
                    return
                if yDir < 0:
                    self.rect.top = wall.rect.bottom
                    return

        if xDir: 
            self.facing = xDir
            self.rect.move_ip(xDir*self.speed, 0)
            self.rect = self.rect.clamp(SCREENRECT)
            self.xDir = xDir
        if yDir:
            self.rect.move_ip(0, yDir*self.speed)
            self.rect = self.rect.clamp(SCREENRECT)
            self.yDir = yDir
        if xDir > 0:
            self.image = self.images[0]
        elif xDir < 0:
            self.image = self.images[1]
#        self.rect.top = self.origtop - (self.rect.left//self.bounce%2)

    def gunpos(self):
        pos = self.facing*self.gun_offset + self.rect.centerx
        return pos, self.rect.top


class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('white')
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 450)

    def update(self):
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, 0, self.color)



#Load images, assign to sprite classes
#(do this before the classes are used, after screen setup)
img = load_image('slimeIdle.gif')
player.images = [img, pygame.transform.flip(img, 1, 0)]

# Initialize Game Groups
all = pygame.sprite.RenderUpdates()

#assign default groups to each sprite class
player.containers = all
Score.containers = all

#Create Some Starting Values
global score
kills = 0
clock = pygame.time.Clock()

#initialize our starting sprites
#global SCORE
player1 = player((512, 512))
if pygame.font:
    all.add(Score())

level = [
        "WWWWWWWWWWWWWWWW",
        "W              W",
        "W              W",
        "W              W",
        "W              W",
        "W              W",
        "W              W",
        "W              W",
        "W              W",
        "W              W",
        "W              W",
        "W              W",
        "W              W",
        "W              W",
        "W              W",
        "WWWWWWWWWWWWWWWW"
        ]

x = y = 0

for row in level:
    for col in row:
        if col == "W":
            wall((x,y))
        x +=64

    y += 64
    x = 0

while player1.alive():


    #get input
    for event in pygame.event.get():
        if event.type == QUIT or \
            (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
    keystate = pygame.key.get_pressed()
    # clear/erase the last drawn sprites
    all.clear(screen, background)

    #update all the sprites
    all.update()

    xDir = player1.xDir
    yDir = player1.yDir
    for event in pygame.event.get():
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

#                if snake.
#        if .key == pygame.K_UP :
#            yDir = -1
#        if event.key == pygame.K_DOWN :
#            yDir = 1

#        if event.key == pygame.K_LEFT :
#            xDir = -1
#        if event.key == pygame.K_RIGHT :
#            xDir = 1

    xDir = keystate[K_RIGHT] - keystate[K_LEFT]
    yDir = keystate[K_DOWN] - keystate[K_UP]


    #handle player input
#        if keystate
#       direction = keystate[K_RIGHT] - keystate[K_LEFT]
    player1.move(xDir, yDir)
#        firing = keystate[K_SPACE]
#        player1.reloading = firing

        #draw the scene
    dirty = all.draw(screen)
    pygame.display.update(dirty)

    #cap the framerate
    clock.tick(40)

    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)

    pygame.display.flip()

if pygame.mixer:
    pygame.mixer.music.fadeout(1000)
pygame.time.wait(1000)
pygame.quit()



#call the "main" function if running this script
#if __name__ == '__main__': main()

