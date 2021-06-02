from constants import *

from SpaceObjects import Bomb
from render import *
from starsystem import *
from common import *

# from textures import *
from resources import *
from effects import addExplosion
from common import *


def returnRaceTechRate(race):
    if race == RACE_0_ID:
        return RACE_0_TECH_RATE
    elif race == RACE_1_ID:
        return RACE_1_TECH_RATE
    elif race == RACE_2_ID:
        return RACE_2_TECH_RATE
    elif race == RACE_3_ID:
        return RACE_3_TECH_RATE
    elif race == RACE_4_ID:
        return RACE_4_TECH_RATE

    elif race == RACE_6_ID:
        return RACE_6_TECH_RATE
    elif race == RACE_7_ID:
        return RACE_7_TECH_RATE


def bombGenerator():
    texOb = TEXTURE_MANAGER.bomb_texOb_list[0]

    armor = randint(BOMB_ARMOR_MIN, BOMB_ARMOR_MAX)
    mass = randint(BOMB_MASS_MIN, BOMB_MASS_MAX)
    radius = randint(BOMB_RADIUS_MIN, BOMB_RADIUS_MAX)
    damage = randint(BOMB_DAMAGE_MIN, BOMB_DAMAGE_MAX)

    speed = randint(BOMB_SPEED_MIN, BOMB_SPEED_MAX)

    bomb = Bomb(texOb, armor, damage, radius, mass, speed)

    return bomb


class CommonForItems(CommonInstance):
    def __init__(
        self, race, item_texOb, modules_num_max, mass, condition_max, deterioration_rate
    ):
        self.item_texOb = item_texOb
        CommonInstance.__init__(
            self, self.item_texOb.texture, (self.item_texOb.w, self.item_texOb.h)
        )

        if self.animated == False:
            self.renderInSlot = self.renderFrame
        else:
            self.renderInSlot = self.renderFrames

        self.w, self.h = w, h
        self.in_SPACE = False  # this flag is needed for grap function to check if the item was already collected or not
        self.DAMAGED = False

        self.ID = 0
        self.race = race
        self.mass = mass
        self.modules_num_max = modules_num_max
        self.condition_max = condition_max
        self.condition = condition_max
        self.deterioration_rate = deterioration_rate
        self.modules_list = []
        self.days_LOCKED = 0
        self.price = 0
        self.info = []
        self.owner = None

    def deterioration(self):
        self.condition -= self.deterioration_rate
        if self.condition <= 0:
            self.DAMAGED = True
            if self.owner is not None:  # not sure if's it really needed
                self.updateOwnerPropetries()

    def repair(self):
        self.condition = self.condition_max
        if self.DAMAGED == True:
            self.DAMAGED = False

    def insertModule(self, module):
        if len(self.modules_list) < self.modules_num_max:
            module.activation(self)
            self.mass += module.mass
            self.modules_list.append(module)
            return True
        else:
            return False

    def renderFrame(self, slot_rect):
        self.renderStaticFrameOnRect(slot_rect)
        if self.subtype == ROCKET_ID or self.subtype == TORPED_ID:
            drawSimpleText(
                (slot_rect[0], slot_rect[1] + self.h / 2),
                str(self.ammo_max) + "/" + str(self.ammo),
            )

        i = 0
        for m in self.modules_list:
            drawTexturedRect(
                m.texture_ID,
                [
                    slot_rect[0] + (1.1 * INSERTED_MODULE_SIZE) * i,
                    slot_rect[1],
                    INSERTED_MODULE_SIZE,
                    INSERTED_MODULE_SIZE,
                ],
                -1,
            )
            i += 1

    def renderFrames(self, slot_rect):
        self.renderStaticFramesLoopOnRect(slot_rect)
        if self.subtype == ROCKET_ID or self.subtype == TORPED_ID:
            renderSimpleText(
                (slot_rect[0], slot_rect[1]), str(self.ammo_max) + "/" + str(self.ammo)
            )

        i = 0
        for m in self.modules_list:
            drawTexturedRect(
                m.texture_ID,
                [
                    slot_rect[0] + (1.1 * INSERTED_MODULE_SIZE) * i,
                    slot_rect[1],
                    INSERTED_MODULE_SIZE,
                    INSERTED_MODULE_SIZE,
                ],
                -1,
            )
            i += 1


class radarItem(CommonForItems):
    def __init__(
        self,
        race,
        item_texOb,
        radius_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    ):
        CommonForItems.__init__(
            self,
            race,
            item_texOb,
            modules_num_max,
            mass,
            condition_max,
            deterioration_rate,
        )

        self.type = EQUIPMENT_ID
        self.subtype = RADAR_ID

        self.radius_orig = radius_orig
        self.radius_add = 0

        self.updatePropetries()
        self.countPrice()
        self.updateInfo()

    def countPrice(self):
        radius_rate = float(self.radius_orig) / RADAR_RADIUS_MIN

        modules_num_rate = float(self.modules_num_max) / RADAR_MODULES_NUM_MAX

        effectiveness_rate = (
            RADAR_RADIUS_WEIGHT * radius_rate
            + RADAR_MODULES_NUM_WEIGHT * modules_num_rate
        )

        mass_rate = float(self.mass) / RADAR_MASS_MIN
        condition_rate = float(self.condition) / self.condition_max

        self.price = int((3 * effectiveness_rate - mass_rate - condition_rate) * 100)

    def updatePropetries(self):
        self.radius = self.radius_orig + self.radius_add

    def updateOwnerPropetries(self):
        self.owner.updateRadarAbility()

    def returnRadiusStr(self):
        if self.radius_add == 0:
            return "radius:" + str(self.radius_orig)
        else:
            return "radius:" + str(self.radius_orig) + "+" + str(self.radius_add)

    def updateInfo(self):
        self.info = [
            "RADAR",
            self.returnRadiusStr(),
            "modules:" + str(self.modules_num_max),
            "condition:" + str(self.condition) + "/" + str(self.condition_max),
            "mass:" + str(self.mass),
            "price:" + str(self.price),
        ]


