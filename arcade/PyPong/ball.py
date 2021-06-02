import random
import sounds
import util

from config import Config


class Ball:
    def __init__(self):
        self.sprite = util.load_image(Config.path_ballsprite)
        self.rect = self.sprite.get_rect()
        self.rect.centerx = Config.widthwindow // 2
        self.rect.centery = random.randrange(0, Config.heightwindow - self.rect.h)
        self.dx = random.choice((1, -1))
        self.dy = random.choice((1, -1))
        self.speed = 1

    def restart(self):
        self.rect.centerx = Config.widthwindow // 2
        self.rect.centery = random.randrange(0, Config.heightwindow - self.rect.h)
        self.dx = random.choice((1, -1))
        self.dy = random.choice((1, -1))
        self.speed = 1

    def update(self):
        self.rect.centerx += self.dx * self.speed
        self.rect.centery += self.dy * self.speed

    def collides(self, racket_right, racket_left):
        _, y = self.rect.bottomleft
        if y >= Config.heightwindow or self.rect.y <= 0:
            self.hit_with_wall()
            return None
        if self.rect.collidelist((racket_right, racket_left)) > -1:
            self.hit_with_racket()
            return None
        if self.rect.centerx >= Config.widthwindow:
            sounds.goal.play()
            racket_left.mark += 1
            self.restart()
            return None
        if self.rect.centerx <= 0:
            sounds.goal.play()
            racket_right.mark += 1
            self.restart()
            return None

    def draw(self, window):
        window.blit(self.sprite, self.rect)

    def hit_with_racket(self):
        sounds.hit.play()
        self.rect.centery += random.choice((1, -1))
        self.dy = random.choice((1, -1))
        self.dx *= -1
        self.speed += 1

    def hit_with_wall(self):
        self.rect.centerx += random.choice((1, -1))
        self.dy *= -1
        self.speed += 1

    def is_goal(self):
        if self.rect.centerx >= Config.widthwindow:
            return "p_left"
        if self.rect.centerx <= 0:
            return "p_right"
        return False
