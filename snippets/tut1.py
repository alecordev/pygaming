import sys
import pygame


class Constants:
    SCREEN_SIZE = (500, 500)
    FPS = 30


class Colors:
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


pygame.init()
window = pygame.display.set_mode(Constants.SCREEN_SIZE)
pygame.display.set_caption("Title of the Window")

x = 50
y = 50
width = 40
height = 60
vel = 5

running = True

while running:
    pygame.time.Clock().tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel

    window.fill(
        Colors.BLACK
    )  # clean previous things by re-drawing an all black background
    pygame.draw.rect(window, Colors.RED, (x, y, width, height))
    pygame.display.update()

pygame.quit()
sys.exit()
