try:
    import random
    import pygame
    from pygame.locals import *
    from functions import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")
    raise SystemExit("Error al importar los modulos")


class Map:
    def __init__(self):
        self.image = pygame.Surface(SIZEMAP)
        self.emptyimage = self.image.copy()
        self.minimap = load_image(PATHS["menus"] + "backgroundminimap.png", False)
        self.emptyminimap = self.minimap.copy()
        self.miniteama = load_image(PATHS["sprites"] + "teama.png", True)
        self.miniteamb = load_image(PATHS["sprites"] + "teamb.png", True)
        self.miniteamc = load_image(PATHS["sprites"] + "teamc.png", True)
        self.scrollx = 0
        self.scrolly = 0
        self.alerts = []
        self.revealmap = False

    def draw(self, surface, teams):
        surface.blit(
            self.image, ACTWINDPOS, ((self.scrollx, self.scrolly), ACTWINDSIZE)
        )
        self.drawminimap(teams)
        surface.blit(self.minimap, MINIMAPOS)

    def clean(self):
        self.image.blit(
            self.emptyimage, (self.scrollx, self.scrolly), ((0, 0), ACTWINDSIZE)
        )

    def scroll(self, coord):
        mousex, mousey = coord
        if (mousex > GUISIZE[0] - 5) and (self.scrollx + ACTWINDSIZE[0] < SIZEMAP[0]):
            self.scrollx += 15
        if (mousey > GUISIZE[1] - 5) and (self.scrolly + ACTWINDSIZE[1] < SIZEMAP[1]):
            self.scrolly += 15
        if (mousex < GUIPOS[0] + 15) and (self.scrollx > 0):
            self.scrollx -= 15
        if (mousey < GUIPOS[1] + 15) and (self.scrolly > 0):
            self.scrolly -= 15

    def drawminimap(self, teams):
        self.minimap.blit(self.emptyminimap, (0, 0))
        for i in teams[2].sprites():
            if not i.owner:
                pos = Map.mousemaptominimap(i.rect.center)
                self.minimap.blit(self.miniteamc, pos)
        for i in teams[0].sprites():
            if i.type != "bullet":
                pos = Map.mousemaptominimap(i.rect.center)
                self.minimap.blit(self.miniteama, pos)
                if not self.revealmap:
                    for j in teams[1].sprites():
                        if j.type != "bullet":
                            dist = distance(i.rect, j.rect)
                            if dist <= i.view * 100:
                                pos = Map.mousemaptominimap(j.rect.center)
                                self.minimap.blit(self.miniteamb, pos)
                                break
                else:
                    for j in teams[1].sprites():
                        if j.type != "bullet":
                            pos = Map.mousemaptominimap(j.rect.center)
                            self.minimap.blit(self.miniteamb, pos)

        pos = (
            MINIMASIZE[0] * self.scrollx // SIZEMAP[0],
            MINIMASIZE[1] * self.scrolly // SIZEMAP[1],
        )
        pygame.draw.rect(self.minimap, WHITE, (pos, MINIMAPRECT), 1)
        for alert in self.alerts:
            if alert[0] > 0:
                alert[0] -= 1
                pygame.draw.rect(self.minimap, RED, alert[1], 1)
            else:
                self.alerts.remove(alert)

    def goto(self, coord):
        self.scrollx, self.scrolly = Map.mouseoverminimaptomap(coord)

    def mouseovermap(self, coord):
        x, y = coord
        toret = (x + self.scrollx - ACTWINDPOS[0], y + self.scrolly - ACTWINDPOS[1])
        return toret

    def mouseoverminimaptomap(coord):
        x = coord[0] - ACTWINDSIZE[0] // 2
        y = coord[1] - ACTWINDSIZE[1] // 2
        if x < 0:
            x = 0
        elif (x + ACTWINDSIZE[0]) > SIZEMAP[0]:
            x = SIZEMAP[0] - ACTWINDSIZE[0]
        if y < 0:
            y = 0
        elif (y + ACTWINDSIZE[1]) > SIZEMAP[1]:
            y = SIZEMAP[1] - ACTWINDSIZE[1]
        return x, y

    def mouseminimaptomap(coord):
        x, y = coord[0] - MINIMAPOS[0], coord[1] - MINIMAPOS[1]
        x = x * SIZEMAP[0] // MINIMASIZE[0]
        y = y * SIZEMAP[1] // MINIMASIZE[1]
        return x, y

    def mousemaptominimap(coord):
        x, y = coord
        x = x * MINIMASIZE[0] // SIZEMAP[0]
        y = y * MINIMASIZE[1] // SIZEMAP[1]
        return x, y

    def addalert(self, coord):
        rect = pygame.Rect((0, 0), (15, 15))
        rect.center = Map.mousemaptominimap(coord)
        self.alerts.append([5, rect])

    def cameraistopleft(self):
        if self.scrollx < 700 and self.scrolly < 700:
            return True
