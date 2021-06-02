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

# from textures import *
from operator import itemgetter, attrgetter


class NPC(CommonForShip):
    def __init__(self, starsystem, name, race, face_texOb, subtype):
        CommonForShip.__init__(self, starsystem, name, race, face_texOb, subtype)
        self.being_GRAPPING = False
        self.grapping_main_target = None
        self.day_landed = 0

        self.QUEST_TASK_queue = []
        self.NEEDS_TASK_queue = []

        self.taskExecution_inDynamic = self.doNothing
        self.taskExecution_inStatic = self.doNothing

        if self.race == RACE_0_ID:
            self.thinkInSpace = self.thinkInSpaceRace0
        elif self.race == RACE_1_ID:
            self.thinkInSpace = self.thinkInSpaceRace1
        elif self.race == RACE_2_ID:
            self.thinkInSpace = self.thinkInSpaceRace2
        elif self.race == RACE_3_ID:
            self.thinkInSpace = self.thinkInSpaceRace3
        elif self.race == RACE_4_ID:
            self.thinkInSpace = self.thinkInSpaceRace4
        elif self.race == RACE_6_ID:
            self.thinkInSpace = self.thinkInSpaceRace6
        elif self.race == RACE_7_ID:
            self.thinkInSpace = self.thinkInSpaceRace7

    def update(self, timer):
        for t in self.flow_TEXT_list:
            t.update(timer)
        if timer > 0:
            self.updatePosition()
            self.taskExecution_inDynamic()  # depr

    def updateHidden(self, timer):
        self.updatePositionHidden()

    def insertQuestTask(self, task_id):
        # print('+++insert QT', self.name, self.returnCurTaskStr(task_id)                        # debug
        self.QUEST_TASK_queue.insert(0, task_id)
        self.taskManager()
        # print self.name, 'new_Cur_task =', self.returnCurTaskStr(self.task_id_being_exec)     # debug

    def removeQuestTask(self, task_id):
        # print('---remove QT', self.name, self.returnCurTaskStr(task_id)                        # debug
        self.QUEST_TASK_queue.remove(task_id)
        self.taskManager()
        # print self.name, 'new_Cur_task =', self.returnCurTaskStr(self.task_id_being_exec)     # debug

    def insertNeedsTask(self, task_id):
        # print('+++insert NT', self.name, self.returnCurTaskStr(task_id)                        # debug
        self.NEEDS_TASK_queue.insert(0, task_id)
        self.taskManager()
        # print self.name, 'new_Cur_task =', self.returnCurTaskStr(self.task_id_being_exec)     # debug

    def removeNeedsTask(self, task_id):
        # print('---remove NT', self.name, self.returnCurTaskStr(task_id)                        # debug
        self.NEEDS_TASK_queue.remove(task_id)
        self.taskManager()
        # print self.name, 'new_Cur_task =', self.returnCurTaskStr(self.task_id_being_exec)     # debug

    def sensorium(self, asteroid_list, mineral_list, container_list):
        self.see_ASTEROID = False
        self.see_CONTAINER = False
        self.see_MINERAL = False

        visible_asteroid_with_distance_tuples = []
        visible_container_with_distance_tuples = []
        visible_mineral_with_distance_tuples = []

        for a in asteroid_list:
            ship_asteroid_dist = lengthBetweenPoints(
                (self.points.center[0], self.points.center[1]),
                (a.points.center[0], a.points.center[1]),
            )
            if ship_asteroid_dist <= self.radius:
                visible_asteroid_with_distance_tuples.append((a, ship_asteroid_dist))
                self.see_ASTEROID = True

        for c in container_list:
            ship_container_dist = lengthBetweenPoints(
                (self.points.center[0], self.points.center[1]),
                (c.points.center[0], c.points.center[1]),
            )
            if ship_container_dist <= self.radius:
                visible_container_with_distance_tuples.append((c, ship_container_dist))
                self.see_CONTAINER = True
                # print self.name, 'CONTAINEEEEEEER'

        for m in mineral_list:
            ship_mineral_dist = lengthBetweenPoints(
                (self.points.center[0], self.points.center[1]),
                (m.points.center[0], m.points.center[1]),
            )
            if ship_mineral_dist <= self.radius:
                visible_mineral_with_distance_tuples.append((m, ship_mineral_dist))
                self.see_MINERAL = True
                # print self.name, 'MINERAAAAAAAAAAAAAl'

        # sorting lists to find which one object is closer
        # will be repleaced by finding min dist, sort is too heavy
        self.visible_asteroid_with_distance_tuples = sorted(
            visible_asteroid_with_distance_tuples, key=itemgetter(1)
        )
        self.visible_container_with_distance_tuples = sorted(
            visible_container_with_distance_tuples, key=itemgetter(1)
        )
        self.visible_mineral_with_distance_tuples = sorted(
            visible_mineral_with_distance_tuples, key=itemgetter(1)
        )

    def thinkInSpaceRace0(self):
        ##########################################################
        if self.race != RACE_6_ID and self.race != RACE_7_ID:  # DEPR
            if (
                len(self.QUEST_TASK_queue) == 0
            ):  # and len(self.NEEDS_TASK_queue) == 0:      # DEPR
                self.questManager()
        ##########################################################

        # ASTEROID AWARNESS
        if self.see_ASTEROID == True:
            if randint(1, 2) == 1:
                (a, ship_asteroid_dist) = self.visible_asteroid_with_distance_tuples[0]
                self.setSingleSurgicalWeaponTarget(a)

        # SELFPRESERVATION MANAGER
        if self.subtype != WARRIOR_ID:
            if self.korpus.armor < 0.1 * self.korpus.armor_max:
                if self.repair_NEEDED == False:
                    self.landing_reason_id_list.append(REPAIR_NEEDED_id)
                    self.repair_NEEDED = True

        # HYPER-JUMP MANAGER
        if self.quest_ob != None:
            if self.starsystem != self.quest_ob.starsystem:
                if (
                    self.task_id_being_exec != LANDING_task_id
                    and self.task_id_being_exec != HYPER_JUMP_task_id
                ):
                    self.insertNeedsTask(HYPER_JUMP_task_id)

        # LANDING MANAGER
        if len(self.landing_reason_id_list) != 0:
            if (
                self.task_id_being_exec != LANDING_task_id
                and self.task_id_being_exec != HYPER_JUMP_task_id
            ):
                # self.insertNeedsTask(LANDING_task_id)
                pass

        # GRABBING MANAGER
        if (
            self.task_id_being_exec != LANDING_task_id
            and self.task_id_being_exec != HYPER_JUMP_task_id
        ):
            if self.subtype == TRADER_ID or self.type == PIRAT_ID:
                if self.ableTo_GRAB == True:
                    if self.see_CONTAINER == True:
                        if GRABBING_CONTAINER_task_id not in self.NEEDS_TASK_queue:
                            self.insertNeedsTask(GRABBING_CONTAINER_task_id)
                    else:
                        if GRABBING_CONTAINER_task_id in self.NEEDS_TASK_queue:
                            self.removeNeedsTask(GRABBING_CONTAINER_task_id)

                    if self.see_MINERAL == True and self.see_CONTAINER == False:
                        if GRABBING_MINERAL_task_id not in self.NEEDS_TASK_queue:
                            self.insertNeedsTask(GRABBING_MINERAL_task_id)
                    else:
                        if GRABBING_MINERAL_task_id in self.NEEDS_TASK_queue:
                            self.removeNeedsTask(GRABBING_MINERAL_task_id)

                else:  # remove apropriate grab task if ship not able to grab
                    if GRABBING_MINERAL_task_id in self.NEEDS_TASK_queue:
                        self.removeNeedsTask(GRABBING_MINERAL_task_id)
                    if GRABBING_CONTAINER_task_id in self.NEEDS_TASK_queue:
                        self.removeNeedsTask(GRABBING_CONTAINER_task_id)

    def thinkInSpaceRace1(self):
        self.thinkInSpaceRace0()

    def thinkInSpaceRace2(self):
        self.thinkInSpaceRace0()

    def thinkInSpaceRace3(self):
        self.thinkInSpaceRace0()

    def thinkInSpaceRace4(self):
        self.thinkInSpaceRace0()

    def thinkInSpaceRace6(self):
        self.thinkInSpaceRace7()

    def thinkInSpaceRace7(self):
        for k in self.starsystem.SHIP_list:
            if k.race != self.race:
                self.setTargetPosToObCoord(k)
                self.setWeaponsToTarget(k)
                break

    def questManager(self):
        """
        if self.subtype == RANGER_ID:
           if self.subsubtype == WARRIOR_ID:
              self.starsystemLiberationQuestGenerator()

           elif self.subsubtype == PIRAT_ID:
                self.terrorShipQuestGenerator()

           elif self.subsubtype == TRADER_ID:
                self.quest_id = TRADE_GOODS_quest_id

           elif self.subsubtype == DIPLOMAT_ID:
                self.quest_id = DIPLOMACY_VISIT_quest_id

        elif self.subtype == WARRIOR_ID:
             if randint(1,2) == 1:
                self.arestShipQuestGenerator()
             else:
                self.starsystemLiberationQuestGenerator()

        elif self.subtype == PIRAT_ID:
             self.terrorShipQuestGenerator()

        elif self.subtype == TRADER_ID:
             self.quest_id = TRADE_GOODS_quest_id

        elif self.subtype == DIPLOMAT_ID:
             self.quest_id = DIPLOMACY_VISIT_quest_id
        """
        self.starsystemLiberationQuestGenerator()
        # pass

    def starsystemLiberationQuestGenerator(self):
        self.quest_ob = self.starsystem.returnClosestCapturedSs()  # main quest ob
        if self.quest_ob != None:
            print self.name, "have got starsystemLiberationQuestGenerator"
            self.quest_id = STARSYSTEM_LIBERATION_quest_id

            self.quest_target_starsystem = self.quest_ob
            self.target_starsystem = self.quest_target_starsystem

            self.insertQuestTask(DESTROY_ALIEN_task_id)  # improove
        else:
            self.quest_id = None
            self.QUEST_TASK_queue = []

    def arestShipQuestGenerator(self):
        self.quest_ob = self.starsystem.returnPirat()  # main quest ob
        if self.quest_ob != None:
            self.quest_id = AREST_SHIP_quest_id
            # self.QUEST_TASK_queue = [AREST_REQUEST_task_id, FIRE_LOW_task_id, FIRE_HIGH_task_id]

            self.FOLLOW_QUEST_OB = False
            self.quest_target_ship = self.quest_ob
            self.quest_target_planet = None
            self.quest_target_starsystem = None
            self.ob_to_follow = self.quest_ob  # can be changed during one quest
        else:
            self.quest_id = None
            self.QUEST_TASK_queue = []

    def terrorShipQuestGenerator(self):
        self.quest_ob = self.starsystem.returnTrader()  # main quest ob
        if self.quest_ob != None:
            self.quest_id = TERROR_SHIP_quest_id
            # self.QUEST_TASK_queue = [TERROR_REQUEST_task_id, FIRE_LOW_task_id, FIRE_HIGH_task_id]

            self.FOLLOW_QUEST_OB = False
            self.quest_target_ship = self.quest_ob
            self.quest_target_planet = None
            self.quest_target_starsystem = None
            self.ob_to_follow = self.quest_ob  # can be changed during one quest
        else:
            self.quest_id = None
            self.QUEST_TASK_queue = []

    #    elif self.quest_id == TRADE_GOODS_quest_id:
    #         self.QUEST_TASK_queue = [LANDING_task_id, BUY_GOODS_task_id, FIND_PLACE_TO_SELL_GOODS_task_id, LAUNCING_task_id, HYPER_JUMP_task_id, LANDING_task_id, SELL_GOODS_task_id]

    #    elif self.quest_id == DIPLOMACY_VISIT_quest_id:
    #         self.QUEST_TASK_queue = [SELFPRESERVATION_task_id]

    def taskManager(self):
        self.task_id_being_exec = None
        self.taskExecution_inDynamic = self.doNothing
        self.taskExecution_inStatic = self.doNothing

        if len(self.NEEDS_TASK_queue) != 0:
            (
                self.taskExecution_inDynamic,
                self.taskExecution_inStatic,
            ) = self.initAndReturnNeedsExecutionFunction()
        elif len(self.QUEST_TASK_queue) != 0:
            (
                self.taskExecution_inDYnamic,
                self.taskExecution_inStatic,
            ) = self.initAndReturnQuestExecutionFunction()

    def initAndReturnQuestExecutionFunction(self):
        self.task_id_being_exec = self.QUEST_TASK_queue[0]

        if self.task_id_being_exec == DESTROY_ALIEN_task_id:
            self.destroyAlienTaskInit()
            return (
                self.destroyAlienTaskExecution_inDynamic,
                self.destroyAlienTaskExecution_inStatic,
            )

        elif self.task_id_being_exec == AREST_REQUEST_task_id:
            self.arestRequestTaskInit()
            return (
                self.arestRequestTaskExecution_inDynamic,
                self.arestRequestTaskExecution_inStatic,
            )

        elif self.task_id_being_exec == TERROR_REQUEST_task_id:
            self.terrorRequestTaskInit()
            return (
                self.terrorRequestTaskExecution_inDynamic,
                self.terrorRequestTaskExecution_inStatic,
            )

        elif self.task_id_being_exec == FIRE_LOW_task_id:
            self.fireLowTaskInit()
            return (
                self.fireLowTaskExecution_inDynamic,
                self.fireLowTaskExecution_inStatic,
            )

        elif self.task_id_being_exec == FIRE_HIGH_task_id:
            self.fireHighTaskInit()
            return (
                self.fireHighTaskExecution_inDynamic,
                self.fireHighTaskExecution_inStatic,
            )

        # print('===set active', self.name, self.returnCurTaskStr(self.task_id_being_exec)

    def initAndReturnNeedsExecutionFunction(self):
        self.task_id_being_exec = self.NEEDS_TASK_queue[0]

        if self.task_id_being_exec == HYPER_JUMP_task_id:
            self.hyperJumpTaskInit()
            return (
                self.hyperJumpTaskExecution_inDynamic,
                self.hyperJumpTaskExecution_inStatic,
            )

        elif self.task_id_being_exec == LANDING_task_id:
            self.landingTaskInit()
            return (
                self.landingTaskExecution_inDynamic,
                self.landingTaskExecution_inStatic,
            )

        elif self.task_id_being_exec == LAUNCHING_task_id:
            self.launchingTaskInit()
            return (
                self.launchingTaskExecution_inDynamic,
                self.launchingTaskExecution_inStatic,
            )

        elif self.task_id_being_exec == GRABBING_MINERAL_task_id:
            self.grabbingMineralTaskInit()
            return (
                self.grabbingTaskExecution_inDynamic,
                self.grabbingTaskExecution_inStatic,
            )

        elif self.task_id_being_exec == GRABBING_CONTAINER_task_id:
            self.grabbingContainerTaskInit()
            return (
                self.grabbingTaskExecution_inDynamic,
                self.grabbingTaskExecution_inStatic,
            )

        # print('===set active', self.name, self.returnCurTaskStr(self.task_id_being_exec)

    # *********** DESTROY_ALIEN_task_id *****
    def destroyAlienTaskInit(self):
        pass

    def destroyAlienTaskExecution_inDynamic(self):
        pass

    def destroyAlienTaskExecution_inStatic(self):
        if self.target_ship == None:
            self.findAlienShip()
        else:
            self.setWeaponsToTarget(self.target_ship)
            self.calculateWayToCoord(
                (self.target_ship.points.center[0], self.target_ship.points.center[1])
            )

    def findAlienShip(self):
        self.target_ship = None
        for k in self.starsystem.SHIP_list:
            if k.race == RACE_6_ID or k.race == RACE_7_ID:
                self.target_ship = k
                return True

    # *********** FIRE_HIGH_task_id *****
    def fireHighTaskInit(self):
        pass

    def fireHighTaskExecution_inDynamic(self):
        pass

    def fireHighTaskExecution_inStatic(self):
        pass

    # *********** HYPER JUMP ***********
    def hyperJumpTaskInit(self):
        self.hyperJumpPreparation(self.target_starsystem)  # improve to check ss

        self.calculateWayToCoord((self.jump_pos_x, self.jump_pos_y))

        # self.functions_inDynamic_queue = [self.navigateHyperJumpPoint, self.hyperJumpInEffect, self.hyperJumpEvent, self.hyperJumpOutEffect, self.cleaningUpAfterHyperJump]
        self.functions_inDynamic_queue = [
            self.navigateHyperJumpPoint,
            self.hyperJumpEvent,
            self.cleaningUpAfterHyperJump,
        ]
        self.functions_inDynamic_remove_queue = []

    def hyperJumpTaskExecution_inDynamic(self):
        for f in self.functions_inDynamic_queue:
            if f():
                self.functions_inDynamic_remove_queue.append(f)
            else:
                break

        for f in self.functions_inDynamic_remove_queue:
            self.functions_inDynamic_queue.remove(f)
        self.functions_inDynamic_remove_queue = []

    def hyperJumpTaskExecution_inStatic(self):
        pass

    # def navigateHyperJumpPoint(self):          # see shipCommon.py

    # def hyperJumpInEffect(self):               # see shipCommon.py

    # def hyperJumpOutEffect(self):              # see shipCommon.py

    def cleaningUpAfterHyperJump(self):
        self.removeNeedsTask(HYPER_JUMP_task_id)
        self.target_starsystem = None

        ###TEXTURE_MANAGER.loadDynamicObTex(self)  # will see if it really needed
        return True

    # *********** LANDING ***********
    def landingTaskInit(self):
        self.target_planet = self.starsystem.returnClosestPlanet(self)  # improve

        # self.functions_inDynamic_queue = [self.checkLanding, self.fadeOutEffect, self.landingEvent]
        self.functions_inDynamic_queue = [self.checkLanding, self.landingEvent]
        self.functions_inDynamic_remove_queue = []

    def landingTaskExecution_inDynamic(self):
        for f in self.functions_inDynamic_queue:
            if f():
                self.functions_inDynamic_remove_queue.append(f)
            else:
                break

        for f in self.functions_inDynamic_remove_queue:
            self.functions_inDynamic_queue.remove(f)
        self.functions_inDynamic_remove_queue = []

    def landingTaskExecution_inStatic(self):
        self.calculateWayToCoord(
            (self.target_planet.points.center[0], self.target_planet.points.center[1])
        )  # refresh target coord because of planet movement

    # def checkLanding(self):               # see shipCommon.py

    # def fadeOutEffect(self):              # see shipCommon.py

    # def landingEvent(self):               # see shipCommon.py

    # *********** LAUNCHING ***********
    def launchingTaskInit(self):
        self.launchEvent()

    def launchingTaskExecution_inDynamic(self):
        if self.in_SPACE == True and self.fadeInEffect():
            self.removeNeedsTask(LAUNCHING_task_id)

    def launchingTaskExecution_inStatic(self):
        pass

    # def fadeInEffect(self):               # see shipCommon.py
    #    # effect when launching
    #    if self.alpha < 1.0:
    #       self.alpha += 0.1
    #       return False
    #    else:
    #       self.alpha = 1.0
    #       return True

    def arestRequestTaskExecution(self):
        self.removeQuestTask(AREST_REQUEST_task_id)

    def terrorRequestTaskExecution(self):
        self.removeQuestTask(TERROR_REQUEST_task_id)

    def fireLowTaskExecution(self):
        if self.setSingleSurgicalWeaponTarget(self.quest_ob):
            self.removeQuestTask(FIRE_LOW_task_id)
        else:
            self.setTargetPosToObCoord(self.quest_ob)

    def fireHighTaskExecution(self):
        self.setTargetPosToObCoord(self.quest_ob)
        self.setWeaponsToTarget(self.quest_ob)

    def thinkAtInhabitedPlanet(self):
        # for reason in self.landing_reason_id_list:    # debug
        #    print self.name, reason                   # debug
        if self.task_id_being_exec == LANDING_task_id:
            self.removeNeedsTask(LANDING_task_id)

        for reason in self.landing_reason_id_list:
            if reason == REPAIR_NEEDED_id:
                if self.buyRepair():
                    print self.name, "bought Repair"
                else:
                    self.dirtyWork()
                    print self.name, "do dirty work"

                if self.korpus.armor > 0.9 * self.korpus.armor_max:
                    self.landing_reason_id_list.remove(REPAIR_NEEDED_id)
                    self.repair_NEEDED = False

            if reason == SELL_NEEDED_id:
                print "Before ___ free_space/speed", int(
                    self.korpus.space - self.mass
                ), "/", self.speed  # debug
                for slot in self.korpus.otsec_slot_list:
                    if slot.item != None:
                        if slot.item.type == CONTAINER_ID:
                            if slot.item.item.type == GOODS_id:
                                earn_money = self.target_planet.kosmoport.shop.sell(
                                    slot.item.item
                                )
                                self.credits += earn_money

                                # print('+$', self.name, 'sold ', slot.item.item.returnTypeStr(), ', mass * price = earn ==>', slot.item.mass, ' * ', int(earn_money/slot.item.mass), ' = ', earn_money

                                slot.item = None
                self.sell_NEEDED = False

                self.updateDriveAbility()
                self.landing_reason_id_list.remove(SELL_NEEDED_id)
                print "After ___ free_space/speed", int(
                    self.korpus.space - self.mass
                ), "/", self.speed  # debug

            """
            elif self.task_id_being_exec == FIND_PLACE_TO_SELL_GOODS_task_id:
                 if self.task_init_FINISHED == False:
                    self.task_init_FINISHED = True
                 else:
                    pass

            elif self.task_id_being_exec == BUY_GOODS_task_id:
                 if self.task_init_FINISHED == False:
                    self.task_init_FINISHED = True
                 else:
                    pass

            elif self.task_id_being_exec == SELL_GOODS_task_id:
                 if self.task_init_FINISHED == False:
                    self.task_init_FINISHED = True
                 else:
                    pass
            """

        if (
            len(self.landing_reason_id_list) == 0
            and self.task_id_being_exec != LAUNCHING_task_id
        ):
            # print('___________', self.name, 'deside there is no reason to stay at Inhabitedplanet'
            self.insertNeedsTask(LAUNCHING_task_id)

    def thinkAtUninhabitedPlanet(self):
        for reason in self.landing_reason_id_list:
            if reason == REPAIR_NEEDED_id:
                self.dirtyWork()
                print self.name, "do dirty work on uninhabited land"

                if self.korpus.armor > 0.9 * self.korpus.armor_max:
                    self.landing_reason_id_list.remove(REPAIR_NEEDED_id)
                    self.repair_NEEDED = False

        if (
            len(self.landing_reason_id_list) == 0
            and self.task_id_being_exec != LAUNCHING_task_id
        ):
            # print('___________', self.name, 'deside there is no reason to stay at Uninhabitedplanet'
            self.insertNeedsTask(LAUNCHING_task_id)

    def setSingleSurgicalWeaponTarget(self, target):
        ship_target_dist = lengthBetweenPoints(
            (self.points.center[0], self.points.center[1]),
            (target.points.center[0], target.points.center[1]),
        )
        for w_slot in self.armed_weapon_slot_list:
            if w_slot.item.subtype == LAZER_ID:
                if ship_target_dist <= w_slot.item.radius:
                    w_slot.target = target
                    return True
        return False

    def setTargetPosToObCoord(self, k):
        vector_len = randint(int(0.75 * self.w), int(2 * self.w))
        alfa = randint(0, 360) / 57.0

        dx = sin(alfa) * vector_len
        dy = cos(alfa) * vector_len

        self.setTargetPosCoord((k.points.center[0] + dx, k.points.center[1] + dy))

    def grabbingContainerTaskInit(self):
        for tuple in self.visible_container_with_distance_tuples:
            (c, dist) = tuple
            if c.mass < self.korpus.grapple_slot.item.strength:
                self.grapping_main_target = c
                self.calculateWayToCoord(
                    (c.points.center[0] - 10, c.points.center[1] - 10)
                )
                break

    def grabbingMineralTaskInit(self):
        for tuple in self.visible_mineral_with_distance_tuples:
            (m, dist) = tuple
            if m.mass < self.korpus.grapple_slot.item.strength:
                self.grapping_main_target = m
                self.calculateWayToCoord(
                    (m.points.center[0] - 10, m.points.center[1] - 10)
                )
                break

    def grabbingTaskExecution_inDynamic(self):
        # this updating must be performed slow --> optimization
        if self.ableTo_GRAB == True:

            self.checkGrabQueue()
            self.grabExecution()
            self.grappleRemoveQueueManager()

    def checkGrabTaskCondition(self):
        if self.grapping_main_target != None:
            if (
                self.grapping_main_target.alive == False
                or self.grapping_main_target.in_SPACE == False
            ):
                self.grapping_main_target = None

        if self.task_id_being_exec == GRABBING_MINERAL_task_id:
            if len(self.korpus.grapple_slot.item.grapple_list) == 0:
                self.grapping_main_target = None
                self.removeNeedsTask(GRABBING_MINERAL_task_id)
        elif self.task_id_being_exec == GRABBING_CONTAINER_task_id:
            if len(self.korpus.grapple_slot.item.grapple_list) == 0:
                self.grapping_main_target = None
                self.removeNeedsTask(GRABBING_CONTAINER_task_id)

    def checkAndIfOKAddItemToGrabQueue(self, item):
        # in Static
        ship_item_dist = lengthBetweenPoints(
            (self.points.center[0], self.points.center[1]),
            (item.points.center[0], item.points.center[1]),
        )
        if ship_item_dist < self.korpus.grapple_slot.item.radius:
            self.addToGrappleTargetList(item)

    def grabbingTaskExecution_inStatic(self):
        # bug: improove to avoid add dublicated items to grapple list
        if self.ableTo_GRAB == True:
            if self.grapping_main_target != None:
                self.checkAndIfOKAddItemToGrabQueue(self.grapping_main_target)
                if self.see_CONTAINER == True:
                    for (c, dist) in self.visible_container_with_distance_tuples:
                        if (
                            len(self.korpus.grapple_slot.item.grapple_list)
                            == self.korpus.grapple_slot.item.maxNumItem
                        ):
                            break
                        self.checkAndIfOKAddItemToGrabQueue(c)
                else:
                    for (m, dist) in self.visible_mineral_with_distance_tuples:
                        if (
                            len(self.korpus.grapple_slot.item.grapple_list)
                            == self.korpus.grapple_slot.item.maxNumItem
                        ):
                            break
                        self.checkAndIfOKAddItemToGrabQueue(m)

        self.checkGrabTaskCondition()
        self.analizeWhatToDoWithNewStuff()  # (improove)

    def analizeWhatToDoWithNewStuff(self):
        for slot in self.korpus.otsec_slot_list:
            if slot.item != None and slot.item.type == CONTAINER_ID:
                if slot.item.item.subtype == MINERAL_id:
                    if slot.item.mass > 1:
                        self.landing_reason_id_list.append(SELL_NEEDED_id)
                        self.sell_NEEDED = True
