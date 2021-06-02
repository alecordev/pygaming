try:
    import random
    import pygame
    import square
    import gunner
    import scout
    import star
    import offensive
    import bullet
    import mainbuilding
    import defensebuilding
    import bagexplosion
    from pygame.locals import *
    from functions import *
    from sounds import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")
    raise SystemExit("Error al importar los modulos")


class Team(pygame.sprite.LayeredDirty):
    def __init__(self, color, map):
        pygame.sprite.LayeredDirty.__init__(self)
        self.make_units = {
            "square": square.Square,
            "gunner": gunner.Gunner,
            "scout": scout.Scout,
            "star": star.Star,
            "offensive": offensive.Offensive,
        }
        self.costs = {
            "square": 300,
            "gunner": 150,
            "scout": 100,
            "star": 150,
            "offensive": 200,
        }
        self.resources = 1000
        self.maxresources = 1000
        self.contaddresources = 0
        self.selectedunit = None
        self.base = None
        self.color = color
        self.pob = 0
        self.maxpob = 10
        self.map = map
        self.shield = []
        self.reaction = 0
        self.bagexplosion = bagexplosion.BagExplosion()
        if self.color == "a":
            self.base = mainbuilding.MainBuilding((0, 0), self.color, 0)
            shield1 = defensebuilding.Defensebuilding((250, 250), self.color)
            shield2 = defensebuilding.Defensebuilding((250, 0), self.color)
            shield3 = defensebuilding.Defensebuilding((0, 250), self.color)
            units = (
                self.base,
                shield1,
                shield2,
                shield3,
                bullet.Bullet(shield1, None, "bullet1.png"),
                bullet.Bullet(shield2, None, "bullet1.png"),
                bullet.Bullet(shield3, None, "bullet1.png"),
            )
            self.add(units)
            self.shield = [shield1, shield2, shield3]
        elif self.color == "b":
            self.base = mainbuilding.MainBuilding((2750, 2785), self.color, 0)
            shield1 = defensebuilding.Defensebuilding((2600, 2610), self.color)
            shield2 = defensebuilding.Defensebuilding((2600, 2860), self.color)
            shield3 = defensebuilding.Defensebuilding((2850, 2600), self.color)
            units = (
                self.base,
                shield1,
                shield2,
                shield3,
                bullet.Bullet(shield1, None, "bullet1.png"),
                bullet.Bullet(shield2, None, "bullet1.png"),
                bullet.Bullet(shield3, None, "bullet1.png"),
            )
            self.add(units)
            self.shield = [shield1, shield2, shield3]
        elif self.color == "c":
            self.base = mainbuilding.MainBuilding((1360, 1375), self.color, 1)
            units = (
                self.base,
                mainbuilding.MainBuilding((0, 2750), self.color, 2),
                mainbuilding.MainBuilding((2750, 0), self.color, 2),
            )
            self.add(units)

    def append(self, unit, coord=None):
        if self.pob < self.maxpob and self.resources - self.costs[unit] >= 0:
            self.resources -= self.costs[unit]
            self.contaddresources = 0
            coord = self.selectedunit.rect.center if not coord else coord
            if unit == "gunner":
                gunner = self.make_units[unit](coord, self.color)
                b = bullet.Bullet(gunner, None, "bullet.png")
                self.add(gunner, b)
            else:
                self.add(self.make_units[unit](coord, self.color))
            self.pob += 1
            return True
        else:
            return False

    def selection(self, coord):
        selected = False
        building = False
        aux = None
        for i in self.sprites():
            if i.rect.collidepoint(coord) and not selected:
                if i.type == "planet":
                    building = True
                    aux = i
                elif i.type == "defense":
                    building = True
                    aux = i
                else:
                    building = False
                    selected = True
                    i.notselected = False
                    self.selectedunit = i
            else:
                i.notselected = True
        if building:
            self.selectedunit = aux
        elif not selected:
            self.selectedunit = None

    def selectedunitmoveto(self, coord, enemyteam=[], neutralteam=[]):
        if self.selectedunit:
            if enemyteam:
                for enemy in enemyteam.sprites():
                    if enemy.rect.collidepoint(coord):
                        if enemy.type != "planet" and enemy.type != "bullet":
                            self.selectedunit.target = enemy
                        else:
                            if self.selectedunit.type == "settler":
                                self.selectedunit.target = enemy
                            else:
                                self.selectedunit.target = None
                                self.selectedunit.moveto = coord
                        return None
            if neutralteam:
                if self.selectedunit.type == "settler":
                    for planet in neutralteam.sprites():
                        if planet.rect.collidepoint(coord):
                            self.selectedunit.target = planet
                            return None
                        else:
                            self.selectedunit.target = None
                            self.selectedunit.moveto = coord
            self.selectedunit.target = None
            self.selectedunit.moveto = coord

    def update(self):
        self.contaddresources += 1
        if self.contaddresources == 50:
            self.contaddresources = 0
            self.resources += 150
            self.resources = (
                self.maxresources
                if self.resources > self.maxresources
                else self.resources
            )
        deadsprites = []
        contdefenses = 0
        contplanets = 0
        for sprite in self.sprites():
            if sprite.alert:
                self.map.addalert(sprite.rect.center)
                sprite.alert = False
            if sprite.type == "defense":
                contdefenses += 1
            elif sprite.type == "planet":
                contplanets += 1
            if sprite.life <= 0:
                if sprite.type != "bullet":
                    playsound("deadunit")
                    self.bagexplosion.append(sprite.rect.center)
                    self.pob -= 1
                deadsprites.append(sprite)
            elif sprite.erase:
                playsound("landing")
                deadsprites.append(sprite)
                self.pob -= 1
            else:
                sprite.update()
        if contdefenses == 0:
            self.base.open = True
        if self.selectedunit and self.selectedunit.life <= 0:
            self.selectedunit = None
        self.maxresources = 1000 * contplanets
        self.maxpob = 10 * contplanets
        self.pob = 0 if self.pob < 0 else self.pob
        self.remove(deadsprites)
        self.reaction += 1
        self.bagexplosion.draw(self.map.image)
        self.bagexplosion.update()

    def collisions(self, enemyteam, neutralteam):
        dict1 = pygame.sprite.groupcollide(self, enemyteam, False, False)
        dict2 = pygame.sprite.groupcollide(self, neutralteam, False, False)
        for i in self.sprites():
            coll = dict1[i] if i in dict1 else []
            coll += dict2[i] if i in dict2 else []
            i.collisionedwith = coll
            if i.aggressive and i.target == None:
                for j in enemyteam.sprites():
                    if (
                        j.type != "planet"
                        and j.type != "bullet"
                        and distance(i.rect, j.rect) <= i.view * 100
                    ):
                        i.target = j
                        break

    def conquest(self, neutralteam):
        for i in neutralteam.sprites():
            if self.color == i.owner:
                if i not in self.sprites():
                    sprites = self.sprites()
                    sprites.insert(0, i)
                    self.empty()
                    self.add(sprites)
                    self.resources
            else:
                self.remove(i)

    def supr(self):
        if self.selectedunit:
            if self.selectedunit.type == "unit" or self.selectedunit.type == "settler":
                playsound("deadunit")
                self.selectedunit.life = 0
                self.remove(self.selectedunit)
                self.selectedunit = None
                self.pob -= 1

    def automata(self, enemyteam, neutralteam):
        if self.reaction >= 100:
            self.reaction = 0
            planets = []
            units = ("square", "gunner", "star", "scout")
            for unit in self.sprites():
                if unit.type == "planet":
                    if unit.priority == 0:
                        planets.insert(0, unit)
                    elif unit.priority == 1:
                        planets.insert(1, unit)
                    elif unit.priority == 2:
                        planets.append(unit)
                elif unit.type == "settler":
                    if enemyteam.base.open:
                        if unit.target == None:
                            unit.target = enemyteam.base
                    else:
                        neutralplanets = neutralteam.sprites()
                        for planet in neutralteam.sprites():
                            if planet.owner != self.color:
                                if unit.target == None:
                                    unit.target = planet
                                    break
                                else:
                                    if unit.target.owner == self.color:
                                        for planet in neutralteam.sprites():
                                            if planet.owner != self.color:
                                                unit.target = planet
                        if not unit.target:
                            unit.target = random.choice(neutralplanets)
                elif unit.type == "defense":
                    pass
                elif unit.type == "bullet":
                    pass
                else:
                    if unit.target == None:
                        enemys = enemyteam.sprites()
                        random.shuffle(enemys)
                        for enemy in enemys:
                            if enemy.type != "planet" and enemy.type != "bullet":
                                unit.target = enemy
                                break
                    else:
                        if unit.target.life <= 0:
                            unit.target = None
            if self.pob == self.maxpob:
                for unit in self.sprites():
                    if (
                        unit.type != "settler"
                        and unit.type != "planet"
                        and unit.type != "bullet"
                        and unit.type != "defense"
                    ):
                        unit.life = 0
                        break
            for planet in planets:
                if planet.priority == 0:
                    self.append(units[random.randint(0, 3)], planet.rect.center)
                else:
                    self.append(units[random.randint(0, 2)], planet.rect.center)