def radarGenerator(race_id, revision_id=-1):
    tech_rate = returnRaceTechRate(race_id)

    item_texOb = TEXTURE_MANAGER.returnItemTexOb(RADAR_ITEM_TEXTURE_ID, revision_id)

    radius_orig = randint(RADAR_RADIUS_MIN, RADAR_RADIUS_MAX)
    modules_num_max = randint(RADAR_MODULES_NUM_MIN, RADAR_MODULES_NUM_MAX)

    mass = randint(RADAR_MASS_MIN, RADAR_MASS_MAX)
    condition_max = int(randint(RADAR_CONDITION_MIN, RADAR_CONDITION_MAX) * tech_rate)

    deterioration_rate = 1

    radar = radarItem(
        race_id,
        item_texOb,
        radius_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    )

    return radar


class driveItem(CommonForItems):
    def __init__(
        self,
        race,
        item_texOb,
        speed_orig,
        hyper_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    ):
        CommonForItems.__init__(
            self,
            race,
            item_texOb,
            modules_num_max,
            mass,
            condition_max,
            deterioration_rate,
        )

        self.type = EQUIPMENT_ID
        self.subtype = DRIVE_ID

        self.speed_orig = speed_orig
        self.speed_add = 0

        self.hyper_orig = hyper_orig
        self.hyper_add = 0

        self.pTexture = TEXTURE_MANAGER.returnParticleTexObBy_ColorID(
            self.item_texOb.color_id
        )
        self.pNum = 5
        self.pSize = 6
        self.pVelocity = 1.2
        self.pAlphaInit = 1.0
        self.pAlphaEnd = 0.0
        self.pd_alpha = 0.05

        self.updatePropetries()
        self.countPrice()
        self.updateInfo()

    def countPrice(self):
        speed_rate = float(self.speed_orig) / DRIVE_SPEED_MIN
        hyper_rate = float(self.hyper_orig) / DRIVE_HYPER_MIN
        modules_num_rate = float(self.modules_num_max) / DRIVE_MODULES_NUM_MAX

        effectiveness_rate = (
            DRIVE_SPEED_WEIGHT * speed_rate
            + DRIVE_HYPER_WEIGHT * hyper_rate
            + DRIVE_MODULES_NUM_WEIGHT * modules_num_rate
        )

        mass_rate = float(self.mass) / DRIVE_MASS_MIN
        condition_rate = float(self.condition) / self.condition_max

        self.price = int((3 * effectiveness_rate - mass_rate - condition_rate) * 100)

    def updatePropetries(self):
        self.speed = self.speed_orig + self.speed_add
        self.hyper = self.hyper_orig + self.hyper_add

    def updateOwnerPropetries(self):
        self.owner.updateDriveAbility()

    def returnSpeedStr(self):
        if self.speed_add == 0:
            return "speed:" + str(self.speed_orig)
        else:
            return "speed:" + str(self.speed_orig) + "+" + str(self.speed_add)

    def returnHyperStr(self):
        if self.hyper_add == 0:
            return "hyper:" + str(self.hyper_orig)
        else:
            return "hyper:" + str(self.hyper_orig) + "+" + str(self.hyper_add)

    def updateInfo(self):
        self.info = [
            "DRIVE",
            self.returnSpeedStr(),
            self.returnHyperStr(),
            "modules:" + str(self.modules_num_max),
            "condition:" + str(self.condition) + "/" + str(self.condition_max),
            "mass:" + str(self.mass),
            "price:" + str(self.price),
        ]


def driveGenerator(race_id, revision_id=-1):
    tech_rate = returnRaceTechRate(race_id)

    item_texOb = TEXTURE_MANAGER.returnItemTexOb(DRIVE_ITEM_TEXTURE_ID, revision_id)

    speed_orig = randint(DRIVE_SPEED_MIN, DRIVE_SPEED_MAX)
    hyper_orig = randint(DRIVE_HYPER_MIN, DRIVE_HYPER_MAX)
    modules_num_max = randint(DRIVE_MODULES_NUM_MIN, DRIVE_MODULES_NUM_MAX)

    mass = randint(DRIVE_MASS_MIN, DRIVE_MASS_MAX)
    condition_max = int(randint(DRIVE_CONDITION_MIN, DRIVE_CONDITION_MAX)) * tech_rate
    deterioration_rate = 1

    drive = driveItem(
        race_id,
        item_texOb,
        speed_orig,
        hyper_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    )
    return drive


class bakItem(CommonForItems):
    def __init__(
        self,
        race,
        item_texOb,
        fuel_max_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    ):
        CommonForItems.__init__(
            self,
            race,
            item_texOb,
            modules_num_max,
            mass,
            condition_max,
            deterioration_rate,
        )

        self.type = EQUIPMENT_ID
        self.subtype = BAK_ID

        self.fuel_max_orig = fuel_max_orig
        self.fuel_max_add = 0
        self.fuel_max = fuel_max_orig
        self.fuel = fuel_max_orig

        self.updatePropetries()
        self.countPrice()
        self.updateInfo()

    def countPrice(self):
        fuel_rate = float(self.fuel_max_orig) / BAK_FUEL_MIN
        modules_num_rate = float(self.modules_num_max) / BAK_MODULES_NUM_MAX

        effectiveness_rate = (
            BAK_FUEL_WEIGHT * fuel_rate + BAK_MODULES_NUM_WEIGHT * modules_num_rate
        )

        mass_rate = float(self.mass) / BAK_MASS_MIN
        condition_rate = float(self.condition) / self.condition_max

        self.price = int((3 * effectiveness_rate - mass_rate - condition_rate) * 100)

    def updatePropetries(self):
        self.fuel_max = self.fuel_max_orig + self.fuel_max_add

    def updateOwnerPropetries(self):
        self.owner.updateJumpAbility()

    def returnFuelStr(self):
        if self.fuel_max_add == 0:
            return "fuel:" + str(self.fuel_max_orig) + "/" + str(self.fuel)
        else:
            return (
                "fuel:"
                + str(self.fuel_max_orig)
                + "+"
                + str(self.fuel_max_add)
                + "/"
                + str(self.fuel)
            )

    def updateInfo(self):
        self.info = [
            "BAK",
            self.returnFuelStr(),
            "modules:" + str(self.modules_num_max),
            "condition:" + str(self.condition) + "/" + str(self.condition_max),
            "mass:" + str(self.mass),
            "price:" + str(self.price),
        ]


