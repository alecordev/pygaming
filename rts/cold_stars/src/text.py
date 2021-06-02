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


from random import randint
from render import drawSimpleColoredText


class vericalFlowText:
    def __init__(self, ob, str, color):
        self.expired = False
        self.ob = ob
        self.str = str
        self.color = color

        kof1 = 0.1 * randint(3, 18)
        kof2 = 0.1 * randint(5, 15)
        self.pos_x = ob.points.center[0] - ob.points.w / 2 * kof1
        self.pos_y = ob.points.center[1] + ob.points.h / 2 * kof2
        self.existance_time = 70  # TEXT_EXISTANCE_TIME
        self.speed = 2

    def update(self, timer):
        self.pos_y += self.speed
        if self.speed > 0.5:
            self.speed -= 0.1

        self.existance_time -= 1
        if self.existance_time < 0:
            self.ob.flow_TEXT_list.remove(self)

    def render(self):
        drawSimpleColoredText((self.pos_x, self.pos_y), self.str, self.color)
