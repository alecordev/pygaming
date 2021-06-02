import os
import sys
import logging

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(asctime)s] - PID: %(process)d - TID: %(thread)d - %(levelname)s - %(message)s",
)

import numpy as np
import pygame


class GameConstants:
    SCREEN_SIZE = (800, 600)
    FPS = 60


class Animation:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Animation example")

        self.clock = pygame.time.Clock()
        self.fps = GameConstants.FPS
        self.screen = pygame.display.set_mode(
            GameConstants.SCREEN_SIZE, pygame.DOUBLEBUF, 32
        )

        pygame.mouse.set_visible(False)

    def start(self):
        self.screen.fill((0, 0, 0))
        x = np.random.randint(0, GameConstants.SCREEN_SIZE[0])
        y = np.random.randint(0, GameConstants.SCREEN_SIZE[1])
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

                if event.type == pygame.KEYUP:
                    logging.info(f"{event.key} pressed")
                    if event.key == pygame.K_ESCAPE:
                        self.exit()

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_p]:
                x += 1
                y += 1
                self.screen.set_at((x, y), (255, 255, 255))
                # pygame.draw.circle(pygame.Surface(), (255, 255, 255), (300, 300), 0)

            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(self.fps)

    @staticmethod
    def exit():
        logging.debug(f"Exiting")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Animation().start()
