import sys
import logging

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(asctime)s] - PID: %(process)d - TID: %(thread)d - %(levelname)s - %(message)s",
)

import pygame

from shared import game
from scenes import scenes


class Breakout:
    def __init__(self):
        self.__lives = 5
        self.__score = 0

        self.__level = game.Level(self)
        self.__level.load(0)
        # self.__level.load_random()

        self.__pad = game.Pad(
            (
                game.GameConstants.SCREEN_SIZE[0] / 2,
                game.GameConstants.SCREEN_SIZE[1] - game.GameConstants.PAD_SIZE[1],
            ),
            pygame.image.load(game.GameConstants.SPRITE_PAD),
        )
        self.__balls = [
            game.Ball(
                (400, 400), pygame.image.load(game.GameConstants.SPRITE_BALL), self
            ),
        ]

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Game Programming with Python and pygame")

        self.__clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            game.GameConstants.SCREEN_SIZE, pygame.DOUBLEBUF, 32
        )

        pygame.mouse.set_visible(False)

        self.__scenes = (
            scenes.PlayingGameScene(self),
            scenes.GameOverScene(self),
            scenes.HighscoreScene(self),
            scenes.MenuScene(self),
        )

        self.__current_scene = 3
        self.__sounds = (
            pygame.mixer.Sound(game.GameConstants.SOUND_FILE_GAMEOVER),
            pygame.mixer.Sound(game.GameConstants.SOUND_FILE_HIT_BRICK),
            pygame.mixer.Sound(game.GameConstants.SOUND_FILE_HIT_BRICK_LIFE),
            pygame.mixer.Sound(game.GameConstants.SOUND_FILE_HIT_BRICK_SPEED),
            pygame.mixer.Sound(game.GameConstants.SOUND_FILE_HIT_WALL),
            pygame.mixer.Sound(game.GameConstants.SOUND_FILE_HIT_PAD),
        )

    def start(self):
        while 1:
            self.__clock.tick(100)

            self.screen.fill((0, 0, 0))

            current_scene = self.__scenes[self.__current_scene]
            current_scene.handle_events(pygame.event.get())
            current_scene.render()

            pygame.display.update()

    def change_scene(self, scene):
        self.__current_scene = scene

    def get_level(self):
        return self.__level

    def get_score(self):
        return self.__score

    def increase_score(self, score):
        self.__score += score

    def get_lives(self):
        return self.__lives

    def get_balls(self):
        return self.__balls

    def get_pad(self):
        return self.__pad

    def play_sound(self, audio_file):
        sound = self.__sounds[audio_file]

        sound.stop()
        sound.play()

    def reduce_lives(self):
        self.__lives -= 1

    def increase_lives(self):
        self.__lives += 1

    def reset(self):
        self.__lives = 5
        self.__score = 0
        self.__level.load(0)


if __name__ == "__main__":
    logging.info("Starting game")
    Breakout().start()
