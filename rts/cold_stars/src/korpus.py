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


from common import *
from resources import *
from slot import *


class KorpusInstance:
    def __init__(
        self,
        texOb,
        max_weapons,
        grapple_INHIBIT,
        space,
        armor_max,
        protection,
        nominal_temperature,
    ):
        self.texOb = texOb

        self.slot_tex_ID, (self.slot_w, self.slot_h) = slot_tex_ID, (slot_w, slot_h)

        self.w, self.h = texOb.w, texOb.h
        self.w_orig = self.w

        self.space = space
        self.armor_max = armor_max
        self.armor = armor_max
        self.protection = protection
        self.nominal_temperature = nominal_temperature

        self.race = texOb.race_id
        self.type = KORPUS_ID
        self.subtype = texOb.subtype_id
        self.size = texOb.size_id
        self.mod = texOb.mod_id

        self.color = texOb.color_id

        self.total_slot_list = []

        self.weapon_slot_list = []
        self.slot_list = []
        self.otsec_slot_list = []

        ######### KONTUR SIZE (RECT)
        if self.w > self.h:
            kontur_w = 500
            kontur_h = self.h * kontur_w / self.w
        else:
            kontur_h = 500
            kontur_w = self.w * kontur_h / self.h

        self.kontur_rect = pygame.Rect(0, 0, kontur_w, kontur_h)
        self.kontur_rect.center = (VIEW_WIDTH / 2, VIEW_HEIGHT / 3)
        #######################################################

        ######### WEAPONS SLOT
        self.weapon_slot1 = None
        self.weapon_slot2 = None
        self.weapon_slot3 = None
        self.weapon_slot4 = None
        self.weapon_slot5 = None

        if max_weapons >= 1:
            self.weapon_slot1 = SlotForShip(
                slot_tex_ID,
                (
                    self.kontur_rect.centerx + 1 * self.slot_w,
                    self.kontur_rect.centery - self.slot_h / 2,
                ),
                (self.slot_w, self.slot_h),
                WEAPON_ID,
                None,
            )
            self.total_slot_list.append(self.weapon_slot1)
            self.weapon_slot_list.append(self.weapon_slot1)

        if max_weapons >= 2:
            self.weapon_slot2 = SlotForShip(
                slot_tex_ID,
                (
                    self.kontur_rect.centerx + 1 * self.slot_w,
                    self.kontur_rect.centery - self.slot_h / 2 + 1.1 * self.slot_h,
                ),
                (self.slot_w, self.slot_h),
                WEAPON_ID,
                None,
            )
            self.total_slot_list.append(self.weapon_slot2)
            self.weapon_slot_list.append(self.weapon_slot2)

        if max_weapons >= 3:
            self.weapon_slot3 = SlotForShip(
                slot_tex_ID,
                (
                    self.kontur_rect.centerx + 1 * self.slot_w,
                    self.kontur_rect.centery - self.slot_h / 2 - 1.1 * self.slot_h,
                ),
                (self.slot_w, self.slot_h),
                WEAPON_ID,
                None,
            )
            self.total_slot_list.append(self.weapon_slot3)
            self.weapon_slot_list.append(self.weapon_slot3)

        if max_weapons >= 4:
            self.weapon_slot4 = SlotForShip(
                slot_tex_ID,
                (
                    self.kontur_rect.centerx + 2.2 * self.slot_w,
                    self.kontur_rect.centery - self.slot_h / 2 + 1.1 * self.slot_h / 2,
                ),
                (self.slot_w, self.slot_h),
                WEAPON_ID,
                None,
            )
            self.total_slot_list.append(self.weapon_slot4)
            self.weapon_slot_list.append(self.weapon_slot4)

        if max_weapons >= 5:
            self.weapon_slot5 = SlotForShip(
                slot_tex_ID,
                (
                    self.kontur_rect.centerx + 2.2 * self.slot_w,
                    self.kontur_rect.centery - self.slot_h / 2 - 1.1 * self.slot_h / 2,
                ),
                (self.slot_w, self.slot_h),
                WEAPON_ID,
                None,
            )
            self.total_slot_list.append(self.weapon_slot5)
            self.weapon_slot_list.append(self.weapon_slot5)

        total_weapon_num = len(self.weapon_slot_list)
        #####################################################

        ######### EQUPMENT SLOT
        self.drive_slot = SlotForShip(
            slot_tex_ID,
            (
                self.kontur_rect.centerx - 5 * self.slot_w,
                self.kontur_rect.centery - self.slot_h / 2 + 1.1 * self.slot_h / 2,
            ),
            (self.slot_w, self.slot_h),
            EQUIPMENT_ID,
            DRIVE_ID,
        )
        self.total_slot_list.append(self.drive_slot)

        self.bak_slot = SlotForShip(
            slot_tex_ID,
            (
                self.kontur_rect.centerx - 5 * self.slot_w,
                self.kontur_rect.centery - self.slot_h / 2 - 1.1 * self.slot_h / 2,
            ),
            (self.slot_w, self.slot_h),
            EQUIPMENT_ID,
            BAK_ID,
        )
        self.total_slot_list.append(self.bak_slot)

        self.radar_slot = SlotForShip(
            slot_tex_ID,
            (
                self.kontur_rect.centerx + 4 * self.slot_w,
                self.kontur_rect.centery - self.slot_h / 2 + 1.1 * self.slot_h / 2,
            ),
            (self.slot_w, self.slot_h),
            EQUIPMENT_ID,
            RADAR_ID,
        )
        self.total_slot_list.append(self.radar_slot)

        self.scaner_slot = SlotForShip(
            slot_tex_ID,
            (
                self.kontur_rect.centerx + 4 * self.slot_w,
                self.kontur_rect.centery - self.slot_h / 2 - 1.1 * self.slot_h / 2,
            ),
            (self.slot_w, self.slot_h),
            EQUIPMENT_ID,
            SCANER_ID,
        )
        self.total_slot_list.append(self.scaner_slot)

        self.energyBlock_slot = SlotForShip(
            slot_tex_ID,
            (
                self.kontur_rect.centerx - 2 * self.slot_w,
                self.kontur_rect.centery - self.slot_h / 2,
            ),
            (self.slot_w, self.slot_h),
            EQUIPMENT_ID,
            ENERGYBLOCK_ID,
        )
        self.total_slot_list.append(self.energyBlock_slot)

        if grapple_INHIBIT == False:
            self.grapple_slot = SlotForShip(
                slot_tex_ID,
                (
                    self.kontur_rect.centerx - 3 * self.slot_w,
                    self.kontur_rect.centery - self.slot_h / 2 + 1.1 * self.slot_h,
                ),
                (self.slot_w, self.slot_h),
                EQUIPMENT_ID,
                GRAPPLE_ID,
            )
            self.total_slot_list.append(self.grapple_slot)
        else:
            self.grapple_slot = None

        self.protector_slot = SlotForShip(
            slot_tex_ID,
            (
                self.kontur_rect.centerx - 3 * self.slot_w,
                self.kontur_rect.centery - self.slot_h / 2 - 1.1 * self.slot_h,
            ),
            (self.slot_w, self.slot_h),
            EQUIPMENT_ID,
            PROTECTOR_ID,
        )
        self.total_slot_list.append(self.protector_slot)

        self.droid_slot = SlotForShip(
            slot_tex_ID,
            (
                self.kontur_rect.centerx - 1 * self.slot_w,
                self.kontur_rect.centery - self.slot_h / 2 + 1.1 * self.slot_h,
            ),
            (self.slot_w, self.slot_h),
            EQUIPMENT_ID,
            DROID_ID,
        )
        self.total_slot_list.append(self.droid_slot)

        self.freezer_slot = SlotForShip(
            slot_tex_ID,
            (
                self.kontur_rect.centerx - 1 * self.slot_w,
                self.kontur_rect.centery - self.slot_h / 2 - 1.1 * self.slot_h,
            ),
            (self.slot_w, self.slot_h),
            EQUIPMENT_ID,
            FREEZER_ID,
        )
        self.total_slot_list.append(self.freezer_slot)
        ##################################################

        ######### OTSEC SLOT
        i = 1
        otsec_max = 10
        while i <= otsec_max:
            self.otsec_slot = SlotForShip(
                slot_tex_ID,
                (
                    self.kontur_rect.centerx - 6 * self.slot_w + i * 1.0 * self.slot_w,
                    self.kontur_rect.centery - 3 * self.slot_h,
                ),
                (self.slot_w, self.slot_h),
                OTSEC_SLOT_ID,
                None,
            )
            self.total_slot_list.append(self.otsec_slot)
            i += 1
        #################################################

        ######### GATE SLOT
        self.gate = SlotForShip(
            slot_tex_ID,
            (
                self.kontur_rect.centerx - 5 * self.slot_w,
                self.kontur_rect.centery + 3 * self.slot_h,
            ),
            (self.slot_w, self.slot_h),
            GATE_SLOT_ID,
            None,
        )
        self.total_slot_list.append(self.gate)
        #################################################

        self.removeAllItemsFromAllSlots()

        for slot in self.total_slot_list:
            if slot.type != OTSEC_SLOT_ID:
                self.slot_list.append(slot)
            else:
                self.otsec_slot_list.append(slot)

        # !!!NEW
        self.owner = None

        self.price = randint(200, 400)
        self.info = [
            "space:" + str(self.space),
            "armor" + str(self.armor_max) + "/" + str(self.armor),
            "protection:" + str(self.protection),
            "price:" + str(self.price),
        ]

        self.renderInSlot = self._renderFrame
        self.texture = self.texOb.texture

    def removeAllItemsFromAllSlots(self):
        for slot in self.total_slot_list:
            slot.item = None

    def _renderFrame(self, slot_rect):
        drawTexturedRect(self.texture, slot_rect, -1.0)

    def _renderFrames(self, slot_rect):
        drawTexturedRect(self.texture_ID[self._tex_frame], slot_rect, -1.0)
        self.updateAnimationFrameLoop()


