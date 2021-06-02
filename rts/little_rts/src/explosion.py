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


class Explosion(pygame.sprite.DirtySprite):
    def __init__(self, coord):
        pygame.sprite.DirtySprite.__init__(self)
        self.sprites = load_sprites("spritesfire1.png", (100, 94))
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = coord
        self.life = 27
        self.indexsprite = 1
        self.dirty = 2

    def update(self):
        self.life -= 1
        if self.life == 0:
            self.dirty = 0
            return None
        self.image = self.sprites[self.indexsprite]
        self.indexsprite += 1
