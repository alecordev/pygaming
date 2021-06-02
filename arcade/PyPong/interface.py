import pygame

from config import Config


class Interface:
    pygame.font.init()
    font = pygame.font.Font(Config.font_qgear, 50)

    def draw(window, mark_l, mark_r):
        window.blit(
            Interface.font.render(str(mark_l), False, Config.white), Config.pos_mark_l
        )
        window.blit(
            Interface.font.render(str(mark_r), False, Config.white), Config.pos_mark_r
        )

        pygame.draw.rect(window, Config.white, (247, 0, 6, 500))
