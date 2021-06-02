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


class KeyEventsInInvertar:
    def __init__(self, UPDATE):
        self.RUNNING = True
        self.UPDATE = UPDATE

    def update(self):
        self.mouse_left_button_click = False
        self.invertar_HIDE = False

        self.mx, self.my = pygame.mouse.get_pos()
        self.my = (
            VIEW_HEIGHT - self.my
        )  # change direction of the Y axis (pygame and opengl Y axis are opposite)

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                self.RUNNING = False
                return self.RUNNING

            elif evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_ESCAPE:
                    self.invertar_HIDE = True

            elif evt.type == pygame.MOUSEBUTTONDOWN:
                if evt.button == 1:
                    self.mouse_left_button_click = True

            elif evt.type == pygame.KEYUP:
                pass

            elif evt.type == self.UPDATE:
                pass

    def readControlKeys(self):
        self.update()
        return (
            self.RUNNING,
            self.invertar_HIDE,
            self.mx,
            self.my,
            self.mouse_left_button_click,
        )
