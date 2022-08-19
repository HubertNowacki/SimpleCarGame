import pygame
from pygame.locals import *
import random, time, sys

pygame.init()

FPS = pygame.time.Clock()

screen_width = 400
screen_height = 600
speed = 5
player_speed = 5
score = 0

color_black = pygame.Color(0, 0, 0)
color_blue = pygame.Color(0, 0, 255)
color_red = pygame.Color(255, 0, 0)
color_green = pygame.Color(0, 255, 0)
color_white = pygame.Color(255, 255, 255)

font = pygame.font.SysFont("Do Hyeon", 80)
font_small = pygame.font.SysFont("Do Hyeon", 60)
game_over = font.render("XD NO BEKA", True, color_black)

with open("Highscore.txt") as reader:
    highscore_gamee = reader.readlines()
    highscore_game = int(highscore_gamee[0])
    highscore = font.render((highscore_gamee[0]), True, color_black)

background = pygame.image.load("AnimatedStreet.png")

DISPLAY = pygame.display.set_mode((400, 600))
DISPLAY.fill(pygame.Color(255, 255, 255))
pygame.display.set_caption("CarGameSim")

pygame.draw.circle(DISPLAY, color_blue, (200, 50), 30)
pygame.draw.circle(DISPLAY, color_blue, (100, 50), 30)
pygame.draw.rect(DISPLAY, color_green, (100, 200, 100, 50), 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width + 40), 0)

    def move(self):
        global score
        self.rect.move_ip(0, speed)
        if self.rect.bottom > 600:
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 270), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_UP]:
            self.rect.move_ip(0, -player_speed)
        if pressed_key[K_DOWN]:
            self.rect.move_ip(0, player_speed)
        if self.rect.left > 0:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(-player_speed, 0)
        if self.rect.right < screen_width:
            if pressed_key[K_RIGHT]:
                self.rect.move_ip(player_speed, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

increase_speed = pygame.USEREVENT + 1
pygame.time.set_timer(increase_speed, 1000)

while True:
    for event in pygame.event.get():
        if event.type == increase_speed:
            speed += 2
            if player_speed < 50:
                player_speed += 1
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY.blit(background, (0, 0))
    scores = font_small.render("SCORE: " + str(score), True, color_black)
    DISPLAY.blit(scores, (10, 10))

    for entity in all_sprites:
        DISPLAY.blit(entity.image, entity.rect)
        entity.move()
    if pygame.sprite.spritecollideany(P1, enemies):
        if score > highscore_game:
            with open("Highscore.txt", "w") as writer:
                writer.write(repr(score))
                new_highscore = font_small.render("NEW HIGHSCORE", True, color_black)
                highscore = font.render(str(score), True, color_black)
        DISPLAY.fill(color_red)
        DISPLAY.blit(game_over, (30, 250))
        if score > highscore_game:
            DISPLAY.blit(new_highscore, (30, 400))
        DISPLAY.blit(highscore, (150, 480))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FPS.tick(60)
