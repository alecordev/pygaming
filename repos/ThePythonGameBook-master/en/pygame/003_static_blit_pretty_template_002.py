# -*- coding: utf-8 -*-
"""003_static_blit_pretty_template.py"""
import pygame
import random


class PygView(object):
    width = 0
    height = 0

    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        PygView.width = width
        PygView.height = height
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.DOUBLEBUF
        )
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((110, 110, 140))  # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont("mono", 24, bold=True)

    def paint(self):
        """painting on the surface"""
        # pygame.draw.line(Surface, color, start, end, width)
        pygame.draw.line(self.background, (0, 255, 0), (10, 10), (50, 100))
        pygame.draw.line(self.background, (0, 0, 0), (0, 0), (1000, 500))
        pygame.draw.line(self.background, (255, 255, 0), (1000, 0), (0, 500))
        # ...

        pygame.draw.ellipse(
            self.background, (200, 110, 100), (0, PygView.height - 60, 100, 60)
        )
        pygame.draw.ellipse(
            self.background, (0, 200, 200), (PygView.width - 45, 0, 20, 90)
        )
        for x in range(100, 19, -20):
            pygame.draw.circle(
                self.background,
                (0, 0, random.randint(0, 255)),
                (PygView.width // 2, PygView.height // 2),
                x,
            )
        # pygame.draw.circle(self.background, (0,0,0), (200,80), (36))
        # pygame.draw.rect(self.background, (0,255,100), (PygView.width / 2 - 50 , PygView.height / 2 - 25, 100, 50))
        pygame.draw.line(
            self.background, (255, 40, 255), (PygView.width, 0), (0, PygView.height)
        )
        pygame.draw.line(
            self.background, (255, 90, 205), (0, 0), (PygView.width, PygView.height)
        )

        # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
        pygame.draw.rect(
            self.background, (0, 255, 0), (50, 50, 100, 25)
        )  # rect: (x1, y1, width, height)
        pygame.draw.rect(self.background, (0, 0, 255), (70, 70, 80, 30))
        # pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
        pygame.draw.circle(self.background, (0, 200, 0), (200, 50), 35)
        # pygame.draw.polygon(Surface, color, pointlist, width=0): return Rect
        pygame.draw.polygon(
            self.background, (0, 180, 0), ((250, 100), (300, 0), (350, 50))
        )
        # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle, width=1): return Rect
        pygame.draw.arc(
            self.background, (0, 150, 0), (400, 10, 150, 100), 0, 3.14
        )  # radiant instead of grad
        # ...
        # pygame.draw.polygon(self.background, (0,255,188), ((370,300), (320,200), (185,200), (190,200), (170,300)))
        pygame.draw.polygon(
            self.background,
            (255, 165, 0),
            (
                (PygView.width / 2, 0),
                (PygView.width / 2 - 90, PygView.height - 80),
                (PygView.width / 2, PygView.height),
                (PygView.width / 2 + 90, PygView.height - 80),
                (PygView.width / 2, 0),
            ),
        )

    def run(self):
        self.paint()
        myball = Spaceship()  # creating the Ball object
        myship = Spaceship(color=(100, 200, 100), x=400, y=200, control="ijkl")
        self.allsprites = []
        self.allsprites.append(myball)
        self.allsprites.append(myship)
        running = True
        while running:
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000.0
            self.playtime += seconds
            self.draw_text(
                "FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
                    self.clock.get_fps(), " " * 5, self.playtime
                )
            )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # keys that you press once and release
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_q:  # stopper
                        myball.dx = 0
                        myball.dy = 0
                        myball.x = PygView.width // 3  # one third without remainder
                        myball.y = PygView.height // 2  # one half without remainder
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            for sprite in self.allsprites:
                sprite.update(seconds)
            for sprite in self.allsprites:
                sprite.blit(self.screen)

            # myball.update(seconds)
            # myball.blit(self.screen) # blitting it
        pygame.quit()

    def draw_text(self, text):
        """Center text in window"""
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surface, (50, 150))


class Spaceship(object):
    """this is not a native pygame sprite but instead a pygame surface"""

    def __init__(self, radius=50, color=(0, 0, 255), x=0, y=0, slim=20, control="wasd"):
        """create a (black) surface and paint a blue ball on it"""
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.slim = slim
        self.control = control
        # create a rectangular surface for the ball 50x50
        self.surface = pygame.Surface((2 * self.radius, 2 * self.radius))
        pygame.draw.polygon(
            self.surface,
            self.color,
            (
                (0, 0 + self.slim),
                (self.radius // 2, self.radius),
                (0, 2 * self.radius - self.slim),
                (self.radius * 2, self.radius),
            ),
        )
        # pygame.draw.circle(self.surface, color, (radius, radius), radius) # draw blue filled circle on ball surface
        # self.surface = self.surface.convert() # for faster blitting.
        # to avoid the black background, make black the transparent color:
        self.surface.set_colorkey((0, 0, 0))
        self.surface = (
            self.surface.convert_alpha()
        )  # faster blitting with transparent color

    def wrap(self):
        # wrap around screen
        if self.x < 0:
            self.x = PygView.width
        if self.x > PygView.width:
            self.x = 0
        if self.y < 0:
            self.y = PygView.height
        if self.y > PygView.height:
            self.y = 0

    def checkbounce(self):
        if self.x > PygView.width:
            self.x = PygView.width
            self.dx *= -1
        if self.x < 0:
            self.x = 0
            self.dx *= -1
        if self.y > PygView.height:
            self.y = PygView.height
            self.dy *= -1
        if self.y < 0:
            self.y = 0
            self.dy *= -1

    def update(self, seconds):
        if self.control == "wasd":
            pressedkeys = (
                pygame.key.get_pressed()
            )  # keys that you can press all the time
            if pressedkeys[pygame.K_a]:
                self.dx -= 1
            if pressedkeys[pygame.K_d]:
                self.dx += 1
            if pressedkeys[pygame.K_w]:
                self.dy -= 1
            if pressedkeys[pygame.K_s]:
                self.dy += 1
        elif self.control == "ijkl":
            pressedkeys = pygame.key.get_pressed()
            if pressedkeys[pygame.K_j]:
                self.dx -= 1
            if pressedkeys[pygame.K_l]:
                self.dx += 1
            if pressedkeys[pygame.K_k]:
                self.dy += 1
            if pressedkeys[pygame.K_i]:
                self.dy -= 1
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.checkbounce()

    def blit(self, ground):
        """blit the Spaceship on the background"""
        ground.blit(self.surface, (self.x - self.radius, self.y - self.radius))


if __name__ == "__main__":
    PygView(1000, 500).run()  # call with width of window and fps
