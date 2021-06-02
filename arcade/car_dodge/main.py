import random

import os
import pygame

os.environ["SDL_VIDEO_CENTERED"] = "1"

display_width = 1000
display_height = 536
black = (0, 0, 0)
white = (255, 255, 255)
red = (250, 0, 0)
grey = (166, 175, 179)
blue = (29, 164, 209)
green = (12, 105, 19)
brightred = (255, 0, 0)
brightgreen = (0, 255, 0)
car_width = 150
thing_height = 300
thing_width = 150
gameOver = False

pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Simple Dodging Game")
clock = pygame.time.Clock()

carImg = pygame.image.load("Player.png")
car2Img = pygame.image.load("Enemy.png")
back = pygame.image.load("back.jpg").convert()
gameDisplay.blit(back, (0, 0))


def things_dodged(count):
    message("Score : " + str(count), red, 40, 10, 10)


def things(thingx, thingy):
    gameDisplay.blit(car2Img, (thingx, thingy))


def carDisplay(x, y):
    gameDisplay.blit(carImg, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()


def message(msg, color, size, x, y):
    font = pygame.font.Font(None, size)
    text = font.render(msg, True, color)
    gameDisplay.blit(text, (x, y))


def game_loop():
    x = display_width * 0.45
    y = display_height * 0.73
    x_change = 0
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 10
    gameExit = False
    dodged = 0
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -20
                elif event.key == pygame.K_RIGHT:
                    x_change = 20
                elif event.key == pygame.K_LEFT and event.key == pygame.K_RIGHT:
                    x_change = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    x_change = 0
        x = x + x_change
        gameDisplay.blit(back, (0, 0))

        things(thing_startx, thing_starty)
        thing_starty = thing_starty + thing_speed
        carDisplay(x, y)
        things_dodged(dodged)
        if x > display_width - car_width or x <= 0:
            crash()
            gameOver = True

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(30, (display_width - 150))
            dodged = dodged + 1
            if dodged % 10 == 0:
                thing_speed = thing_speed + 2

        if y < thing_starty + thing_height:  # y crossover
            if thing_startx < x + car_width and thing_startx + thing_width > x:
                crash()
                gameOver = True
        pygame.display.update()
        clock.tick(30)


def crash():
    gameDisplay.blit(back, (0, 0))
    message(
        "You Crashed!", brightred, 120, (display_width / 3.75), (display_height / 2.5)
    )
    message(
        "Press spacebar to continue or Q to quit",
        blue,
        40,
        (display_width / 3.75),
        (display_height / 1.5),
    )
    pygame.display.update()
    crashed = True
    while crashed == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    game_loop()


def game_intro():
    intro = True
    gameDisplay.blit(back, (0, 0))
    message(
        "Simple Dodging Game", brightred, 90, (display_width / 5), (display_height / 3)
    )
    message("P = Play", green, 60, (display_width / 3.5), (display_height / 2))
    message("Q = Quit", green, 60, (display_width / 1.75), (display_height / 2))
    pygame.display.update()
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


game_intro()
pygame.quit()
quit()
