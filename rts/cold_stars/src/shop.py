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
from render import *
from resources import *


class ShopItem:
    def __init__(self, item_icon_tex, (item_icon_w, item_icon_h), rect):
        self.item_icon_tex, (self.item_icon_w, self.item_icon_h) = (
            item_icon_tex,
            (item_icon_w, item_icon_h),
        )
        self.icon_rect = rect
        self.amount = 0
        self.price = 0
        self.subtype = None

        self.scroll_rect = pygame.Rect(
            self.icon_rect[0], self.icon_rect[1], self.icon_rect[2], self.icon_rect[3]
        )

    def renderIcon(self):
        drawTexturedRect(self.item_icon_tex, self.icon_rect, -1)

    def renderAmount(self):
        drawDynamicLabelList(
            slot_marked_tex,
            (
                self.icon_rect[0] + (self.icon_rect[2] + 5),
                self.icon_rect[1] + self.icon_rect[3],
            ),
            [str(self.amount) + ", 1 = " + str(self.price) + "$"],
        )


class Shop:
    def __init__(self, bg_texOb):
        self.bg_texOb = bg_texOb
        # self.background_tex = bg_texOb.texture
        self.item_list = []

        mineral_icon_rect = pygame.Rect(
            (VIEW_WIDTH - (INTERFACE_ICON_SIZE + 150), 1 * (INTERFACE_ICON_SIZE + 5)),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )
        food_icon_rect = pygame.Rect(
            (VIEW_WIDTH - (INTERFACE_ICON_SIZE + 150), 2 * (INTERFACE_ICON_SIZE + 5)),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )
        medicine_icon_rect = pygame.Rect(
            (VIEW_WIDTH - (INTERFACE_ICON_SIZE + 150), 3 * (INTERFACE_ICON_SIZE + 5)),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )
        military_icon_rect = pygame.Rect(
            (VIEW_WIDTH - (INTERFACE_ICON_SIZE + 150), 4 * (INTERFACE_ICON_SIZE + 5)),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )
        drug_icon_rect = pygame.Rect(
            (VIEW_WIDTH - (INTERFACE_ICON_SIZE + 150), 5 * (INTERFACE_ICON_SIZE + 5)),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )
        exclusive_icon_rect = pygame.Rect(
            (VIEW_WIDTH - (INTERFACE_ICON_SIZE + 150), 6 * (INTERFACE_ICON_SIZE + 5)),
            (INTERFACE_ICON_SIZE, INTERFACE_ICON_SIZE),
        )

        self.minerals = ShopItem(
            mineral_icon_tex, (mineral_icon_w, mineral_icon_h), mineral_icon_rect
        )
        self.item_list.append(self.minerals)

        self.food = ShopItem(food_icon_tex, (food_icon_w, food_icon_h), food_icon_rect)
        self.item_list.append(self.food)

        self.medicine = ShopItem(
            medicine_icon_tex, (medicine_icon_w, medicine_icon_h), medicine_icon_rect
        )
        self.item_list.append(self.medicine)

        self.military = ShopItem(
            military_icon_tex, (military_icon_w, military_icon_h), military_icon_rect
        )
        self.item_list.append(self.military)

        self.drug = ShopItem(drug_icon_tex, (drug_icon_w, drug_icon_h), drug_icon_rect)
        self.item_list.append(self.drug)

        self.exclusive = ShopItem(
            exclusive_icon_tex,
            (exclusive_icon_w, exclusive_icon_h),
            exclusive_icon_rect,
        )
        self.item_list.append(self.exclusive)

        self.minerals.amount = randint(MINERALS_AMOUNT_MIN, MINERALS_AMOUNT_MAX)
        self.food.amount = randint(FOOD_AMOUNT_MIN, FOOD_AMOUNT_MAX)
        self.medicine.amount = randint(MEDICINE_AMOUNT_MIN, MEDICINE_AMOUNT_MAX)
        self.military.amount = randint(MILITARY_AMOUNT_MIN, MILITARY_AMOUNT_MAX)
        self.drug.amount = randint(DRUG_AMOUNT_MIN, DRUG_AMOUNT_MAX)
        self.exclusive.amount = randint(EXCLUSIVE_AMOUNT_MIN, EXCLUSIVE_AMOUNT_MAX)

        self.updatePrices()

    def linkTexture(self):
        self.background_tex = self.bg_texOb.texture

    def unlinkTexture(self):
        self.background_tex = None

    def updatePrices(self):  # depr
        self.updateMineralsPrice()
        self.updateFoodPrice()
        self.updateMedicinePrice()
        self.updateMilitaryPrice()
        self.updateDrugPrice()
        self.updateExclusivePrice()

    def updateMineralsPrice(self):
        self.minerals.price = MINERAL_BASE_PRICE + int(
            MINERAL_BASE_PRICE * MINERALS_AMOUNT_MAX / (float(self.minerals.amount) + 1)
        )

    def updateFoodPrice(self):
        self.food.price = FOOD_BASE_PRICE + int(
            FOOD_BASE_PRICE * FOOD_AMOUNT_MAX / (float(self.food.amount) + 1)
        )

    def updateMedicinePrice(self):
        self.medicine.price = MEDICINE_BASE_PRICE + int(
            MEDICINE_BASE_PRICE
            * MEDICINE_AMOUNT_MAX
            / (float(self.medicine.amount) + 1)
        )

    def updateMilitaryPrice(self):
        self.military.price = MILITARY_BASE_PRICE + int(
            MILITARY_BASE_PRICE
            * MILITARY_AMOUNT_MAX
            / (float(self.military.amount) + 1)
        )

    def updateDrugPrice(self):
        self.drug.price = DRUG_BASE_PRICE + int(
            DRUG_BASE_PRICE * DRUG_AMOUNT_MAX / (float(self.drug.amount) + 1)
        )

    def updateExclusivePrice(self):
        self.exclusive.price = EXCLUSIVE_BASE_PRICE + int(
            EXCLUSIVE_BASE_PRICE
            * EXCLUSIVE_AMOUNT_MAX
            / (float(self.exclusive.amount) + 1)
        )

    def sell(self, goods):
        if goods.subtype == MINERAL_id:
            self.minerals.amount += goods.mass
            earn_money = goods.mass * self.minerals.price
            self.updateMineralsPrice()
            return earn_money

        elif goods.subtype == FOOD_id:
            self.food.amount += goods.mass
            earn_money = goods.mass * self.food.price
            self.updateFoodPrice()
            return earn_money

        elif goods.subtype == MEDICINE_id:
            self.medicine.amount += goods.mass
            earn_money = goods.mass * self.medicine.price
            self.updateMedicinePrice()
            return earn_money

        elif goods.subtype == MILITARY_id:
            self.military.amount += goods.mass
            earn_money = goods.mass * self.military.price
            self.updateMilitaryPrice()
            return earn_money

        elif goods.subtype == DRUG_id:
            self.drug.amount += goods.mass
            earn_money = goods.mass * self.drug.price
            self.updateDrugPrice()
            return earn_money

        elif goods.subtype == EXCLUSIVE_id:
            self.exclusive.amount += goods.mass
            earn_money = goods.mass * self.exclusive.price
            self.updateExclusivePrice()
            return earn_money

    def buy(self, item):
        if goods.subtype == MINERAL_id:
            self.minerals.amount -= goods.mass
            spend_money = goods.mass * self.minerals.price
            self.updateMineralsPrice()
            return spend_money

        elif goods.subtype == FOOD_id:
            self.food.amount -= goods.mass
            spend_money = goods.mass * self.food.price
            self.updateFoodPrice()
            return spend_money

        elif goods.subtype == MEDICINE_id:
            self.medicine.amount -= goods.mass
            spend_money = goods.mass * self.medicine.price
            self.updateMedicinePrice()
            return spend_money

        elif goods.subtype == MILITARY_id:
            self.military.amount -= goods.mass
            spend_money = goods.mass * self.military.price
            self.updateMilitaryPrice()
            return spend_money

        elif goods.subtype == DRUG_id:
            self.drug.amount -= goods.mass
            spend_money = goods.mass * self.drug.price
            self.updateDrugPrice()
            return spend_money

        elif goods.subtype == EXCLUSIVE_id:
            self.exclusive.amount -= goods.mass
            spend_money = goods.mass * self.exclusive.price
            self.updateExclusivePrice()
            return spend_money

    def renderBackground(self):
        drawFullScreenTexturedQuad(self.background_tex, VIEW_WIDTH, VIEW_HEIGHT, -1)

    def renderInternals(self):
        for item in self.item_list:
            item.renderIcon()
            item.renderAmount()
