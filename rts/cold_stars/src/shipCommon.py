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
from items import *
from effects import *
from SpaceObjects import Container
from math import *
from text import vericalFlowText

from points import *
from skill import *


class CommonForShip:
    def __init__(self, starsystem, name, race, face_texOb, subtype):
        self.alive = True
        self.alreadyInRemoveQueue = False

        self.starsystem = starsystem

        self.ID = ENTITY_ID_GENERATOR.returnNextID()
        self.name = name
        self.race = race
        self.face_texOb = face_texOb

        self.type = SHIP_ID
        self.subtype = subtype

        ######### SKILL
        self.skill = skill()
        #################################

        ######### TARGET COORDINATES #####
        self.calculateWayToCoord = self.calculateWayToCoord_TRUE
        self.Gl_LIST_direction_ID = None

        self.direction_list_x = []
        self.direction_list_y = []
        self.angle_list = []

        self.direction_list_END = True
        self.turn_list_END = True

        self.target_pos_x = None
        self.target_pos_y = None
        self.jump_pos_x = None
        self.jump_pos_y = None
        #################################

        ######### QUEST section
        self.quest_ob = None  # main quest ob
        self.FOLLOW_QUEST_OB = False
        self.task_init_FINISHED = False
        self.target_ship = None
        self.target_planet = None
        self.target_starsystem = None
        self.target_starsystem_dist = 0

        self.ob_to_follow = None  # can be changed during one quest
        self.task_id_being_exec = None
        ##################################

        ######### LOCATION STATUS
        self.in_SPACE = True
        self.is_LANDED = False
        self.in_KOSMOPORT = False
        self.in_UNINHABITED_LAND = False
        ####################################

        ######### LANDING SECTION
        self.landing_reason_id_list = []
        self.repair_NEEDED = False
        self.fuel_NEEDED = False
        self.rocket_reload_NEEDED = False
        self.buy_NEEDED = False
        self.sell_NEEDED = False
        ###################################

        ######### ABILITIES STATUS
        self.ableTo_RADAR = False
        self.ableTo_DRIVE = False
        self.ableTo_JUMP = False
        self.ableTo_ENERGIZE = False
        self.ableTo_PROTECT = False
        self.ableTo_REPAIR = False
        self.ableTo_FREEZE = False
        self.ableTo_GRAB = False
        self.ableTo_SCAN = False
        self.ableTo_FIRE = False
        ###################################

        ######### haractersitics
        self.radius = VISIBLE_DISTANCE_WITHOUT_RADAR
        self.mass = 0  # depends on all items mass
        self.speed = 0  # depends on mass and drive

        self.hyper = 0  # depends on drive and bak
        self.repair = 0  # depends on droid
        self.freeze = 0  # depends on freezer
        self.scan = 0  # depends on scaner

        self.energy = 0
        self.temperature = -100

        self.minerals = 0
        self.credits = randint(200, 2000)

        self.dist2star_rate = 100
        self.energy_restoration_rate = 1

        self.info = []

        ######### WAR SECTION
        self.flow_TEXT_list = []
        self.agressors_name_list = []  # improve: names > ids
        self.reloaded_weapon_list = []
        self.fire_delay = 0
        ##########################################

        self.alpha = 1.0  # !!!???

        ### debug
        self.rotation_trajectory_center_x = None
        self.rotation_trajectory_center_y = None
        self.xk = None
        self.yk = None
        self.xk1 = None
        self.yk1 = None
        self.xk2 = None
        self.yk2 = None
        ### debug

    def doNothing(self):
        pass

    def initPositionInSpace(self, (pos_x, pos_y)=(0, 0), angle=-1):
        # init ship posisition
        if pos_x == 0 and pos_y == 0:
            pos_x = randint(-800, 800)
            pos_y = randint(-800, 800)

        if angle == -1:
            angle = randint(0, 360)

        self.points.setCenter(pos_x, pos_y)
        self.points.setAngle(angle)
        self.points.update()

    def fadeOutEffect(self):
        # effect when landing
        if self.alpha > 0:
            self.alpha -= 0.1
            return False
        else:
            self.alpha = 0.0
            return True

    def fadeInEffect(self):
        # effect when launching
        if self.alpha < 1.0:
            self.alpha += 0.1
            return False
        else:
            self.alpha = 1.0
            return True

    def checkLanding(self):
        ship_landing_dist = lengthBetweenPoints(
            (self.points.center[0], self.points.center[1]),
            (self.target_planet.points.center[0], self.target_planet.points.center[1]),
        )
        if ship_landing_dist < self.target_planet.w / 2:
            return self.target_planet.landingRequest()
        return False

    def landingEvent(self):
        self.starsystem.removeShipFromStarsystem(self)
        self.target_planet.manageIncomingShip(self)

        print self.name, "landed -->"

        return True

    def launchEvent(self):
        self.target_planet.manageOutcomeShip(self)
        self.starsystem.appendShipToStarsystem(self)

        self.points.setCenter(
            self.target_planet.points.center[0], self.target_planet.points.center[1]
        )

        self.target_planet = None

        self.is_LANDED = False
        self.in_SPACE = True

        print self.name, "launched <--"

        return True

    # def calculateWayToCoord = calculateWayToCoord_TRUE or calculateWayToCoord_FAKE

    def calculateWayToCoord_TRUE(self, (x, y)):
        self.setTargetPosCoord((x, y))
        self.calculateDetaledWayToPosition()  # under constraction
        self.calculateTurnWayToPosition()  # remove (perform if ship is selected by cursor)
        self.calculateWayVisualisation()  # remove (perform if ship is selected by cursor)

    def calculateWayToCoord_FAKE(self, (x, y)):
        self.setTargetPosCoord(x, y)
        self.calculateTurnWayToPosition()

    def setTargetPosCoord(self, (x, y)):  # depr
        self.target_pos_x = x
        self.target_pos_y = y

    def calculateDetaledWayToPosition(self):
        ## print('skeep calculateDetaledWayToPosition'
        # create lists of coordinates and angles for ship movement
        # if self.target_pos_x != None and self.target_pos_y != None:

        # self.direction_list_x_part1, self.direction_list_y_part1, self.angle_list_part1 = self.calculateRoundDetaledWay((self.points.center[0], self.points.center[1]), (self.target_pos_x, self.target_pos_y), self.points.angle, 100, 3)

        # if len(self.direction_list_x_part1) > 0:

        # last_pos_x = self.direction_list_x_part1[len(self.direction_list_x_part1)-1]
        # last_pos_y = self.direction_list_y_part1[len(self.direction_list_x_part1)-1]

        last_pos_x = self.points.center[0]
        last_pos_y = self.points.center[1]

        self.direction_list_x_part1 = []
        self.direction_list_y_part1 = []
        self.angle_list_part1 = []

        (
            self.direction_list_x_part2,
            self.direction_list_y_part2,
            self.angle_list_part2,
        ) = follow_static_obj(
            (last_pos_x, last_pos_y), (self.target_pos_x, self.target_pos_y), self.speed
        )

        self.direction_list_x = (
            self.direction_list_x_part1 + self.direction_list_x_part2
        )
        self.direction_list_y = (
            self.direction_list_y_part1 + self.direction_list_y_part2
        )
        self.angle_list = self.angle_list_part1 + self.angle_list_part2
        self.len_direction_list = len(self.direction_list_x)

        self.i = 0
        self.direction_list_END = False

    def calculateRoundDetaledWay(
        self, (pos_x, pos_y), (target_x, target_y), alpha, R, speed
    ):  # not working yet
        direction_list_x = []
        direction_list_y = []
        angle_list = []

        self.xk = None
        self.yk = None

        # vychislenie centrov okruzhnostej traektorij na osnovanii tekuwego polozhenija ob'ekta
        gamma1 = (alpha + 90) / 57.295779
        gamma2 = (alpha - 90) / 57.295779

        self.center1_x = pos_x + R * cos(gamma1)
        self.center1_y = pos_y + R * sin(gamma1)

        self.center2_x = pos_x + R * cos(gamma2)
        self.center2_y = pos_y + R * sin(gamma2)

        # find colsest center
        len1 = lengthBetweenPoints(
            (self.center1_x, self.center1_y), (target_x, target_y)
        )
        len2 = lengthBetweenPoints(
            (self.center2_x, self.center2_y), (target_x, target_y)
        )

        if len1 < len2:
            print "len1 < len2"
            self.rotation_trajectory_center_x = self.center1_x
            self.rotation_trajectory_center_y = self.center1_y

        if len2 < len1:
            print "len2 < len1"
            self.rotation_trajectory_center_x = self.center2_x
            self.rotation_trajectory_center_y = self.center2_y

        self.d_a = 0.01

        # vychislenija tochek kasanija k okruzhnosti lucha isxodjawego iz target_xy
        dx = target_x - self.rotation_trajectory_center_x
        dy = target_y - self.rotation_trajectory_center_y

        L = sqrt(dx ** 2 + dy ** 2)

        L1 = sqrt(L ** 2 - R ** 2)  # L1 = L2
        a1 = asin((self.rotation_trajectory_center_x - target_x) / float(L))
        b1 = asin(R / float(L))

        if self.rotation_trajectory_center_y < target_y:
            k = -1
        else:
            k = 1

        self.xk1 = target_x + L1 * sin(a1 - b1)
        self.yk1 = target_y + k * L1 * cos(a1 - b1)

        self.xk2 = target_x + L1 * sin(a1 + b1)
        self.yk2 = target_y + k * L1 * cos(a1 + b1)

        # an1 =
        len1 = lengthBetweenPoints(
            (self.xk1, self.yk1), (self.points.midLeft[0], self.points.midLeft[1])
        )
        len2 = lengthBetweenPoints(
            (self.xk2, self.yk2), (self.points.midLeft[0], self.points.midLeft[1])
        )

        if len1 > len2:
            # if self.rotation_trajectory_center_y > target_y:
            self.xk = self.xk1
            self.yk = self.yk1
            # clockwise = False
            ## print('clockwise = False'

        if len1 <= len2:
            # if self.rotation_trajectory_center_y < target_y:
            self.xk = self.xk2
            self.yk = self.yk2
            # clockwise = True
            ## print('clockwise = True'

        if atan2(pos_y, pos_x) < atan2(self.yk, self.xk):
            clockwise = True
            # print('clockwise = True'
        else:
            clockwise = False
            # print('clockwise = False'

        # print a1 -alpha / 57.295779
        # if a1 -alpha / 57.295779 > 0:
        #   clockwise = True
        # else:
        #   clockwise = False

        angle = alpha / 57.295779
        self_x, self_y = pos_x, pos_y
        i = 0

        if clockwise == True:
            while (abs(self.xk - self_x) > 2) or (abs(self.yk - self_y) > 2):
                # print i
                angle += self.d_a
                self_x = self.rotation_trajectory_center_x + R * cos(angle - pi / 2)
                self_y = self.rotation_trajectory_center_y + R * sin(angle - pi / 2)

                direction_list_x.append(self_x)
                direction_list_y.append(self_y)
                angle_list.append(angle * 57.295779)
                i += 1

        elif clockwise == False:
            while (abs(self.xk - self_x) > 2) or (abs(self.yk - self_y) > 2):
                # print i
                angle -= self.d_a
                self_x = self.rotation_trajectory_center_x + R * cos(angle + pi / 2)
                self_y = self.rotation_trajectory_center_y + R * sin(angle + pi / 2)

                direction_list_x.append(self_x)
                direction_list_y.append(self_y)
                angle_list.append(angle * 57.295779)
                i += 1

        return direction_list_x, direction_list_y, angle_list

    def calculateTurnWayToPosition(self):
        if self.target_pos_x != None and self.target_pos_y != None:
            (
                self.turn_direction_list_x,
                self.turn_direction_list_y,
                _,
            ) = follow_static_obj(
                (self.points.center[0], self.points.center[1]),
                (self.target_pos_x, self.target_pos_y),
                self.turn_step,
            )
            self.len_turn_direction_list = len(self.turn_direction_list_x)

            self.turn_i = 0
            self.turn_list_END = False

    def calculateWayVisualisation(self):
        if self.target_pos_x != None and self.target_pos_y != None:
            (
                self.draw_direction_list_x,
                self.draw_direction_list_y,
                _,
            ) = follow_static_obj(
                (self.points.center[0], self.points.center[1]),
                (self.target_pos_x, self.target_pos_y),
                self.draw_step,
            )
            self.draw_orbit_list_len = len(self.draw_direction_list_x)
            # self.Gl_LIST_direction_ID = GlListCompileDirection(DOT_BLUE_TEX, self.draw_direction_list_x, self.draw_direction_list_y, self.len_turn_direction_list, 1)
            # self.calculateTurnWayToPosition()
            # self.Gl_TURN_LIST_direction_ID = GlListCompileDirection(DOT_RED_TEX, self.turn_direction_list_x, self.turn_direction_list_y, self.len_turn_direction_list, 1, pointer_size = DOT_SIZE * 1.4)

    def renderDirection(self):
        if self.Gl_LIST_direction_ID != None:
            glCallList(self.Gl_LIST_direction_ID)
            glCallList(self.Gl_TURN_LIST_direction_ID)

    def updatePosition(self):
        if self.direction_list_END == False:
            if self.i < (self.len_direction_list - 1):
                self.points.setCenter(
                    self.direction_list_x[self.i], self.direction_list_y[self.i]
                )
                self.points.setAngle(self.angle_list[self.i])
                self.points.update()  # remove to perform this only for visible ships (fitted the screen)
                self.i += 1
            else:
                self.direction_list_END = True

    def updatePositionHidden(self):  # perform once per turn
        # performs only once per turn, need for ships which are outide current starsystem
        if self.turn_list_END == False:
            if self.turn_i < (self.len_turn_direction_list - 1):
                self.points.setCenter(
                    self.turn_direction_list_x[self.turn_i],
                    self.turn_direction_list_y[self.turn_i],
                )
                self.turn_i += 1
            else:
                self.turn_list_END = True

    def setKorpus(self, korpus):
        self.korpus = korpus
        self.korpus.owner = self

        self.putAllItemsToSlots()

        self.texOb = self.korpus.texOb

        self.w, self.h = self.korpus.w, self.korpus.h

        self.size = returnObjectSize(self.korpus.w, self.korpus.h)
        self.collision_threshold = (self.w + self.h) / 2

        # New!!!
        self.points = points()
        self.points.createSpaceShipCascade(self.w, self.h)

        # self.drive_jet = driveTrailEffect(self, TEXTURE_MANAGER.returnParticleTexObByColorId(RED_COLOR_ID), 5,            self.size * 10,   1.0,      1.0,        0.0,       0.1)
        if self.ableTo_DRIVE:
            drive = self.korpus.drive_slot.item
            self.drive_jet = driveTrailEffect(
                self,
                drive.pTexture,
                drive.pNum,
                self.size * drive.pSize,
                drive.pVelocity,
                drive.pAlphaInit,
                drive.pAlphaEnd,
                drive.pd_alpha,
            )
        if self.ableTo_PROTECT:
            self.shield = shieldEffect(
                self, self.korpus.protector_slot.item.shield_texOb
            )

        self.korpus.owner = self

        self.linkTexture()

    def putAllItemsToSlots(self):
        # manage item list to specific slot or to otsec  slot if approptiate slot is not avalibale or already is used by other item
        for item in self.item_list:
            slot = returnFirstFreeSlotBySlotType(
                item.type, item.subtype, self.korpus.slot_list
            )
            if slot != None:
                self.putItemToSlot(item, slot)
            else:
                otsec_slot = returnFirstFreeSlotBySlotType(
                    OTSEC_SLOT_ID, None, self.korpus.otsec_slot_list
                )
                if otsec_slot != None:
                    self.putItemToSlot(item, otsec_slot)

        self.updateAllStuff()

    def putItemToSlot(self, item, slot):
        slot.item = item
        item.rect = pygame.Rect(
            (slot.rect[0], slot.rect[1]), (slot.rect[2], slot.rect[3])
        )
        item.owner = self

    def updateAllStuff(self):
        # this function set actual ship propretries relying to all equipment placed in slots
        # used when ship change items in slot
        # !!! all this stuff can be called separately by item deterioration function if item becomes broken !!!

        self.updateRadarAbility()
        self.updateDriveAbility()
        self.updateJumpAbility()
        self.updateEnergyAbility()
        # self.updateProtectionAbility() is performing inside self.updateEnergyAbility() , because energy shield depends on energy and consume it much
        self.updateFireAbility()

        self.updateRepairAbility()
        self.updateFreezeAbility()
        self.updateGrabAbility()
        self.updateScanAbility()

    def updateRadarAbility(self):
        radar = self.korpus.radar_slot.item
        self.radar = radar
        if radar != None and radar.condition > 0:
            self.radius = radar.radius
            self.ableTo_RADAR = True
        else:
            self.radius = VISIBLE_DISTANCE_WITHOUT_RADAR
            self.ableTo_RADAR = False

    def updateDriveAbility(self):
        # calculate mass and then actual ship speed depending on drive power and actual mass
        # used each time when ship picked up/bought or drop/sold something.

        ### mass calculation ###
        self.mass = 0
        for slot in self.korpus.total_slot_list:
            if slot.item != None:
                self.mass += slot.item.mass

        ### speed calculation ###
        self.ableTo_DRIVE = False
        self.speed = 0

        drive = self.korpus.drive_slot.item
        self.drive = drive
        if drive != None and drive.condition > 0:
            self.speed = drive.speed - self.mass / 70
            if self.speed > 0:
                self.ableTo_DRIVE = True

        ### constants for direction visualization ###
        if self.ableTo_DRIVE:
            self.turn_step = self.speed * TURN_TIME
            self.draw_step = self.turn_step / int(4 * self.speed / DRIVE_SPEED_MIN)

    def updateJumpAbility(self):
        drive = self.korpus.drive_slot.item
        bak = self.korpus.bak_slot.item
        self.bak = bak
        if (drive != None and drive.condition > 0) and (
            bak != None and bak.condition > 0
        ):
            self.hyper = min(drive.hyper, bak.fuel)
            self.ableTo_JUMP = True
        else:
            self.hyper = 0
            self.ableTo_JUMP = False

    def updateEnergyAbility(self):
        energyBlock = self.korpus.energyBlock_slot.item
        self.energyBlock = energyBlock
        if energyBlock != None and energyBlock.condition > 0:
            self.energy = energyBlock.energy
            self.ableTo_ENERGIZE = True
        else:
            self.energy = 0
            self.ableTo_ENERGIZE = False

        self.updateProtectionAbility()

    def updateProtectionAbility(self):
        protector = self.korpus.protector_slot.item
        self.protector = protector
        if (
            protector != None and protector.condition > 0
        ) and self.ableTo_ENERGIZE == True:
            self.protection = protector.protection + self.korpus.protection
            self.ableTo_PROTECT = True
        else:
            self.protection = self.korpus.protection
            self.ableTo_PROTECT = False

    def updateRepairAbility(self):
        droid = self.korpus.droid_slot.item
        self.droid = droid
        if droid != None and droid.condition > 0:
            self.repair = droid.repair
            self.ableTo_REPAIR = True
        else:
            self.repair = 0
            self.ableTo_REPAIR = False

    def updateFreezeAbility(self):
        freezer = self.korpus.freezer_slot.item
        self.freezer = freezer
        if freezer != None and freezer.condition > 0:
            self.freeze = freezer.freeze
            self.ableTo_FREEZE = True
        else:
            self.freeze = 0
            self.ableTo_FREEZE = False

    def updateGrabAbility(self):
        self.ableTo_GRAB = False
        if self.korpus.grapple_slot != None:
            grapple = self.korpus.grapple_slot.item
            self.grapple = grapple
            if grapple != None and grapple.condition > 0:
                self.ableTo_GRAB = True

    def updateScanAbility(self):
        scaner = self.korpus.scaner_slot.item
        self.scaner = scaner
        if scaner != None:
            self.scan = scaner.scan
            self.ableTo_SCAN = True
        else:
            self.scan = 0
            self.ableTo_SCAN = False

    def updateFireAbility(self):
        self.armed_weapon_slot_list = []

        self.sum_damage = 0
        sum_fire_radius = 0
        for w_slot in self.korpus.weapon_slot_list:
            if w_slot.item != None and w_slot.item.condition > 0:
                self.armed_weapon_slot_list.append(w_slot)
                self.sum_damage += w_slot.item.damage
                sum_fire_radius += w_slot.item.radius

        if len(self.armed_weapon_slot_list) != 0:
            self.average_fire_radius = sum_fire_radius / len(
                self.armed_weapon_slot_list
            )
            self.ableTo_FIRE = True
        else:
            self.average_fire_radius = 0
            self.ableTo_FIRE = False

    """
    def returnAllItemList(self):
        # this list is used in case of explosion, some stuff move to container and then out to the space
        self.all_item_list = []
        for slot in self.korpus.slot_list:
            if slot.item != None:
               self.all_item_list.append(slot.item)
        for slot in self.korpus.otsec_slot_list:
            if slot.item != None:
               self.all_item_list.append(slot.item)
        return self.all_item_list
    """

    def buyFuel(self):
        if self.korpus.bak_slot.item != None:
            fuel_dif = (
                self.korpus.bak_slot.item.fuel_max - self.korpus.bak_slot.item.fuel
            )
            if self.credits >= fuel_dif:
                self.korpus.bak_slot.item.fuel = self.korpus.bak_slot.item.fuel_max
                self.credits -= fuel_dif
                self.korpus.bak_slot.item.updateInfo()

    def buyRepair(self):
        armor_dif = self.korpus.armor_max - self.korpus.armor
        if self.credits >= armor_dif:
            self.korpus.armor = self.korpus.armor_max
            self.credits -= armor_dif
            return True
        else:
            return False

    def dirtyWork(self):
        self.korpus.armor += 0.1 * self.korpus.armor_max

    def armorRestoration(self):
        # droid works
        if self.korpus.armor < self.korpus.armor_max:
            if self.ableTo_REPAIR == True:
                self.korpus.armor += self.repair
                self.korpus.droid_slot.item.deterioration()

    def energyRestoration(self):
        # performs once per turn
        if self.korpus.energyBlock_slot.item != None:
            self.energy += (
                self.energy_restoration_rate
                * self.korpus.energyBlock_slot.item.restoration
            )
            self.korpus.energyBlock_slot.item.energy = self.energy

    def temperatureRestoration(self):
        # performs once per turn
        if self.temperature > -100:
            if self.ableTo_FREEZE == True:
                self.temperature -= self.freeze
        else:
            self.temperature = -100

    def hyperJumpPreparation(self, target_starsystem):
        # performs once
        self.target_starsystem = target_starsystem
        self.target_starsystem_dist = lengthBetweenPoints(
            (self.starsystem.rectOnMap.centerx, self.starsystem.rectOnMap.centery),
            (
                self.target_starsystem.rectOnMap.centerx,
                self.target_starsystem.rectOnMap.centery,
            ),
        )
        _y = (
            self.target_starsystem.rectOnMap.centery - self.starsystem.rectOnMap.centery
        )
        _x = (
            self.target_starsystem.rectOnMap.centerx - self.starsystem.rectOnMap.centerx
        )
        self._a = atan2(_x, _y)
        self.jump_pos_x, self.jump_pos_y = returnGeneratedTargetCoordinates(
            800, self._a, (0, 0)
        )

    def navigateHyperJumpPoint(self):
        if (
            abs(self.points.center[0] - self.jump_pos_x) < 10
            and abs(self.points.center[1] - self.jump_pos_y) < 10
        ):
            print self.name
            return True
        else:
            return False

    def hyperJumpEvent(self):
        if self.alive == True:
            if self.ableTo_JUMP:
                if (
                    self.target_starsystem_dist < self.korpus.drive_slot.item.hyper
                    and self.target_starsystem_dist < self.korpus.bak_slot.item.fuel
                ):
                    # print('-> -> ->', self.name, 'JUMPED to', self.target_starsystem.name
                    self.korpus.bak_slot.item.fuel -= int(self.target_starsystem_dist)
                    self.korpus.bak_slot.item.updateInfo()

                    self.starsystem.removeShipFromStarsystem(self)
                    self.target_starsystem.appendShipToStarsystem(self)

                    self.starsystem = self.target_starsystem
                    self.target_starsystem = None
                    self.jump_pos_x, self.jump_pos_y = None, None

                    self.target_reset()

                    self.red, self.green, self.blue = (
                        self.starsystem.red,
                        self.starsystem.green,
                        self.starsystem.blue,
                    )
                    return True
        return False

    def hyperJumpInEffect(self):
        delta = 10
        self.w += delta
        self.updateRenderConstants()
        if self.w > 3 * self.korpus.w_orig:
            return True
        else:
            return False

    def hyperJumpOutEffect(self):
        delta = 10
        self.w -= delta
        self.updateRenderConstants()
        if self.w < (self.korpus.w_orig + delta):
            self.w = self.korpus.w_orig
            return True
        else:
            return False

    def target_reset(self):
        for w_slot in self.armed_weapon_slot_list:
            w_slot.target_EXIST = False

    def weaponsReload(self):
        # reload wepons
        # used once at the beginning of turn

        self.reloaded_weapon_list = []
        for w_slot in self.armed_weapon_slot_list:
            if w_slot.item.subtype == ROCKET_ID:
                if w_slot.item.ammo > 0:
                    self.reloaded_weapon_list.append(w_slot)
            else:
                self.reloaded_weapon_list.append(w_slot)

        self.fire_delay = 10
        self.delay = 30

    def setWeaponsToTarget(
        self,
        target,
        (
            slot_1_SELECTED,
            slot_2_SELECTED,
            slot_3_SELECTED,
            slot_4_SELECTED,
            slot_5_SELECTED,
        )=(True, True, True, True, True),
    ):
        ### set Target for selected non-targeted weapon slots ###
        if self.korpus.weapon_slot1 != None:
            self.korpus.weapon_slot1.SELECTED = slot_1_SELECTED
        if self.korpus.weapon_slot2 != None:
            self.korpus.weapon_slot2.SELECTED = slot_2_SELECTED
        if self.korpus.weapon_slot3 != None:
            self.korpus.weapon_slot3.SELECTED = slot_3_SELECTED
        if self.korpus.weapon_slot4 != None:
            self.korpus.weapon_slot4.SELECTED = slot_4_SELECTED
        if self.korpus.weapon_slot5 != None:
            self.korpus.weapon_slot5.SELECTED = slot_5_SELECTED

        ship_target_dist = lengthBetweenPoints(
            (self.points.center[0], self.points.center[1]),
            (target.points.center[0], target.points.center[1]),
        )
        for w_slot in self.armed_weapon_slot_list:
            if (
                w_slot.SELECTED == True
                and w_slot.target == None
                and ship_target_dist <= w_slot.item.radius
            ):
                w_slot.target = target

    def weaponTargetAchievable(self, w_slot):
        ### check for each slot if target is still achievable, if not - reset the slot target to None ###
        if (
            (w_slot.target.alive == False)
            or (w_slot.target.in_SPACE == False)
            or (w_slot.target.starsystem.name != self.starsystem.name)
        ):
            w_slot.target = None
            return False
        else:
            ship_slotTarget_dist = lengthBetweenPoints(
                (self.points.center[0], self.points.center[1]),
                (w_slot.target.points.center[0], w_slot.target.points.center[1]),
            )
            if ship_slotTarget_dist > w_slot.item.radius:
                w_slot.target = None
                return False

        return True

    def weaponsFire(self, timer):
        if timer < TURN_TIME - self.fire_delay:
            for w_slot in self.reloaded_weapon_list:
                if w_slot.target != None:
                    if self.weaponTargetAchievable(w_slot):
                        w_slot.item.target = w_slot.target
                        w_slot.item.Fire()
                        # if self.name == 'plr': # debug
                        #   print w_slot.item.condition, w_slot.item.condition_max

                        self.reloaded_weapon_list.remove(w_slot)
                        self.fire_delay += self.delay
                        break

    def resetWeaponTargets(
        self,
        (
            slot_1_SELECTED,
            slot_2_SELECTED,
            slot_3_SELECTED,
            slot_4_SELECTED,
            slot_5_SELECTED,
        ),
    ):
        ### reset Target for selected targeted weapon slots ###
        if self.korpus.weapon_slot1 != None:
            self.korpus.weapon_slot1.SELECTED = slot_1_SELECTED
        if self.korpus.weapon_slot2 != None:
            self.korpus.weapon_slot2.SELECTED = slot_2_SELECTED
        if self.korpus.weapon_slot3 != None:
            self.korpus.weapon_slot3.SELECTED = slot_3_SELECTED
        if self.korpus.weapon_slot4 != None:
            self.korpus.weapon_slot4.SELECTED = slot_4_SELECTED
        if self.korpus.weapon_slot5 != None:
            self.korpus.weapon_slot5.SELECTED = slot_5_SELECTED

        for w_slot in self.armed_weapon_slot_list:
            if w_slot.target != None:
                if w_slot.SELECTED == False:
                    w_slot.target = None

    def checkGrabQueue(self):
        # execute within game loop
        for item in self.korpus.grapple_slot.item.grapple_list:
            ship_item_dist = lengthBetweenPoints(
                (self.points.center[0], self.points.center[1]),
                (item.points.center[0], item.points.center[1]),
            )
            if (
                ship_item_dist > self.korpus.grapple_slot.item.radius
                or item.alive == False
                or item.in_SPACE == False
            ):
                self.addToGrappleRemoveQueue(item)

    def resetGrappleTargets(self):  # hunters ???
        if self.ableTo_GRAB == True:
            self.korpus.grapple_slot.item.grapple_list = []

    def addToGrappleTargetList(self, item):
        # if item not in self.korpus.grapple_slot.item.grapple_list:
        self.korpus.grapple_slot.item.grapple_list.append(item)
        item.hunters_list.append(self)

    def addToGrappleRemoveQueue(self, item):
        self.korpus.grapple_slot.item.grapple_remove_queue.append(item)

    def grappleRemoveQueueManager(self):
        for item in self.korpus.grapple_slot.item.grapple_remove_queue:
            self.korpus.grapple_slot.item.grapple_list.remove(item)
        self.korpus.grapple_slot.item.grapple_remove_queue = []

    def grabExecution(self):
        # print self.name
        # in DYNAMIC
        for item in self.korpus.grapple_slot.item.grapple_list:
            item.target_pos_x, item.target_pos_y = (
                self.points.center[0],
                self.points.center[1],
            )  ##
            item.speed = self.korpus.grapple_slot.item.speed
            item.stepCalculation()
            if (
                abs(self.points.center[0] - item.points.center[0]) < 20
                and abs(self.points.center[1] - item.points.center[1]) < 20
                and item.is_COLLECTED == False
            ):
                self.takeToOtsec(item)
                # print "   ", self.name, "grab ", item.returnTypeStr(), " mass:", item.mass            # debug

    def takeToOtsec(self, ob):
        # moving object from Space to ship otsec
        # used when item(container or mineral) was grabbed from the space

        ob.in_SPACE = False
        ob.is_COLLECTED = True

        ob.owner = self

        ob.hunters_list = []

        if ob.type != CONTAINER_ID and ob.subtype == MINERAL_id:
            ob.starsystem.MINERAL_list.remove(ob)
            slot = returnSlotWithGoodsBySubtype(MINERAL_id, self.korpus.otsec_slot_list)
            if slot != None:
                slot.item.item.mass += ob.mass
                slot.item.updateInfo()
            else:
                slot = returnFirstFreeSlotBySlotType(
                    OTSEC_SLOT_ID, None, self.korpus.otsec_slot_list
                )
                if slot != None:
                    texOb = TEXTURE_MANAGER.container_texOb_list[0]
                    c = Container(texOb, ob)  # create container, put item in
                    slot.item = c

        elif ob.type == CONTAINER_ID:
            ob.starsystem.CONTAINER_list.remove(ob)
            if ob.subtype == EQUIPMENT_ID or ob.subtype == WEAPON_ID:
                slot = returnFirstFreeSlotBySlotType(
                    OTSEC_SLOT_ID, None, self.korpus.otsec_slot_list
                )
                if slot != None:
                    slot.item = ob.item

            elif ob.subtype == MODULE_ID:
                slot = returnFirstFreeSlotBySlotType(
                    OTSEC_SLOT_ID, None, self.korpus.otsec_slot_list
                )
                if slot != None:
                    slot.item = ob.item

            elif ob.subtype == GOODS_id:
                slot = returnSlotWithGoodsBySubtype(
                    ob.item.subtype, self.korpus.otsec_slot_list
                )
                if slot != None:
                    slot.item.mass += ob.mass
                    slot.item.updateInfo()
                else:
                    slot = returnFirstFreeSlotBySlotType(
                        OTSEC_SLOT_ID, None, self.korpus.otsec_slot_list
                    )
                    if slot != None:
                        slot.item = ob

        elif ob.type == BOMB_ID:
            ob.starsystem.BOMB_list.remove(ob)
            slot = returnFirstFreeSlotBySlotType(
                OTSEC_SLOT_ID, None, self.korpus.otsec_slot_list
            )
            if slot != None:
                slot.item = ob

        self.item_list.append(ob)
        self.updateDriveAbility()  # up-to-date mass and speed

    def dropToSpace(self, item):
        if item.type == BOMB_ID:
            ob = item
            self.starsystem.BOMB_list.append(ob)

        elif item.type == CONTAINER_ID:
            ob = item
            self.starsystem.CONTAINER_list.append(ob)

        elif (
            item.type == EQUIPMENT_ID
            or item.type == WEAPON_ID
            or item.type == MODULE_ID
        ):
            texOb = TEXTURE_MANAGER.container_texOb_list[0]
            ob = Container(texOb, item)
            self.starsystem.CONTAINER_list.append(ob)  # pack item to container

        ob.starsystem = self.starsystem  # must be improved after hyper jump
        ob.points.setCenter(self.points.center[0], self.points.center[1])
        ob.target_pos_x, ob.target_pos_y = returnGeneratedTargetCoordinates(
            randint(50, 100),
            randint(0, 360) / 57.0,
            (ob.points.center[0], ob.points.center[1]),
        )

        ob.in_SPACE = True

    def updateInfo(self):
        self.info = []

        self.info.append("race:" + self.returnRaceStr())
        self.info.append("name:" + str(self.name))
        self.info.append("type:" + self.returnTypeStr())
        self.info.append("korp size:" + str(self.korpus.size))
        self.info.append(
            "armor:"
            + str(int(self.korpus.armor))
            + "/"
            + str(int(self.korpus.armor_max))
        )
        self.info.append(
            "space all/free:"
            + str(int(self.korpus.space))
            + "/"
            + str(int(self.korpus.space - self.mass))
        )
        self.info.append("speed:" + str(int(self.speed)))
        self.info.append("energy:" + str(int(self.energy)))
        self.info.append("temperature:" + str(int(self.temperature)))
        self.info.append("radius:" + str(int(self.radius)))
        self.info.append("protection:" + self.returnProtectionStr())

        if self.name != "plr":
            self.info.append(self.returnCurTaskStr(self.task_id_being_exec))  # debug
            self.info.append(self.returnQuestTaskListStr())  # debug
            self.info.append(self.returnNeedsTaskListStr())  # debug

    def returnQuestTaskListStr(self):
        str = "QTL: "
        for task in self.QUEST_TASK_queue:
            str += self.returnCurTaskStr(task) + ";   "
        return str

    def returnNeedsTaskListStr(self):
        str = "NTL: "
        for task in self.NEEDS_TASK_queue:
            str += self.returnCurTaskStr(task) + ";   "
        return str

    def returnCurTaskStr(self, task_id):
        if task_id == HYPER_JUMP_task_id:
            return "HYPER_JUMP_to_" + self.returnTargetSsnameStr()
        elif task_id == DESTROY_ALIEN_task_id:
            return "DESTROY_ALIEN_task_id"
        elif task_id == LANDING_task_id:
            return "LANDING_task_id"
        elif task_id == LAUNCHING_task_id:
            return "LAUNCHING_task_id"
        elif task_id == AREST_REQUEST_task_id:
            return "AREST_REQUEST_task_id"
        elif task_id == TERROR_REQUEST_task_id:
            return "TERROR_REQUEST_task_id"
        elif task_id == FIRE_LOW_task_id:
            return "FIRE_LOW_task_id"
        elif task_id == FIRE_HIGH_task_id:
            return "FIRE_HIGH_task_id"
        elif task_id == FIND_PLACE_TO_SELL_GOODS_task_id:
            return "FIND_PLACE_TO_SELL_GOODS_task_id"
        elif task_id == BUY_GOODS_task_id:
            return "BUY_GOODS_task_id"
        elif task_id == SELL_GOODS_task_id:
            return "SELL_GOODS_task_id"
        elif task_id == GRABBING_MINERAL_task_id:
            return "GRABBING_MINERAL_task_id, items:" + str(
                len(self.korpus.grapple_slot.item.grapple_list)
            )
        elif task_id == GRABBING_CONTAINER_task_id:
            return "GRABBING_CONTAINER_task_id, items:" + str(
                len(self.korpus.grapple_slot.item.grapple_list)
            )
        elif task_id == None:
            return "None"
        else:
            return "unknown"

    def returnTargetSsnameStr(self):
        if self.target_starsystem != None:
            return self.target_starsystem.name
        else:
            return ""

    def returnTypeStr(self):
        if self.subtype == RANGER_ID:
            if self.subsubtype == WARRIOR_ID:
                return "ranger-warrior"
            elif self.subsubtype == PIRAT_ID:
                return "ranger-pirat"
            elif self.subsubtype == TRADER_ID:
                return "ranger-trader"
            elif self.subsubtype == DIPLOMAT_ID:
                return "ranger-diplomat"

            else:
                return "ranger-unknown"

        elif self.subtype == WARRIOR_ID:
            return "warrior"
        elif self.subtype == PIRAT_ID:
            return "pirat"
        elif self.subtype == TRADER_ID:
            return "trader"
        elif self.subtype == DIPLOMAT_ID:
            return "diplomat"

        else:
            return "unknown"

    def returnProtectionStr(self):
        # used in updateInfo
        if self.ableTo_PROTECT:
            return (
                str(int(self.korpus.protector_slot.item.protection))
                + "+"
                + str(int(self.korpus.protection))
            )
        else:
            return str(int(self.korpus.protection))

    def renderInfo(self):
        self.updateInfo()
        drawDynamicLabelList(
            text_background_tex,
            (
                self.points.center[0] + self.points.w / 2,
                self.points.center[1] + self.points.h / 2,
            ),
            self.info,
        )
        drawTexturedRect(
            self.face_texOb.texture,
            [
                self.points.center[0] + self.points.w,
                self.points.center[1] + self.points.h,
                70,
                70,
            ],
            -1.0,
        )

    # def renderItemInfoInSlot(self):
    #    if self.SlotWithItemUnderCursor != None:
    #       self.SlotWithItemUnderCursor.item.updateInfo()
    #       drawDynamicLabelList(text_background_tex, (self.SlotWithItemUnderCursor.rect.right, self.SlotWithItemUnderCursor.rect.bottom), self.SlotWithItemUnderCursor.item.info)

    def hit(self, agressor, weapon, rate=1):
        if agressor.type == SHIP_ID:
            damage = int(
                agressor.skill.attack
                / self.skill.defence
                * (1 - self.protection / 100.0)
                * weapon.damage
            )
        else:
            damage = int(
                100.0
                / self.skill.defence
                * (1 - self.protection / 100.0)
                * weapon.damage
            )
        self.korpus.armor -= damage * rate

        if (
            self.korpus.protector_slot.item != None and self.energy > 0
        ):  # improve by repalce ableToProtect
            self.energy -= WEAPON_ENERGY_CONSUMPTION_RATE * damage
            # self.temperature += 1
            self.korpus.protector_slot.item.deterioration()
            # NEW !!!
            self.shield.alpha = 1.0

        t = vericalFlowText(self, str(damage), self.korpus.color)
        self.flow_TEXT_list.append(t)

        if self.korpus.armor <= 0:
            addExplosion(self)

            item_drop_num = randint(1, 4)
            item_drop_queue = []
            i = 0
            while i < item_drop_num:
                if len(self.item_list) >= 2:
                    rand_item = self.item_list[randint(0, len(self.item_list) - 1)]
                    self.item_list.remove(rand_item)
                    item_drop_queue.append(rand_item)
                i += 1

            self.starsystem.addContainers(
                (self.points.center[0], self.points.center[1]), item_drop_queue
            )

            # self.starsystem.screen_QUAKE_runtime_counter = 50
            # self.starsystem.screen_QUAKE_amlitudaDiv2 = 5
            self.alive = False

            if agressor.type == SHIP_ID:
                agressor.skill.addExpirience(self.skill.expirience / 200.0)

            if self.alive == False:
                if self.alreadyInRemoveQueue == False:
                    self.starsystem.SHIP_remove_queue.append(self)
                    self.alreadyInRemoveQueue = True

                    # self.dead()

    def temperatureInfluence(self):
        if self.temperature > 2 * self.korpus.nominal_temperature:
            pass
        elif self.temperature > 2.5 * self.korpus.nominal_temperature:
            pass
        elif self.temperature > 3 * self.korpus.nominal_temperature:
            pass
        elif self.temperature > 3.5 * self.korpus.nominal_temperature:
            pass
        elif self.temperature > 4 * self.korpus.nominal_temperature:
            pass

    def returnRaceStr(self):
        if self.race == RACE_0_ID:
            return "texnologi"
        elif self.race == RACE_1_ID:
            return "voiny"
        elif self.race == RACE_2_ID:
            return "zhuliki"
        elif self.race == RACE_3_ID:
            return "humans"
        elif self.race == RACE_4_ID:
            return "bio"
        elif self.race == RACE_6_ID:
            return "evil 6"
        elif self.race == RACE_7_ID:
            return "evil 7"

        elif self.race == None:
            return "unknown"

    # def renderDynamicFrame2(self):
    # self.drawDynamic2(self.texture_ID, (self.points.center[0], self.points.center[1]), self.angle, (self.minus_w_div_2, self.minus_h_div_2,  self.plus_w_div_2, self.plus_h_div_2 ), (self.red, self.green, self.blue, self.alpha))

    # def renderDynamicFrames2(self):
    # self.drawDynamic2(self.texture_ID[self._tex_frame], (self.points.center[0], self.points.center[1]), self.angle, (self.minus_w_div_2, self.minus_h_div_2, self.plus_w_div_2, self.plus_h_div_2 ), (self.red, self.green, self.blue, self.alpha))
    # self.updateAnimationFrame()

    # def renderStaticFrameTrueSizeInTheMiddleOfRect(self, rect):

    # def renderStaticFramesLoopTrueSizeInTheMiddleOfRect(self, rect):
    # drawTexturedRect(self.texture_ID[self._tex_frame], [rect[0] + rect[2]/2 - self.w/2, rect[1] + rect[3]/2 - self.h/2, self.w, self.h], -1.0)
    # self.updateAnimationFrameLoop()

    # def renderGrappingJet(self):

    def renderInKosmoport(self, slot_rect):
        drawTexturedRect(
            self.texture,
            [
                slot_rect.centerx - self.w / 2,
                slot_rect.centery - self.h / 2,
                self.w,
                self.h,
            ],
            -1.0,
        )

    def renderInSpace(self):
        self.points.update()  # update all control points relevant for drawing

        # render grapping jet
        if self.ableTo_GRAB == True:
            for i in self.korpus.grapple_slot.item.grapple_list:
                len, angle_radian = returnLengthAngleBetweenPoints(
                    (self.points.center[0], self.points.center[1]),
                    (i.points.center[0], i.points.center[1]),
                )
                angle_degree = angle_radian * DEGREES_IN_RADIAN
                drawLine(
                    grapple_jet_tex,
                    (self.points.center[0], self.points.center[1], -2),
                    len,
                    angle_degree,
                    6,
                )

        # render entity quad
        glBindTexture(GL_TEXTURE_2D, self.texture)
        drawQuadPer2DVertex(
            self.points.bottomLeft,
            self.points.bottomRight,
            self.points.topRight,
            self.points.topLeft,
            -3,
        )

        # debug
        # if self.rotation_trajectory_center_x != None and self.rotation_trajectory_center_y != None:
        #   drawTexturedRect(particle1_tex, [self.rotation_trajectory_center_x, self.rotation_trajectory_center_y, 40, 40], -1.0)
        # if self.target_pos_x != None and self.target_pos_y != None:
        #   drawTexturedRect(particle2_tex, [self.target_pos_x, self.target_pos_y, 40, 40], -1.0)
        # if self.xk1 != None and self.yk1 != None:
        # drawTexturedRect(particle0_tex, [self.xk1, self.yk1, 40, 40], -1.0)
        # if self.xk2 != None and self.yk2 != None:
        # drawTexturedRect(particle0_tex, [self.xk2, self.yk2, 40, 40], -1.0)

        # if self.xk != None and self.yk != None:
        #   drawTexturedRect(particle0_tex, [self.xk, self.yk, 40, 40], -1.0)

    def renderProtectionShield(self):
        if self.ableTo_PROTECT:
            self.shield.render()

    def renderDriveJet(self):
        if self.ableTo_DRIVE:
            self.drive_jet.update()
            self.drive_jet.render()

    def linkTexture(self):
        self.texture = self.texOb.texture
        self.korpus.texture = self.texOb.texture
