try:
    import pygame
    from pygame.locals import *
    from functions import *
    from sounds import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")
    raise SystemExit("Error al importar los modulos")


class MainBuilding(pygame.sprite.DirtySprite):
    def __init__(self, coord, color, priority=None):
        pygame.sprite.DirtySprite.__init__(self)
        self.type = "planet"
        self.name = "Base"
        self.lifemax = 1
        self.life = 1
        self.attack = 0
        self.speed = 0
        self.armor = 0
        self.view = 5
        self.color = color
        self.landings = [0, 20]
        self.settler = 0
        self.owner = None
        self.image = load_image(PATHS["sprites"] + color + "core.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = coord
        self.target = None
        self.notselected = True
        self.collisionedwith = []
        self.dirty = 2
        if self.color != "c":
            self.comm = {
                "scout": 0,
                "square": 0,
                "star": 0,
                "gunner": 0,
                "offensive": 0,
            }
            self.open = False
        else:
            self.comm = {"square": 0, "star": 0, "gunner": 0, "offensive": 0}
            self.open = True
        self.erase = False
        self.alert = False
        self.aggressive = False
        self.priority = priority

    def update(self):
        if self.color == "c":
            if self.settler > 0:
                self.owner = "a"
            elif self.settler < 0:
                self.owner = "b"
            else:
                self.owner = None
        else:
            if self.landings[0] >= self.landings[1]:
                self.life = 0

    def attack(self):
        return None

    def toString(self):
        return None

    def proportionlife(self, n):
        toret = n * self.life // self.lifemax
        toret = 0 if toret < 0 else toret
        return toret

    def proportionlevel(self, n):
        return n

    def percent(self):
        return 100 * self.life // self.lifemax

    def stop(self):
        return None
