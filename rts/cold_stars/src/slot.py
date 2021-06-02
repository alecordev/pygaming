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


from common import CommonInstance
from constants import *
from render import *


class SlotCommon(CommonInstance):
    def __init__(self, texture_ID_list, (x, y), (w, h), type, subtype):
        CommonInstance.__init__(self, texture_ID_list, (w, h))
        if self.animated == False:
            self.render = self.renderFrame
        else:
            self.render = self.renderFrames

        self.rect = pygame.Rect(
            (x, y), (self.w, self.h)
        )  # create rect with size of the texture

        self.type = type
        self.subtype = subtype

        self.flash = False

        self.item = None
        self.FIRED = False
        self.target_EXIST = False
        self.SELECTED = False
        self.GL_LIST_slot_ID = None
        self.target = None


class SlotForShip(SlotCommon):
    def __init__(self, texture_ID_list, (x, y), (w, h), type, subtype):
        SlotCommon.__init__(self, texture_ID_list, (x, y), (w, h), type, subtype)

    def renderFrame(self, flash_tex):
        self.renderStaticFrame()
        if self.flash == True:
            drawTexturedRect(flash_tex, self.rect, -1.0)
        if self.item != None:
            self.item.renderInSlot(self.rect)

    def renderFrames(self, flash_tex):
        self.renderStaticFramesLoop()
        if self.flash == True:
            drawTexturedRect(flash_tex, self.rect, -1.0)
        if self.item != None:
            self.item.renderInSlot(self.rect)


class SlotForAngar(SlotCommon):
    def __init__(self, texture_ID_list, (x, y), (w, h), type, subtype):
        SlotCommon.__init__(self, texture_ID_list, (x, y), (w, h), type, subtype)

    def renderFrame(self):
        self.renderStaticFrame()
        if self.item != None:
            self.item.renderInKosmoport(self.rect)

    def renderFrames(self):
        self.renderStaticFramesLoop()
        if self.item != None:
            self.item.renderInKosmoport(self.rect)


class SlotForStore(SlotCommon):
    def __init__(self, texture_ID_list, (x, y), (w, h), type, subtype):
        SlotCommon.__init__(self, texture_ID_list, (x, y), (w, h), type, subtype)

    def renderFrame(self):
        self.renderStaticFrame()
        if self.item != None:
            self.item.renderInSlot(self.rect)

    def renderFrames(self):
        self.renderStaticFramesLoop()
        if self.item != None:
            self.item.renderInSlot(self.rect)


def putItemIn(item, slot):
    slot.item = item.item
    slot.item.rect.centerx = slot.rect.centerx
    slot.item.rect.centery = slot.rect.centery
    slot.item.rect[2] = slot.rect[2]
    slot.item.rect[3] = slot.rect[3]
