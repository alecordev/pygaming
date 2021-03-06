"""
Shows the direction of collision. This method uses masks (pixel perfect)
collision methods, and is a little (possibly over) complicated. It finds the
direction of a collision by calculating a finite difference between colliding
mask elements in both directions. This technique can be extended to find the
actually angle of collision (normal vector) between two simple colliding
shapes.

-Written by Sean J. McKiernan 'Mekire'
"""

import os
import sys
import random
import pygame as pg


CAPTION = "Direction of Collision: Masks"
SCREEN_SIZE = (500, 500)
BACKGROUND_COLOR = (40, 40, 40)
COLOR_KEY = (255, 0, 255)
TEXT_COLOR = (200, 200, 230)

DIRECT_DICT = {
    pg.K_LEFT: (-1, 0),
    pg.K_RIGHT: (1, 0),
    pg.K_UP: (0, -1),
    pg.K_DOWN: (0, 1),
}

OPPOSITE_DICT = {
    pg.K_LEFT: "right",
    pg.K_RIGHT: "left",
    pg.K_UP: "bottom",
    pg.K_DOWN: "top",
}


class Player(pg.sprite.Sprite):
    """
    This time we inherit from pygame.sprite.Sprite.  We are going to take
    advantage of the sprite.Group collission functions (though as usual, doing
    all this without using pygame.sprite is not much more complicated).
    """

    def __init__(self, rect, speed, direction=pg.K_RIGHT):
        """
        Arguments are a rect representing the Player's location and
        dimension, the speed(in pixels/frame) of the Player, and the Player's
        starting direction (given as a key-constant).
        """
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(rect)
        self.mask = self.make_mask()
        self.speed = speed
        self.direction = direction
        self.collision_direction = None
        self.first_collision_per_frame = None
        self.old_direction = None  # The Players previous direction every frame.
        self.direction_stack = []  # Held keys in the order they were pressed.
        self.redraw = False  # Force redraw if needed.
        self.image = None
        self.frame = 0
        self.frames = self.get_frames()
        self.animate_timer = 0.0
        self.animate_fps = 7.0
        self.walkframes = []
        self.walkframe_dict = self.make_frame_dict()
        self.adjust_images()

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask_surface = pg.Surface(self.rect.size).convert_alpha()
        mask_surface.fill((0, 0, 0, 0))
        mask_surface.fill(pg.Color("white"), (10, 20, 30, 30))
        mask = pg.mask.from_surface(mask_surface)
        return mask

    def get_frames(self):
        """Get a list of all frames."""
        sheet = SKEL_IMAGE
        indices = [[0, 0], [1, 0], [2, 0], [3, 0]]
        return get_images(sheet, indices, self.rect.size)

    def make_frame_dict(self):
        """
        Create a dictionary of direction keys to frames. We can use
        transform functions to reduce the size of the sprite sheet needed.
        """
        frames = {
            pg.K_LEFT: [self.frames[0], self.frames[1]],
            pg.K_RIGHT: [
                pg.transform.flip(self.frames[0], True, False),
                pg.transform.flip(self.frames[1], True, False),
            ],
            pg.K_DOWN: [self.frames[3], pg.transform.flip(self.frames[3], True, False)],
            pg.K_UP: [self.frames[2], pg.transform.flip(self.frames[2], True, False)],
        }
        return frames

    def adjust_images(self):
        """Update the sprite's walkframes as the sprite's direction changes."""
        if self.direction != self.old_direction:
            self.walkframes = self.walkframe_dict[self.direction]
            self.old_direction = self.direction
            self.redraw = True
        self.make_image()

    def make_image(self):
        """Update the sprite's animation as needed."""
        now = pg.time.get_ticks()
        if self.redraw or now - self.animate_timer > 1000 / self.animate_fps:
            if self.direction_stack:
                self.frame = (self.frame + 1) % len(self.walkframes)
                self.image = self.walkframes[self.frame]
            self.animate_timer = now
        if not self.image:
            self.image = self.walkframes[self.frame]
        self.redraw = False

    def add_direction(self, key):
        """Add a pressed direction key on the direction stack."""
        if key in DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            self.direction_stack.append(key)
            self.direction = self.direction_stack[-1]

    def pop_direction(self, key):
        """Pop a released key from the direction stack."""
        if key in DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            if self.direction_stack:
                self.direction = self.direction_stack[-1]

    def update(self, obstacles):
        """Adjust the image and move as needed."""
        self.adjust_images()
        self.collision_direction = None
        if self.direction_stack:
            self.movement(obstacles, 0)
            self.movement(obstacles, 1)

    def movement(self, obstacles, i):
        """Move player and then check for collisions; adjust as necessary."""
        change = self.speed * DIRECT_DICT[self.direction][i]
        self.rect[i] += change
        collisions = pg.sprite.spritecollide(self, obstacles, False)
        callback = pg.sprite.collide_mask
        collide = pg.sprite.spritecollideany(self, collisions, callback)
        if collide and not self.collision_direction:
            self.collision_direction = self.get_collision_direction(collide)
        while collide:
            self.rect[i] += 1 if change < 0 else -1
            collide = pg.sprite.spritecollideany(self, collisions, callback)

    def get_collision_direction(self, other_sprite):
        """Find what side of an object the player is running into."""
        dx = self.get_finite_difference(other_sprite, 0, self.speed)
        dy = self.get_finite_difference(other_sprite, 1, self.speed)
        abs_x, abs_y = abs(dx), abs(dy)
        if abs_x > abs_y:
            return "right" if dx > 0 else "left"
        elif abs_x < abs_y:
            return "bottom" if dy > 0 else "top"
        else:
            return OPPOSITE_DICT[self.direction]

    def get_finite_difference(self, other_sprite, index, delta=1):
        """
        Find the finite difference in area of mask collision with the
        rects position incremented and decremented in axis index.
        """
        base_offset = [
            other_sprite.rect.x - self.rect.x,
            other_sprite.rect.y - self.rect.y,
        ]
        offset_high = base_offset[:]
        offset_low = base_offset[:]
        offset_high[index] += delta
        offset_low[index] -= delta
        first_term = self.mask.overlap_area(other_sprite.mask, offset_high)
        second_term = self.mask.overlap_area(other_sprite.mask, offset_low)
        return first_term - second_term

    def draw(self, surface):
        """Draw method seperated out from update."""
        surface.blit(self.image, self.rect)