def bakGenerator(race_id, revision_id=-1):
    tech_rate = returnRaceTechRate(race_id)

    item_texOb = TEXTURE_MANAGER.returnItemTexOb(BAK_ITEM_TEXTURE_ID, revision_id)

    fuel_max_orig = randint(BAK_FUEL_MIN, BAK_FUEL_MAX)

    modules_num_max = randint(BAK_MODULES_NUM_MIN, BAK_MODULES_NUM_MAX)

    mass = randint(BAK_MASS_MIN, BAK_MASS_MAX)
    condition_max = int(randint(BAK_CONDITION_MIN, BAK_CONDITION_MAX) * tech_rate)

    deterioration_rate = 1

    bak = bakItem(
        race_id,
        item_texOb,
        fuel_max_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    )

    return bak


class energyBlockItem(CommonForItems):
    def __init__(
        self,
        race,
        item_texOb,
        energy_max_orig,
        restoration_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    ):
        CommonForItems.__init__(
            self,
            race,
            item_texOb,
            modules_num_max,
            mass,
            condition_max,
            deterioration_rate,
        )

        self.type = EQUIPMENT_ID
        self.subtype = ENERGYBLOCK_ID

        self.energy_max_orig = energy_max_orig
        self.energy_max_add = 0

        self.energy = energy_max_orig

        self.restoration_orig = restoration_orig
        self.restoration_add = 0

        self.updatePropetries()
        self.countPrice()
        self.updateInfo()

    def countPrice(self):
        energy_rate = float(self.energy_max_orig) / GENERATOR_ENERGY_MIN
        restoration_rate = float(self.restoration_orig) / GENERATOR_RESTORATION_MIN
        modules_num_rate = float(self.modules_num_max) / GENERATOR_MODULES_NUM_MAX

        effectiveness_rate = (
            GENERATOR_ENERGY_WEIGHT * energy_rate
            + GENERATOR_RESTORATION_WEIGHT * restoration_rate
            + GENERATOR_MODULES_NUM * modules_num_rate
        )

        mass_rate = float(self.mass) / GENERATOR_MASS_MIN
        condition_rate = float(self.condition) / self.condition_max

        self.price = int((3 * effectiveness_rate - mass_rate - condition_rate) * 100)

    def updatePropetries(self):
        self.energy_max = self.energy_max_orig + self.energy_max_add
        self.restoration = self.restoration_orig + self.restoration_add

    def updateOwnerPropetries(self):
        self.owner.updateEnergyAbility()

    def returnEnergyStr(self):
        if self.energy_max_add == 0:
            return "energy:" + str(self.energy_max_orig) + "/" + str(self.energy)
        else:
            return (
                "energy:"
                + str(self.energy_max_orig)
                + "+"
                + str(self.energy_max_add)
                + "/"
                + str(self.energy)
            )

    def returnRestorationStr(self):
        if self.restoration_add == 0:
            return "restoration:" + str(self.restoration_orig)
        else:
            return (
                "restoration:"
                + str(self.restoration_orig)
                + "+"
                + str(self.restoration_add)
            )

    def updateInfo(self):
        self.info = [
            "energyBlock",
            self.returnEnergyStr(),
            self.returnRestorationStr(),
            "modules:" + str(self.modules_num_max),
            "condition:" + str(self.condition) + "/" + str(self.condition_max),
            "mass:" + str(self.mass),
            "price:" + str(self.price),
        ]


def energyBlockGenerator(race_id, revision_id=-1):
    tech_rate = returnRaceTechRate(race_id)

    item_texOb = TEXTURE_MANAGER.returnItemTexOb(
        ENERGYBLOCK_ITEM_TEXTURE_ID, revision_id
    )

    energy_max_orig = randint(GENERATOR_ENERGY_MIN, GENERATOR_ENERGY_MAX)
    restoration_orig = randint(GENERATOR_RESTORATION_MIN, GENERATOR_RESTORATION_MAX)
    modules_num_max = randint(GENERATOR_MODULES_NUM_MIN, GENERATOR_MODULES_NUM_MAX)

    mass = randint(GENERATOR_MASS_MIN, GENERATOR_MASS_MAX)
    condition_max = int(
        randint(GENERATOR_CONDITION_MIN, GENERATOR_CONDITION_MAX) * tech_rate
    )

    deterioration_rate = 1

    energyBlock = energyBlockItem(
        race_id,
        item_texOb,
        energy_max_orig,
        restoration_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    )

    return energyBlock


class protectorItem(CommonForItems):
    def __init__(
        self,
        race,
        item_texOb,
        protection_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    ):
        CommonForItems.__init__(
            self,
            race,
            item_texOb,
            modules_num_max,
            mass,
            condition_max,
            deterioration_rate,
        )

        self.type = EQUIPMENT_ID
        self.subtype = PROTECTOR_ID

        self.protection_orig = protection_orig
        self.protection_add = 0

        self.updatePropetries()
        self.countPrice()
        self.updateInfo()

        self.shield_texOb = TEXTURE_MANAGER.returnShieldEffectTexObBy_RevisionID_and_ColorID(
            self.item_texOb.revision_id, self.item_texOb.color_id
        )

    def countPrice(self):
        protection_rate = float(self.protection_orig) / PROTECTOR_PROTECTION_MIN
        modules_num_rate = float(self.modules_num_max) / PROTECTOR_MODULES_NUM_MAX

        effectiveness_rate = (
            PROTECTOR_PROTECTION_WEIGHT * protection_rate
            + PROTECTOR_MODULES_NUM_WEIGHT * modules_num_rate
        )

        mass_rate = float(self.mass) / PROTECTOR_MASS_MIN
        condition_rate = float(self.condition) / self.condition_max

        self.price = int((3 * effectiveness_rate - mass_rate - condition_rate) * 100)

    def updatePropetries(self):
        self.protection = self.protection_orig + self.protection_add

    def updateOwnerPropetries(self):
        self.owner.updateProtectionAbility()

    def returnProtectionStr(self):
        if self.protection_add == 0:
            return "protection:" + str(self.protection_orig)
        else:
            return (
                "protection:"
                + str(self.protection_orig)
                + "+"
                + str(self.protection_add)
            )

    def updateInfo(self):
        self.info = [
            "PROTECTOR",
            self.returnProtectionStr(),
            "modules:" + str(self.modules_num_max),
            "condition:" + str(self.condition) + "/" + str(self.condition_max),
            "mass:" + str(self.mass),
            "price:" + str(self.price),
        ]


