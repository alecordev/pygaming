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

from math import *


class points:
    def __init__(self):
        pass

    def createCenterPoint(self):
        self.center = [0, 0]

    def createRocketCascade(self, w, h):
        self.angle = 0
        self.w, self.h = w, h

        self.addMainQuad()

        self.addMidLeftPoint()  # trail vector
        self.addMidFarLeftPoint()  # drive trail vector

        self.updated = False

    def createSpaceShipCascade(self, w, h):
        self.angle = 0
        self.w, self.h = w, h

        self.addMainQuad()

        self.addMidLeftPoint()
        self.addMidFarLeftPoint()
        self.addShieldCascade()

        self.updated = False

    def addMainQuad(self):
        # Origin entity rect (for rotation only transformation)
        self.center_origin = [0, 0]
        self.bottomLeft_origin = [-self.w / 2, -self.h / 2]
        self.bottomRight_origin = [+self.w / 2, -self.h / 2]
        self.topRight_origin = [+self.w / 2, +self.h / 2]
        self.topLeft_origin = [-self.w / 2, +self.h / 2]

        # Actual entity rect
        self.center = [0, 0]
        self.bottomLeft = [-self.w / 2, -self.h / 2]
        self.bottomRight = [+self.w / 2, -self.h / 2]
        self.topRight = [+self.w / 2, +self.h / 2]
        self.topLeft = [-self.w / 2, +self.h / 2]

        self.points = [
            (self.center_origin, self.center),
            (self.bottomLeft_origin, self.bottomLeft),
            (self.bottomRight_origin, self.bottomRight),
            (self.topRight_origin, self.topRight),
            (self.topLeft_origin, self.topLeft),
        ]

    def addMidLeftPoint(self):
        self.midLeft_origin = [-self.w / 2, 0]
        self.midLeft = [-self.w / 2, 0]

        self.points.append((self.midLeft_origin, self.midLeft))

    def addMidFarLeftPoint(self):
        self.midFarLeft_origin = [-self.w, 0]
        self.midFarLeft = [-self.w, 0]

        self.points.append((self.midFarLeft_origin, self.midFarLeft))

    def addShieldCascade(self):
        factor = 1.6
        w, h = self.w, self.h

        # Origin entity rect (for rotation only transformation)
        self.bottomFarLeft_origin = [-w / factor, -h / factor]
        self.bottomFarRight_origin = [+w / factor, -h / factor]
        self.topFarRight_origin = [+w / factor, +h / factor]
        self.topFarLeft_origin = [-w / factor, +h / factor]

        # Actual entity rect
        self.bottomFarLeft = [-w / factor, -h / factor]
        self.bottomFarRight = [+w / factor, -h / factor]
        self.topFarRight = [+w / factor, +h / factor]
        self.topFarLeft = [-w / factor, +h / factor]

        self.points.append((self.bottomFarLeft_origin, self.bottomFarLeft))
        self.points.append((self.bottomFarRight_origin, self.bottomFarRight))
        self.points.append((self.topFarRight_origin, self.topFarRight))
        self.points.append((self.topFarLeft_origin, self.topFarLeft))

    def setCenter(self, pos_x, pos_y):
        self.center = [pos_x, pos_y]
        self.updated = False

    def setAngle(self, angle):
        self.angle = angle
        self.updated = False

    def update(self):  # will be moved plain C in future
        if self.updated == False:
            pos_x = self.center[0]
            pos_y = self.center[1]

            self.angle_degree = self.angle  # depr

            self.angle_radian = self.angle_degree / 57.295779
            cosa = cos(self.angle_radian)
            sina = sin(self.angle_radian)

            for (p_origin, p) in self.points:
                # rotation around center
                p[0] = (p_origin[0]) * cosa - (p_origin[1]) * sina
                p[1] = (p_origin[0]) * sina + (p_origin[1]) * cosa
                # moving to position
                p[0] += pos_x
                p[1] += pos_y

            self.updated = True


# def rrr(self, angle, target_angle, angle_speed):
#    if (angle - target_angle) > 2*angle_speed:
#       if angle < target_angle:
#          angle += angle_speed
#       elif angle > target_angle:
#          angle -= angle_speed
#    return angle
