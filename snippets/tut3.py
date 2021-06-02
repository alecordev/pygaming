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

is_jumping = False
jump_count = 10

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

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT] and x < Constants.SCREEN_SIZE[0] - vel - width:
        x += vel

    if not is_jumping:
        if keys[pygame.K_UP] and y > vel:
            y -= vel
        if keys[pygame.K_DOWN] and y < Constants.SCREEN_SIZE[1] - vel - height:
            y += vel

        if keys[pygame.K_SPACE]:
            is_jumping = True
    else:
        if jump_count >= -10:
            y -= (jump_count * abs(jump_count)) * 0.5
            jump_count -= 1
        else:  # This will execute if our jump is finished
            jump_count = 10
            is_jumping = False

    window.fill(
        Colors.BLACK
    )  # clean previous things by re-drawing an all black background
    pygame.draw.rect(window, Colors.RED, (x, y, width, height))
    pygame.display.update()

pygame.quit()
sys.exit()