def protectorGenerator(race_id, revision_id=-1):
    tech_rate = returnRaceTechRate(race_id)

    item_texOb = TEXTURE_MANAGER.returnItemTexOb(PROTECTOR_ITEM_TEXTURE_ID, revision_id)

    protection_orig = randint(PROTECTOR_PROTECTION_MIN, PROTECTOR_PROTECTION_MAX)
    modules_num_max = randint(PROTECTOR_MODULES_NUM_MIN, PROTECTOR_MODULES_NUM_MAX)

    mass = randint(PROTECTOR_MASS_MIN, PROTECTOR_MASS_MAX)
    condition_max = int(
        randint(PROTECTOR_CONDITION_MIN, PROTECTOR_CONDITION_MAX) * tech_rate
    )
    deterioration_rate = 1

    protector = protectorItem(
        race_id,
        item_texOb,
        protection_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    )

    return protector


class droidItem(CommonForItems):
    def __init__(
        self,
        race,
        item_texOb,
        repair_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    ):
        CommonForItems.__init__(
            self,
            race,
            item_texOb,
            modules_num_max,
            mass,
            condition_max,
            deterioration_rate,
        )

        self.type = EQUIPMENT_ID
        self.subtype = DROID_ID

        self.repair_orig = repair_orig
        self.repair_add = 0

        self.updatePropetries()
        self.countPrice()
        self.updateInfo()

    def countPrice(self):
        repair_rate = float(self.repair_orig) / DROID_REPAIR_MIN
        modules_num_rate = float(self.modules_num_max) / DROID_MODULES_NUM_MAX

        effectiveness_rate = (
            DROID_REPAIR_WEIGHT * repair_rate
            + DROID_MODULES_NUM_WEIGHT * modules_num_rate
        )

        mass_rate = float(self.mass) / DROID_MASS_MIN
        condition_rate = float(self.condition) / self.condition_max

        self.price = int((3 * effectiveness_rate - mass_rate - condition_rate) * 100)

    def updatePropetries(self):
        self.repair = self.repair_orig + self.repair_add

    def updateOwnerPropetries(self):
        self.owner.updateRepairAbility()

    def returnRepairStr(self):
        if self.repair_add == 0:
            return "repair:" + str(self.repair_orig)
        else:
            return "repair:" + str(self.repair_orig) + "+" + str(self.repair_add)

    def updateInfo(self):
        self.info = [
            "DROID",
            self.returnRepairStr(),
            "modules:" + str(self.modules_num_max),
            "condition:" + str(self.condition) + "/" + str(self.condition_max),
            "mass:" + str(self.mass),
            "price:" + str(self.price),
        ]


def droidGenerator(race_id, revision_id=-1):
    tech_rate = returnRaceTechRate(race_id)

    item_texOb = TEXTURE_MANAGER.returnItemTexOb(DROID_ITEM_TEXTURE_ID, revision_id)

    repair_orig = randint(DROID_REPAIR_MIN, DROID_REPAIR_MAX)
    modules_num_max = randint(DROID_MODULES_NUM_MIN, DROID_MODULES_NUM_MAX)

    mass = randint(DROID_MASS_MIN, DROID_MASS_MAX)
    condition_max = int(randint(DROID_CONDITION_MIN, DROID_CONDITION_MAX) * tech_rate)
    deterioration_rate = 1

    droid = droidItem(
        race_id,
        item_texOb,
        repair_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    )

    return droid


class freezerItem(CommonForItems):
    def __init__(
        self,
        race,
        item_texOb,
        freeze_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    ):
        CommonForItems.__init__(
            self,
            race,
            item_texOb,
            modules_num_max,
            mass,
            condition_max,
            deterioration_rate,
        )

        self.type = EQUIPMENT_ID
        self.subtype = FREEZER_ID

        self.freeze_orig = freeze_orig
        self.freeze_add = 0

        self.updatePropetries()
        self.countPrice()
        self.updateInfo()

    def countPrice(self):
        freeze_rate = float(self.freeze_orig) / FREEZER_FREEZE_MIN
        modules_num_rate = float(self.modules_num_max) / FREEZER_MODULES_NUM_MAX

        effectiveness_rate = (
            FREEZER_FREEZE_WEIGHT * freeze_rate
            + FREEZER_MODULES_NUM_WEIGHT * modules_num_rate
        )

        mass_rate = float(self.mass) / FREEZER_MASS_MIN
        condition_rate = float(self.condition) / self.condition_max

        self.price = int((3 * effectiveness_rate - mass_rate - condition_rate) * 100)

    def updatePropetries(self):
        self.freeze = self.freeze_orig + self.freeze_add

    def updateOwnerPropetries(self):
        self.owner.updateFreezeAbility()

    def updateInfo(self):
        self.info = [
            "FREEZER",
            self.returnFreezeStr(),
            "modules:" + str(self.modules_num_max),
            "condition:" + str(self.condition) + "/" + str(self.condition_max),
            "mass:" + str(self.mass),
            "price:" + str(self.price),
        ]

    def returnFreezeStr(self):
        if self.freeze_add == 0:
            return "freeze:" + str(self.freeze_orig)
        else:
            return "freeze:" + str(self.freeze_orig) + "+" + str(self.freeze_add)


def freezerGenerator(race_id, revision_id=-1):
    tech_rate = returnRaceTechRate(race_id)

    item_texOb = TEXTURE_MANAGER.returnItemTexOb(FREEZER_ITEM_TEXTURE_ID, revision_id)

    freeze_orig = randint(FREEZER_FREEZE_MIN, FREEZER_FREEZE_MAX)
    modules_num_max = randint(FREEZER_MODULES_NUM_MIN, FREEZER_MODULES_NUM_MAX)

    mass = randint(FREEZER_MASS_MIN, FREEZER_MASS_MAX)
    condition_max = int(
        randint(FREEZER_CONDITION_MIN, FREEZER_CONDITION_MAX) * tech_rate
    )

    deterioration_rate = 1

    freezer = freezerItem(
        race_id,
        item_texOb,
        freeze_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    )

    return freezer


