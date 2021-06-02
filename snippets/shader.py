import os
import sys
import pygame

CELL_SIZE = (50, 50)
SUN_SIZE = (75, 75)
BACKGROUND_COLOR = (240, 240, 255)


class Sun(object):
    def __init__(self, pos):
        self.image = self.make_image()
        self.rect = self.image.get_rect(center=pos)
        self.click = False

    def make_image(self):
        image = pygame.Surface(SUN_SIZE).convert_alpha()
        rect = image.get_rect()
        image.fill((0, 0, 0, 0))
        pygame.draw.ellipse(image, pygame.Color("black"), rect)
        pygame.draw.ellipse(image, pygame.Color("orange"), rect.inflate(-10, -10))
        return image

    def update(self, screen_rect):
        if self.click:
            self.rect.move_ip(pygame.mouse.get_rel())
            self.rect.clamp_ip(screen_rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.make_image()
        self.rect = self.image.get_rect(center=pos)
        self.shadow_strips = self.make_shadow_elements()

    def make_image(self):
        image = pygame.Surface(CELL_SIZE).convert_alpha()
        image.fill(pygame.Color("Red"))
        image.fill((0, 0, 0, 0), image.get_rect().inflate(-30, -30))
        return image

    def make_shadow_elements(self):
        shadow_strips = []
        for j in range(self.rect.height):
            strip = pygame.Surface((self.rect.width, 1)).convert_alpha()
            strip.fill((0, 0, 0, 0))
            for i in range(self.rect.width):
                pixel = self.image.get_at((i, j))
                if pixel != (0, 0, 0, 0):
                    alpha = min(j * 5, 255)
                    strip.set_at((i, 0), (0, 0, 0, alpha))
            shadow_strips.append(strip)
        return shadow_strips[::-1]

    def draw_shadow(self, surface, sun):
        slope = self.get_sun_slope(sun)
        sign = 1 if sun[1] < self.rect.centery else -1
        for i, strip in enumerate(self.shadow_strips):
            pos = (self.rect.x + i * slope * sign, self.rect.bottom + i * sign)
            surface.blit(strip, pos)

    def get_sun_slope(self, sun):
        rise = self.rect.centery - sun[0]
        run = self.rect.centerx - sun[1]
        try:
            return rise / float(run)
        except ZeroDivisionError:
            return 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Control(object):
    def __init__(self, screen_size):
        pygame.init()
        os.environ["SDL_VIDEO_CENTERED"] = "TRUE"
        self.screen = pygame.display.set_mode(screen_size)
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.done = False
        self.player = Player((200, 200))
        self.sun = Sun((50, 50))

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.sun.rect.collidepoint(event.pos):
                    self.sun.click = True
                    pygame.mouse.get_rel()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.sun.click = False

    def update(self):
        self.sun.update(self.screen_rect)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.sun.draw(self.screen)
        self.player.draw_shadow(self.screen, self.sun.rect.center)
        self.player.draw(self.screen)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    app = Control((500, 500))
    app.main_loop()
    pygame.quit()
    sys.exit()
