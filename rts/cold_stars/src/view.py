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


import OpenGL

OpenGL.ERROR_CHECKING = False
OpenGL.ERROR_LOGGING = False

from OpenGL.GL import *
from OpenGL.GLU import *

from math import *


class view:
    def __init__(self, screen_w, screen_h):
        self.width = screen_w
        self.height = screen_h
        self.fov = 45
        self.aspect = screen_w / float(screen_h)

        self.ortho_near = 1.0
        self.ortho_far = 1000.0

        self.perspective_near = 0.1
        self.perspective_far = 10.0

        self.z_for_particles = -3
        temp = 2 * self.z_for_particles * tan(self.fov * 3.14159265 / 360.0)

        self.rate_x = temp * self.aspect / float(self.width)
        self.rate_y = temp / float(self.height)

        self.w_div_2_mult_rate_x = self.width / 2 * self.rate_x
        self.h_div_2_mult_rate_y = self.height / 2 * self.rate_y

    def setOrtho(self):
        glViewport(0, 0, self.width, self.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(0, self.width, 0, self.height, self.ortho_near, self.ortho_far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def setOrtho2(self):
        # needs for particle system. in future it should be removed
        glViewport(0, 0, self.width, self.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(0, self.width, 0, self.height, -1.0, self.ortho_far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def setPerspective(self):
        glViewport(0, 0, self.width, self.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(
            self.fov, self.aspect, self.perspective_near, self.perspective_far
        )

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def pushView(self):
        self.glLibInternal_current_view = glGetIntegerv(GL_VIEWPORT)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

    def popView(self):
        glViewport(*self.glLibInternal_current_view)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
