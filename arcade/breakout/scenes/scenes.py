import logging

import pygame

from shared import game as core
from scenes import scenes


class Scene:
    def __init__(self, game):
        self.__game = game
        self.__texts = []

    def render(self):
        for text in self.__texts:
            self.__game.screen.blit(text[0], text[1])

    def get_game(self):
        return self.__game

    def handle_events(self, events):
        pass

    def clear_text(self):
        self.__texts = []

    def add_text(
        self, string, x=0, y=0, color=(255, 255, 255), background=(0, 0, 0), size=17
    ):
        font = pygame.font.Font(None, size)  # default font
        self.__texts.append([font.render(string, True, color, background), (x, y)])


class PlayingGameScene(Scene):
    def __init__(self, game):
        super().__init__(game)

    def render(self):
        super().render()

        game = self.get_game()
        level = game.get_level()
        balls = game.get_balls()

        if level.get_pending_bricks() <= 0:
            for ball in balls:
                ball.set_motion(False)

            level.load_next_level()

        if game.get_lives() <= 0:
            game.play_sound(core.GameConstants.SOUND_GAMEOVER)
            game.change_scene(core.GameConstants.GAMEOVER_SCENE)

        pad = game.get_pad()

        for ball in balls:

            # Collision and logic between multiple balls
            for ball2 in balls:
                if ball != ball2 and ball.intersects(ball2):
                    ball.change_direction(ball2)

            for brick in game.get_level().get_bricks():
                if not brick.is_destroyed() and ball.intersects(brick):
                    game.play_sound(brick.get_hit_sound())
                    brick.hit()
                    level.brick_hit()
                    game.increase_score(brick.get_hit_points())
                    ball.change_direction(brick)
                    break

            if ball.intersects(pad):
                game.play_sound(core.GameConstants.SOUND_HIT_PAD)
                ball.change_direction(pad)

            ball.update_position()

            if ball.is_ball_dead():
                ball.set_motion(0)
                game.reduce_lives()

            game.screen.blit(ball.get_sprite(), ball.get_position())

        for brick in game.get_level().get_bricks():
            if not brick.is_destroyed():
                game.screen.blit(brick.get_sprite(), brick.get_position())

        pad.set_position((pygame.mouse.get_pos()[0], pad.get_position()[1]))
        game.screen.blit(pad.get_sprite(), pad.get_position())

        self.clear_text()
        self.add_text(
            f"Your score: {game.get_score()}",
            x=0,
            y=core.GameConstants.SCREEN_SIZE[1] - 60,
            size=30,
        )

        self.add_text(
            f"Lives: {game.get_lives()}",
            x=0,
            y=core.GameConstants.SCREEN_SIZE[1] - 30,
            size=30,
        )

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for ball in self.get_game().get_balls():
                    ball.set_motion(True)


class GameOverScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.__player_name = ""
        self.__highscore_sprite = pygame.image.load(core.GameConstants.SPRITE_HIGHSCORE)

    def render(self):
        self.get_game().screen.blit(self.__highscore_sprite, (50, 50))

        self.clear_text()
        self.add_text("Your name: ", 300, 200, size=30)
        self.add_text(self.__player_name, 420, 200, size=30)
        # self.add_text('Press F1 to restart the game', 400, 400, size=30)
        super().render()

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game = self.get_game()
                    core.Highscore().add(self.__player_name, game.get_score())
                    game.reset()
                    game.change_scene(core.GameConstants.HIGHSCORE_SCENE)
                elif 65 <= event.key <= 122:
                    self.__player_name += chr(event.key)
                if event.key == pygame.K_F1:
                    self.get_game().reset()
                    self.get_game().change_scene(core.GameConstants.PLAYING_SCENE)


class HighscoreScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.__highscore_sprite = pygame.image.load(core.GameConstants.SPRITE_HIGHSCORE)

    def render(self):
        self.get_game().screen.blit(self.__highscore_sprite, (50, 50))
        self.clear_text()
        highscore = core.Highscore()

        x = 350
        y = 100
        for score in highscore.get_score():
            self.add_text(score[0], x, y, size=30)
            self.add_text(str(score[0]), x + 200, y, size=30)

            y += 30

        self.add_text("Press F1 to start a new game", x, y + 60, size=30)

        super().render()

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.get_game().reset()
                    self.get_game().change_scene(core.GameConstants.PLAYING_SCENE)


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.add_text("F1 - Start Game", x=300, y=200, size=30)
        self.add_text("F2 - Highscore", x=300, y=240, size=30)
        self.add_text("F3 - Quit Game", x=300, y=280, size=30)

        self.__menu_sprite = pygame.image.load(core.GameConstants.SPRITE_MENU)

    def render(self):
        self.get_game().screen.blit(self.__menu_sprite, (50, 50))
        super().render()

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_F1:
                    self.get_game().change_scene(core.GameConstants.PLAYING_SCENE)
                if event.key == pygame.K_F2:
                    self.get_game().change_scene(core.GameConstants.HIGHSCORE_SCENE)
                if event.key == pygame.K_F3:
                    exit()
