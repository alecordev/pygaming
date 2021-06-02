import pygame as pg
from .. import tools
import random


class Game(tools.States):
    def __init__(self, screen_rect):
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.score_text, self.score_rect = self.make_text(
            "Game State", (255, 255, 255), (screen_rect.centerx, 100), 50
        )
        self.pause_text, self.pause_rect = self.make_text(
            "PAUSED", (255, 255, 255), screen_rect.center, 50
        )

        # game specific content
        self.bg_color = (0, 0, 0)
        self.pause = False

        paddle_width = 10
        paddle_height = 100
        paddle_y = self.screen_rect.centery - (paddle_height // 2)
        padding = 25  # padding from wall
        pad_right = screen_rect.width - paddle_width - padding

    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.button_sound.sound.play()
                self.done = True
                self.next = "MENU"
            elif event.key == pg.K_p:
                self.pause = not self.pause
        # elif event.type == self.background_music.track_end:
        #    self.background_music.track = (self.background_music.track+1) % len(self.background_music.tracks)
        #    pg.mixer.music.load(self.background_music.tracks[self.background_music.track])
        #    pg.mixer.music.play()

    def movement(self, keys):
        pass

    def update(self, now, keys):
        if not self.pause:
            pass
        else:
            self.pause_text, self.pause_rect = self.make_text(
                "PAUSED", (255, 255, 255), self.screen_rect.center, 50
            )
        self.movement(keys)
        if self.quit:
            return True

    def render(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.score_text, self.score_rect)
        if self.pause:
            screen.blit(self.pause_text, self.pause_rect)

    def make_text(self, message, color, center, size):
        font = tools.Font.load("arial.ttf", size)
        text = font.render(message, True, color)
        rect = text.get_rect(center=center)
        return text, rect

    def adjust_score(self, hit_side):
        if hit_side == -1:
            self.score[1] += 1
        elif hit_side == 1:
            self.score[0] += 1

    def const_event(self, keys):
        pass

    def cleanup(self):
        pass
        # pg.mixer.music.stop()
        # self.background_music.setup(self.background_music_volume)

    def entry(self):
        pass
        # pg.mixer.music.play()
