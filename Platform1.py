import pygame
import sys
from pygame.locals import *

pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Comic Sans MS', 30)

clock = pygame.time.Clock()
time_elapsed = 0

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1200
WIDTH = 300
HEIGHT = 200
FPS = 48
WHITE = (255, 255, 255)
BG = pygame.image.load("Background1.png")
background_objects = (0.25, (40, 40, 114, 67))
scroll = [0, 0]

def if_time_elapsed(seconds):
    global time_elapsed
    if time_elapsed > seconds*1000:
        return True
    else:
        return False


def load_map(file):
    f = open(file, 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


gamemap = load_map('level')
housemap = load_map('levelinside')

grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')
grassL_img = pygame.image.load('grassL.png')
grassR_img = pygame.image.load('grassR.png')
dirtSR = pygame.image.load('DirtSideR.png')
cloud = pygame.image.load('Cloud.png')
Gslime = pygame.image.load('slime.png')
main_Menu = pygame.image.load('Main_Menu.png')
standingL = pygame.image.load("WL1.png")
house = pygame.image.load("HouseTest.png")
doorhitbox = pygame.image.load("doorhitbox.png")
houseinside = pygame.image.load("houseinside.png")
heart1 = pygame.transform.scale(pygame.image.load("Heart1.png"), (245, 40))
heart2 = pygame.transform.scale(pygame.image.load("Heart2.png"), (245, 40))
heart3 = pygame.transform.scale(pygame.image.load("Heart3.png"), (245, 40))
heart4 = pygame.transform.scale(pygame.image.load("Heart4.png"), (245, 40))
heart5 = pygame.transform.scale(pygame.image.load("Heart5.png"), (245, 40))
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
JumpR = [pygame.image.load("Wjump2.png"), pygame.image.load("Wjump2.png"),
         pygame.image.load("Wjump2.png"), pygame.image.load("Wjump2.png")]
JumpL = [pygame.image.load("WjumpL2.png"), pygame.image.load("WjumpL2.png"),
         pygame.image.load("WjumpL2.png"), pygame.image.load("WjumpL2.png")]
Falling = [pygame.image.load("Wfalling1.png"), pygame.image.load("Wfalling1.png"),
           pygame.image.load("Wfalling2.png"), pygame.image.load("Wfalling2.png")]
FallingL = [pygame.image.load("WfallingL1.png"), pygame.image.load("WfallingL1.png"),
            pygame.image.load("WfallingL2.png"), pygame.image.load("WfallingL2.png")]
TakenDamage = [pygame.image.load("WTakingDamage.png"), pygame.image.load("WTakingDamage.png")]


def collision_test(rect, tiles):
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
    rect.y += int(movement[1])
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
        self.playing = False
        self.player = Player()
        self.tile_rects = []
        self.dirt_img = pygame.image.load("dirt.png").convert()
        self.grass_img = pygame.image.load("grass.png").convert()
        self.enemy = slime(140, 40, 5, 145)
        self.enemy2 = slime(200, 40, 150, 210)
        self.inhouse = False

    def new(self):
        global scroll
        self.player.initialise()
        self.enemy.initialise()
        self.enemy2.initialise()
        scroll = [0, -300]
        self.run()

    def restart(self):
        self.new()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def inside_house(self):
        self.display.blit(houseinside, (0, 0))
        self.drawtiles()

    def outside(self):
        self.display.blit(BG.convert(), (0, 0))

        obj_rect = pygame.Rect(int(40 - scroll[0] * 0.35), int(40 - scroll[1] * 0.25), 114, 67)

        obj_rect1 = pygame.Rect(int(140 - scroll[0] * 0.5), int(50 - scroll[1] * 0.5), 114, 67)

        door_rect = pygame.Rect((110 - scroll[0]), (38 - scroll[1]), 19, 27)
        self.drawtiles()
        house_rect = pygame.Rect((50 - scroll[0]), (7 - scroll[1]), 106, 55)

        self.display.blit(house, (house_rect.x, house_rect.y))
        if self.player.rect.x > 100 and self.player.rect.x < 119:
            self.display.blit(doorhitbox, (door_rect.x, door_rect.y))



    def update(self):
        global time_elapsed

        if self.player.rect.y > 215:
            self.restart()
        t = clock.tick(FPS)
        time_elapsed += t

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
                    self.player.moving_left = False
                    self.player.lookingright = True
                    self.player.lookingleft = False
                    self.player.standing = False
                if event.key == K_LEFT:
                    self.player.moving_left = True
                    self.player.moving_right = False
                    self.player.lookingleft = True
                    self.player.lookingright = False
                    self.player.standing = False
                if event.key == K_UP:
                    if self.player.air_timer < 6:
                        self.player.vertical_momentum = -5
                if event.key == K_r:
                    self.restart()
                if event.key == K_e and self.player.rect.x > 100 and self.player.rect.x < 119:
                    self.inhouse = True
            if event.type == KEYUP:
                if event.key == K_e:
                    pass
                if event.key == K_RIGHT:
                    self.player.moving_right = False
                    self.player.standing = True
                if event.key == K_LEFT:
                    self.player.moving_left = False
                    self.player.standing = True

    def main_menu(self):
        textsurface = myfont.render('Start Game', False, WHITE)
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

            self.screen.blit(pygame.transform.scale(main_Menu, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))

            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(500, 400, 200, 50)

            if button_1.collidepoint(mx, my):
                if click:
                    self.new()

            pygame.draw.rect(self.screen, (255, 0, 0), button_1)
            self.screen.blit(textsurface, (550, 420))

            pygame.display.update()
            clock.tick(60)

    def draw(self):
        if self.inhouse == False:
            self.outside()
        if self.inhouse == True:
            self.inside_house()
        self.player.animate()
        self.screen.blit(pygame.transform.scale(self.display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))

        print(self.player.rect.y)


    def drawtiles(self):
        self.tile_rects.clear()
        if self.inhouse == False:
            if scroll[0] <=0:
                scroll[0] = 0
            if scroll[0] >= 420:
                scroll[0] = 420
            scroll[0] += (self.player.rect.x - 110 - scroll[0]) / 20
            scroll[1] += (self.player.rect.y - 100 - scroll[1]) / 20
            self.tile_rects.clear()
            y = 0
            for layer in gamemap:
                x = 0
                for tile in layer:
                    if tile == '1':
                        self.display.blit(dirt_img.convert(), (int(x * 16 - scroll[0]), int(y * 16 - scroll[1])))
                    if tile == '2':
                        self.display.blit(grass_img.convert(), (int(x * 16 - scroll[0]), int(y * 16 - scroll[1])))
                    if tile == '3':
                        self.display.blit(grassL_img.convert_alpha(), (int(x * 16 - scroll[0]), int(y * 16 - scroll[1])))
                    if tile == '4':
                        self.display.blit(grassR_img.convert_alpha(), (int(x * 16 - scroll[0]), int(y * 16 - scroll[1])))
                    if tile == '5':
                        self.display.blit(dirtSR.convert_alpha(), (int(x * 16 - scroll[0]), int(y * 16 - scroll[1])))
                    if tile != '0':
                        self.tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                    x += 1
                y += 1
        if self.inhouse == True:
            self.tile_rects.clear()
            y = 0
            for layer in housemap:
                x = 0
                for tile in layer:
                    if tile == '1':
                        self.display.blit(dirt_img.convert(), (int(x * 16 - scroll[0]), int(y * 16 - scroll[1])))
                    if tile != '0':
                        self.tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                    x += 1
                y += 1


class Player(object):
    def __init__(self):
        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.rect = pygame.Rect(50, 40, 16, 25)
        self.movement = [0, 0]
        self.air_timer = 0
        self.collisions = []
        self.lookingleft = False
        self.lookingright = True
        self.walkCount = 0
        self.idleCount = 0
        self.jumpCount = 0
        self.fallCount = 0
        self.damageCount = 0
        self.standing = True
        self.jumping = False
        self.falling = False
        self.enemy_rects = []
        self.takingdamage = False
        self.health = 100

    def initialise(self):
        self.rect.x = 50
        self.rect.y = 40
        self.lookingright = True
        self.health = 100

    def update(self):

        self.moving()
        self.rect, collisions = move(self.rect, self.movement, g.tile_rects)
        if collisions['bottom']:
            self.jumping = False
            self.air_timer = 0
            self.vertical_momentum = 0
        else:
            self.air_timer += 1
        if collisions['top']:
            self.vertical_momentum = 0
        self.check_for_damage()
        self.check_life()

    def moving(self):
        self.falling = False
        if self.air_timer > 3 and self.vertical_momentum < 0:
            self.jumping = True
        elif self.air_timer > 30 and self.vertical_momentum >= 3:
            self.falling = True
        self.movement = [0, 0]
        if self.moving_right:
            self.movement[0] += 2
        if self.moving_left:
            self.movement[0] -= 2
        self.movement[1] += self.vertical_momentum
        self.vertical_momentum += 0.4
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3

    def animate(self):
        if self.walkCount + 1 >= 48:
            self.walkCount = 0
        if self.idleCount + 1 >= 48:
            self.idleCount = 0
        if self.jumpCount + 1 >= 24:
            self.jumpCount = 0
        if self.fallCount + 1 >= 24:
            self.fallCount = 0

        if self.takingdamage:
            if if_time_elapsed(0.2):
                self.takingdamage = False

            g.display.blit(TakenDamage[1].convert_alpha(),
                           (int(self.rect.x - scroll[0]), int(self.rect.y - scroll[1])))

        elif self.jumping and self.lookingright:
            g.display.blit(JumpR[int(self.jumpCount // 6)].convert_alpha(), (int(self.rect.x - scroll[0]), int(self.rect.y - scroll[1])))
            self.jumpCount += 1
            self.jumping = False
        elif self.jumping and self.lookingleft:
            g.display.blit(JumpL[int(self.jumpCount // 6)].convert_alpha(),
                           (int(self.rect.x - scroll[0]), int(self.rect.y - scroll[1])))
            self.jumpCount += 1
            self.jumping = False
        elif self.falling and self.lookingright:
            g.display.blit(Falling[int(self.fallCount // 6)].convert_alpha(),
                           (int(self.rect.x - scroll[0]), int(self.rect.y - scroll[1])))
            self.fallCount += 1
        elif self.falling and self.lookingleft:
            g.display.blit(FallingL[int(self.fallCount // 6)].convert_alpha(),
                           (int(self.rect.x - scroll[0]), int(self.rect.y - scroll[1])))
            self.fallCount += 1
        elif not self.standing:
            if self.lookingright:
                g.display.blit(walkRight[int(self.walkCount // 6)].convert_alpha(),
                               (int(self.rect.x - scroll[0]), int(self.rect.y - scroll[1])))
                self.walkCount += 1
            elif self.lookingleft:
                g.display.blit(walkLeft[int(self.walkCount // 6)].convert_alpha(),
                               (int(self.rect.x - scroll[0]), int(self.rect.y - scroll[1])))
                self.walkCount += 1
        else:
            if self.lookingright:
                g.display.blit(IdleRight[int(self.idleCount // 6)].convert_alpha(),
                               (int(self.rect.x - scroll[0]), int(self.rect.y - scroll[1])))
                self.idleCount += 1
            elif self.lookingleft:
                g.display.blit(IdleLeft[int(self.idleCount // 6)].convert_alpha(),
                               (int(self.rect.x - scroll[0]), int(self.rect.y - scroll[1])))
                self.idleCount += 1

    def check_for_damage(self):
        pass


    def check_life(self):
        if self.health <= 0:
            g.restart()

class slime(object):
    def __init__(self, x, y, start, end):
        self.rect = pygame.Rect(x, y, 9, 7)
        self.x = x
        self.y = y
        self.movement = [0, 0]
        self.vertical_momentum = 0
        self.collisions = []
        self.start = start
        self.end = end
        self.direction = 1
        self.target = end
        self.jumpCount = 0

    def initialise(self):
        self.vertical_momentum = 0
        self.direction = 1
        self.rect.x = self.x
        self.rect.y = self.y

    def render(self):
        self.move()
        self.jump()
        g.display.blit(Gslime, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

    def move(self):
        self.target = self.end
        self.movement = [0, 0]
        if self.rect.x * self.direction < self.target:
            self.movement[0] += 1 * self.direction
        if self.rect.x == self.end:
            self.rect.x = self.target - 1
            self.target = self.start
            self.direction = -1
        if self.rect.x == self.start:
            self.rect.x = self.start + 1
            self.target = self.end
            self.direction = 1
        self.vertical_momentum += 0.2
        self.movement[1] += self.vertical_momentum
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3
        self.rect, collisions = move(self.rect, self.movement, g.tile_rects)
        if collisions['bottom']:
            self.vertical_momentum = 0
        if collisions['top']:
            self.vertical_momentum = 0

    def jump(self):
        if self.jumpCount + 1 == 48:
            self.jumpCount = 0
        self.jumpCount += 1
        if 96 // self.jumpCount == 8:
            self.vertical_momentum = -3


g = Game()
while g.running:
    g.main_menu()


pygame.quit()
