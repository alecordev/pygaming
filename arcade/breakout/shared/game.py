import hashlib
import operator
import os
import logging
import random

import pygame

from shared import game
from scenes import scenes


class GameConstants:
    SCREEN_SIZE = (800, 600)
    BRICK_SIZE = (100, 30)
    BALL_SIZE = (16, 16)
    PAD_SIZE = (139, 13)

    SPRITE_BALL = os.path.join("res", "ball.png")
    SPRITE_PAD = os.path.join("res", "pad.png")
    SPRITE_BRICK = os.path.join("res", "standard.png")
    SPRITE_SPEEDBRICK = os.path.join("res", "speed.png")
    SPRITE_LIFEBRICK = os.path.join("res", "life.png")
    SPRITE_HIGHSCORE = os.path.join("res", "highscore.png")
    SPRITE_MENU = os.path.join("res", "menu.png")

    SOUND_FILE_HIT_BRICK = os.path.join("res", "BrickHit.wav")
    SOUND_FILE_HIT_BRICK_LIFE = os.path.join("res", "ExtraLife.wav")
    SOUND_FILE_HIT_BRICK_SPEED = os.path.join("res", "SpeedUp.wav")
    SOUND_FILE_HIT_WALL = os.path.join("res", "WallBounce.wav")
    SOUND_FILE_HIT_PAD = os.path.join("res", "PadBounce.wav")
    SOUND_FILE_GAMEOVER = os.path.join("res", "GameOver.wav")

    SOUND_GAMEOVER = 0
    SOUND_HIT_BRICK = 1
    SOUND_HIT_BRICK_LIFE = 2
    SOUND_HIT_BRICK_SPEED = 3
    SOUND_HIT_WALL = 4
    SOUND_HIT_PAD = 5

    PLAYING_SCENE = 0
    GAMEOVER_SCENE = 1
    HIGHSCORE_SCENE = 2
    MENU_SCENE = 3


class GameObject:
    def __init__(self, position, size, sprite):
        self.__position = position
        self.__size = size
        self.__sprite = sprite

    def set_position(self, position):
        self.__position = position

    def get_position(self):
        return self.__position

    def get_size(self):
        return self.__size

    def get_sprite(self):
        return self.__sprite

    def intersects(self, other):
        if self.__intersects_y(other) and self.__intersects_x(other):
            return True
        return False

    def __intersects_x(self, other):
        other_position = other.get_position()
        other_size = other.get_size()

        if (
            self.__position[0] >= other_position[0]
            and self.__position[0] <= other_position[0] + other_size[0]
        ):
            return True
        if (self.__position[0] + self.__size[0]) > other_position[0] and (
            self.__position[0] + self.__size[0]
        ) < (other_position[0] + other_size[0]):
            return True

        return False

    def __intersects_y(self, other):
        other_position = other.get_position()
        other_size = other.get_size()

        if (
            self.__position[1] >= other_position[1]
            and self.__position[1] <= other_position[1] + other_size[1]
        ):
            return True
        if (self.__position[1] + self.__size[1]) > other_position[1] and (
            self.__position[1] + self.__size[1]
        ) <= (other_position[1] + other_size[1]):
            return True

        return False


class Brick(GameObject):
    def __init__(self, position, sprite, game):
        self.__game = game
        self.__hit_points = 100
        self.__lives = 1
        super(Brick, self).__init__(position, GameConstants.BRICK_SIZE, sprite)

    def get_game(self):
        return self.__game

    def is_destroyed(self):
        return self.__lives <= 0

    def get_hit_points(self):
        return self.__hit_points

    def hit(self):
        self.__lives -= 1

    def get_hit_sound(self):
        return GameConstants.SOUND_HIT_BRICK


class LifeBrick(Brick):
    def __init__(self, position, sprite, game):
        super().__init__(position, sprite, game)

    def hit(self):
        game = self.get_game()
        game.increase_lives()

        super().hit()

    def get_hit_sound(self):
        return GameConstants.SOUND_HIT_BRICK_LIFE


class SpeedBrick(Brick):
    def __init__(self, position, sprite, game):
        super().__init__(position, sprite, game)

    def hit(self):
        game = self.get_game()

        for ball in game.get_balls():
            ball.set_speed(ball.get_speed() + 1)

        super().hit()

    def get_hit_sound(self):
        return GameConstants.SOUND_HIT_BRICK_SPEED


