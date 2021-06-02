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


class Scout(unit.Unit):
    def __init__(self, coord, team):
        unit.Unit.__init__(self)
        self.type = "settler"
        self.name = "scout"
        self.lifemax = 90
        self.life = 90
        self.attack = "--"
        self.speed = 1
        self.armor = 4
        self.view = 8
        self.level = "--"
        self.uplevel = 0
        self.deaths = 0
        self.animation = 1
        self.attacks = {
            "unit": self.attackunit,
            "planet": self.attackmainbase,
            "defense": self.attackbuilding,
        }
        self.team = team
        self.indexsprite = 0
        self.direction = 0  # 0 bottom, 1 top, 2 right, 3 left
        self.frames = 0
        self.collisionedwith = []
        self.comm = {"move": 0}
        self.target = None
        self.notselected = True
        self.erase = False
        self.alert = False
        self.aggressive = False
        self.landing = False
        self.imagesnotselected = (
            (
                load_image(PATHS["sprites"] + team + "perdix_bottom_0.png"),
                load_image(PATHS["sprites"] + team + "perdix_bottom_1.png"),
            ),
            (
                load_image(PATHS["sprites"] + team + "perdix_top_0.png"),
                load_image(PATHS["sprites"] + team + "perdix_top_1.png"),
            ),
            (
                load_image(PATHS["sprites"] + team + "perdix_right_0.png"),
                load_image(PATHS["sprites"] + team + "perdix_right_1.png"),
            ),
            (
                load_image(PATHS["sprites"] + team + "perdix_left_0.png"),
                load_image(PATHS["sprites"] + team + "perdix_left_1.png"),
            ),
        )
        self.imageselected = (
            (
                load_image(PATHS["sprites"] + team + "perdixselected_bottom_0.png"),
                load_image(PATHS["sprites"] + team + "perdixselected_bottom_1.png"),
            ),
            (
                load_image(PATHS["sprites"] + team + "perdixselected_top_0.png"),
                load_image(PATHS["sprites"] + team + "perdixselected_top_1.png"),
            ),
            (
                load_image(PATHS["sprites"] + team + "perdixselected_right_0.png"),
                load_image(PATHS["sprites"] + team + "perdixselected_right_1.png"),
            ),
            (
                load_image(PATHS["sprites"] + team + "perdixselected_left_0.png"),
                load_image(PATHS["sprites"] + team + "perdixselected_left_1.png"),
            ),
        )
        self.animation2 = (
            load_image(PATHS["sprites"] + team + "perdix_75.png"),
            load_image(PATHS["sprites"] + team + "perdix_50.png"),
            load_image(PATHS["sprites"] + team + "perdix_25.png"),
        )
        self.animation1 = (self.animation2[2], self.animation2[1], self.animation2[0])
        self.image = self.animation1[0]
        self.rect = self.imagesnotselected[0][0].get_rect()
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
                self.image = self.imagesnotselected[self.direction][self.indexsprite]
            else:
                self.image = self.imageselected[self.direction][self.indexsprite]
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
        mov = (self.bottom, self.top, self.right, self.left)
        listmov = []
        x, y = self.moveto
        if self.rect.centerx < x:
            listmov.append(2)
        if self.rect.centerx > x:
            listmov.append(3)
        if self.rect.centery < y:
            listmov.append(0)
        if self.rect.centery > y:
            listmov.append(1)
        for i in listmov:
            mov[i]()

    def reply(self, enemy):
        fx, fy = 0, 0
        x, y = enemy.rect.center
        if self.rect.centerx > x:
            fx = self.rect.centerx + 100
        if self.rect.centerx < x:
            fx = self.rect.centerx - 100
        if self.rect.centery > y:
            fy = self.rect.centery + 100
        if self.rect.centery < y:
            fy = self.rect.centery - 100
        self.moveto = fx, fy
        self.alert = True

    def attackmainbase(self):
        if self.target.open:
            if not self.landing:
                self.animation = 2
                self.speed = 3
                self.target.landings[0] += 1
                self.landing = True
                if self.target.color == "c":
                    if self.team == "a":
                        self.target.settler += 1
                    else:
                        self.target.settler -= 1

    def proportionlevel(self, n):
        return n

    def top(self):
        self.rect.centery -= self.speed
        self.direction = 1

    def bottom(self):
        self.rect.centery += self.speed
        self.direction = 0

    def right(self):
        self.rect.centerx += self.speed
        self.direction = 2

    def left(self):
        self.rect.centerx -= self.speed
        self.direction = 3
