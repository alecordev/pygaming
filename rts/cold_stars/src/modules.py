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
from resources import *


class CommonForModules(CommonInstance):
    def __init__(self, (texture_ID_list, (w, h))):
        CommonInstance.__init__(self, texture_ID_list, (w, h))
        if self.animated == False:
            self.renderInSlot = self.renderStatic
        else:
            self.renderInSlot = self.renderAnimated

        self.w, self.h = w, h

        self.ID = 0

        self.type = MODULE_ID
        self.subtype = None

        self.mass = 1
        self.info = []

        self.owner = None

    def renderStatic(self, slot_rect):
        self.renderStaticFrameOnRect(slot_rect)

    def renderAnimated(self, slot_rect):
        self.renderStaticFramesLoopOnRect(slot_rect)


class lazerModule(CommonForModules):
    def __init__(self, (texture_ID, (w, h))):
        CommonForModules.__init__(self, (texture_ID, (w, h)))
        self.subtype = LAZER_ID

        self.damage_add = 0
        self.radius_add = 0

    def activation(self, item):
        item.damage_add += self.damage_add
        item.radius_add += self.radius_add
        item.updatePropetries()

    def updateInfo(self):
        self.info = []
        self.info.append("Lazer Module")
        if self.damage_add > 0:
            self.info.append("damage +" + str(self.damage_add))
        if self.radius_add > 0:
            self.info.append("radius +" + str(self.radius_add))
        self.info.append("mass:" + str(self.mass))


def lazerModuleGenerator():
    lazer_module = lazerModule((module_tex, (module_w, module_h)))
    lazer_module.damage_add = randint(LAZER_MODULE_DAMAGE_MIN, LAZER_MODULE_DAMAGE_MAX)
    lazer_module.radius_add = randint(LAZER_MODULE_RADIUS_MIN, LAZER_MODULE_RADIUS_MAX)

    lazer_module.updateInfo()
    return lazer_module


class rocketModule(CommonForModules):
    def __init__(self, (texture_ID, (w, h))):
        CommonForModules.__init__(self, (texture_ID, (w, h)))
        self.subtype = ROCKET_ID

        self.ammo_max_add = 0
        self.damage_add = 0
        self.radius_add = 0

    def activation(self, item):
        item.ammo_max_add += self.ammo_max_add
        item.damage_add += self.damage_add
        item.radius_add += self.radius_add
        item.updatePropetries()

    def updateInfo(self):
        self.info = []
        self.info.append("Rocket Module")
        if self.ammo_max_add > 0:
            self.info.append("ammo_max +" + str(self.ammo_max_add))
        if self.damage_add > 0:
            self.info.append("damage +" + str(self.damage_add))
        if self.radius_add > 0:
            self.info.append("radius +" + str(self.radius_add))
        self.info.append("mass:" + str(self.mass))


def rocketModuleGenerator():
    rocket_module = rocketModule((module_tex, (module_w, module_h)))
    rocket_module.ammo_max_add = randint(ROCKET_MODULE_AMMO_MIN, ROCKET_MODULE_AMMO_MAX)
    rocket_module.damage_add = randint(
        ROCKET_MODULE_DAMAGE_MIN, ROCKET_MODULE_DAMAGE_MAX
    )
    rocket_module.radius_add = randint(
        ROCKET_MODULE_RADIUS_MIN, ROCKET_MODULE_RADIUS_MAX
    )

    rocket_module.updateInfo()
    return rocket_module


class generatorModule(CommonForModules):
    def __init__(self, (texture_ID, (w, h))):
        CommonForModules.__init__(self, (texture_ID, (w, h)))
        self.subtype = ENERGYBLOCK_ID

        self.energy_max_add = 0
        self.restoration_add = 0

    def activation(self, item):
        item.energy_max_add += self.energy_max_add
        item.restoration_add += self.restoration_add
        item.updatePropetries()

    def updateInfo(self):
        self.info = []
        self.info.append("Generator Module")
        if self.energy_max_add > 0:
            self.info.append("energy +" + str(self.energy_max_add))
        if self.restoration_add > 0:
            self.info.append("restoration +" + str(self.restoration_add))
        self.info.append("mass:" + str(self.mass))


