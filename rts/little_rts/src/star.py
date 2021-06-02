try:
    import random
    import pygame
    import unit
    from pygame.locals import *
    from functions import *
    from sounds import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")
    raise SystemExit("Error al importar los modulos")


class Star(unit.Unit):
    def __init__(self, coord, team):
        unit.Unit.__init__(self)
        self.type = "unit"
        self.name = "Fast"
        self.lifemax = 100
        self.life = 100
        self.attack = 10
        self.speed = 6
        self.armor = 5
        self.view = 5
        self.level = [1, 3]
        self.deaths = 0
        self.indexsprite = 0
        self.frames = 0
        self.collisionedwith = []
        self.comm = {"move": 0, "passive": 0, "aggressive": 1}
        self.target = None
        self.erase = False
        self.alert = False
        self.aggressive = True
        self.notselected = True
        self.landing = False
        self.imagesnotselected = (
            load_image(PATHS["sprites"] + team + "star.png"),
            load_image(PATHS["sprites"] + team + "star_1.png"),
        )
        self.imageselected = (
            load_image(PATHS["sprites"] + team + "star_selected.png"),
            load_image(PATHS["sprites"] + team + "star_selected_1.png"),
        )
        self.animation2 = (
            load_image(PATHS["sprites"] + team + "star_75.png"),
            load_image(PATHS["sprites"] + team + "star_50.png"),
            load_image(PATHS["sprites"] + team + "star_25.png"),
        )
        self.animation1 = (self.animation2[2], self.animation2[1], self.animation2[0])
        self.animation = 1
        self.attacks = {
            "unit": self.attackunit,
            "settler": self.attackunit,
            "planet": self.attackmainbase,
            "defense": self.attackbuilding,
        }
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

    def move(self):
        if self.target:
            if self.target.life <= 0:
                self.target = None
            else:
                self.moveto = self.target.rect.center
                if self.target in self.collisionedwith:
                    self.attacks[self.target.type]()
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
        playsound("attack")
        self.target.reply(self)
        if self.target.name == "Defensinve":
            self.target.life -= self.attack + 3 - self.target.armor
        else:
            self.target.life -= self.attack - self.target.armor
        if self.target.life <= 0:
            self.target.life = 0
            self.uplevel()
            self.stop()
            self.target = None
            return None
        if self.target.rect.centery < self.rect.centery:
            self.target.rect.centery -= 50
        if self.target.rect.centery > self.rect.centery:
            self.target.rect.centery += 50
        if self.target.rect.centerx < self.rect.centerx:
            self.target.rect.centerx -= 50
        if self.target.rect.centerx > self.rect.centerx:
            self.target.rect.centerx += 50
        self.target.stop()

    def attackbuilding(self):
        playsound("attack")
        self.target.reply(self)
        self.target.life -= self.attack - self.target.armor
        if self.target.life <= 0:
            self.target.life = 0
            self.uplevel()
            self.stop()
            self.target = None
            return None
        if self.target.rect.centery > self.rect.centery:
            self.rect.centery -= 50
        if self.target.rect.centery < self.rect.centery:
            self.rect.centery += 50
        if self.target.rect.centerx > self.rect.centerx:
            self.rect.centerx -= 50
        if self.target.rect.centerx < self.rect.centerx:
            self.rect.centerx += 50
        self.stop()

    def attackmainbase(self):
        pass
