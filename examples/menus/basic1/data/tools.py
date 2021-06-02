# from .sound import Sound, Music
import pygame as pg
import os
import random


class Sound:
    def __init__(self, filename):
        self.path = os.path.join("resources", "sound")
        self.fullpath = os.path.join(self.path, filename)
        pg.mixer.init(frequency=22050, size=-16, channels=2, buffer=128)
        self.sound = pg.mixer.Sound(self.fullpath)


class Music:
    def __init__(self, volume):
        self.path = os.path.join("resources", "music")
        self.setup(volume)

    def setup(self, volume):
        self.track_end = pg.USEREVENT + 1
        self.tracks = []
        self.track = 0
        for track in os.listdir(self.path):
            self.tracks.append(os.path.join(self.path, track))
        random.shuffle(self.tracks)
        pg.mixer.music.set_volume(volume)
        pg.mixer.music.set_endevent(self.track_end)
        pg.mixer.music.load(self.tracks[0])


class Image:
    path = "resources/graphics"

    @staticmethod
    def load(filename):
        p = os.path.join(Image.path, filename)
        return pg.image.load(os.path.abspath(p))


class Font:
    path = "resources/fonts"

    @staticmethod
    def load(filename, size):
        p = os.path.join(Font.path, filename)
        return pg.font.Font(os.path.abspath(p), size)


class States:
    def __init__(self):
        self.bogus_rect = pg.Surface([0, 0]).get_rect()
        self.screen_rect = self.bogus_rect
        self.button_volume = 0.1
        self.button_sound = Sound("button.wav")
        self.button_sound.sound.set_volume(self.button_volume)
        # self.background_music_volume = .3
        # self.background_music = Music(self.background_music_volume)
        self.bg_color = (25, 25, 25)
        self.timer = 0.0
        self.quit = False
        self.done = False

        self.text_basic_color = (255, 255, 255)
        self.text_hover_color = (255, 0, 0)
        self.text_color = self.text_basic_color

        self.options = ["Menu1", "Menu2", "Quit"]
        self.next_list = ["MENU1", "MENU2"]
        self.selected_index = 0

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
        font = Font.load("arial.ttf", size)
        text = font.render(message, True, color)
        rect = text.get_rect(center=center)
        return text, rect

    def pre_render_options(self):
        font_deselect = Font.load("arial.ttf", 50)
        font_selected = Font.load("arial.ttf", 75)

        rendered_msg = {"des": [], "sel": []}
        for option in self.options:
            d_rend = font_deselect.render(option, 1, (255, 255, 255))
            d_rect = d_rend.get_rect()
            s_rend = font_selected.render(option, 1, (255, 0, 0))
            s_rect = s_rend.get_rect()
            rendered_msg["des"].append((d_rend, d_rect))
            rendered_msg["sel"].append((s_rend, s_rect))
        self.rendered = rendered_msg

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for i, opt in enumerate(self.rendered["des"]):
                if opt[1].collidepoint(pg.mouse.get_pos()):
                    self.selected_index = i
                    self.select_option(i)
                    break
        elif event.type == pg.KEYDOWN:
            if event.key in [pg.K_UP, pg.K_w]:
                self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.change_selected_option(1)
            elif event.key == pg.K_RETURN:
                self.select_option(self.selected_index)

    def select_option(self, i):
        if i == len(self.next_list):
            self.quit = True
        else:
            self.button_sound.sound.play()
            self.next = self.next_list[i]
            self.done = True
            self.selected_index = 0

    def change_selected_option(self, op=0):
        for i, opt in enumerate(self.rendered["des"]):
            if opt[1].collidepoint(pg.mouse.get_pos()):
                self.selected_index = i

        self.selected_index += op
        max_ind = len(self.rendered["des"]) - 1
        if self.selected_index < 0:
            self.selected_index = max_ind
        elif self.selected_index > max_ind:
            self.selected_index = 0

    def render(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.title, self.title_rect)
        for i, opt in enumerate(self.rendered["des"]):
            opt[1].center = (
                self.screen_rect.centerx,
                self.from_bottom + i * self.spacer,
            )
            if i == self.selected_index:
                rend_img, rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img, rend_rect)
            else:
                screen.blit(opt[0], opt[1])