class scanerItem(CommonForItems):
    def __init__(
        self,
        race,
        item_texOb,
        scan_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    ):
        CommonForItems.__init__(
            self,
            race,
            item_texOb,
            modules_num_max,
            mass,
            condition_max,
            deterioration_rate,
        )

        self.type = EQUIPMENT_ID
        self.subtype = SCANER_ID

        self.scan_orig = scan_orig
        self.scan_add = 0

        self.updatePropetries()
        self.countPrice()
        self.updateInfo()

    def countPrice(self):
        scan_rate = float(self.scan_orig) / SCANER_SCAN_MIN
        modules_num_rate = float(self.modules_num_max) / SCANER_MODULES_NUM_MAX

        effectiveness_rate = (
            SCANER_SCAN_WEIGHT * scan_rate
            + SCANER_MODULES_NUM_WEIGHT * modules_num_rate
        )

        mass_rate = float(self.mass) / SCANER_MASS_MIN
        condition_rate = float(self.condition) / self.condition_max

        self.price = int((3 * effectiveness_rate - mass_rate - condition_rate) * 100)

    def updatePropetries(self):
        self.scan = self.scan_orig + self.scan_add

    def updateOwnerPropetries(self):
        self.owner.updateScanAbility()

    def returnScanStr(self):
        if self.scan_add == 0:
            return "scan:" + str(self.scan_orig)
        else:
            return "scan:" + str(self.scan_orig) + "+" + str(self.scan_add)

    def updateInfo(self):
        self.info = [
            "SCANER",
            self.returnScanStr(),
            "modules:" + str(self.modules_num_max),
            "condition:" + str(self.condition) + "/" + str(self.condition_max),
            "mass:" + str(self.mass),
            "price:" + str(self.price),
        ]


def scanerGenerator(race_id, revision_id=-1):
    tech_rate = returnRaceTechRate(race_id)

    item_texOb = TEXTURE_MANAGER.returnItemTexOb(SCANER_ITEM_TEXTURE_ID, revision_id)

    scan_orig = randint(SCANER_SCAN_MIN, SCANER_SCAN_MAX)
    modules_num_max = randint(SCANER_MODULES_NUM_MIN, SCANER_MODULES_NUM_MAX)

    mass = randint(SCANER_MASS_MIN, SCANER_MASS_MAX)
    condition_max = int(randint(SCANER_CONDITION_MIN, SCANER_CONDITION_MAX) * tech_rate)

    deterioration_rate = 1

    scaner = scanerItem(
        race_id,
        item_texOb,
        scan_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    )

    return scaner


class grappleItem(CommonForItems):
    def __init__(
        self,
        race,
        item_texOb,
        strength_orig,
        radius_orig,
        speed_orig,
        maxNumItem_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    ):
        CommonForItems.__init__(
            self,
            race,
            item_texOb,
            modules_num_max,
            mass,
            condition_max,
            deterioration_rate,
        )

        self.type = EQUIPMENT_ID
        self.subtype = GRAPPLE_ID

        self.grapple_list = []
        self.grapple_remove_queue = []

        self.strength_orig = 0
        self.strength_add = 0

        self.radius_orig = 0
        self.radius_add = 0
        self.radius = 0

        self.speed_orig = 0
        self.speed_add = 0

        self.maxNumItem_orig = 0
        self.maxNumItem_add = 0

        self.updatePropetries()
        self.countPrice()
        self.updateInfo()

    def countPrice(self):
        strength_rate = float(self.strength_orig) / GRAPPLE_STRENGTH_MIN
        radius_rate = float(self.radius_orig) / GRAPPLE_RADIUS_MIN
        speed_rate = float(self.speed_orig) / GRAPPLE_SPEED_MIN
        maxNumItem_rate = float(self.maxNumItem_orig) / GRAPPLE_MAXNUMITEM_MIN

        modules_num_rate = float(self.modules_num_max) / GRAPPLE_MODULES_NUM_MAX

        effectiveness_rate = (
            GRAPPLE_STRENGTH_WEIGHT * strength_rate
            + GRAPPLE_RADIUS_WEIGHT * radius_rate
            + GRAPPLE_SPEED_WEIGHT * speed_rate
            + GRAPPLE_MAXNUMITEM_WEIGHT * maxNumItem_rate
            + GRAPPLE_MODULES_NUM_WEIGHT * modules_num_rate
        )

        mass_rate = float(self.mass) / GRAPPLE_MASS_MIN
        condition_rate = float(self.condition) / self.condition_max

        self.price = int((3 * effectiveness_rate - mass_rate - condition_rate) * 100)

    def updatePropetries(self):
        self.strength = self.strength_orig + self.strength_add
        self.radius = self.radius_orig + self.radius_add
        self.speed = self.speed_orig + self.speed_add
        self.maxNumItem = self.maxNumItem_orig + self.maxNumItem_add

    def updateOwnerPropetries(self):
        self.owner.updateGrabAbility()

    def returnStrengthStr(self):
        if self.strength_add == 0:
            return "strength:" + str(self.strength_orig)
        else:
            return "strength:" + str(self.strength_orig) + "+" + str(self.strength_add)

    def returnRadiusStr(self):
        if self.radius_add == 0:
            return "radius:" + str(self.radius_orig)
        else:
            return "radius:" + str(self.radius_orig) + "+" + str(self.radius_add)

    def returnSpeedStr(self):
        if self.speed_add == 0:
            return "speed:" + str(self.speed_orig)
        else:
            return "speed:" + str(self.speed_orig) + "+" + str(self.speed_add)

    def returnMaxNumItemStr(self):
        if self.maxNumItem_add == 0:
            return "maxNumItem:" + str(self.maxNumItem_orig)
        else:
            return (
                "maxNumItem:"
                + str(self.maxNumItem_orig)
                + "+"
                + str(self.maxNumItem_add)
            )

    def updateInfo(self):
        self.info = [
            "GRAPPLE",
            self.returnStrengthStr(),
            self.returnRadiusStr(),
            self.returnSpeedStr(),
            self.returnMaxNumItemStr(),
            "modules:" + str(self.modules_num_max),
            "condition:" + str(self.condition) + "/" + str(self.condition_max),
            "mass:" + str(self.mass),
            "price:" + str(self.price),
        ]


