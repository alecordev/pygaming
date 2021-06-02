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
from render import *
from resources import *


class Goverment:
    def __init__(self, bg_texOb, face_texOb):
        self.bg_texOb = bg_texOb
        self.face_texOb = face_texOb

    def linkTexture(self):
        self.background_tex = self.bg_texOb.texture

    def unlinkTexture(self):
        self.background_tex = None

    def renderBackground(self):
        drawFullScreenTexturedQuad(self.background_tex, VIEW_WIDTH, VIEW_HEIGHT, -1)

    def renderFace(self):
        drawTexturedRect(self.face_texOb.texture, [VIEW_WIDTH - 250, 50, 150, 200], -1)
