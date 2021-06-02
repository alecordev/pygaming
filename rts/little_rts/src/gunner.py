try:
    import random
    import pygame
    import bullet
    import unit
    from pygame.locals import *
    from functions import *
    from sounds import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")
    raise SystemExit("Error al importar los modulos")


class Gunner(unit.Unit):
    def __init__(self, coord, team):
        unit.Unit.__init__(self)
        self.type = "unit"
        self.name = "Gunner"
        self.lifemax = 75
        self.life = 75
        self.attack = 10
        self.speed = 3
        self.armor = 1
        self.view = 6
        self.level = [1, 3]
        self.deaths = 0
        self.animation = 1
        self.indexsprite = 0
        self.frames = 0
        self.moveto = coord
        self.collisionedwith = []
        self.comm = {"move": 0, "passive": 0, "aggressive": 1}
        self.target = None
        self.notselected = True
        self.bullet = None
        self.erase = False
        self.alert = False
        self.aggressive = True
        self.landing = False
        self.imagesnotselected = (
            load_image(PATHS["sprites"] + team + "gunner.gif"),
            load_image(PATHS["sprites"] + team + "gunner_1.gif"),
        )
        self.imageselected = (
            load_image(PATHS["sprites"] + team + "selected_gunner.gif"),
            load_image(PATHS["sprites"] + team + "selected_gunner_1.gif"),
        )
        self.attacks = {
            "unit": self.attackunit,
            "settler": self.attackunit,
            "planet": self.attackmainbase,
            "defense": self.attackunit,
        }
        self.animation2 = (
            load_image(PATHS["sprites"] + team + "gunner_75.png"),
            load_image(PATHS["sprites"] + team + "gunner_50.png"),
            load_image(PATHS["sprites"] + team + "gunner_25.png"),
        )
        self.animation1 = (self.animation2[2], self.animation2[1], self.animation2[0])
        self.image = self.animation1[0]
        self.rect = self.imagesnotselected[0].get_rect()
        self.rect.center = coord
        x, y = random.randint(0, 50), random.randint(0, 50)
        self.moveto = (self.rect.centerx + x, self.rect.centery + y)

    def update(self):
        def animation(unit):
            images = unit.animation1 if unit.animation == 1 else unit.animation2
            unit.frames += 1
            if unit.frames == 30:
                unit.frames = 0
                unit.indexsprite += 1
                if unit.indexsprite == 3:
                    if self.animation == 2:
                        self.erase = True
                    self.animation = 0
                    self.indexsprite = 0
                    self.frames = 0
                    return None
            unit.image = images[unit.indexsprite]

        if self.animation:
            animation(self)
        else:
            if self.notselected:
                self.image = self.imagesnotselected[self.indexsprite]
            else:
                self.image = self.imageselected[self.indexsprite]
            self.frames += 1
            if self.frames == 29:
                self.indexsprite = (self.indexsprite + 1) % 2
                self.frames = 0
        self.move()
        self.bullet.update()

    def move(self):
        if self.target:
            if not self.attacks[self.target.type]():
                self.moveto = self.target.rect.center
            else:
                return None
        x, y = self.moveto
        if self.rect.centerx < x:
            self.rect.centerx += self.speed
        if self.rect.centerx > x:
            self.rect.centerx -= self.speed
        if self.rect.centery < y:
            self.rect.centery += self.speed
        if self.rect.centery > y:
            self.rect.centery -= self.speed

    def attackunit(self):
        if self.view * 100 >= distance(self.rect, self.target.rect):
            self.bullet.target = self.target
            return True
        self.bullet.target = None
        return False

    def attackbuilding(self):
        return None

    def attackmainbase(self):
        return False