def grappleGenerator(race_id, revision_id=-1):
    tech_rate = returnRaceTechRate(race_id)

    item_texOb = TEXTURE_MANAGER.returnItemTexOb(GRAPPLE_ITEM_TEXTURE_ID, revision_id)

    strength_orig = randint(GRAPPLE_STRENGTH_MIN, GRAPPLE_STRENGTH_MAX)
    radius_orig = randint(GRAPPLE_RADIUS_MIN, GRAPPLE_RADIUS_MAX)
    speed_orig = randint(GRAPPLE_SPEED_MIN, GRAPPLE_SPEED_MAX)
    maxNumItem_orig = randint(GRAPPLE_MAXNUMITEM_MIN, GRAPPLE_MAXNUMITEM_MAX)
    modules_num_max = randint(GRAPPLE_MODULES_NUM_MIN, GRAPPLE_MODULES_NUM_MAX)

    mass = randint(GRAPPLE_MASS_MIN, GRAPPLE_MASS_MAX)
    condition_max = int(
        randint(GRAPPLE_CONDITION_MIN, GRAPPLE_CONDITION_MAX) * tech_rate
    )

    deterioration_rate = 1

    grapple = grappleItem(
        race_id,
        item_texOb,
        strength_orig,
        radius_orig,
        speed_orig,
        maxNumItem_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    )

    return grapple


class LazerWeapon(CommonForItems):
    def __init__(
        self,
        race,
        item_texOb,
        damage_orig,
        radius_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    ):
        CommonForItems.__init__(
            self,
            race,
            item_texOb,
            modules_num_max,
            mass,
            condition_max,
            deterioration_rate,
        )

        self.type = WEAPON_ID
        self.subtype = LAZER_ID

        self.damage_orig = damage_orig
        self.damage_add = 0

        self.radius_orig = radius_orig
        self.radius_add = 0

        self.lazerEffect_texOb = TEXTURE_MANAGER.returnLazerEffectTexObBy_RevisionID_and_ColorID(
            self.item_texOb.revision_id, self.item_texOb.color_id
        )
        self.particle_texOb = TEXTURE_MANAGER.returnParticleTexObBy_ColorID(
            self.item_texOb.color_id
        )

        self.l_tex, (self.l_w, self.l_h) = (
            self.lazerEffect_texOb.texture,
            (self.lazerEffect_texOb.w, self.lazerEffect_texOb.h),
        )

        self.target = None

        self.updatePropetries()
        self.countPrice()
        self.updateInfo()

    def countPrice(self):
        damage_rate = float(self.damage_orig) / LAZER_DAMAGE_MIN
        radius_rate = float(self.radius_orig) / LAZER_RADIUS_MIN
        modules_num_rate = float(self.modules_num_max) / LAZER_MODULES_NUM_MAX

        effectiveness_rate = (
            LAZER_DAMAGE_WEIGHT * damage_rate
            + LAZER_RADIUS_WEIGHT * radius_rate
            + LAZER_MODULES_NUM_WEIGHT * modules_num_rate
        )

        mass_rate = float(self.mass) / LAZER_MASS_MIN
        condition_rate = float(self.condition) / self.condition_max

        self.price = int((3 * effectiveness_rate - mass_rate - condition_rate) * 100)

    def updatePropetries(self):
        self.damage = self.damage_orig + self.damage_add
        self.radius = self.radius_orig + self.radius_add

        self.pSize = 60  # needs for lazer effect

    def updateOwnerPropetries(self):
        self.owner.updateFireAbility()

    def returnDamageStr(self):
        if self.damage_add == 0:
            return "damage:" + str(self.damage_orig)
        else:
            return "damage:" + str(self.damage_orig) + "+" + str(self.damage_add)

    def returnRadiusStr(self):
        if self.radius_add == 0:
            return "radius:" + str(self.radius_orig)
        else:
            return "radius:" + str(self.radius_orig) + "+" + str(self.radius_add)

    def updateInfo(self):
        self.info = [
            "LAZER",
            self.returnDamageStr(),
            self.returnRadiusStr(),
            "modules:" + str(self.modules_num_max),
            "condition:" + str(self.condition) + "/" + str(self.condition_max),
            "mass:" + str(self.mass),
            "price: " + str(self.price),
        ]

    def Fire(self):
        ### DEFINE LOCAL VARIABLES ###
        l_owner = self.owner
        l_target = self.target
        ###############################

        if l_owner.energy > (WEAPON_ENERGY_CONSUMPTION_RATE * self.damage):
            lazer.play()
            l = lazerEffect(
                (self.l_tex, (self.l_w, self.l_h)),
                l_owner,
                l_target,
                self.particle_texOb,
                self.pSize,
            )
            l.starsystem.effect_LAZER_list.append(l)

            l_owner.energy -= WEAPON_ENERGY_CONSUMPTION_RATE * self.damage

            l_target.hit(l_owner, self)

            if l_target.type == SHIP_ID:
                l_target.temperature += WEAPON_HEATING_RATE * self.damage

            self.deterioration()


def lazerGenerator(race_id, revision_id=-1):
    if race_id == -1:
        race_id = RACES_GOOD_LIST[randint(0, len(RACES_GOOD_LIST) - 1)]

    tech_rate = returnRaceTechRate(race_id)

    item_texOb = TEXTURE_MANAGER.returnItemTexOb(LAZER_ITEM_TEXTURE_ID, revision_id)

    damage_orig = randint(LAZER_DAMAGE_MIN, LAZER_DAMAGE_MAX)
    radius_orig = randint(LAZER_RADIUS_MIN, LAZER_RADIUS_MAX)
    modules_num_max = randint(LAZER_MODULES_NUM_MIN, LAZER_MODULES_NUM_MAX)

    mass = randint(LAZER_MASS_MIN, LAZER_MASS_MAX)
    condition_max = int(randint(LAZER_CONDITION_MIN, LAZER_CONDITION_MAX) * tech_rate)
    deterioration_rate = 1

    lazer = LazerWeapon(
        race_id,
        item_texOb,
        damage_orig,
        radius_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    )

    return lazer


