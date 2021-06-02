import os
import sys

import pygame

from player import Player
from engine import Platform

pygame.init()


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    platformImage = "images/platform.png"
    size = width, height = 800, 600
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    player = Player("images/player.png")

    platformList = []
    for i in range(0, 10):
        platform = Platform(platformImage, i * 50, 600 - (i * 50))
        platformList.append(platform)

    platformSprites = pygame.sprite.RenderPlain(platformList)

    goalImage = pygame.image.load("images/goal.png")
    goalRect = goalImage.get_rect()
    goalRect.topleft = 700, 500

    clock = pygame.time.Clock()

    while 1:
        screen.fill(black)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            else:
                player.move(event)

        if not pygame.sprite.spritecollide(player, platformSprites, False):
            player.isFalling = 1
        else:
            player.isFalling = 0

        player.update()

        platformSprites.draw(screen)
        screen.blit(player.image, player.rect)
        screen.blit(goalImage, goalRect)

        pygame.display.flip()

        if player.rect.bottom > 600:
            print("Game over")
            return

        if player.rect.colliderect(goalRect):
            print("You win!")
            return


if __name__ == "__main__":
    main()
