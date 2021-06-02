try:
    import pygame
    import map
    from pygame.locals import *
    from functions import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")


class Interface:
    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        self.window = pygame.display.set_mode(GUISIZE)
        self.map = map.Map()
        self.teams = None
        self.click = []
        self.font30 = pygame.font.Font(path(PATHS["fonts"] + "qgear.ttf"), 30)
        self.font14 = pygame.font.Font(path(PATHS["fonts"] + "qgear.ttf"), 14)
        self.font12 = pygame.font.Font(path(PATHS["fonts"] + "qgear.ttf"), 12)
        self.font10 = pygame.font.Font(path(PATHS["fonts"] + "qgear.ttf"), 10)
        self.backinfo = [
            load_image(PATHS["menus"] + "backgroundinfo.png", False),
            load_image(PATHS["menus"] + "backgroundinfo.png", False),
        ]
        self.backcomm = [
            load_image(PATHS["menus"] + "backgroundcomm.png", False),
            load_image(PATHS["menus"] + "backgroundcomm.png", False),
        ]
        self.backresor = [
            load_image(PATHS["menus"] + "backgroundresource.png", False),
            load_image(PATHS["menus"] + "backgroundresource.png", False),
        ]
        self.windowrects = (
            (pygame.Rect(ACTWINDPOS, ACTWINDSIZE), self.clickinactwin),
            (pygame.Rect(MINIMAPOS, MINIMASIZE), self.clickinminimap),
            (pygame.Rect(COMMPOS, COMMSIZE), self.clickincommwin),
        )
        self.drawinfos = {
            "unit": self.drawinfounit,
            "settler": self.drawinfounit,
            "planet": self.drawinfoplanet,
            "defense": self.drawinfodefense,
            "bullet": self.drawinfobullet,
        }
        self.commbuttons = {
            "move": {0: load_image(PATHS["menus"] + "commgoto.png", True)},
            "passive": {
                0: load_image(PATHS["menus"] + "passive_0.png", True),
                1: load_image(PATHS["menus"] + "passive_1.png", True),
            },
            "aggressive": {
                0: load_image(PATHS["menus"] + "agressive_0.png", True),
                1: load_image(PATHS["menus"] + "agressive_1.png", True),
            },
            "scout": {0: load_image(PATHS["menus"] + "perdix.png", True)},
            "square": {0: load_image(PATHS["menus"] + "square.png", True)},
            "star": {0: load_image(PATHS["menus"] + "star.png", True)},
            "gunner": {0: load_image(PATHS["menus"] + "gunner.png", True)},
            "offensive": {0: load_image(PATHS["menus"] + "offensive.png", True)},
        }
        self.buttonrects = {
            "move": pygame.Rect((2, 2), (82, 82)),
            "scout": pygame.Rect((2, 2), (82, 82)),
            "square": pygame.Rect((85, 2), (82, 82)),
            "star": pygame.Rect((167, 2), (82, 82)),
            "passive": pygame.Rect((85, 85), (82, 82)),
            "aggressive": pygame.Rect((167, 85), (82, 82)),
            "gunner": pygame.Rect((2, 85), (82, 82)),
            "offensive": pygame.Rect((85, 85), (82, 82)),
        }
        self.buttonactions = {
            "passive": self.setpassive,
            "aggressive": self.setagressive,
            "scout": self.basebutton1,
            "square": self.basebutton2,
            "star": self.basebutton3,
            "gunner": self.basebutton4,
            "offensive": self.basebutton5,
        }
        self.helpinfo = {
            "scout": self.font10.render("Create Scout cost 100", False, WHITE),
            "square": self.font10.render("Create Defensive cost 300", False, WHITE),
            "star": self.font10.render("Create Fast cost 150", False, WHITE),
            "move": self.font10.render("Mover unidad seleccionada a", False, WHITE),
            "passive": self.font10.render("Cambiar a actitud pasiva", False, WHITE),
            "aggressive": self.font10.render(
                "Cambiar a actitud agresiva", False, WHITE
            ),
            "gunner": self.font10.render("Create Gunner cost 150", False, WHITE),
            "offensive": self.font10.render("Create Offensive cost 200", False, WHITE),
        }

    def linkteams(self, teams):
        self.teams = teams  # Type list, index 0 is human player

    def managementclick(self, coord, typeclick):
        for pair in self.windowrects:
            if pair[0].collidepoint(coord):
                pair[1](coord, typeclick)

    def clickinactwin(self, coord, typeclick):
        mouse = self.map.mouseovermap(coord)
        if typeclick == 1:
            self.teams[2].selection(mouse)
            self.teams[0].selection(mouse)
            self.teams[1].selection(mouse)
        else:
            self.teams[0].selectedunitmoveto(mouse, self.teams[1], self.teams[2])

    def clickinminimap(self, coord, typeclick):
        mouse = map.Map.mouseminimaptomap(coord)
        if typeclick == 1:
            self.map.goto(mouse)
        else:
            self.teams[0].selectedunitmoveto(mouse)

    def clickincommwin(self, coord, typeclick):
        if self.teams[0].selectedunit:
            coord = Interface.mouseoverwindowtocomm(coord)
            for key, date in self.buttonrects.items():
                if date.collidepoint(coord):
                    if key in self.teams[0].selectedunit.comm:
                        self.click.append([10, date])
                        try:
                            self.buttonactions[key]()
                        except KeyError:
                            pass

    def help(self, coord):
        if self.teams[0].selectedunit:
            coord = Interface.mouseoverwindowtocomm(coord)
            for i in self.teams[0].selectedunit.comm:
                if self.buttonrects[i].collidepoint(coord):
                    self.window.blit(self.helpinfo[i], (15, 735))

    def draw(self):
        self.map.draw(self.window, self.teams)
        self.drawinfo()
        self.window.blit(self.backinfo[0], INFOPOS)
        self.drawcomm()
        self.window.blit(self.backcomm[0], COMMPOS)
        self.drawresource()
        self.window.blit(self.backresor[0], RESOURPOS)

    def drawcomm(self):
        unit = self.teams[0].selectedunit
        if unit:
            self.backcomm[0].blit(self.backcomm[1], (0, 0))
            for i in self.click:
                i[0] -= 1
                if i[0] >= 0:
                    pygame.draw.rect(self.backcomm[0], SILVER, i[1], 2)
                else:
                    self.click.remove(i)
            for i, j in unit.comm.items():
                self.backcomm[0].blit(self.commbuttons[i][j], self.buttonrects[i])
        else:
            self.backcomm[0].blit(self.backcomm[1], (0, 0))

    def drawinfo(self):
        for i in self.teams:
            if i.selectedunit:
                self.backinfo[0].blit(self.backinfo[1], (0, 0))
                self.drawinfos[i.selectedunit.type](i.selectedunit)
                return None
            else:
                self.backinfo[0].blit(self.backinfo[1], (0, 0))

    def drawinfounit(self, unit):
        name = self.font14.render(unit.name, False, WHITE)
        life = self.font10.render(
            str(unit.life) + "-" + str(unit.lifemax), False, WHITE
        )
        armor = self.font12.render("Armor: " + str(unit.armor), False, WHITE)
        damage = self.font12.render("Damage: " + str(unit.attack), False, WHITE)
        speed = self.font12.render("Speed: " + str(unit.speed), False, WHITE)
        sight = self.font12.render("Sight: " + str(unit.view), False, WHITE)
        level = self.font12.render("Level: " + str(unit.level[0]), False, WHITE)
        widthlife = unit.proportionlife(name.get_width())
        rectlife = pygame.Surface((widthlife, 5))
        percentlife = unit.percent()
        if percentlife > 70:
            rectlife.fill((0, 100, 0))
        elif percentlife > 30:
            rectlife.fill((255, 165, 0))
        else:
            rectlife.fill((139, 0, 0))
        widthlevel = unit.proportionlevel(100)
        rectlevel = pygame.Surface((widthlevel, 5))
        rectlevel.fill(WHITE)
        self.backinfo[0].blit(name, (7, 6))
        pygame.draw.rect(
            self.backinfo[0], GREEN, ((7, 20), (name.get_width() + 2, 7)), 1
        )
        self.backinfo[0].blit(rectlife, (8, 21))
        self.backinfo[0].blit(life, (13, 27))
        self.backinfo[0].blit(armor, (75, 50))
        self.backinfo[0].blit(damage, (75, 65))
        self.backinfo[0].blit(speed, (75, 80))
        self.backinfo[0].blit(sight, (75, 95))
        self.backinfo[0].blit(level, (75, 110))
        pygame.draw.rect(self.backinfo[0], WHITE, ((75, 123), (100 + 2, 7)), 1)
        self.backinfo[0].blit(rectlevel, (76, 124))

    def drawinfoplanet(self, planet):
        name = self.font14.render(planet.name, False, WHITE)
        self.backinfo[0].blit(name, (7, 6))
        if planet.color == "c":
            if planet.settler > 0:
                settler = self.font12.render(
                    "Red Team: " + str(planet.settler), False, RED
                )
            elif planet.settler < 0:
                settler = self.font12.render(
                    "Blue Team: " + str(planet.settler * -1), False, BLUE
                )
            else:
                settler = self.font12.render("Neutral", False, WHITE)
        elif planet.color == "a":
            settler = self.font12.render("Red Team", False, RED)
        else:
            settler = self.font12.render("Blue Team", False, BLUE)
        self.backinfo[0].blit(settler, (75, 50))

    def drawinfodefense(self, defense):
        name = self.font14.render(defense.name, False, WHITE)
        life = self.font10.render(
            str(defense.life) + "-" + str(defense.lifemax), False, WHITE
        )
        armor = self.font12.render("Armor: " + str(defense.armor), False, WHITE)
        damage = self.font12.render("Damage: " + str(defense.attack), False, WHITE)
        sight = self.font12.render("Sight: " + str(defense.view), False, WHITE)
        widthlife = defense.proportionlife(name.get_width())
        rectlife = pygame.Surface((widthlife, 5))
        percentlife = defense.percent()
        if percentlife > 70:
            rectlife.fill((0, 100, 0))
        elif percentlife > 30:
            rectlife.fill((255, 165, 0))
        else:
            rectlife.fill((139, 0, 0))
        widthlevel = defense.proportionlevel(100)
        rectlevel = pygame.Surface((widthlevel, 5))
        rectlevel.fill(WHITE)
        self.backinfo[0].blit(name, (7, 6))
        pygame.draw.rect(
            self.backinfo[0], GREEN, ((7, 20), (name.get_width() + 2, 7)), 1
        )
        self.backinfo[0].blit(rectlife, (8, 21))
        self.backinfo[0].blit(life, (13, 27))
        self.backinfo[0].blit(armor, (75, 50))
        self.backinfo[0].blit(damage, (75, 65))
        self.backinfo[0].blit(sight, (75, 80))

    def drawinfobullet(self, bullet):
        name = self.font14.render(bullet.name, False, WHITE)
        self.backinfo[0].blit(name, (7, 6))

    def drawresource(self):
        self.backresor[0].blit(self.backresor[1], (0, 0))
        if self.teams[0].pob >= self.teams[0].maxpob:
            pob = self.font12.render(
                (str(self.teams[0].pob) + "-" + str(self.teams[0].maxpob)), False, RED
            )
        else:
            pob = self.font12.render(
                (str(self.teams[0].pob) + "-" + str(self.teams[0].maxpob)), False, WHITE
            )
        self.backresor[0].blit(pob, (46, 18))
        pos = [(130, 11), (130, 23), (130, 35)]
        for i in self.teams[0].shield:
            rectlife = pygame.Surface((i.proportionlife(98), 6))
            if i.percent() > 70:
                rectlife.fill((0, 100, 0))
            elif i.percent() > 30:
                rectlife.fill((255, 165, 0))
            else:
                rectlife.fill((139, 0, 0))
            self.backresor[0].blit(rectlife, pos.pop(0))
        land = self.font12.render(
            (
                str(self.teams[0].base.landings[0])
                + "-"
                + str(self.teams[0].base.landings[1])
            ),
            False,
            WHITE,
        )
        self.backresor[0].blit(land, (265, 18))
        if self.teams[0].resources > 0:
            resor = self.font12.render(str(self.teams[0].resources), False, WHITE)
        else:
            resor = self.font12.render(str(self.teams[0].resources), False, RED)
        self.backresor[0].blit(resor, (380, 18))
        pos = [(464, 11), (464, 23), (464, 35)]
        for i in self.teams[1].shield:
            rectlife = pygame.Surface((i.proportionlife(98), 6))
            if i.percent() > 70:
                rectlife.fill((0, 100, 0))
            elif i.percent() > 30:
                rectlife.fill((255, 165, 0))
            else:
                rectlife.fill((139, 0, 0))
            self.backresor[0].blit(rectlife, pos.pop(0))
            land = self.font12.render(
                (
                    str(self.teams[1].base.landings[0])
                    + "-"
                    + str(self.teams[1].base.landings[1])
                ),
                False,
                WHITE,
            )
            self.backresor[0].blit(land, (602, 18))

    def setpassive(self):
        unit = self.teams[0].selectedunit
        unit.comm["passive"] = 1
        unit.comm["aggressive"] = 0
        unit.aggressive = 0
        unit.target = None
        unit.stop()

    def setagressive(self):
        unit = self.teams[0].selectedunit
        unit.comm["passive"] = 0
        unit.comm["aggressive"] = 1
        unit.aggressive = 1

    def basebutton1(self):
        self.teams[0].append("scout")

    def basebutton2(self):
        self.teams[0].append("square")

    def basebutton3(self):
        self.teams[0].append("star")

    def basebutton4(self):
        self.teams[0].append("gunner")

    def basebutton5(self):
        self.teams[0].append("offensive")

    def mouseoverwindowtocomm(coord):
        x, y = coord
        x = x - COMMPOS[0]
        y = y - COMMPOS[1]
        return x, y

    def revealmap(self):
        self.map.revealmap = False if self.map.revealmap else True
