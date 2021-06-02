try:
    import pygame
    from pygame.locals import *
    from functions import *
    from sounds import *
    from settings import *
except ImportError:
    write_log("Error al importar los modulos")
    raise SystemExit("Error al importar los modulos")


class Bullet(pygame.sprite.DirtySprite):
    def __init__(self, gunner, target, namebullet):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = load_image(PATHS["sprites"] + namebullet)
        self.rect = self.image.get_rect()
        self.rect.center = gunner.rect.center
        self.gunner = gunner
        self.gunner.bullet = self
        self.target = target
        self.selftarget = None
        self.speed = 10
        self.dirty = 2
        self.life = 1
        self.type = "bullet"
        self.name = "Bullet"
        self.alert = False
        self.erase = False
        self.aggressive = False
        self.view = 0
        self.comm = {}
        self.armor = 0

    def update(self):
        if self.target:
            self.selftarget = self.target
        if not self.selftarget:
            self.rect.center = self.gunner.rect.center
        else:
            self.move()
        if self.gunner.life <= 0:
            self.life = 0

    def move(self):
        if self.selftarget:
            if self.rect.colliderect(self.selftarget.rect):
                self.attack()
                self.rect.center = self.gunner.rect.center
                self.selftarget = None
                return None
            x, y = self.selftarget.rect.center
            if self.rect.centerx < x:
                self.rect.centerx += self.speed
            if self.rect.centerx > x:
                self.rect.centerx -= self.speed
            if self.rect.centery < y:
                self.rect.centery += self.speed
            if self.rect.centery > y:
                self.rect.centery -= self.speed

    def attack(self):
        if self.target:
            self.target.reply(self.gunner)
            self.target.life -= self.gunner.attack - self.target.armor
            if self.target.life <= 0:
                self.target.life = 0
                self.target = None
                self.gunner.target = None
                self.gunner.uplevel()

    def reply(self, enemy):
        return None

    def remove(self):
        return None
