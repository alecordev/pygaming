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


from pygame import *
from render import *
from resources import *
from common import lengthBetweenPoints
from playerCreation import player


class interfaceInSpace:
    def __init__(self):
        self.starsystem_button_tex = starsystem_ICON_tex
        self.galaxy_button_rect = pygame.Rect(
            (
                VIEW_WIDTH - (INTERFACE_ICON_SIZE + 5),
                VIEW_HEIGHT - (INTERFACE_ICON_SIZE + 5),
            ),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )

    def mouseInteraction(self, (mx, my), lb, (vpCoordinate_x, vpCoordinate_y)):
        CURSOR_INTERSECT_OBJECT = False

        mxvp = mx + vpCoordinate_x
        myvp = my + vpCoordinate_y

        ####################################################################################################
        if CURSOR_INTERSECT_OBJECT != True:
            ss_cursor_dist = lengthBetweenPoints(
                (
                    self.galaxy_button_rect.centerx + vpCoordinate_x,
                    self.galaxy_button_rect.centery + vpCoordinate_y,
                ),
                (mxvp, myvp),
            )
            if ss_cursor_dist < self.galaxy_button_rect[2] / 2:
                CURSOR_INTERSECT_OBJECT = True

                if lb == True:
                    if player.in_WORLDMAP == False:
                        player.in_WORLDMAP = True
                    else:
                        player.in_WORLDMAP = False

        ####################################################################################################

        if CURSOR_INTERSECT_OBJECT == True:
            return True
        else:
            return False

    def render(self):
        glLoadIdentity()
        drawTexturedRect(self.starsystem_button_tex, self.galaxy_button_rect, -1.0)
        # print self.galaxy_button_rect