def generatorModuleGenerator():
    generator_module = generatorModule((module_tex, (module_w, module_h)))
    generator_module.energy_max_add = randint(
        GENERATOR_MODULE_ENERGY_MIN, GENERATOR_MODULE_ENERGY_MAX
    )
    generator_module.restoration_add = randint(
        GENERATOR_MODULE_RESTORATION_MIN, GENERATOR_MODULE_RESTORATION_MAX
    )

    generator_module.updateInfo()
    return generator_module


class freezerModule(CommonForModules):
    def __init__(self, (texture_ID, (w, h))):
        CommonForModules.__init__(self, (texture_ID, (w, h)))
        self.subtype = FREEZER_ID

        self.freeze_add = 0

    def activation(self, item):
        item.freeze_add += self.freeze_add
        item.updatePropetries()

    def updateInfo(self):
        self.info = [
            "Freezer Module",
            "freezer +" + str(self.freeze_add),
            "mass:" + str(self.mass),
        ]


def freezerModuleGenerator():
    freezer_module = freezerModule((module_tex, (module_w, module_h)))
    freezer_module.freeze_add = randint(
        FREZZER_MODULE_FREEZE_MIN, FREZZER_MODULE_FREEZE_MAX
    )

    freezer_module.updateInfo()
    return freezer_module


class grappleModule(CommonForModules):
    def __init__(self, (texture_ID, (w, h))):
        CommonForModules.__init__(self, (texture_ID, (w, h)))
        self.subtype = GRAPPLE_ID

        self.strength_add = 0
        self.radius_add = 0
        self.speed_add = 0
        self.maxNumItem_add = 0

    def activation(self, item):
        item.strength_add += self.strength_add
        item.radius_add += self.radius_add
        item.speed_add += self.speed_add
        item.maxNumItem_add += self.maxNumItem_add
        item.updatePropetries()

    def updateInfo(self):
        self.info = []
        self.info.append("Grapple Module")
        if self.strength_add > 0:
            self.info.append("strength +" + str(self.strength_add))
        if self.radius_add > 0:
            self.info.append("radius +" + str(self.radius_add))
        if self.speed_add > 0:
            self.info.append("speed +" + str(self.speed_add))
        if self.maxNumItem_add > 0:
            self.info.append("maxNumItem +" + str(self.maxNumItem_add))
        self.info.append("mass:" + str(self.mass))


def grappleModuleGenerator():
    grapple_module = grappleModule((module_tex, (module_w, module_h)))
    grapple_module.strength_add = randint(
        GRAPPLE_MODULE_STRENGTH_MIN, GRAPPLE_MODULE_STRENGTH_MAX
    )
    grapple_module.radius_add = randint(
        GRAPPLE_MODULE_RADIUS_MIN, GRAPPLE_MODULE_RADIUS_MAX
    )
    grapple_module.speed_add = randint(
        GRAPPLE_MODULE_SPEED_MIN, GRAPPLE_MODULE_SPEED_MAX
    )
    grapple_module.maxNumItem_add = randint(
        GRAPPLE_MODULE_MAXNUMITEM_MIN, GRAPPLE_MODULE_MAXNUMITEM_MAX
    )

    grapple_module.updateInfo()
    return grapple_module


class radarModule(CommonForModules):
    def __init__(self, (texture_ID, (w, h))):
        CommonForModules.__init__(self, (texture_ID, (w, h)))
        self.subtype = RADAR_ID

        self.radius_add = 0

    def activation(self, item):
        item.radius_add += self.radius_add
        item.updatePropetries()

    def updateInfo(self):
        self.info = [
            "Radar Module",
            "radius +" + str(self.radius_add),
            "mass:" + str(self.mass),
        ]


def radarModuleGenerator():
    radar_module = radarModule((module_tex, (module_w, module_h)))
    radar_module.radius_add = randint(RADAR_MODULE_RADIUS_MIN, RADAR_MODULE_RADIUS_MAX)

    radar_module.updateInfo()
    return radar_module