class Ball(GameObject):
    def __init__(self, position, sprite, game):
        self.__game = game
        self.__speed = 3
        self.__increment = [2, 2]
        self.__direction = [1, 1]
        self.__in_motion = False

        super().__init__(position, GameConstants.BALL_SIZE, sprite)

    def set_speed(self, new_speed):
        self.__speed = new_speed

    def reset_speed(self):
        self.set_speed(3)

    def get_speed(self):
        return self.__speed

    def is_in_motion(self):
        return self.__in_motion

    def set_motion(self, is_moving):
        self.__in_motion = is_moving
        self.reset_speed()

    def change_direction(self, game_object):
        position = self.get_position()
        size = self.get_size()
        object_position = game_object.get_position()
        object_size = game_object.get_size()

        if (
            position[1] > object_position[1]
            and position[1] < (object_position[1] + object_position[1])
            and position[0] > object_position[0]
            and position[0] < object_position[0] + object_size[1]
        ):
            self.set_position((position[0], object_position[1] + object_size[1]))
            self.__direction[1] *= -1

        elif (
            position[1] + size[1] > object_position[1]
            and position[1] + size[1] < (object_position[1] + object_size[1])
            and position[0] > object_position[0]
            and position[0] < (object_position[0] + object_size[0])
        ):
            self.set_position((position[0], object_position[1] - object_size[1]))
            self.__direction[1] *= -1

        elif (
            position[0] + size[0] > object_position[0]
            and position[0] + size[0] < object_position[0] + object_size[0]
        ):
            self.set_position((object_position[0] - size[0], position[1]))
            self.__direction[0] *= -1

        else:
            self.set_position((object_position[0] + object_size[0], position[1]))
            self.__direction[0] *= -1
            self.__direction[1] *= -1

    def update_position(self):
        # self.set_position(pygame.mouse.get_pos())

        if not self.is_in_motion():
            pad_position = self.__game.get_pad().get_position()
            self.set_position(
                (
                    pad_position[0] + (GameConstants.PAD_SIZE[0] / 2),
                    GameConstants.SCREEN_SIZE[1]
                    - GameConstants.PAD_SIZE[1]
                    - GameConstants.BALL_SIZE[1],
                )
            )
            return

        position = self.get_position()
        size = self.get_size()

        new_position = [
            position[0] + (self.__increment[0] * self.__speed) * self.__direction[0],
            position[1] + (self.__increment[1] * self.__speed) * self.__direction[1],
        ]

        if new_position[0] + size[0] >= GameConstants.SCREEN_SIZE[0]:
            self.__direction[0] *= -1
            new_position = [GameConstants.SCREEN_SIZE[0] - size[0], new_position[1]]
            self.__game.play_sound(GameConstants.SOUND_HIT_WALL)

        if new_position[0] <= 0:
            self.__direction[0] *= -1
            new_position = [0, new_position[1]]
            self.__game.play_sound(GameConstants.SOUND_HIT_WALL)

        if new_position[1] + size[1] >= GameConstants.SCREEN_SIZE[1]:
            self.__direction[1] *= -1
            new_position = [new_position[0], GameConstants.SCREEN_SIZE[1] - size[1]]

        if new_position[1] <= 0:
            self.__direction[1] *= -1
            new_position = [new_position[0], 0]
            self.__game.play_sound(GameConstants.SOUND_HIT_WALL)

        self.set_position(new_position)

    def is_ball_dead(self):
        position = self.get_position()
        size = self.get_size()

        if position[1] + size[1] >= GameConstants.SCREEN_SIZE[1]:
            return True

        return False


class Pad(GameObject):
    def __init__(self, position, sprite):
        super().__init__(position, GameConstants.PAD_SIZE, sprite)

    def set_position(self, position):
        new_position = [position[0], position[1]]
        size = self.get_size()

        if new_position[0] + size[0] > GameConstants.SCREEN_SIZE[0]:
            new_position[0] = GameConstants.SCREEN_SIZE[0] - size[0]

        super().set_position(new_position)


