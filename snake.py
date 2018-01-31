import pygame, sys, os, copy, random, time, pygame_textinput
from datetime import datetime

pygame.init()

width = 600
height = 600
scale = 20
score = 0

food_x = 20
food_y = 20


name, date = ""
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("IDP - Snake")
clock = pygame.time.Clock()

background = (16, 78, 139)
snake_colour = (236, 240, 241)
food_colour = (148, 49, 38)
snake_head = (247, 220, 111)


class Snake:
    def __init__(self, x_start, y_start):
        self.x = x_start
        self.y = y_start
        self.w = 20
        self.h = 20
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x, self.y]]
        self.length = 1

    def reset(self):
        self.x = width / 2 - scale
        self.y = height / 2 - scale
        self.w = 20
        self.h = 20
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x, self.y]]
        self.length = 1

    def show(self):
        for i in range(self.length):
            if i is not 0:
                pygame.draw.rect(display, snake_colour, (self.history[i][0], self.history[i][1], self.w, self.h))
            else:
                pygame.draw.rect(display, snake_head, (self.history[i][0], self.history[i][1], self.w, self.h))

    def check_eaten(self):
        if abs(self.history[0][0] - food_x) < scale and abs(self.history[0][1] - food_y) < scale:
            return True

    def grow(self):
        self.length += 1
        self.history.append(self.history[self.length - 2])

    def death(self):
        i = self.length - 1
        while i > 0:
            if abs(self.history[0][0] - self.history[i][0]) < self.w and abs(self.history[0][1] - self.history[i][1]) < self.h and self.length > 2:
                return True
            i -= 1

    def update(self):
        i = self.length - 1
        while i > 0:
            self.history[i] = copy.deepcopy(self.history[i - 1])
            i -= 1
        self.history[0][0] += self.x_dir*scale
        self.history[0][1] += self.y_dir*scale


class Food:
    def new_location(self):
        global food_x, food_y
        food_x = random.randrange(1, width / scale - 1) * scale
        food_y = random.randrange(1, height / scale - 1) * scale

    def show(self):
        pygame.draw.rect(display, food_colour, (food_x, food_y, scale, scale))


def show_score():
    font = pygame.font.SysFont("monospace", 20)
    text = font.render("Score: " + str(score), True, snake_colour)
    display.blit(text, (scale, scale))

green = (0, 139, 0)
bright_green = (0, 255, 0)

textinput = pygame_textinput.TextInput()
_image_library = {}

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image

def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(display, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
        else:
            pygame.draw.rect(display, ic, (x, y, w, h))
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    display.blit(textSurf, textRect)

def test():
    print(textinput.get_text())

def button_action():
    global score, name, date
    name = textinput.get_text()
    snake = Snake(width / 2, height / 2)
    food = Food()
    food.new_location()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if snake.y_dir == 0:
                    if event.key == pygame.K_UP:
                        snake.x_dir = 0
                        snake.y_dir = -1
                    if event.key == pygame.K_DOWN:
                        snake.x_dir = 0
                        snake.y_dir = 1
                if snake.x_dir == 0:
                    if event.key == pygame.K_LEFT:
                        snake.x_dir = -1
                        snake.y_dir = 0
                    if event.key == pygame.K_RIGHT:
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
            pygame.mixer.music.load("resources/eten.mp3")
            pygame.mixer.music.play(0)
            snake.grow()
        if snake.death():
            score = 0
            font = pygame.font.SysFont("monospace", 50)
            text = font.render("Game Over!", False, snake_colour)
            display.blit(text, (width / 2 - 135, height / 2.2))
            pygame.display.update()
            pygame.mixer.music.load("resources/gameover.mp3")
            pygame.mixer.music.play(0)
            date = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
            time.sleep(4)
            snake.reset()
        if snake.history[0][0] > width - 1:
            snake.history[0][0] = 0
        if snake.history[0][0] < 0:
            snake.history[0][0] = width
        if snake.history[0][1] > height - 1:
            snake.history[0][1] = 0
        if snake.history[0][1] < 0:
            snake.history[0][1] = height
        pygame.display.update()
        clock.tick(20)


def gameloop():
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        display.fill((255, 255, 255))
        textinput.update(events)
        display.blit(get_image('resources/beginscherm.png'), (0, 0))
        display.blit(textinput.get_surface(), (25, 530))
        font = pygame.font.SysFont("monospace", 20)
        text = font.render("Voer je naam in:", False, (255, 255, 255))
        display.blit(text, (25, 500))
        button("START!", 225, 520, 100, 50, green, bright_green, button_action)
        pygame.display.update()
        clock.tick(20)


gameloop()