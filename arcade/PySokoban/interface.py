import pygame

import game
import player
import util
from config import Config


class Interface:
    def __init__(self):
        pygame.display.init()
        pygame.display.set_caption("PySokoban")
        self.main_window = pygame.display.set_mode(Config.size_window)
        self.scrollx = 0
        self.scrolly = 0
        self.map_game = None
        self.map_clear = None
        self.human_player = None
        self.game_board = None

    def load_level(self, nlvl):
        self.human_player = player.Player()
        self.game_board = game.Game()
        lines = util.load_map(nlvl)
        height = 0
        width = 0
        for row, string in enumerate(lines):
            for col, char in enumerate(string):
                if char == "p":
                    self.human_player.set_position(col, row)
                elif char == "*":
                    self.game_board.add_block("wall", col, row)
                elif char == "#":
                    self.game_board.add_block("box", col, row)
                elif char == "o":
                    self.game_board.add_block("target", col, row)

        self.game_board.ncol = max((len(r) for r in lines)) - 1
        self.game_board.nrow = len(lines)
        height = Config.size_tile * self.game_board.nrow
        width = Config.size_tile * self.game_board.ncol
        self.map_game = pygame.Surface((width, height))
        self.map_game.fill(Config.backcolor)
        self.map_clear = self.map_game.copy()

        return self.human_player, self.game_board

    def draw(self, *items):
        self.scroll()
        self.map_game.blit(self.map_clear, dest=(0, 0))
        for item in items:
            item.draw(self.map_game)
        self.main_window.blit(self.map_game, dest=(self.scrollx, self.scrolly))

    def scroll(self):
        xp, yp = self.human_player.rect.center
        width = self.map_game.get_rect().w
        height = self.map_game.get_rect().h

        if xp + 250 > Config.widthwindow:
            if -1 * self.scrollx + Config.widthwindow < width:
                self.scrollx -= 2

        elif xp + 250 > 0:
            if self.scrollx < 0:
                self.scrollx += 2

        if yp + 250 > Config.heightwindow:
            if -1 * self.scrolly + Config.widthwindow < height:
                self.scrolly -= 2

        elif yp + 250 > 0:
            if self.scrolly < 0:
                self.scrolly += 2