class driveModule(CommonForModules):
    def __init__(self, (texture_ID, (w, h))):
        CommonForModules.__init__(self, (texture_ID, (w, h)))
        self.subtype = DRIVE_ID

        self.speed_add = 0
        self.hyper_add = 0

    def activation(self, item):
        item.speed_add += self.speed_add
        item.hyper_add += self.hyper_add
        item.updatePropetries()

    def updateInfo(self):
        self.info = []
        self.info.append("Drive Module")
        if self.speed_add > 0:
            self.info.append("speed +" + str(self.speed_add))
        if self.hyper_add > 0:
            self.info.append("hyper +" + str(self.hyper_add))
        self.info.append("mass:" + str(self.mass))


def driveModuleGenerator():
    drive_module = driveModule((module_tex, (module_w, module_h)))
    drive_module.speed_add = randint(DRIVE_MODULE_SPEED_MIN, DRIVE_MODULE_SPEED_MAX)
    drive_module.hyper_add = randint(DRIVE_MODULE_HYPER_MIN, DRIVE_MODULE_HYPER_MAX)

    drive_module.updateInfo()
    return drive_module


class protectorModule(CommonForModules):
    def __init__(self, (texture_ID, (w, h))):
        CommonForModules.__init__(self, (texture_ID, (w, h)))
        self.subtype = PROTECTOR_ID

        self.protection_add = 0

    def activation(self, item):
        item.protection_add += self.protection_add
        item.updatePropetries()

    def updateInfo(self):
        self.info = [
            "Protector Module",
            "protection +" + str(self.protection_add),
            "mass:" + str(self.mass),
        ]


def protectorModuleGenerator():
    protector_module = protectorModule((module_tex, (module_w, module_h)))
    protector_module.protection_add = randint(
        PROTECTOR_MODULE_PROTECTION_MIN, PROTECTOR_MODULE_PROTECTION_MAX
    )

    protector_module.updateInfo()
    return protector_module


class bakModule(CommonForModules):
    def __init__(self, (texture_ID, (w, h))):
        CommonForModules.__init__(self, (texture_ID, (w, h)))
        self.subtype = BAK_ID

        self.fuel_max_add = 0

    def activation(self, item):
        item.fuel_max_add += self.fuel_max_add
        item.updatePropetries()

    def updateInfo(self):
        self.info = [
            "Bak Module",
            "fuel +" + str(self.fuel_max_add),
            "mass:" + str(self.mass),
        ]


def bakModuleGenerator():
    bak_module = bakModule((module_tex, (module_w, module_h)))
    bak_module.fuel_max_add = randint(BAK_MODULE_FUEL_MIN, BAK_MODULE_FUEL_MAX)

    bak_module.updateInfo()
    return bak_module


class droidModule(CommonForModules):
    def __init__(self, (texture_ID, (w, h))):
        CommonForModules.__init__(self, (texture_ID, (w, h)))
        self.subtype = DROID_ID

        self.repair_add = 0

    def activation(self, item):
        item.repair_add += self.repair_add
        item.updatePropetries()

    def updateInfo(self):
        self.info = [
            "Droid Module",
            "repair +" + str(self.repair_add),
            "mass:" + str(self.mass),
        ]


def droidModuleGenerator():
    droid_module = droidModule((module_tex, (module_w, module_h)))
    droid_module.repair_add = randint(DROID_MODULE_REPAIR_MIN, DROID_MODULE_REPAIR_MAX)

    droid_module.updateInfo()
    return droid_module


class scanerModule(CommonForModules):
    def __init__(self, (texture_ID, (w, h))):
        CommonForModules.__init__(self, (texture_ID, (w, h)))
        self.subtype = SCANER_ID

        self.scan_add = 0

    def activation(self, item):
        item.scan_add += self.scan_add
        item.updatePropetries()

    def updateInfo(self):
        self.info = [
            "Scaner Module",
            "scan +" + str(self.scan_add),
            "mass:" + str(self.mass),
        ]


def scanerModuleGenerator():
    scaner_module = scanerModule((module_tex, (module_w, module_h)))
    scaner_module.scan_add = randint(SCANER_MODULE_SCAN_MIN, SCANER_MODULE_SCAN_MAX)

    scaner_module.updateInfo()
    return scaner_module
