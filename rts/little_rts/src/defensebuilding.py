try:
    import pygame
    from pygame.locals import *
    from functions import *
    from sounds import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")
    raise SystemExit("Error al importar los modulos")


class Defensebuilding(pygame.sprite.DirtySprite):
    def __init__(self, coord, team):
        pygame.sprite.DirtySprite.__init__(self)
        self.type = "defense"
        self.name = "Shield"
        self.lifemax = 500
        self.life = 500
        self.attack = 30
        self.speed = "--"
        self.armor = 5
        self.view = 8
        self.level = None
        self.deaths = 0
        self.image = load_image(PATHS["sprites"] + team + "defensebuilding.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = coord
        self.target = None
        self.notselected = True
        self.collisionedwith = []
        self.comm = {}
        self.open = False
        self.erase = False
        self.alert = False
        self.aggressive = True
        self.bullet = None
        self.dirty = 2

    def update(self):
        if self.target:
            self.bullet.target = self.target
        self.bullet.update()

    def uplevel(self):
        return None

    def attack(self):
        return None

    def reply(self, enemy):
        if not self.target:
            self.target = enemy
        self.alert = True

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
