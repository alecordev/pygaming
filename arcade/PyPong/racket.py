import util
from config import Config


class Racket:
    def __init__(self, side):
        self.sprite = util.load_image(Config.path_wallsprite, transparent=False)
        self.rect = self.sprite.get_rect()
        if side == "R":
            self.rect.centerx = Config.widthwindow - self.rect.w - 10
        else:  # LEFT
            self.rect.centerx = self.rect.w + 10
        self.rect.centery = Config.heightwindow // 2
        self.direction = False
        self.mov = {"up": self.up, "down": self.down}
        self.mark = 0
        self.speed = 5

    def update(self):
        try:
            self.mov[self.direction]()
        except KeyError:
            pass  # Do nothing

    def draw(self, window):
        window.blit(self.sprite, self.rect)

    def up(self):
        if self.rect.y > 0 + self.speed:
            self.rect.centery -= self.speed

    def down(self):
        _, y = self.rect.bottomleft
        if y < Config.heightwindow - self.speed:
            self.rect.centery += self.speed

    def computerAI(self, ball):
        if ball.rect.centery - 25 > self.rect.centery:
            self.direction = "down"
            return None
        if ball.rect.centery + 25 < self.rect.centery:
            self.direction = "up"
            return None
        self.direction = False
