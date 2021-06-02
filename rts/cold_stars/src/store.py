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

from items import *
from slot import SlotForStore
from korpus import *


class Store:
    def __init__(self, bg_texOb):
        self.bg_texOb = bg_texOb

        self.slot_tex_ID, (self.slot_w, self.slot_h) = slot_tex_ID, (slot_w, slot_h)

        self.slot_w = self.slot_w / 1.3
        self.slot_h = self.slot_h / 1.3

        self.korpus_num = 3
        self.lazer_num = 3
        self.rocket_num = 2
        self.torped_num = 2
        self.radar_num = 1
        self.grapple_num = 1
        self.drive_num = 1
        self.protector_num = 1
        self.bak_num = 1
        self.droid_num = 1
        self.scaner_num = 1
        self.freezer_num = 1
        self.energyBlock_num = 1

        self.items_list = []
        self.storeInitItemsGenerator()

        self.slot_list = []
        self.createSlots()

        self.manageInitItems()

    def linkTexture(self):
        self.background_tex = self.bg_texOb.texture

    def unlinkTexture(self):
        self.background_tex = None

    def createSlots(self):
        row = 3
        clm = 10
        x0 = 120
        y0 = VIEW_HEIGHT - (row + 2) * self.slot_h

        row_act = 1
        while row_act <= row:
            clm_act = 1
            while clm_act <= clm:
                slot = SlotForStore(
                    slot_tex_ID,
                    (
                        x0 + clm_act * 1.1 * self.slot_w,
                        y0 + row_act * 1.1 * self.slot_h,
                    ),
                    (self.slot_w, self.slot_h),
                    STORE_SLOT_ID,
                    None,
                )
                slot.item = None
                self.slot_list.append(slot)
                clm_act += 1
            row_act += 1

    def manageInitItems(self):
        # used only once
        for item in self.items_list:
            slot = returnFirstFreeSlotBySlotType(STORE_SLOT_ID, None, self.slot_list)
            if slot != None:
                slot.item = item
                item.rect = slot.rect

    def soldItem(self, ob, slot):
        store_slot = returnFirstFreeSlotBySlotType(STORE_SLOT_ID, None, self.slot_list)
        if store_slot != None:
            store_slot.item = slot.item

            ob.credits += slot.item.price
            slot.item = None

    def buyItem(self, ob, slot):
        otsec_slot = returnFirstFreeSlotBySlotType(
            OTSEC_SLOT_ID, None, ob.korpus.otsec_slot_list
        )
        if otsec_slot != None:
            otsec_slot.item = slot.item
            ob.credits -= slot.item.price
            slot.item = None

    def buyKorpus(self, ob, slot):
        new_korpus = slot.item
        slot.item = ob.korpus
        slot.item.owner = None
        ob.credits += slot.item.price
        ob.credits -= new_korpus.price
        ob.setKorpus(new_korpus)

    def manager(self, player, left_button_click, (mx, my)):
        for slot in player.korpus.total_slot_list:
            slot_cursor_dist = lengthBetweenPoints(
                (slot.rect.centerx, slot.rect.centery), (mx, my)
            )
            if slot_cursor_dist < slot.rect[2] / 2:
                ############## sold item ##############
                if slot.item != None:
                    drawDynamicLabelList(
                        text_background_tex,
                        (slot.rect.right, slot.rect.bottom),
                        slot.item.info,
                    )
                    if left_button_click == True:
                        self.soldItem(player, slot)

        for slot in self.slot_list:
            slot_cursor_dist = lengthBetweenPoints(
                (slot.rect.centerx, slot.rect.centery), (mx, my)
            )
            if slot_cursor_dist < slot.rect[2] / 2:
                ############## buy item ##############
                if slot.item != None:
                    drawDynamicLabelList(
                        text_background_tex,
                        (slot.rect.right, slot.rect.bottom),
                        slot.item.info,
                    )
                    if left_button_click == True:
                        if player.credits >= slot.item.price:
                            if slot.item.type != KORPUS_ID:
                                self.buyItem(player, slot)
                            else:
                                self.buyKorpus(player, slot)

    def renderBackground(self):
        drawFullScreenTexturedQuad(self.background_tex, VIEW_WIDTH, VIEW_HEIGHT, -1)

    def renderInternals(self):
        for slot in self.slot_list:
            slot.render()

    def createAndAddKorpusItem(self, race_id, revision_id=-1):
        self.items_list.append(korpusGenerator(RACE_0_ID, WARRIOR_ID, 3, 0))

    def createAndAddLazerItem(self, race_id, revision_id=-1):
        self.items_list.append(lazerGenerator(race_id, revision_id))

    def createAndAddRocketItem(self, race_id, revision_id=-1):
        self.items_list.append(rocketGenerator(race_id, revision_id))

    def createAndAddTorpedItem(self, race_id, revision_id=-1):
        self.items_list.append(torpedGenerator(race_id, revision_id))

    def createAndAddRadarItem(self, race_id, revision_id=-1):
        self.items_list.append(radarGenerator(race_id, revision_id))

    def createAndAddGrappleItem(self, race_id, revision_id=-1):
        self.items_list.append(grappleGenerator(race_id, revision_id))

    def createAndAddDriveItem(self, race_id, revision_id=-1):
        self.items_list.append(driveGenerator(race_id, revision_id))

    def createAndAddProtectorItem(self, race_id, revision_id=-1):
        self.items_list.append(protectorGenerator(race_id, revision_id))

    def createAndAddBakItem(self, race_id, revision_id=-1):
        self.items_list.append(bakGenerator(race_id, revision_id))

    def createAndAddDroidItem(self, race_id, revision_id=-1):
        self.items_list.append(droidGenerator(race_id, revision_id))

    def createAndAddScanerItem(self, race_id, revision_id=-1):
        self.items_list.append(scanerGenerator(race_id, revision_id))

    def createAndAddFreezerItem(self, race_id, revision_id=-1):
        self.items_list.append(freezerGenerator(race_id, revision_id))

    def createAndAddEnergyBlockItem(self, race_id, revision_id=-1):
        self.items_list.append(energyBlockGenerator(race_id, revision_id))

    def storeInitItemsGenerator(self):
        race_id = RACES_GOOD_LIST[randint(0, len(RACES_GOOD_LIST) - 1)]
        revision_id = 0

        for i in range(0, int(self.korpus_num)):
            self.createAndAddKorpusItem(race_id, revision_id)

        for i in range(0, int(self.lazer_num)):
            self.createAndAddLazerItem(race_id, revision_id)

        for i in range(0, int(self.rocket_num)):
            self.createAndAddRocketItem(race_id, revision_id)

        for i in range(0, int(self.torped_num)):
            self.createAndAddTorpedItem(race_id, revision_id)

        for i in range(0, int(self.radar_num)):
            self.createAndAddRadarItem(race_id, revision_id)

        for i in range(0, int(self.grapple_num)):
            self.createAndAddGrappleItem(race_id, revision_id)

        for i in range(0, int(self.drive_num)):
            self.createAndAddDriveItem(race_id, revision_id)

        for i in range(0, int(self.protector_num)):
            self.createAndAddProtectorItem(race_id, revision_id)

        for i in range(0, int(self.bak_num)):
            self.createAndAddBakItem(race_id, revision_id)

        for i in range(0, int(self.droid_num)):
            self.createAndAddDroidItem(race_id, revision_id)

        for i in range(0, int(self.scaner_num)):
            self.createAndAddScanerItem(race_id, revision_id)

        for i in range(0, int(self.freezer_num)):
            self.createAndAddFreezerItem(race_id, revision_id)

        for i in range(0, int(self.energyBlock_num)):
            self.createAndAddEnergyBlockItem(race_id, revision_id)
