import os
import pygame


class Bomb:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.image = None
        self.spritesheet = pygame.image.load("explosion.png").convert_alpha()
        self.frame = 0
        self.frames = []  # all frames off the sprite sheet
        self.timer = 0.0  # timer for animation
        self.fps = 30.0  # fps of animation
        self.get_images(8, 6, 3)  # rip images from the sprite sheet
        self.done = False

    def get_images(self, num_img_row, num_img_col, empty_frames=0):
        for col in range(num_img_col):
            for row in range(num_img_row):
                loc = ((self.rect.width * row, self.rect.height * col), self.rect.size)
                self.frames.append(self.spritesheet.subsurface(loc))
        if empty_frames:
            for empty_frame in range(empty_frames):
                self.frames.pop()
        self.make_image()

    def make_image(self):
        if pygame.time.get_ticks() - self.timer > 1000 / self.fps:
            try:
                self.frame += 1
                self.image = self.frames[self.frame]
                self.timer = pygame.time.get_ticks()
            except IndexError:
                self.done = True
        if not self.image:
            self.image = self.frames[self.frame]

    def update(self, surf):
        self.make_image()
        surf.blit(self.image, self.rect)


class Control:
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.screen = pygame.display.set_mode((256, 256))
        pygame.display.set_caption("Press Space Bar")
        pygame.init()
        self.Clock = pygame.time.Clock()
        self.done = False
        self.bombs = []

    def event_loop(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bombs.append(Bomb((0, 0, 256, 256)))

    def update(self):
        while not self.done:
            self.event_loop()
            self.screen.fill(0)
            for bomb in self.bombs[:]:
                bomb.update(self.screen)
                if bomb.done:
                    self.bombs.remove(bomb)
            pygame.display.update()
            self.Clock.tick(60)


if __name__ == "__main__":
    app = Control()
    app.update()
    pygame.quit()