class RocketWeapon(CommonForItems):
    # this class manage rocket fire
    def __init__(
        self,
        race,
        item_texOb,
        ammo_max_orig,
        damage_orig,
        radius_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    ):
        CommonForItems.__init__(
            self,
            race,
            item_texOb,
            modules_num_max,
            mass,
            condition_max,
            deterioration_rate,
        )

        self.type = WEAPON_ID
        self.subtype = ROCKET_ID

        self.ammo_max_orig = ammo_max_orig
        self.ammo_max_add = 0

        self.damage_orig = damage_orig
        self.damage_add = 0

        self.radius_orig = radius_orig
        self.radius_add = 0

        self.ammo = self.ammo_max_orig
        self.target = None

        self.updatePropetries()
        self.countPrice()
        self.updateInfo()

        self.bullet_texOb = TEXTURE_MANAGER.rocketBullet_texOb_list[
            randint(0, len(TEXTURE_MANAGER.rocketBullet_texOb_list) - 1)
        ]
        self.bullet_size = returnObjectSize(self.bullet_texOb.w, self.bullet_texOb.h)
        self.bullet_armor = ROCKET_ARMOR
        self.bullet_speed_init = ROCKET_START_SPEED
        self.bullet_speed_max = ROCKET_SPEED_MAX
        self.bullet_d_speed = ROCKET_DELTA_SPEED
        self.bullet_live_time = ROCKET_EXISTANCE_TIME
        self.bullet_angular_speed = ROCKET_ANGULAR_SPEED

    def countPrice(self):
        ammo_rate = float(self.ammo_max_orig) / ROCKET_AMMO_MIN
        damage_rate = float(self.damage_orig) / ROCKET_DAMAGE_MIN
        radius_rate = float(self.radius_orig) / ROCKET_RADIUS_MIN
        modules_num_rate = float(self.modules_num_max) / ROCKET_MODULES_NUM_MAX

        effectiveness_rate = (
            ROCKET_AMMO_WEIGHT * ammo_rate
            + ROCKET_DAMAGE_WEIGHT * damage_rate
            + ROCKET_RADIUS_WEIGHT * radius_rate
            + ROCKET_MODULES_NUM_WEIGHT * modules_num_rate
        )

        mass_rate = float(self.mass) / ROCKET_MASS_MIN
        condition_rate = float(self.condition) / self.condition_max

        self.price = int((3 * effectiveness_rate - mass_rate - condition_rate) * 100)

    def updatePropetries(self):
        self.ammo_max = self.ammo_max_orig + self.ammo_max_add
        self.damage = self.damage_orig + self.damage_add
        self.radius = self.radius_orig + self.radius_add

    def updateOwnerPropetries(self):
        self.owner.updateFireAbility()

    def returnAmmoStr(self):
        if self.ammo_max_add == 0:
            return "ammo:" + str(self.ammo_max_orig) + "/" + str(self.ammo)
        else:
            return (
                "ammo:"
                + str(self.ammo_max_orig)
                + "+"
                + str(self.ammo_max_add)
                + "/"
                + str(self.ammo)
            )

    def returnDamageStr(self):
        if self.damage_add == 0:
            return "damage:" + str(self.damage_orig)
        else:
            return "damage:" + str(self.damage_orig) + "+" + str(self.damage_add)

    def returnRadiusStr(self):
        if self.radius_add == 0:
            return "radius:" + str(self.radius_orig)
        else:
            return "radius:" + str(self.radius_orig) + "+" + str(self.radius_add)

    def updateInfo(self):
        self.info = [
            "ROCKET",
            self.returnAmmoStr(),
            self.returnDamageStr(),
            self.returnRadiusStr(),
            "modules:" + str(self.modules_num_max),
            "condition:" + str(self.condition) + "/" + str(self.condition_max),
            "mass:" + str(self.mass),
            "price: " + str(self.price),
        ]

    def Fire(self):
        ### DEFINE LOCAL VARIABLES ###
        l_owner = self.owner
        l_target = self.target
        ###############################

        r1 = rocketBulletInstance(
            self.bullet_texOb,
            l_owner,
            l_target,
            self.damage,
            self.bullet_size,
            self.bullet_armor,
            self.bullet_speed_init,
            self.bullet_speed_max,
            self.bullet_d_speed,
            self.bullet_live_time,
            self.bullet_angular_speed,
        )
        r1.points.setCenter(l_owner.points.center[0] + 15, l_owner.points.center[1])
        r1.starsystem.ROCKET_list.append(r1)

        r2 = rocketBulletInstance(
            self.bullet_texOb,
            l_owner,
            l_target,
            self.damage,
            self.bullet_size,
            self.bullet_armor,
            self.bullet_speed_init,
            self.bullet_speed_max,
            self.bullet_d_speed,
            self.bullet_live_time,
            self.bullet_angular_speed,
        )
        r2.points.setCenter(l_owner.points.center[0] - 15, l_owner.points.center[1])
        r2.starsystem.ROCKET_list.append(r2)

        rocketlaunch.play()
        self.ammo -= 2

        self.deterioration()


def rocketGenerator(race_id, revision_id=-1):
    tech_rate = returnRaceTechRate(race_id)

    if race_id == -1:
        race_id = RACES_GOOD_LIST[randint(0, len(RACES_GOOD_LIST) - 1)]

    item_texOb = TEXTURE_MANAGER.returnItemTexOb(ROCKET_ITEM_TEXTURE_ID, revision_id)

    ammo_max_orig = randint(ROCKET_AMMO_MIN, ROCKET_AMMO_MAX)
    damage_orig = randint(ROCKET_DAMAGE_MIN, ROCKET_DAMAGE_MAX)
    radius_orig = randint(ROCKET_RADIUS_MIN, ROCKET_RADIUS_MAX)

    modules_num_max = randint(ROCKET_MODULES_NUM_MIN, ROCKET_MODULES_NUM_MAX)

    mass = randint(ROCKET_MASS_MIN, ROCKET_MASS_MAX)
    condition_max = int(randint(ROCKET_CONDITION_MIN, ROCKET_CONDITION_MAX) * tech_rate)

    deterioration_rate = 1

    rocket = RocketWeapon(
        race_id,
        item_texOb,
        ammo_max_orig,
        damage_orig,
        radius_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    )

    return rocket


