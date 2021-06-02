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


class interfaceInKosmoport:
    def __init__(self):
        self.angar_button_tex = angar_ICON_tex
        self.store_button_tex = store_ICON_tex
        self.shop_button_tex = shop_ICON_tex
        self.starsystem_button_tex = starsystem_ICON_tex
        self.goverment_button_tex = goverment_ICON_tex

        self.angar_button_rect = pygame.Rect(
            (
                VIEW_WIDTH - (INTERFACE_ICON_SIZE + 5),
                VIEW_HEIGHT - (INTERFACE_ICON_SIZE + 5),
            ),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )
        self.store_button_rect = pygame.Rect(
            (
                VIEW_WIDTH - 2 * (INTERFACE_ICON_SIZE + 5),
                VIEW_HEIGHT - (INTERFACE_ICON_SIZE + 5),
            ),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )
        self.shop_button_rect = pygame.Rect(
            (
                VIEW_WIDTH - 3 * (INTERFACE_ICON_SIZE + 5),
                VIEW_HEIGHT - (INTERFACE_ICON_SIZE + 5),
            ),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )
        self.starsystem_button_rect = pygame.Rect(
            (
                VIEW_WIDTH - 4 * (INTERFACE_ICON_SIZE + 5),
                VIEW_HEIGHT - (INTERFACE_ICON_SIZE + 5),
            ),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )
        self.goverment_button_rect = pygame.Rect(
            (
                VIEW_WIDTH - 5 * (INTERFACE_ICON_SIZE + 5),
                VIEW_HEIGHT - (INTERFACE_ICON_SIZE + 5),
            ),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )

        self.angar_scr_SELECTED = True
        self.store_scr_SELECTED = False
        self.shop_scr_SELECTED = False
        self.starsystem_scr_SELECTED = False
        self.goverment_scr_SELECTED = False

    def manager(self, lb, (mx, my)):
        CURSOR_INTERSECT_OBJECT = False
        angarbutton_cursor_dist = lengthBetweenPoints(
            (self.angar_button_rect.centerx, self.angar_button_rect.centery), (mx, my)
        )
        if angarbutton_cursor_dist < self.angar_button_rect[2] / 2:
            CURSOR_INTERSECT_OBJECT = True
            if lb == True:
                self.angar_scr_SELECTED = True
                self.store_scr_SELECTED = False
                self.shop_scr_SELECTED = False
                self.starsystem_scr_SELECTED = False
                self.goverment_scr_SELECTED = False

        if CURSOR_INTERSECT_OBJECT == False:
            storebutton_cursor_dist = lengthBetweenPoints(
                (self.store_button_rect.centerx, self.store_button_rect.centery),
                (mx, my),
            )
            if storebutton_cursor_dist < self.store_button_rect[2] / 2:
                CURSOR_INTERSECT_OBJECT = True
                if lb == True:
                    self.angar_scr_SELECTED = False
                    self.store_scr_SELECTED = True
                    self.shop_scr_SELECTED = False
                    self.starsystem_scr_SELECTED = False
                    self.goverment_scr_SELECTED = False

        if CURSOR_INTERSECT_OBJECT == False:
            shopbutton_cursor_dist = lengthBetweenPoints(
                (self.shop_button_rect.centerx, self.shop_button_rect.centery), (mx, my)
            )
            if shopbutton_cursor_dist < self.shop_button_rect[2] / 2:
                CURSOR_INTERSECT_OBJECT = True
                if lb == True:
                    self.angar_scr_SELECTED = False
                    self.store_scr_SELECTED = False
                    self.shop_scr_SELECTED = True
                    self.starsystem_scr_SELECTED = False
                    self.goverment_scr_SELECTED = False

        if CURSOR_INTERSECT_OBJECT == False:
            starsystembutton_cursor_dist = lengthBetweenPoints(
                (
                    self.starsystem_button_rect.centerx,
                    self.starsystem_button_rect.centery,
                ),
                (mx, my),
            )
            if starsystembutton_cursor_dist < self.starsystem_button_rect[2] / 2:
                CURSOR_INTERSECT_OBJECT = True
                if lb == True:
                    self.angar_scr_SELECTED = False
                    self.store_scr_SELECTED = False
                    self.shop_scr_SELECTED = False
                    self.starsystem_scr_SELECTED = True
                    self.goverment_scr_SELECTED = False

        if CURSOR_INTERSECT_OBJECT == False:
            govermentbutton_cursor_dist = lengthBetweenPoints(
                (
                    self.goverment_button_rect.centerx,
                    self.goverment_button_rect.centery,
                ),
                (mx, my),
            )
            if govermentbutton_cursor_dist < self.goverment_button_rect[2] / 2:
                CURSOR_INTERSECT_OBJECT = True
                if lb == True:
                    self.angar_scr_SELECTED = False
                    self.store_scr_SELECTED = False
                    self.shop_scr_SELECTED = False
                    self.starsystem_scr_SELECTED = False
                    self.goverment_scr_SELECTED = True

    def render(self):
        drawTexturedRect(self.angar_button_tex, self.angar_button_rect, -1)
        drawTexturedRect(self.store_button_tex, self.store_button_rect, -1)
        drawTexturedRect(self.shop_button_tex, self.shop_button_rect, -1)
        drawTexturedRect(self.starsystem_button_tex, self.starsystem_button_rect, -1)
        drawTexturedRect(self.goverment_button_tex, self.goverment_button_rect, -1)
