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
