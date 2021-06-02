import pygame as pg
from .. import tools
import random


class Menu(tools.States):
    def __init__(self, screen_rect):
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.options = ["Play", "Quit"]
        self.next_list = ["GAME"]
        self.title, self.title_rect = self.make_text(
            "Menu State", (75, 75, 75), (self.screen_rect.centerx, 75), 150
        )
        self.pre_render_options()
        self.from_bottom = 200
        self.spacer = 75

    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for i, opt in enumerate(self.rendered["des"]):
                if opt[1].collidepoint(pg.mouse.get_pos()):
                    if i == len(self.next_list):
                        self.quit = True
                    else:
                        self.button_sound.sound.play()
                        self.next = self.next_list[i]
                        self.done = True
                    break

    def update(self, now, keys):
        pg.mouse.set_visible(True)
        if self.quit:
            return True

    def render(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.title, self.title_rect)
        for i, opt in enumerate(self.rendered["des"]):
            opt[1].center = (
                self.screen_rect.centerx,
                self.from_bottom + i * self.spacer,
            )
            if opt[1].collidepoint(pg.mouse.get_pos()):
                rend_img, rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img, rend_rect)
            else:
                screen.blit(opt[0], opt[1])

    def make_text(self, message, color, center, size):
        font = tools.Font.load("arial.ttf", size)
        text = font.render(message, True, color)
        rect = text.get_rect(center=center)
        return text, rect

    def pre_render_options(self):
        font_deselect = tools.Font.load("arial.ttf", 50)
        font_selected = tools.Font.load("arial.ttf", 75)

        rendered_msg = {"des": [], "sel": []}
        for option in self.options:
            d_rend = font_deselect.render(option, 1, (255, 255, 255))
            d_rect = d_rend.get_rect()
            s_rend = font_selected.render(option, 1, (255, 0, 0))
            s_rect = s_rend.get_rect()
            rendered_msg["des"].append((d_rend, d_rect))
            rendered_msg["sel"].append((s_rend, s_rect))
        self.rendered = rendered_msg

    def const_event(self, keys):
        pass

    def cleanup(self):
        pass

    def entry(self):
        pass
