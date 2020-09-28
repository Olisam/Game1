import pygame
import sys
from pygame.locals import *


clock = pygame.time.Clock()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WIDTH = 300
HEIGHT = 200
FPS = 48
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BG = pygame.image.load("Background1.png")
dino = pygame.image.load("W1.png")
background_objects = (0.25, (40, 40, 114, 67))

def load_map(file):
    f = open(file, 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    gamemap = []
    for row in data:
        gamemap.append(list(row))
    return gamemap

scroll = [0, 0]

gamemap = load_map('level')


grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')
grassL_img = pygame.image.load('grassL.png')
grassR_img = pygame.image.load('grassR.png')
cloud = pygame.image.load('Cloud.png')
main_Menu = pygame.image.load('Main_Menu.png')

standingL = pygame.image.load("WL1.png")
walkLeft = [pygame.image.load("WL1.png"), pygame.image.load("WL2.png"),
            pygame.image.load("WL3.png"), pygame.image.load("WL4.png"),
            pygame.image.load("WL5.png"), pygame.image.load("WL6.png"),
            pygame.image.load("WL7.png"), pygame.image.load("WL8.png")]
walkRight = [pygame.image.load("W1.png"), pygame.image.load("W2.png"),
            pygame.image.load("W3.png"), pygame.image.load("W4.png"),
            pygame.image.load("W5.png"), pygame.image.load("W6.png"),
            pygame.image.load("W7.png"), pygame.image.load("W8.png")]
IdleRight = [pygame.image.load("WI1.png"), pygame.image.load("WI1.png"),
            pygame.image.load("WI2.png"), pygame.image.load("WI2.png"),
            pygame.image.load("WI1.png"), pygame.image.load("WI1.png"),
            pygame.image.load("WI2.png"), pygame.image.load("WI2.png")]
IdleLeft = [pygame.image.load("WIL1.png"), pygame.image.load("WIL1.png"),
            pygame.image.load("WIL2.png"), pygame.image.load("WIL2.png"),
            pygame.image.load("WIL1.png"), pygame.image.load("WIL1.png"),
            pygame.image.load("WIL2.png"), pygame.image.load("WIL2.png")]

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Platformer")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.tile_rects = []
        self.dirt_img = pygame.image.load("dirt.png").convert()
        self.grass_img = pygame.image.load("grass.png").convert()

    def new(self):
        self.main_menu()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.player.rect.y > 200:
            sys.exit()
        clock.tick(FPS)
        self.player.update()
        pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.player.moving_right = True
                    self.player.lookingright = True
                    self.player.lookingleft = False
                    self.player.standing = False
                if event.key == K_LEFT:
                    self.player.moving_left = True
                    self.player.lookingleft = True
                    self.player.lookingright = False
                    self.player.standing = False
                if event.key == K_UP:
                    if self.player.air_timer < 6:
                        self.player.vertical_momentum = -5
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.player.moving_right = False
                    self.player.standing = True
                if event.key == K_LEFT:
                    self.player.moving_left = False
                    self.player.standing = True


    def main_menu(self):
        while True:

            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            self.screen.blit(pygame.transform.scale(main_Menu, (1200, 800)), (0, 0))


            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(500, 400, 200, 50)

            if button_1.collidepoint(mx, my):
                if click:
                    self.run()

            pygame.draw.rect(self.screen, (255, 0, 0), button_1)


            pygame.display.update()
            clock.tick(60)

    def draw(self):
        self.display.blit(BG.convert(), (0, 0))


        obj_rect = pygame.Rect(40 - scroll[0] * 0.35, 40 - scroll[1] * 0.25, 114, 67)
        self.display.blit(cloud, (obj_rect.x, obj_rect.y))
        obj_rect1 = pygame.Rect(140 - scroll[0] * 0.5, 50 - scroll[1] * 0.5, 114, 67)
        self.display.blit(cloud, (obj_rect1.x, obj_rect1.y))

        self.drawTiles()
        self.player.draw()
        self.screen.blit(pygame.transform.scale(self.display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))

    def drawTiles(self):
        scroll[0] += (self.player.rect.x - 150 - scroll[0]) / 20
        scroll[1] += (self.player.rect.y - 100 - scroll[1]) / 20
        y = 0
        for layer in gamemap:
            x = 0
            for tile in layer:
                if tile == '1':
                    self.display.blit(dirt_img.convert(), (x * 16-scroll[0], y * 16-scroll[1]))
                if tile == '2':
                    self.display.blit(grass_img.convert(), (x * 16-scroll[0], y * 16-scroll[1]))
                if tile == '3':
                    self.display.blit(grassL_img, (x * 16-scroll[0], y * 16-scroll[1]))
                if tile == '4':
                    self.display.blit(grassR_img, (x * 16-scroll[0], y * 16-scroll[1]))
                if tile != '0':
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                x += 1
            y += 1

class Player(object):
    def __init__(self):
        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.rect = pygame.Rect(30, 40, 16, 25)
        self.movement = [0, 0]
        self.air_timer = 0
        self.collisions = []
        self.lookingleft = False
        self.lookingright = True
        self.walkCount = 0
        self.idleCount = 0
        self.standing = True

    def update(self):
        self.moving()
        self.rect, collisions =move(self.rect, self.movement, g.tile_rects)
        if collisions['bottom'] == True:
            self.air_timer = 0
            self.vertical_momentum = 0
        else:
            self.air_timer += 1
        if collisions['top'] == True:
            self.vertical_momentum = 0


    def moving(self):
        self.movement = [0, 0]
        if self.moving_right == True:
            self.movement[0] += 2
        if self.moving_left == True:
            self.movement[0] -= 2
        self.movement[1] += self.vertical_momentum
        self.vertical_momentum += 0.4
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3

    def draw(self):
        if self.walkCount + 1 >= 48:
            self.walkCount = 0
        if self.idleCount + 1 >= 48:
            self.idleCount = 0

        if not (self.standing):
            if self.lookingright:
                g.display.blit(walkRight[self.walkCount // 6], (self.rect.x-scroll[0], self.rect.y-scroll[1]))
                self.walkCount += 1
            elif self.lookingleft:
                g.display.blit(walkLeft[self.walkCount // 6], (self.rect.x-scroll[0], self.rect.y-scroll[1]))
                self.walkCount += 1
        else:
            if self.lookingright:
                g.display.blit(IdleRight[self.idleCount // 6], (self.rect.x-scroll[0], self.rect.y-scroll[1]))
                self.idleCount += 1
            elif self.lookingleft:
                g.display.blit(IdleLeft[self.idleCount // 6], (self.rect.x-scroll[0], self.rect.y-scroll[1]))
                self.idleCount += 1

g = Game()
while g.running:
    g.new()

pygame.quit()