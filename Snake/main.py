import pygame
import random

W, H = 500, 500
Wc, Hc = 20, 20
w, h = W/Wc, H/Hc

class Fruit:
    def __init__(self):
        self.x = random.randint(0, Wc-1)
        self.y = random.randint(0, Hc-1)

class Part:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self, startX, startY):
        self.body = [Part(startX, startY)]
        self.dir = "RIGHT"
    def move(self):
        headX = self.body[len(self.body)-1].x
        headY = self.body[len(self.body)-1].y
        if self.dir == "UP":
            self.body.append(Part(headX, headY-1))
        elif self.dir == "DOWN":
            self.body.append(Part(headX, headY+1))
        elif self.dir == "LEFT":
            self.body.append(Part(headX-1, headY))
        elif self.dir == "RIGHT":
            self.body.append(Part(headX+1, headY))
        newHeadX = self.body[len(self.body)-1].x
        newHeadY = self.body[len(self.body)-1].y
        if newHeadX == fruit.x and newHeadY == fruit.y:
            fruit.__init__()
        else:
            del self.body[0]
        #print(len(self.body))
    def draw(self):
        for i in range(len(self.body)):
            x = snake.body[i].x
            y = snake.body[i].y
            pygame.draw.rect(win, (0, 255, 0), (x*w, y*h, w, h))

pygame.init()
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake")

snake = Snake(2, 3)
fruit = Fruit()

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        snake.dir = "LEFT"
    elif key[pygame.K_RIGHT]:
        snake.dir = "RIGHT"
    elif key[pygame.K_UP]:
        snake.dir = "UP"
    elif key[pygame.K_DOWN]:
        snake.dir = "DOWN"
    
    win.fill((0, 0, 0))
    snake.move()
    snake.draw()
    pygame.draw.rect(win, (255, 0, 0), (fruit.x * w, fruit.y * h, w, h))
    pygame.display.update()
pygame.quit()