class Block(pg.sprite.Sprite):
    """Something to run head-first into."""

    def __init__(self, location):
        """The location argument is where I will be located."""
        pg.sprite.Sprite.__init__(self)
        self.image = self.make_image()
        self.rect = self.image.get_rect(topleft=location)
        self.mask = pg.mask.from_surface(self.image)

    def make_image(self):
        """Let's not forget aesthetics."""
        image = pg.Surface((50, 50)).convert_alpha()
        image.fill([random.randint(0, 255) for _ in range(3)])
        image.blit(SHADE_MASK, (0, 0))
        return image


class Control(object):
    """Being controlling is our job."""

    text_cache = {}

    def __init__(self):
        """Initialize standard attributes standardly."""
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.done = False
        self.keys = pg.key.get_pressed()
        self.player = Player((0, 0, 50, 50), 3)
        self.player.rect.center = self.screen_rect.center
        self.obstacles = self.make_obstacles()

    def make_obstacles(self):
        """Prepare some obstacles for our player to collide with."""
        obstacles = [Block((400, 400)), Block((300, 270)), Block((150, 170))]
        for i in range(9):
            obstacles.append(Block((i * 50, 0)))
            obstacles.append(Block((450, 50 * i)))
            obstacles.append(Block((50 + i * 50, 450)))
            obstacles.append(Block((0, 50 + 50 * i)))
        return pg.sprite.Group(obstacles)

    def render_text(self, text, font, color, cache=True):
        """
        Returns a rendered surface of the text; if available the surface is
        retrieved from the text_cache to avoid rerendering.
        """
        if text in Control.text_cache:
            return Control.text_cache[text]
        else:
            image = font.render(text, True, color)
            if cache:
                Control.text_cache[text] = image
            return image

    def event_loop(self):
        """Add/pop directions from player's direction stack as necessary."""
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.player.add_direction(event.key)
            elif event.type == pg.KEYUP:
                self.player.pop_direction(event.key)

    def draw(self):
        """Draw all elements to the display surface."""
        self.screen.fill(BACKGROUND_COLOR)
        self.obstacles.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_collision_direction()

    def draw_collision_direction(self):
        """Blit a message to the screen if player is colliding."""
        if self.player.collision_direction:
            direction = self.player.collision_direction
            text = "Collided with {} edge.".format(direction)
            image = self.render_text(text, FONT, TEXT_COLOR)
            rect = image.get_rect(center=(self.screen_rect.centerx, 375))
            self.screen.blit(image, rect)

    def display_fps(self):
        """Show the program's FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps())
        pg.display.set_caption(caption)

    def main_loop(self):
        """Our main game loop; I bet you'd never have guessed."""
        while not self.done:
            self.event_loop()
            self.player.update(self.obstacles)
            self.draw()
            pg.display.update()
            self.clock.tick(self.fps)
            self.display_fps()


def get_images(sheet, frame_indices, size):
    """Get desired images from a sprite sheet."""
    frames = []
    for cell in frame_indices:
        frame_rect = ((size[0] * cell[0], size[1] * cell[1]), size)
        frames.append(sheet.subsurface(frame_rect))
    return frames


def main():
    """Initialize, load our images, create font object, and run the program."""
    global SKEL_IMAGE, SHADE_MASK, FONT
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    SKEL_IMAGE = pg.image.load("skelly.png").convert()
    SKEL_IMAGE.set_colorkey(COLOR_KEY)
    SHADE_MASK = pg.image.load("shader.png").convert_alpha()
    FONT = pg.font.SysFont("arial", 30)
    Control().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
