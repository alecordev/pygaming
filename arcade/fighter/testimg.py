import pygame

background_img = "resources/images/background.png"
shoot_img = "resources/images/shoot.png"

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

background = pygame.image.load(background_img)

all_shoot = pygame.image.load(shoot_img)

enemy1_rect = pygame.Rect(430, 520, 71, 105)
enemy2_rect = pygame.Rect(533, 655, 71, 105)
enemy3_rect = pygame.Rect(602, 648, 71, 105)
enemy4_rect = pygame.Rect(267, 296, 57, 43)

enemy1_img = all_shoot.subsurface(enemy4_rect)

while True:
    screen.blit(background, (0, 0))
    screen.blit(enemy1_img, (200, 100))
    pygame.display.update()
