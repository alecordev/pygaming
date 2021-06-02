try:
    import random
    import pygame
    import explosion
    from pygame.locals import *
    from functions import *
    from sounds import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")
    raise SystemExit("Error al importar los modulos")


class BagExplosion(pygame.sprite.LayeredDirty):
    def __init__(self):
        pygame.sprite.LayeredDirty.__init__(self)

    def update(self):
        for i in self.sprites():
            i.update()
            if i.life == 0:
                self.remove(i)

    def append(self, coord):
        self.add(explosion.Explosion(coord))
