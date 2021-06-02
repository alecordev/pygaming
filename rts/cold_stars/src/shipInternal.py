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

from resources import *
from constants import *


class shipInternal:
    def __init__(self):
        self.mouse_rect = pygame.Rect((-slot_w / 2, -slot_h / 2), (slot_w, slot_h))
        self.taken_item = None
        self.SlotWithItemUnderCursor = None

    def setShip(self, ship):
        self.korpus = ship.korpus
        self.skill = ship.skill
        self.constructControlSkillButtons()

    def constructControlSkillButtons(self):
        x = self.korpus.kontur_rect.right
        y = self.korpus.kontur_rect.centery
        w = skill_w

        self.increment_attack_buttonRect = [x, y - w, w, w]
        self.decrement_attack_buttonRect = [x, y - 2 * w, w, w]

        self.increment_defence_buttonRect = [x + w, y - w, w, w]
        self.decrement_defence_buttonRect = [x + w, y - 2 * w, w, w]

        self.increment_leader_buttonRect = [x + 2 * w, y - w, w, w]
        self.decrement_leader_buttonRect = [x + 2 * w, y - 2 * w, w, w]

        self.increment_trader_buttonRect = [x + 3 * w, y - w, w, w]
        self.decrement_trader_buttonRect = [x + 3 * w, y - 2 * w, w, w]

        self.increment_technic_buttonRect = [x + 4 * w, y - w, w, w]
        self.decrement_technic_buttonRect = [x + 4 * w, y - 2 * w, w, w]

        self.increment_diplomat_buttonRect = [x + 5 * w, y - w, w, w]
        self.decrement_diplomat_buttonRect = [x + 5 * w, y - 2 * w, w, w]

    def skillManager(self, ob, lb, mx, my):
        button_w, button_h = (
            self.increment_attack_buttonRect[2],
            self.increment_attack_buttonRect[3],
        )

        ### ATTACK
        button_cursor_dist = lengthBetweenPoints(
            (
                self.increment_attack_buttonRect[0] + button_w / 2,
                self.increment_attack_buttonRect[1] + button_h / 2,
            ),
            (mx, my),
        )
        if button_cursor_dist < self.increment_attack_buttonRect[2] / 2:
            if lb == True:
                ob.skill.incrementAttack()

        button_cursor_dist = lengthBetweenPoints(
            (
                self.decrement_attack_buttonRect[0] + button_w / 2,
                self.decrement_attack_buttonRect[1] + button_h / 2,
            ),
            (mx, my),
        )
        if button_cursor_dist < self.decrement_attack_buttonRect[2] / 2:
            if lb == True:
                ob.skill.decrementAttack()
        ### ATTACK

        ### DEFENCE
        button_cursor_dist = lengthBetweenPoints(
            (
                self.increment_defence_buttonRect[0] + button_w / 2,
                self.increment_defence_buttonRect[1] + button_h / 2,
            ),
            (mx, my),
        )
        if button_cursor_dist < self.increment_defence_buttonRect[2] / 2:
            if lb == True:
                ob.skill.incrementDefence()

        button_cursor_dist = lengthBetweenPoints(
            (
                self.decrement_defence_buttonRect[0] + button_w / 2,
                self.decrement_defence_buttonRect[1] + button_h / 2,
            ),
            (mx, my),
        )
        if button_cursor_dist < self.decrement_defence_buttonRect[2] / 2:
            if lb == True:
                ob.skill.decrementDefence()
        ### DEFENCE

        ### LEADER
        button_cursor_dist = lengthBetweenPoints(
            (
                self.increment_leader_buttonRect[0] + button_w / 2,
                self.increment_leader_buttonRect[1] + button_h / 2,
            ),
            (mx, my),
        )
        if button_cursor_dist < self.increment_leader_buttonRect[2] / 2:
            if lb == True:
                ob.skill.incrementLeader()

        button_cursor_dist = lengthBetweenPoints(
            (
                self.decrement_leader_buttonRect[0] + button_w / 2,
                self.decrement_leader_buttonRect[1] + button_h / 2,
            ),
            (mx, my),
        )
        if button_cursor_dist < self.decrement_leader_buttonRect[2] / 2:
            if lb == True:
                ob.skill.decrementLeader()
        ### LEADER

        ### TRADER
        button_cursor_dist = lengthBetweenPoints(
            (
                self.increment_trader_buttonRect[0] + button_w / 2,
                self.increment_trader_buttonRect[1] + button_h / 2,
            ),
            (mx, my),
        )
        if button_cursor_dist < self.increment_leader_buttonRect[2] / 2:
            if lb == True:
                ob.skill.incrementTrader()

        button_cursor_dist = lengthBetweenPoints(
            (
                self.decrement_trader_buttonRect[0] + button_w / 2,
                self.decrement_trader_buttonRect[1] + button_h / 2,
            ),
            (mx, my),
        )
        if button_cursor_dist < self.decrement_trader_buttonRect[2] / 2:
            if lb == True:
                ob.skill.decrementTrader()
        ### TRADER

        ### TECHNIC
        button_cursor_dist = lengthBetweenPoints(
            (
                self.increment_technic_buttonRect[0] + button_w / 2,
                self.increment_technic_buttonRect[1] + button_h / 2,
            ),
            (mx, my),
        )
        if button_cursor_dist < self.increment_technic_buttonRect[2] / 2:
            if lb == True:
                ob.skill.incrementTechnic()

        button_cursor_dist = lengthBetweenPoints(
            (
                self.decrement_technic_buttonRect[0] + button_w / 2,
                self.decrement_technic_buttonRect[1] + button_h / 2,
            ),
            (mx, my),
        )
        if button_cursor_dist < self.decrement_technic_buttonRect[2] / 2:
            if lb == True:
                ob.skill.decrementTechnic()
        ### TECHNIC

        ### DIPLOMAT
        button_cursor_dist = lengthBetweenPoints(
            (
                self.increment_diplomat_buttonRect[0] + button_w / 2,
                self.increment_diplomat_buttonRect[1] + button_h / 2,
            ),
            (mx, my),
        )
        if button_cursor_dist < self.increment_diplomat_buttonRect[2] / 2:
            if lb == True:
                ob.skill.incrementDiplomat()

        button_cursor_dist = lengthBetweenPoints(
            (
                self.decrement_diplomat_buttonRect[0] + button_w / 2,
                self.decrement_diplomat_buttonRect[1] + button_h / 2,
            ),
            (mx, my),
        )
        if button_cursor_dist < self.decrement_diplomat_buttonRect[2] / 2:
            if lb == True:
                ob.skill.decrementDiplomat()
        ### DIPLOMAT

    def renderSkill(self):
        x = self.korpus.kontur_rect.right
        y = self.korpus.kontur_rect.centery
        w = skill_w
        h = skill_h

        for i in range(0, self.skill.attack):
            drawTexturedRect(skill_tex, [x, y + i * h, w, h], -1.0)
        drawTexturedRect(plus_ICON_tex, self.increment_attack_buttonRect, -1.0)
        drawTexturedRect(minus_ICON_tex, self.decrement_attack_buttonRect, -1.0)

        for i in range(0, self.skill.defence):
            drawTexturedRect(skill_tex, [x + w, y + i * h, w, h], -1.0)
        drawTexturedRect(plus_ICON_tex, self.increment_defence_buttonRect, -1.0)
        drawTexturedRect(minus_ICON_tex, self.decrement_defence_buttonRect, -1.0)

        for i in range(0, self.skill.leader):
            drawTexturedRect(skill_tex, [x + 2 * w, y + i * h, w, h], -1.0)
        drawTexturedRect(plus_ICON_tex, self.increment_leader_buttonRect, -1.0)
        drawTexturedRect(minus_ICON_tex, self.decrement_leader_buttonRect, -1.0)

        for i in range(0, self.skill.trader):
            drawTexturedRect(skill_tex, [x + 3 * w, y + i * h, w, h], -1.0)
        drawTexturedRect(plus_ICON_tex, self.increment_trader_buttonRect, -1.0)
        drawTexturedRect(minus_ICON_tex, self.decrement_trader_buttonRect, -1.0)

        for i in range(0, self.skill.technic):
            drawTexturedRect(skill_tex, [x + 4 * w, y + i * h, w, h], -1.0)
        drawTexturedRect(plus_ICON_tex, self.increment_technic_buttonRect, -1.0)
        drawTexturedRect(minus_ICON_tex, self.decrement_technic_buttonRect, -1.0)

        for i in range(0, self.skill.diplomat):
            drawTexturedRect(skill_tex, [x + 5 * w, y + i * h, w, h], -1.0)
        drawTexturedRect(plus_ICON_tex, self.increment_diplomat_buttonRect, -1.0)
        drawTexturedRect(minus_ICON_tex, self.decrement_diplomat_buttonRect, -1.0)

    def renderItemInfoInSlot(self):
        if self.SlotWithItemUnderCursor != None:
            self.SlotWithItemUnderCursor.item.updateInfo()
            drawDynamicLabelList(
                text_background_tex,
                (
                    self.SlotWithItemUnderCursor.rect.right,
                    self.SlotWithItemUnderCursor.rect.bottom,
                ),
                self.SlotWithItemUnderCursor.item.info,
            )

    def renderKorpusInternally(self):
        drawTexturedRect(self.korpus.texture, self.korpus.kontur_rect, -1.0)
        for slot in self.korpus.total_slot_list:
            slot.render(slot_marked_tex)

        self.renderItemInfoInSlot()

        if self.taken_item != None:
            self.taken_item.renderInSlot(self.mouse_rect)
            if self.taken_item.type == MODULE_ID:
                for slot in self.korpus.total_slot_list:
                    if slot.item != None and slot.item.type != MODULE_ID:
                        if slot.item.subtype == self.taken_item.subtype:
                            drawTexturedRect(slot_marked_tex, slot.rect, -1.0)

    def slotManagerFullControl(self, lb, (mx, my)):
        self.mouse_rect.center = mx, my
        self.SlotWithItemUnderCursor = None

        for slot in self.korpus.slot_list:
            slot.flash = False

        ###########################  checking slot ##############################################
        for slot in self.korpus.total_slot_list:
            slot_cursor_dist = lengthBetweenPoints(
                (slot.rect.centerx, slot.rect.centery), (mx, my)
            )
            if slot_cursor_dist < slot.rect[2] / 2:
                ############## take item from the slot ##############
                if self.taken_item == None and slot.item != None:
                    self.SlotWithItemUnderCursor = slot
                    if lb == True:
                        self.taken_item = slot.item
                        slot.item = None
                        self.SlotWithItemUnderCursor = None
                        # print self.taken_item,'taken'

                ############## put item into slot ##################
                elif self.taken_item != None and slot.item == None:
                    if slot.type == self.taken_item.type:
                        if self.taken_item.type == WEAPON_ID:  # huck
                            if lb == True:
                                slot.item = self.taken_item
                                self.taken_item = None

                        elif self.taken_item.type == EQUIPMENT_ID:
                            if slot.subtype == self.taken_item.subtype:
                                if lb == True:
                                    slot.item = self.taken_item
                                    self.taken_item = None
                                    # print slot.item ,'placed'

                    elif slot.type == OTSEC_SLOT_ID:
                        if lb == True:
                            slot.item = self.taken_item
                            self.taken_item = None

                    elif slot.type == GATE_SLOT_ID:
                        if lb == True:
                            self.korpus.owner.dropToSpace(self.taken_item)

                            self.taken_item = None
                            self.korpus.owner.updateDriveAbility()

                elif self.taken_item != None and slot.item != None:
                    if (
                        self.taken_item.type == MODULE_ID
                        and slot.item.type != MODULE_ID
                    ):
                        if self.taken_item.subtype == slot.item.subtype:
                            if lb == True:
                                if slot.item.insertModule(self.taken_item):
                                    self.taken_item = None
                                    self.korpus.owner.updateDriveAbility()

        ############ flash comptable slot for taken item ######
        if self.taken_item != None:
            for slot in self.korpus.slot_list:
                if slot.type == self.taken_item.type:
                    if self.taken_item.type == WEAPON_ID:
                        slot.flash = True

                    elif self.taken_item.type == EQUIPMENT_ID:
                        if slot.subtype == self.taken_item.subtype:
                            slot.flash = True

    def slotManagerLimitedControl(self, lb, (mx, my)):
        self.SlotWithItemUnderCursor = None
        ###########################  checking slot ##############################################
        for slot in self.korpus.slot_list:
            slot_cursor_dist = lengthBetweenPoints(
                (slot.rect.centerx, slot.rect.centery), (mx, my)
            )
            if slot_cursor_dist < slot.rect[2] / 2:
                if slot.item != None:
                    self.SlotWithItemUnderCursor = slot

        ############################ checking otsec ################################################
        for slot in self.korpus.otsec_slot_list:
            slot_cursor_dist = lengthBetweenPoints(
                (slot.rect.centerx, slot.rect.centery), (mx, my)
            )
            if slot_cursor_dist < slot.rect[2] / 2:
                if slot.item != None:
                    self.SlotWithItemUnderCursor = slot

    def renderAll(self):
        glLoadIdentity()  ### !!!
        self.renderSkill()
        self.renderKorpusInternally()
        self.renderItemInfoInSlot()

    def renderInStore(self):
        # glLoadIdentity()     ### !!!
        self.renderKorpusInternally()
        self.renderItemInfoInSlot()
