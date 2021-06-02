try:
    import random
    import pygame
    from pygame.locals import *
    from functions import *
    from sounds import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")
    raise SystemExit("Error al importar los modulos")


class Unit(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2

    def update(self):
        pass

    def move(self):
        pass

    def stop(self):
        self.moveto = self.rect.center

    def attackunit(self):
        pass

    def attackbuilding(self):
        pass

    def attackmainbase(self):
        pass

    def reply(self, enemy):
        if not self.target:
            self.target = enemy
        else:
            if distance(self.rect, self.target.rect) > distance(self.rect, enemy.rect):
                self.target = enemy
        self.alert = True

    def uplevel(self):
        self.deaths += 1
        if self.deaths == self.level[1]:
            self.deaths = 0
            self.level[0] += 1
            self.life = self.lifemax
            self.attack += 10
            self.speed += 1

    def proportionlife(self, n):
        return n * self.life // self.lifemax

    def proportionlevel(self, n):
        return n * self.deaths // self.level[1]

    def percent(self):
        return 100 * self.life // self.lifemax
