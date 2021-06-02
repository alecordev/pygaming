import pygame as pg
from .. import tools
import random


class Menu(tools.States):
    def __init__(self, screen_rect):
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.title, self.title_rect = self.make_text(
            "Menu2 State", (75, 75, 75), (self.screen_rect.centerx, 75), 50
        )
        self.pre_render_options()
        self.from_bottom = 200
        self.spacer = 75

    def update(self, now, keys):
        self.change_selected_option()

    def const_event(self, keys):
        pass

    def cleanup(self):
        pass

    def entry(self):
        pass