def korpusGenerator(race, subtype, size, mod):
    grapple_INHIBIT = False

    if race == -1:
        race = RACES_LIST[randint(0, len(RACES_LIST) - 1)]

    if subtype == -1:
        if race == RACE_0_ID:
            subtype = TEXTURE_MANAGER.RACE0_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE0_SHIP_SUBTYPE_list) - 1)
            ]
        elif race == RACE_1_ID:
            subtype = TEXTURE_MANAGER.RACE1_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE1_SHIP_SUBTYPE_list) - 1)
            ]
        elif race == RACE_2_ID:
            subtype = TEXTURE_MANAGER.RACE2_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE2_SHIP_SUBTYPE_list) - 1)
            ]
        elif race == RACE_3_ID:
            subtype = TEXTURE_MANAGER.RACE3_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE3_SHIP_SUBTYPE_list) - 1)
            ]
        elif race == RACE_4_ID:
            subtype = TEXTURE_MANAGER.RACE4_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE4_SHIP_SUBTYPE_list) - 1)
            ]

        elif race == RACE_6_ID:
            subtype = TEXTURE_MANAGER.RACE6_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE6_SHIP_SUBTYPE_list) - 1)
            ]
        elif race == RACE_7_ID:
            subtype = TEXTURE_MANAGER.RACE7_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE7_SHIP_SUBTYPE_list) - 1)
            ]

    if size == -1:
        if race == RACE_0_ID:
            size = TEXTURE_MANAGER.RACE0_SHIP_SIZE_list[
                randint(0, len(TEXTURE_MANAGER.RACE0_SHIP_SIZE_list) - 1)
            ]
        elif race == RACE_1_ID:
            size = TEXTURE_MANAGER.RACE1_SHIP_SIZE_list[
                randint(0, len(TEXTURE_MANAGER.RACE1_SHIP_SIZE_list) - 1)
            ]
        elif race == RACE_2_ID:
            size = TEXTURE_MANAGER.RACE2_SHIP_SIZE_list[
                randint(0, len(TEXTURE_MANAGER.RACE2_SHIP_SIZE_list) - 1)
            ]
        elif race == RACE_3_ID:
            size = TEXTURE_MANAGER.RACE3_SHIP_SIZE_list[
                randint(0, len(TEXTURE_MANAGER.RACE3_SHIP_SIZE_list) - 1)
            ]
        elif race == RACE_4_ID:
            size = TEXTURE_MANAGER.RACE4_SHIP_SIZE_list[
                randint(0, len(TEXTURE_MANAGER.RACE4_SHIP_SIZE_list) - 1)
            ]

        elif race == RACE_6_ID:
            size = TEXTURE_MANAGER.RACE6_SHIP_SIZE_list[
                randint(0, len(TEXTURE_MANAGER.RACE6_SHIP_SIZE_list) - 1)
            ]
        elif race == RACE_7_ID:
            size = TEXTURE_MANAGER.RACE7_SHIP_SIZE_list[
                randint(0, len(TEXTURE_MANAGER.RACE7_SHIP_SIZE_list) - 1)
            ]

    if mod == -1:
        if race == RACE_0_ID:
            mod = TEXTURE_MANAGER.RACE0_SHIP_MOD_list[
                randint(0, len(TEXTURE_MANAGER.RACE0_SHIP_MOD_list) - 1)
            ]
        elif race == RACE_1_ID:
            mod = TEXTURE_MANAGER.RACE1_SHIP_MOD_list[
                randint(0, len(TEXTURE_MANAGER.RACE1_SHIP_MOD_list) - 1)
            ]
        elif race == RACE_2_ID:
            mod = TEXTURE_MANAGER.RACE2_SHIP_MOD_list[
                randint(0, len(TEXTURE_MANAGER.RACE2_SHIP_MOD_list) - 1)
            ]
        elif race == RACE_3_ID:
            mod = TEXTURE_MANAGER.RACE3_SHIP_MOD_list[
                randint(0, len(TEXTURE_MANAGER.RACE3_SHIP_MOD_list) - 1)
            ]
        elif race == RACE_4_ID:
            mod = TEXTURE_MANAGER.RACE4_SHIP_MOD_list[
                randint(0, len(TEXTURE_MANAGER.RACE4_SHIP_MOD_list) - 1)
            ]

        elif race == RACE_6_ID:
            mod = TEXTURE_MANAGER.RACE6_SHIP_MOD_list[
                randint(0, len(TEXTURE_MANAGER.RACE6_SHIP_MOD_list) - 1)
            ]
        elif race == RACE_7_ID:
            mod = TEXTURE_MANAGER.RACE7_SHIP_MOD_list[
                randint(0, len(TEXTURE_MANAGER.RACE7_SHIP_MOD_list) - 1)
            ]

    if subtype == RANGER_ID:
        max_weapons = randint(2, 5)
        subtype_space_kof = 1.0

    elif subtype == WARRIOR_ID:
        max_weapons = randint(3, 5)
        subtype_space_kof = 1.0

    elif subtype == PIRAT_ID:
        max_weapons = randint(3, 4)
        subtype_space_kof = 0.8

    elif subtype == TRADER_ID:
        max_weapons = randint(1, 3)
        subtype_space_kof = 1.2

    elif subtype == DIPLOMAT_ID:
        max_weapons = 1
        subtype_space_kof = 0.8
        grapple_INHIBIT = True

    if size == 0:
        size_space_kof = 1.0
    elif size == 1:
        size_space_kof = 1.1
    elif size == 2:
        size_space_kof = 1.2
    elif size == 3:
        size_space_kof = 1.3
    elif size == 4:
        size_space_kof = 1.4
    elif size == 5:
        size_space_kof = 1.5
    elif size == 6:
        size_space_kof = 1.6
    elif size == 7:
        size_space_kof = 1.7
    elif size == 8:
        size_space_kof = 1.8
    elif size == 9:
        size_space_kof = 1.9

    # print "desired data", (race, subtype, size, mod)
    ## print('race, subtype, size =', race, subtype, size

    ship_texOb_list = []
    for texOb in TEXTURE_MANAGER.ship_texOb_list:
        if texOb.race_id == race:
            ## print('texOb.subtype =', texOb.subtype
            if texOb.subtype_id == subtype:
                ## print('texOb.size', texOb.size
                ship_texOb_list.append(texOb)

    if len(ship_texOb_list) > 1:
        texOb = ship_texOb_list[randint(0, len(ship_texOb_list) - 1)]
    else:
        texOb = ship_texOb_list[0]

    space = int(
        subtype_space_kof * size_space_kof * randint(KORPUS_SPACE_MIN, KORPUS_SPACE_MAX)
    )
    armor_max = space
    protection = randint(KORPUS_PROTECTION_MIN, KORPUS_PROTECTION_MAX)
    nominal_temperature = randint(KORPUS_NOMINAL_TEMP_MIN, KORPUS_NOMINAL_TEMP_MAX)

    korpus = KorpusInstance(
        texOb,
        max_weapons,
        grapple_INHIBIT,
        space,
        armor_max,
        protection,
        nominal_temperature,
    )

    return korpus
