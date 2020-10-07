import pygame
import random
from pygame.locals import *
from os import path

pygame.font.init()
myfont = pygame.font.SysFont('Blox (BRK)', 200)
myfont2 = pygame.font.SysFont('VCR OSD Mono', 80)
myfont3 = pygame.font.SysFont('VCR OSD Mono', 40)
snakepic = pygame.transform.scale(pygame.image.load('snakeformainmenu.png'), (450, 450))
deadsnake = pygame.transform.scale(pygame.image.load('deadsnake.png'), (450, 450))

width = 1000
height = 1000
rows = 20
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()



class snake(object):
    def __init__(self):
        self.colour = (255, 0, 0)
        self.x = 50
        self.y = 50
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.snake_pos = [500, 50]
        self.snake_body = [[500, 50], [500 - 50, 50], [500 - (2 * 50), 50], [500 - (3 * 50), 50]]

    def initialise(self):
        self.snake_pos = [500, 50]
        self.snake_body = [[500, 50], [500 - 50, 50], [500 - (2 * 50), 50], [500 - (3 * 50), 50]]
        self.direction = 'RIGHT'
        self.change_to = self.direction

    def move(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[K_a]:
                    self.change_to = 'left'

                elif keys[K_d]:
                    self.change_to = 'right'

                elif keys[K_w]:
                    self.change_to = 'up'

                elif keys[K_s]:
                    self.change_to = 'down'
                elif keys[K_r]:
                    g.maingame()
                elif keys[K_e]:
                    g.game_over()

        if self.change_to == 'up' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'down' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'left' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'right' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        if self.direction == 'UP':
            self.snake_pos[1] -= 50
        if self.direction == 'DOWN':
            self.snake_pos[1] += 50
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 50
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 50

        if self.snake_pos[0] >= 1000 and self.direction != 'LEFT':
            self.snake_pos[0] = 0

        if self.snake_pos[0] < 0 and self.direction != 'RIGHT':
            self.snake_pos[0] = 1000

        if self.snake_pos[1] >= 1000 and self.direction != 'UP':
            self.snake_pos[1] = 0

        if self.snake_pos[1] < 0 and self.direction != 'DOWN':
            self.snake_pos[1] = 1000

        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == apple.x and self.snake_pos[1] == apple.y:
            apple.newloc()
            g.score += 1
        else:
            self.snake_body.pop()

        for part in self.snake_body[1:]:
            if self.snake_pos[0] == part[0] and self.snake_pos[1] == part[1]:
                g.game_over()
        print(self.snake_body)


    def draw(self):


        n = len(self.snake_body)
        for pos, name in enumerate(self.snake_body):
            if pos == 0:
                pygame.draw.rect(screen, (78, 207, 86), pygame.Rect(name[0], name[1], 50, 50))
            elif pos < (n // (4 / 2)):
                pygame.draw.rect(screen, (130, 231, 138), pygame.Rect(name[0] + 2, name[1] + 2, 46, 46))
            elif pos < (n // (4 / 3)):
                pygame.draw.rect(screen, (183, 255, 191), pygame.Rect(name[0] + 4, name[1] + 4, 42, 42))
            elif pos < (n):
                pygame.draw.rect(screen, (183, 255, 191), pygame.Rect(name[0] + 6, name[1] + 6, 38, 38))




    def reset(self):
        self.initialise()
        g.score = 4

class food(object):
    def __init__(self):
        self.x = random.randrange(0, 20) * 50
        self.y = random.randrange(0, 20) * 50

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 50, 50))

    def newloc(self):
        self.x = random.randrange(0, 20) * 50
        self.y = random.randrange(0, 20) * 50

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for i in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def redrawWindow(surface):
    scoresurface = myfont2.render(str(g.score), False, (0, 150, 0))
    surface.fill((0, 0, 0))
    screen.blit(scoresurface, (480, 440))
    drawGrid(width, rows, surface)
    apple.draw()
    s.draw()
    pygame.display.update()

def load_map(file):
    f = open(file, 'r')
    data = f.read()
    f.close()
    game_hs = []
    game_hs.append(data)
    return game_hs


class Game():
    def __init__(self):
        pygame.init()
        self.score = 3
        self.load_data()

    def load_data(self):
        pass

    def main_menu(self):

        textsurface = myfont.render('Snake', False, (255, 180, 0))
        startsurface = myfont2.render('Start', False, (0, 0, 0))
        while True:
            screen.fill((255, 255, 255))

            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(380, 400, 230, 80)
            button_1_overlay = pygame.Rect(373, 400, 240, 80)

            if button_1.collidepoint(mx, my):
                pygame.draw.rect(screen, (0, 0, 0), button_1_overlay, 3)
                if click:
                    g.maingame()

            pygame.draw.rect(screen, (255, 255, 255), button_1)
            screen.blit(textsurface, (250, 150))
            screen.blit(startsurface, (380, 400))
            screen.blit(snakepic, (550, 600))

            pygame.display.update()
            clock.tick(10)


    def maingame(self):
        s.reset()
        while True:
            pygame.time.delay(50)
            clock.tick(12)
            s.move()
            redrawWindow(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    def game_over(self):
        self.is_highscore()
        with open('HS_FILE', 'r') as f3:
            data = f3.read()
            newhighscore = data

        highscoreis = myfont3.render('HIGH SCORE:', False, (0, 0, 0))
        highscoresurface = myfont3.render(str(newhighscore), False, (0, 0, 200))
        textsurface = myfont.render('Game Over', False, (255, 180, 0))
        startsurface = myfont2.render('Restart', False, (0, 0, 0))
        while True:
            click = False
            screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(333, 500, 330, 80)
            button_1_overlay = pygame.Rect(333, 500, 330, 80)

            if button_1.collidepoint(mx, my):
                pygame.draw.rect(screen, (0, 0, 0), button_1_overlay, 3)
                if click:
                    g.maingame()

            pygame.draw.rect(screen, (255, 255, 255), button_1)
            screen.blit(textsurface, (60, 150))
            screen.blit(startsurface, (340, 500))
            screen.blit(deadsnake, (500, 562))
            screen.blit(highscoreis, (200, 400))
            screen.blit(highscoresurface, (750, 400))

            pygame.display.update()
            clock.tick(10)

    def is_highscore(self):
        highscore = load_map('HS_FILE')
        if self.score > int(highscore[0]):
            highscore.clear()
            highscore.append(self.score)
            f1 = open('HS_FILE', 'w')
            f1.truncate(0)
            with open('HS_FILE', 'w') as f2:
                f2.write(str(self.score))
        else:
            pass





# main loop
s = snake()
apple = food()
g = Game()
def main():

    while True:
        g.main_menu()
# run
main()