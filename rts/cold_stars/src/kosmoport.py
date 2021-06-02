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
from angar import *
from store import *
from shop import *
from goverment import *


class Kosmoport:
    def __init__(self, race_id):
        self.interface = None

        angarBg_texOb = TEXTURE_MANAGER.angarBg_texOb_list[0]
        storeBg_texOb = TEXTURE_MANAGER.storeBg_texOb_list[0]
        shopBg_texOb = TEXTURE_MANAGER.shopBg_texOb_list[0]
        govermentBg_texOb = TEXTURE_MANAGER.govermentBg_texOb_list[0]

        face_texOb = TEXTURE_MANAGER.returnRandomFaceTexObByRaceId(race_id)

        self.angar = Angar(angarBg_texOb)
        self.store = Store(storeBg_texOb)
        self.shop = Shop(shopBg_texOb)
        self.goverment = Goverment(govermentBg_texOb, face_texOb)
