import socket, time, os, sys, pygame, copy, random, json
from threading import *

pygame.init()

width = 500
height = 500
scale = 10
score = 0

food_x = 10
food_y = 10

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

background = (23, 32, 42)
snake_colour = (236, 240, 241)
food_colour = (148, 49, 38)
snake_head = (247, 220, 111)

# ----------- Snake Class ----------------
class Snake:
    def __init__(self, x_start, y_start):
        self.x = x_start
        self.y = y_start
        self.w = 10
        self.h = 10
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x, self.y]]
        self.length = 1

    def reset(self):
        self.x = width/2-scale
        self.y = height/2-scale
        self.w = 10
        self.h = 10
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x, self.y]]
        self.length = 1

    def show(self):
        for i in range(self.length):
            if not i == 0:
                pygame.draw.rect(display, snake_colour, (self.history[i][0], self.history[i][1], self.w, self.h))
            else:
                pygame.draw.rect(display, snake_head, (self.history[i][0], self.history[i][1], self.w, self.h))

    def check_eaten(self):
        if abs(self.history[0][0] - food_x) < scale and abs(self.history[0][1] - food_y) < scale:
            return True

    def grow(self):
        self.length += 1
        self.history.append(self.history[self.length-2])

    def death(self):
        i = self.length - 1
        while i > 0:
            if abs(self.history[0][0] - self.history[i][0]) < self.w and abs(self.history[0][1] - self.history[i][1]) < self.h and self.length > 2:
                return True
            i -= 1

    def update(self):
        i = self.length - 1
        while i > 0:
            self.history[i] = copy.deepcopy(self.history[i-1])
            i -= 1
        self.history[0][0] += self.x_dir*scale
        self.history[0][1] += self.y_dir*scale


def shutdown():
    if False:
        time.sleep(2)
        serversocket.close()
        os._exit(0)

# ----------- Food Class --------------
class Food:
    def new_location(self):
        global food_x, food_y
        food_x = random.randrange(1, width/scale-1)*scale
        food_y = random.randrange(1, height/scale-1)*scale

    def show(self):
        pygame.draw.rect(display, food_colour, (food_x, food_y, scale, scale))


def show_score():
    font = pygame.font.SysFont("Copperplate Gothic Bold", 20)
    text = font.render("Score: " + str(score), True, snake_colour)
    display.blit(text, (scale, scale))



class clientThread(Thread):

    def __init__(self, clientthread, ip):
        Thread.__init__(self)
        self.ct = clientthread
#        self.name = self.ct.recv(1).decode()
        self.ip = ip
#        print('New server socket thread created for ' + self.ip + ': Sensor ' + self.name)
        print('New server socket thread created for ' + self.ip + ': Sensor ')

    def run(self):
        loop = True

        global score

        snake = Snake(width/2, height/2)
        food = Food()
        food.new_location()

# ----------- Main Game Loop -------------

        while True:
            time.sleep(0.1)
            self.state = 'OK'

            try:
                message = self.ct.recv(100).decode()
            except:
                message = 'not ok'
                self.ct.send(message.encode())
                print('someting went wrong')

            print(message)
            
            try: 
                self.state = json.loads(message)
                print(self.state)
            except: 
                self.state = {'X' : 0 ,'Y' : 0}

            if self.state['Y'] == 1:
                snake.x_dir = 0
                snake.y_dir = -1
            if self.state['Y'] == -1:
                snake.x_dir = 0
                snake.y_dir = 1

            if self.state['X'] == 1:
                snake.x_dir = -1
                snake.y_dir = 0
            if self.state['X'] == -1:
                snake.x_dir = 1
                snake.y_dir = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if snake.y_dir == 0:
                        if event.key == pygame.K_UP or self.state['Y'] == 1:
                            snake.x_dir = 0
                            snake.y_dir = -1
                        if event.key == pygame.K_DOWN or self.state['Y'] == -1:
                            snake.x_dir = 0
                            snake.y_dir = 1

                    if snake.x_dir == 0:
                        if event.key == pygame.K_LEFT or self.state['X'] == 1:
                            snake.x_dir = -1
                            snake.y_dir = 0
                        if event.key == pygame.K_RIGHT or self.state['Y'] == -1:
                            snake.x_dir = 1
                            snake.y_dir = 0

            display.fill(background)

            snake.show()
            snake.update()
            food.show()
            show_score()

            if snake.check_eaten():
                food.new_location()
                score += 1
                snake.grow()

            if snake.death():
                score = 0
                font = pygame.font.SysFont("Copperplate Gothic Bold", 50)
                text = font.render("Game Over!", True, snake_colour)
                display.blit(text, (width/2-50, height/2))
                pygame.display.update()
                time.sleep(3)
                snake.reset()

            if snake.history[0][0] > width:
                snake.history[0][0] = 0
            if snake.history[0][0] < 0:
                snake.history[0][0] = width

            if snake.history[0][1] > height:
                snake.history[0][1] = 0
            if snake.history[0][1] < 0:
                snake.history[0][1] = height

            pygame.display.update()
            clock.tick(10)



serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 12347

serversocket.bind((host, port))

threads = []
t = Thread(target=shutdown)
t.start()

while True:
    serversocket.listen(5)

    print('Waiting for connection... ')
    (conn, (ip, port)) = serversocket.accept()

    ct = clientThread(conn, ip)

    ct.start()

    threads.append(ct)
