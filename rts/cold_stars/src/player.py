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
from shipCommon import *

from kosmoport import *
from korpus import *


class PlayerShip(CommonForShip):
    """This class is for the player ship"""

    def __init__(self, starsystem, name, race, face_texOb, subtype):
        CommonForShip.__init__(self, starsystem, name, race, face_texOb, subtype)

        self.in_INVERTAR = False
        self.in_WORLDMAP = False
        self.is_SCANNING = False

        self.starsystem = None

        self.scanned_ob = None

        self.mxvp, self.myvp = 0, 0

        self.grapping_main_target = None

    def update(self, timer):
        for t in self.flow_TEXT_list:
            t.update(timer)

        if timer > 0:
            self.updatePosition()

            if self.ableTo_GRAB == True:
                self.checkGrabQueue()
                self.grabExecution()
                self.grappleRemoveQueueManager()

            if self.target_planet != None:
                if self.checkLanding():
                    if self.fadeOutEffect():
                        self.landingEvent()

    def caclulateWayToCursor(self, (mxvp, myvp)):
        self.setTargetPosCoord((mxvp, myvp))
        self.calculateTurnWayToPosition()
        self.calculateDetaledWayToPosition()

    def GlListCompileRadius(self):
        for w_slot in self.armed_weapon_slot_list:
            (
                self.w_slot_list_x,
                self.w_slot_list_y,
            ) = getCircleCoordinateRangeLowPrecision(
                self.points.center[0], self.points.center[1], w_slot.item.radius
            )
            w_slot.GL_LIST_slot_ID = GlListCompileDirection(
                DOT_RED_TEX,
                self.w_slot_list_x,
                self.w_slot_list_y,
                len(self.w_slot_list_x),
                1,
            )

        if self.korpus.grapple_slot.item != None:
            (
                self.grapple_list_x,
                self.grapple_list_y,
            ) = getCircleCoordinateRangeLowPrecision(
                self.points.center[0],
                self.points.center[1],
                self.korpus.grapple_slot.item.radius,
            )
            self.GL_LIST_grapple_ID = GlListCompileDirection(
                DOT_BLUE_TEX,
                self.grapple_list_x,
                self.grapple_list_y,
                len(self.grapple_list_x),
                1,
            )

        if self.korpus.radar_slot.item != None:
            (
                self.radar_slot_list_x,
                self.radar_slot_list_y,
            ) = getCircleCoordinateRangeLowPrecision(
                self.points.center[0],
                self.points.center[1],
                self.korpus.radar_slot.item.radius,
            )
            self.GL_LIST_radar_ID = GlListCompileDirection(
                DOT_BLUE_TEX,
                self.radar_slot_list_x,
                self.radar_slot_list_y,
                len(self.radar_slot_list_x),
                1,
            )

    def renderRadius(
        self,
        (
            slot_1_SELECTED,
            slot_2_SELECTED,
            slot_3_SELECTED,
            slot_4_SELECTED,
            slot_5_SELECTED,
        ),
        grapple_SELECTED,
        show_RADAR,
    ):
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
            if w_slot.SELECTED == True:
                glCallList(w_slot.GL_LIST_slot_ID)

        if self.korpus.grapple_slot.item != None and grapple_SELECTED == True:
            glCallList(self.GL_LIST_grapple_ID)

        if self.korpus.radar_slot.item != None and show_RADAR == True:
            glCallList(self.GL_LIST_radar_ID)

    ################################################################################################################################
    def renderIcons(self):
        if self.korpus.grapple_slot.item != None:
            for item in self.korpus.grapple_slot.item.grapple_list:
                drawTexturedRect(
                    grabbing_ICON_tex,
                    [item.points.center[0], item.points.center[1], 20, 20],
                    -1.0,
                )
        i = 0
        for w_slot in self.reloaded_weapon_list:
            if w_slot.target != None:
                drawTexturedRect(
                    w_slot.item.texture_ID,
                    [
                        w_slot.target.points.center[0] - w_slot.target.w / 2 + 23 * i,
                        w_slot.target.points.center[1] + w_slot.target.h / 2,
                        20,
                        20,
                    ],
                    -1.0,
                )
                i += 1

    def taskManager(self):
        pass

    def taskExecution_inDynamic(self):
        pass

    def taskExecution_inStatic(self):
        pass

    def thinkInSpace(self):
        pass

    def sensorium(self, asteroid_list, mineral_list, container_list):
        pass

    def thinkAtInhabitedPlanet(self):
        pass

    def thinkAtUninhabitedPlanet(self):
        pass

    def taskScenarioInSpace(self):
        pass

    def taskScenarioAtInhabitedPlanet(self):
        pass

    def taskScenarioAtUninhabitedPlanet(self):
        pass

    def setGrabItem(self, item):
        if self.ableTo_GRAB == True:
            skeep_grabbing = False
            ship_item_dist = lengthBetweenPoints(
                (self.points.center[0], self.points.center[1]),
                (item.points.center[0], item.points.center[1]),
            )
            if (
                ship_item_dist <= self.korpus.grapple_slot.item.radius
            ):  # check if item lays in range of grapple access area
                for (
                    marked_item
                ) in (
                    self.korpus.grapple_slot.item.grapple_list
                ):  # check if item is already in the grapple target list, if yes it shall be removed
                    if marked_item == item:
                        self.addToGrappleRemoveQueue(item)
                        skeep_grabbing = True
                        break

                if (
                    (item.mass <= self.korpus.grapple_slot.item.strength)
                    and (
                        len(self.korpus.grapple_slot.item.grapple_list)
                        < self.korpus.grapple_slot.item.maxNumItem
                    )
                    and skeep_grabbing == False
                ):  # check the rest condition for grabbing and if yes, grab it
                    item.speed = self.korpus.grapple_slot.item.speed
                    item.stepCalculation()
                    self.addToGrappleTargetList(item)
