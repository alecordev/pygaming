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
from common import *


class Camera:
    def __init__(self):
        self.camera_direction_list_x = []
        self.camera_direction_list_y = []
        self.i = 0
        self.speedr = 20
        self.list_END = True

    def direction(self, (vpCoordinate_x, vpCoordinate_y), player):
        if (
            (player.rect.centerx < VIEW_WIDTH / 8 + vpCoordinate_x)
            or (player.rect.centery < VIEW_HEIGHT / 8 + vpCoordinate_y)
            or (player.rect.centerx > VIEW_WIDTH / 1.2 + vpCoordinate_x)
            or (player.rect.centery > VIEW_HEIGHT / 1.2 + vpCoordinate_y)
        ) and self.list_END == True:
            self.camera_target_x = player.rect.centerx - VIEW_WIDTH / 2
            self.camera_target_y = player.rect.centery - VIEW_HEIGHT / 2
            (
                self.camera_direction_list_x,
                self.camera_direction_list_y,
                not_relevant,
            ) = follow_static_obj(
                (vpCoordinate_x, vpCoordinate_y),
                (self.camera_target_x, self.camera_target_y),
                self.speedr,
            )

            self.i = 0
            self.list_END = False

    def update(self, (vpCoordinate_x, vpCoordinate_y)):
        if self.list_END == False:
            if (
                vpCoordinate_x != self.camera_target_x
                or vpCoordinate_y != self.camera_target_y
            ):
                vpCoordinate_x = self.camera_direction_list_x[self.i]
                vpCoordinate_y = self.camera_direction_list_y[self.i]

                if self.i < len(self.camera_direction_list_x) - 2 * self.speedr:
                    self.i += self.speedr
                else:
                    self.i = len(self.camera_direction_list_x) - self.speedr
                    self.list_END = True
                return vpCoordinate_x, vpCoordinate_y
        else:
            return False, False
