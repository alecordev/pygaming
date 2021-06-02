from itertools import chain

import pygame

import block
from config import Config


class Game:
    def __init__(self):
        self.walls = []
        self.boxs = []
        self.targets = []
        self.ncol = 0
        self.nrow = 0

    def add_block(self, type_, col, row):
        if type_ == "wall":
            self.walls.append(block.Block("wall.png", col, row))
        elif type_ == "box":
            self.boxs.append(block.Block("box.png", col, row))
        else:
            self.targets.append(block.Block("target.png", col, row))

    def update(self):
        pass

    def draw(self, window):
        for b in self.iter_all():
            b.draw(window)

    def is_valid(self, col, row):
        if 0 <= col < self.ncol and 0 <= row < self.nrow:
            size_t = Config.size_tile
            testcol = pygame.Rect(col * size_t, row * size_t, size_t, size_t)
            tmp = self.walls + self.boxs
            return testcol.collidelist(tmp) == -1
        else:
            return False

    def get_box(self, col, row):
        for b in self.boxs:
            if b.col == col and b.row == row:
                return b
        return None

    def iter_all(self):
        for b in chain(self.targets, self.walls, self.boxs):
            yield b

    def lvlcompleted(self):
        for box in self.boxs:
            match = False
            for target in self.targets:
                if box.col == target.col and box.row == target.row:
                    match = True
                    break
            if not match:
                return False
        return True