class torpedWeapon(CommonForItems):
    # this class manage rocket fire
    def __init__(
        self,
        race,
        item_texOb,
        ammo_max_orig,
        damage_orig,
        radius_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    ):
        CommonForItems.__init__(
            self,
            race,
            item_texOb,
            modules_num_max,
            mass,
            condition_max,
            deterioration_rate,
        )

        self.type = WEAPON_ID
        self.subtype = TORPED_ID

        self.ammo_max_orig = ammo_max_orig
        self.ammo_max_add = 0

        self.damage_orig = damage_orig
        self.damage_add = 0

        self.radius_orig = radius_orig
        self.radius_add = 0

        self.ammo = self.ammo_max_orig
        self.target = None

        self.updatePropetries()
        self.countPrice()
        self.updateInfo()

        self.bullet_texOb = TEXTURE_MANAGER.torpedBullet_texOb_list[
            randint(0, len(TEXTURE_MANAGER.torpedBullet_texOb_list) - 1)
        ]
        self.bullet_size = returnObjectSize(self.bullet_texOb.w, self.bullet_texOb.h)
        self.bullet_armor = TORPED_ARMOR
        self.bullet_speed_init = TORPED_START_SPEED
        self.bullet_speed_max = TORPED_SPEED_MAX
        self.bullet_d_speed = TORPED_DELTA_SPEED
        self.bullet_live_time = TORPED_EXISTANCE_TIME
        self.bullet_angular_speed = TORPED_ANGULAR_SPEED

    def countPrice(self):
        ammo_rate = float(self.ammo_max_orig) / ROCKET_AMMO_MIN
        damage_rate = float(self.damage_orig) / ROCKET_DAMAGE_MIN
        radius_rate = float(self.radius_orig) / ROCKET_RADIUS_MIN
        modules_num_rate = float(self.modules_num_max) / ROCKET_MODULES_NUM_MAX

        effectiveness_rate = (
            ROCKET_AMMO_WEIGHT * ammo_rate
            + ROCKET_DAMAGE_WEIGHT * damage_rate
            + ROCKET_RADIUS_WEIGHT * radius_rate
            + ROCKET_MODULES_NUM_WEIGHT * modules_num_rate
        )

        mass_rate = float(self.mass) / ROCKET_MASS_MIN
        condition_rate = float(self.condition) / self.condition_max

        self.price = int((3 * effectiveness_rate - mass_rate - condition_rate) * 100)

    def updatePropetries(self):
        self.ammo_max = self.ammo_max_orig + self.ammo_max_add
        self.damage = self.damage_orig + self.damage_add
        self.radius = self.radius_orig + self.radius_add

    def updateOwnerPropetries(self):
        self.owner.updateFireAbility()

    def returnAmmoStr(self):
        if self.ammo_max_add == 0:
            return "ammo:" + str(self.ammo_max_orig) + "/" + str(self.ammo)
        else:
            return (
                "ammo:"
                + str(self.ammo_max_orig)
                + "+"
                + str(self.ammo_max_add)
                + "/"
                + str(self.ammo)
            )

    def returnDamageStr(self):
        if self.damage_add == 0:
            return "damage:" + str(self.damage_orig)
        else:
            return "damage:" + str(self.damage_orig) + "+" + str(self.damage_add)

    def returnRadiusStr(self):
        if self.radius_add == 0:
            return "radius:" + str(self.radius_orig)
        else:
            return "radius:" + str(self.radius_orig) + "+" + str(self.radius_add)

    def updateInfo(self):
        self.info = [
            "Torpedo",
            self.returnAmmoStr(),
            self.returnDamageStr(),
            self.returnRadiusStr(),
            "modules:" + str(self.modules_num_max),
            "condition:" + str(self.condition) + "/" + str(self.condition_max),
            "mass:" + str(self.mass),
            "price: " + str(self.price),
        ]

    def Fire(self):
        ### DEFINE LOCAL VARIABLES ###
        l_owner = self.owner
        l_target = self.target
        ###############################

        t = rocketBulletInstance(
            self.bullet_texOb,
            l_owner,
            l_target,
            self.damage,
            self.bullet_size,
            self.bullet_armor,
            self.bullet_speed_init,
            self.bullet_speed_max,
            self.bullet_d_speed,
            self.bullet_live_time,
            self.bullet_angular_speed,
        )
        t.points.setCenter(l_owner.points.center[0], l_owner.points.center[1])
        t.starsystem.ROCKET_list.append(t)

        rocketlaunch.play()
        self.ammo -= 1

        self.deterioration()


def torpedGenerator(race_id, revision_id=-1):
    tech_rate = returnRaceTechRate(race_id)

    item_texOb = TEXTURE_MANAGER.returnItemTexOb(TORPED_ITEM_TEXTURE_ID, revision_id)

    ammo_max_orig = randint(TORPED_AMMO_MIN, TORPED_AMMO_MAX)
    damage_orig = randint(TORPED_DAMAGE_MIN, TORPED_DAMAGE_MAX)
    radius_orig = randint(TORPED_RADIUS_MIN, TORPED_RADIUS_MAX)

    modules_num_max = randint(TORPED_MODULES_NUM_MIN, TORPED_MODULES_NUM_MAX)

    mass = randint(TORPED_MASS_MIN, TORPED_MASS_MAX)
    condition_max = int(randint(TORPED_CONDITION_MIN, TORPED_CONDITION_MAX) * tech_rate)

    deterioration_rate = 1

    torped = torpedWeapon(
        race_id,
        item_texOb,
        ammo_max_orig,
        damage_orig,
        radius_orig,
        modules_num_max,
        mass,
        condition_max,
        deterioration_rate,
    )

    return torped
