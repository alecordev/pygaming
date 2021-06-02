"""
Copyright (C) ColdStars, Aleksandr Pivovarov <<coldstars8@gmail.com>>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""


from constants import *


class KeyEventsInKosmoport:
    def __init__(self, UPDATE):

        self.RUNNING = True
        self.turn_END = False
        self.ESC = False

        self.UPDATE = UPDATE

    def update(self):
        self.lb = False
        self.ESC = False
        self.mx, self.my = pygame.mouse.get_pos()
        self.my = (
            VIEW_HEIGHT - self.my
        )  # change direction of the Y axis (pygame and opengl Y axis are opposite)

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                self.RUNNING = False
                return self.RUNNING

            elif evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_SPACE:
                    self.turn_END = True

                if evt.key == pygame.K_ESCAPE:
                    self.ESC = True

            elif evt.type == pygame.MOUSEBUTTONDOWN:
                if evt.button == 1:
                    self.lb = True

            elif evt.type == pygame.KEYUP:
                if evt.key == pygame.K_SPACE:
                    self.turn_END = False

                if evt.key == pygame.K_ESCAPE:
                    self.ESC = False

            elif evt.type == self.UPDATE:
                pass

    def readControlKeys(self):
        self.update()
        return self.RUNNING, self.turn_END, self.lb, self.mx, self.my, self.ESC