class Level:
    def __init__(self, game):
        self.__game = game
        self.__bricks = []
        self.__pending_bricks = 0
        self.__current_level = 0

    def get_bricks(self):
        return self.__bricks

    def get_pending_bricks(self):
        return self.__pending_bricks

    def brick_hit(self):
        self.__pending_bricks -= 1

    def load_next_level(self):
        self.__current_level += 1
        file_name = os.path.join("res", "levels", f"level{self.__current_level}.dat")

        if not os.path.exists(file_name):
            self.load_random()
        else:
            self.load(self.__current_level)

    def load_random(self):
        self.__bricks = []

        x, y = 0, 0

        max_bricks = int(GameConstants.SCREEN_SIZE[0] / GameConstants.BRICK_SIZE[0])
        rows = random.randint(2, 8)

        amount_of_super_power_bricks = 0

        for row in range(0, rows):
            for brick in range(0, max_bricks):
                brick_type = random.randint(0, 3)

                if brick_type == 1 or amount_of_super_power_bricks >= 2:
                    brick = Brick(
                        (x, y),
                        pygame.image.load(GameConstants.SPRITE_BRICK),
                        self.__game,
                    )
                    self.__bricks.append(brick)
                    self.__pending_bricks += 1

                elif brick_type == 2:
                    brick = Brick(
                        (x, y),
                        pygame.image.load(GameConstants.SPRITE_SPEEDBRICK),
                        self.__game,
                    )
                    self.__bricks.append(brick)
                    self.__pending_bricks += 1
                    amount_of_super_power_bricks += 1

                elif brick_type == 3:
                    brick = Brick(
                        (x, y),
                        pygame.image.load(GameConstants.SPRITE_LIFEBRICK),
                        self.__game,
                    )
                    self.__bricks.append(brick)
                    self.__pending_bricks += 1
                    amount_of_super_power_bricks += 1

                x += GameConstants.BRICK_SIZE[0]  # x position of the brick

            x = 0
            y += GameConstants.BRICK_SIZE[1]

    def load(self, level):
        self.__current_level = level
        self.__bricks = []

        x, y = 0, 0
        with open(os.path.join("res", "levels", f"level{level}.dat"), "r") as f:
            for line in f:
                logging.debug(f"Processing {line} from level{level}...")
                for current_brick in line:
                    if current_brick == "1":
                        brick = Brick(
                            (x, y),
                            pygame.image.load(GameConstants.SPRITE_BRICK),
                            self.__game,
                        )
                        self.__bricks.append(brick)
                        self.__pending_bricks += 1

                    elif current_brick == "2":
                        brick = Brick(
                            (x, y),
                            pygame.image.load(GameConstants.SPRITE_SPEEDBRICK),
                            self.__game,
                        )
                        self.__bricks.append(brick)
                        self.__pending_bricks += 1

                    elif current_brick == "3":
                        brick = Brick(
                            (x, y),
                            pygame.image.load(GameConstants.SPRITE_LIFEBRICK),
                            self.__game,
                        )
                        self.__bricks.append(brick)
                        self.__pending_bricks += 1

                    x += GameConstants.BRICK_SIZE[0]  # x position of the brick

                x = 0
                y += GameConstants.BRICK_SIZE[1]


class Highscore:
    def __init__(self):
        self.__highscore = self.load()

    def get_score(self):
        return self.__highscore

    def load(self):
        highscore = []
        if not os.path.exists("highscore.dat"):
            with open("highscore.dat", "w") as f:
                f.write("")
        with open("highscore.dat", "r") as f:
            for line in f:
                name, score, md5 = line.split("[::]")
                md5 = md5.replace("\n", "")

                if str(
                    hashlib.md5(str.encode(str(name + score + "pygame"))).hexdigest()
                ) == str(md5):
                    highscore.append([str(name), int(score), str(md5)])

            highscore.sort(key=operator.itemgetter(1), reverse=True)
            highscore = highscore[0:11]

            return highscore

    def add(self, name, score):
        hash_ = hashlib.md5((str(name + str(score) + "pygame")).encode("utf-8"))
        self.__highscore.append([name, str(score), hash_.hexdigest()])

        with open("highscore.dat", "w") as f:
            for name, score, md5 in self.__highscore:
                f.write(f"{name}[::]{score}[::]{md5}\n")
