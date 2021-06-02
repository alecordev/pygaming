import pygame


class Player:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.width = 50
        self.height = 75
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255, 255, 255))
        starting_loc = (0, screen_rect.height)
        self.rect = self.image.get_rect(bottomleft=starting_loc)
        self.speed = 5
        self.grav = 0.5

        self.jumping = False
        self.y_vel = 0

    def update(self):
        self.rect.clamp_ip(self.screen_rect)
        self.jump_update()

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, x, y):
        self.rect.x += x * self.speed
        self.rect.y += y * self.speed

    def jump_update(self):
        if self.jumping:
            self.y_vel += self.grav
            self.rect.y += self.y_vel
            if self.is_touching_ground():
                self.jumping = False

    def is_touching_ground(self):
        return self.rect.y >= self.screen_rect.height - self.height

    def jump(self):
        if not self.jumping:
            self.y_vel = -12
            self.jumping = True


class Control:
    def __init__(self):
        self.screensize = (600, 400)
        self.screen = pygame.display.set_mode(self.screensize)
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.quit = False
        self.keys = pygame.key.get_pressed()

        self.player = Player(self.screen_rect)

    def run(self):
        while not self.quit:
            now = pygame.time.get_ticks()
            self.held_keys(self.keys)
            self.event_loop()
            self.update()
            self.render()
            pygame.display.update()
            self.clock.tick(self.fps)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.keys = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

    def held_keys(self, keys):
        if keys[pygame.K_a]:
            self.player.move(-1, 0)
        if keys[pygame.K_d]:
            self.player.move(1, 0)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.player.render(self.screen)

    def update(self):
        self.player.update()


app = Control()
app.run()
