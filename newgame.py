#!/usr/bin/env python

import random, os.path

#import basic pygame modules
import pygame
from pygame.locals import *

#game constants
BACKGROUNDCOLOR = [255, 255, 0]
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
        surfaceBig = pygame.transform.scale(surface, (64, 64)) 
        surfaceBig.set_colorkey((255, 0, 255))
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surfaceBig.convert()

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
screen.fill(BACKGROUNDCOLOR)
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
class wall(pygame.sprite.Sprite):
    images = []
    
    def __init__(self, pos):
        walls.append(self)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
#        self.rect = pygame.Rect(pos[0], pos[1], 64, 64)

class player(pygame.sprite.Sprite):
#    speed = 10
    bounce = 24
    gun_offset = -11
    frontImages = []
    sideXImages = []
    sideYImages = []
    backImages = []
    def __init__(self, pos, speed=5):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.speed = speed
        self.xDir = 0
        self.yDir = 0
        self.curentImages =  self.frontImages
        self.image = self.frontImages[0]
        self.rect = self.image.get_rect(center=pos)
        self.rect.size = (64, 64)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, xDir, yDir):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if xDir < 0:
#                    self.rect.left = wall.rect.right + 
                    self.rect.left = wall.rect.right + 5
                    return
                if xDir > 0:
                    self.rect.right = wall.rect.left - 5
                    return
                if yDir > 0:
                    self.rect.bottom = wall.rect.top - 5
                    return
                if yDir < 0:
                    self.rect.top = wall.rect.bottom + 5
                    return

        if xDir: 
            self.facingX = xDir
            self.rect.move_ip(xDir*self.speed, 0)
            self.rect = self.rect.clamp(SCREENRECT)
            self.xDir = xDir
        if yDir:
            self.facingY = yDir
            self.rect.move_ip(0, yDir*self.speed)
            self.rect = self.rect.clamp(SCREENRECT)
            self.yDir = yDir
        if yDir > 0:
            self.curentImages = self.frontImages
        elif yDir < 0:
            self.curentImages = self.backImages
        if xDir > 0:
            self.curentImages = self.sideYImages
            self.image = self.curentImages[0]
        elif xDir < 0:
            self.curentImages = self.sideXImages
            self.image = self.curentImages[0]
        self.image = self.curentImages[0]

#        self.rect.top = self.origtop - (self.rect.left//self.bounce%2)

    def gunpos(self):
        pos = self.facing*self.gun_offset + self.rect.centerx
        return pos, self.rect.top

class shot(pygame.sprite.Sprite):
    speed = -11
    images = []
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images


class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('white')
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 32)

    def update(self):
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, 0, self.color)



#Load images, assign to sprite classes
#(do this before the classes are used, after screen setup)
img1 = load_image('player1Front1.gif')
img2 = load_image('player1Front2.gif')
player.frontImages = [img1, img2]
img3 = load_image('player1Side1.gif')
img4 = load_image('player1Side2.gif')
player.sideXImages = [img3, img4]
player.sideYImages = [pygame.transform.flip(img3, 1, 0), pygame.transform.flip(img4, 1, 0)]
img5 = load_image('player1Back1.gif')
img6 = load_image('player1Back2.gif')
player.backImages = [img5, img6]
img7 = load_image('floor.gif')
wall.images = [img7]
# Initialize Game Groups
all = pygame.sprite.RenderUpdates()

#assign default groups to each sprite class
player.containers = all
wall.containers = all
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
    screen.fill(BACKGROUNDCOLOR)


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
    clock.tick(60)

#    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)


    pygame.display.flip()

if pygame.mixer:
    pygame.mixer.music.fadeout(1000)
pygame.time.wait(1000)
pygame.quit()



#call the "main" function if running this script
#if __name__ == '__main__': main()

