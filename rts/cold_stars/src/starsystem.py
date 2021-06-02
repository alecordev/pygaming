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

from playerCreation import player
from ships import *


class starSystemManager:
    def __init__(self, ss_new):
        self.hSTARSYSTEM_list = [ss for ss in global_STARSYSTEM_list if ss != ss_new]

        self.ss_active = ss_new
        player.starsystem = ss_new
        player.starsystem.appendShipToStarsystem(player)

        self.ss_active.initOrbits()
        TEXTURE_MANAGER.loadAllTexturesInStarsystem(ss_new)

        if OLD_HARDWARE == True:
            ss_new.renderEntities = ss_new.renderEntities_OLD
        else:
            ss_new.renderEntities = ss_new.renderEntities_NEW

    def swap(self, ss_old, ss_new):
        # for ss in self.hSTARSYSTEM_list:
        #    # print('hidden starsystem', ss.name
        self.hSTARSYSTEM_list.append(ss_old)
        self.hSTARSYSTEM_list.remove(ss_new)

        ss_old.clearOrbits()
        ss_new.initOrbits()
        TEXTURE_MANAGER.loadAllTexturesInStarsystem(ss_new)

        if OLD_HARDWARE == True:
            ss_new.renderEntities = ss_new.renderEntities_OLD
        else:
            ss_new.renderEntities = ss_new.renderEntities_NEW


class starSystemInstance:
    def __init__(self, name):

        self.ID = ENTITY_ID_GENERATOR.returnNextID()
        self.CAPTURED = False

        self.screen_QUAKE_runtime_counter = -1
        self.screen_QUAKE_amlitudaDiv2 = 0

        self.name = name
        self.rectOnMap = None  # implement point sprites here
        self.star = None
        self.starsystem = self

        self.red, self.green, self.blue = None, None, None

        self.STAR_list = []
        self.PLANET_list = []

        self.SPUTNIK_list = []
        self.SPUTNIK_remove_queue = []

        self.ASTEROID_list = []
        self.ASTEROID_remove_queue = []

        self.MINERAL_list = []
        self.MINERAL_remove_queue = []

        self.CONTAINER_list = []
        self.CONTAINER_remove_queue = []

        self.BOMB_list = []
        self.BOMB_remove_queue = []

        self.ROCKET_list = []
        self.ROCKET_remove_queue = []

        self.SHIP_list = []
        self.SHIP_remove_queue = []

        self.SHIP_WARRIOR_list = []
        self.SHIP_PIRAT_list = []
        self.SHIP_TRADER_list = []
        self.SHIP_DIPLOMAT_list = []

        self.SHIP_LANDED_PORT_list = []
        self.SHIP_LANDED_LAND_list = []

        # self.SHIP_HYPER_JUMP_queue = []
        # self.SHIP_HYPER_IN_EFFECT_list = []
        # self.SHIP_HYPER_OUT_EFFECT_list = []

        self.BLACKHOLE_list = []

        ### EFFECT lists section
        self.effect_LAZER_list = []
        self.effect_LAZER_remove_queue = []

        self.effect_EXPLOSION_list = []
        self.effect_EXPLOSION_remove_queue = []

        self.effect_DAMAGE_list = []
        self.effect_DAMAGE_remove_queue = []

        self.effect_SHOCKWAVE_list = []
        self.effect_SHOCKWAVE_remove_queue = []
        ### EFFECT lists section

        ### lists for rendering
        self.visible_STAR_list = []
        self.visible_PLANET_list = []

        self.visible_SPUTNIK_list = []
        self.visible_ASTEROID_list = []

        self.visible_CONTAINER_list = []
        self.visible_MINERAL_list = []
        self.visible_BOMB_list = []

        self.visible_SHIP_list = []

        self.visible_ROCKET_list = []

        self.visible_effect_LAZER_list = []
        self.visible_effect_EXPLOSION_list = []
        self.visible_effect_DAMAGE_list = []

        self.visible_BLACKHOLE_list = []
        ##############################################################################################
        self.locked_items_list = []

        self.asteroid_ID = 0

        mixer.music.play(-1)
        mixer.music.set_volume(0.3)
        mixer.music.set_volume(0.0)

        # self.particleSystem_list = []
        # self.particleSystem_remove_queue = []

    def initOrbits(self):
        for p in self.PLANET_list:
            p.detailedOrbitFormation()
            p.update(1)
            # if p.satellite != None:
            #   p.satellite.detaliedSatelliteOrbitFormation()
            #   p.satellite.update(1)

    def clearOrbits(self):
        for p in self.PLANET_list:
            p.orbit_list_x = []
            p.orbit_list_y = []

    def updatelabelPos(self):
        self.label_pos_x = self.rectOnMap.centerx - len(self.name) * LETTER_WIDTH / 2
        self.label_pos_y = self.rectOnMap[1] - TEXT_OFFSET

    def shipWeaponsReload(self):
        # perfoming only once each turn
        # player.weaponsReload()

        for k in self.SHIP_list:  # allow ships to fire next turn
            k.weaponsReload()

    def starImpact(self):
        # performs once per turn
        xc = self.star.points.center[0]
        yc = self.star.points.center[1]
        radius = 1.2 * self.star.w

        # if player.alive == True:
        #   dist = lengthBetweenPoints((xc, yc), (player.points.center[0], player.points.center[1]))
        #   player.dist2star_rate = float(radius)/(dist+0.00001)
        #   player.temperature += player.dist2star_rate
        #   player.energy_restoration_rate = 1 + player.dist2star_rate
        #   if player.dist2star_rate > 1:
        #      player.hit(self.star, self.star, player.dist2star_rate)

        for k in self.SHIP_list:
            dist = lengthBetweenPoints(
                (xc, yc), (k.points.center[0], k.points.center[1])
            )
            k.dist2star_rate = float(radius) / (dist + 0.00001)
            k.temperature += k.dist2star_rate
            k.energy_restoration_rate = 1 + k.dist2star_rate
            if k.dist2star_rate > 1:
                k.hit(self.star, self.star, k.dist2star_rate)

    def temperatureInfluenceEntities(self):
        # performs once per turn
        # if player.alive == True:
        #   player.temperatureInfluence()

        for k in self.SHIP_list:
            k.temperatureInfluence()

    def bombExplosionCollision(self, bomb):
        # performs once when accident happens
        xc = bomb.points.center[0]
        yc = bomb.points.center[1]

        # dist = lengthBetweenPoints((xc, yc), (player.points.center[0], player.points.center[1]))
        # dist_rate = float(bomb.radius)/(dist+0.00001)
        # if dist_rate > 1:
        #   player.hit(bomb.owner, bomb, dist_rate)

        for k in self.SHIP_list:
            dist = lengthBetweenPoints(
                (xc, yc), (k.points.center[0], k.points.center[1])
            )
            dist_rate = float(bomb.radius) / (dist + 0.00001)
            if dist_rate > 1:
                k.hit(bomb.owner, bomb, dist_rate)

        for a in self.ASTEROID_list:
            dist = lengthBetweenPoints(
                (xc, yc), (a.points.center[0], a.points.center[1])
            )
            dist_rate = float(bomb.radius) / (dist + 0.00001)
            if dist_rate > 1:
                a.hit(bomb, bomb)

        for b in self.BOMB_list:
            # if b.ID != bomb.ID:
            dist = lengthBetweenPoints(
                (xc, yc), (b.points.center[0], b.points.center[1])
            )
            dist_rate = float(bomb.radius) / (dist + 0.00001)
            if dist_rate > 1:
                b.hit(bomb, bomb)

    def asteroidAutoGenerator(self, timer, max_num):
        if timer < 0:
            if len(self.ASTEROID_list) < max_num:
                texOb = returnRandomFromTheList(TEXTURE_MANAGER.asteroid_texOb_list)
                a = AsteroidInstance(texOb, self)
                self.ASTEROID_list.append(a)
                # print "Asteroid a_%i instance was created. Total asteroids num ="%self.asteroid_ID, len(self.ASTEROID_list)

    def blackholeAutoGenerator(self, timer, max_num):
        if timer < 0:
            if len(self.BLACKHOLE_list) < max_num:
                texOb = returnRandomFromTheList(TEXTURE_MANAGER.blackhole_texOb_list)
                bh = BlackHoleInstance(
                    "blackhole", texOb, self, randint(-2000, 2000), randint(-2000, 2000)
                )
                self.BLACKHOLE_list.append(bh)

    def mineralAutoGenerator(self, timer, max_num):
        ### DEBUG
        while len(self.MINERAL_list) < max_num:
            texOb = returnRandomFromTheList(TEXTURE_MANAGER.mineral_texOb_list)
            m = MineralInstance(
                texOb,
                self,
                randint(100, 300),
                randint(100, 300),
                randint(100, 300),
                randint(100, 300),
            )
            self.MINERAL_list.append(m)

    def addNumMinerals(self, x, y, num):
        alpha = randint(0, 360) / 57.0
        d_alpha = 3.14 / float(num)
        i = 0
        while i < num:
            _len = randint(60, 100)
            target_x = x + sin(alpha) * _len
            target_y = y + cos(alpha) * _len
            texOb = returnRandomFromTheList(TEXTURE_MANAGER.mineral_texOb_list)
            self.MINERAL_list.append(
                MineralInstance(texOb, self, x, y, target_x, target_y)
            )
            alpha += d_alpha
            i += 1

    def addContainers(self, x, y, item_drop_queue):  # move to ship class
        alpha = randint(0, 360) / 57.0
        d_alpha = 3.14 / float(len(item_drop_queue))
        i = 0
        while i < len(item_drop_queue):
            _len = randint(60, 100)
            target_x = x + sin(alpha) * _len
            target_y = y + cos(alpha) * _len
            texOb = TEXTURE_MANAGER.container_texOb_list[0]
            self.CONTAINER_list.append(
                Container(texOb, item_drop_queue[i], self, x, y, target_x, target_y)
            )
            alpha += d_alpha
            i += 1

    # def sputnikAutoGenerator(self, timer):   # move to planet
    # SPUTNIK_list = []
    ##for sp in SPUTNIK_list:
    ##SPUTNIK_list.append(sp)

    # for P in self.PLANET_list:
    # if P.sputnik_PRESENT == False:
    # sputnik_rand_index = randint(0, len(SPUTNIK_list) - 1)
    ###print SPUTNIK_list
    ###SP = sp_000
    # SP = SPUTNIK_list[sputnik_rand_index]
    # SP.starsystem = self
    ##SP = SPUTNIK_list[1]
    # SP.companion = P
    # SP.init()
    # self.SPUTNIK_list.append(SP)
    # P.sputnik_PRESENT = True

    def updateEntities(self, timer):
        # if timer > 0:
        # if timer < 0:

        for k in self.SHIP_list:
            k.update(timer)

        for le in self.effect_LAZER_list:
            le.update(timer)

        for p in self.PLANET_list:
            p.update(timer)

        for a in self.ASTEROID_list:
            a.update(timer)

        for m in self.MINERAL_list:
            m.update(timer)

        for r in self.ROCKET_list:
            r.update(timer)

        for bh in self.BLACKHOLE_list:
            bh.update(timer)

        for s in self.STAR_list:
            s.update(timer)
        for sp in self.SPUTNIK_list:
            sp.update(timer)
        for c in self.CONTAINER_list:
            c.update(timer)
        for b in self.BOMB_list:
            b.update(timer)

    def updateHiddenEntities(self, timer):
        for p in self.PLANET_list:
            p.updateHidden(timer)

        for sp in self.SPUTNIK_list:
            sp.updateHidden(timer)

        for k in self.SHIP_list:
            k.updateHidden(timer)

    # def launchShips(self):
    ## performs within game loop
    # for k in self.SHIP_LAUNCH_queue:
    # k.launch()
    # self.SHIP_LAUNCH_EFFECT_list.append(k)

    # for k in self.SHIP_LAUNCH_EFFECT_list:
    # if k.fadeInEffect():
    # self.SHIP_LAUNCH_EFFECT_list.remove(k)

    def checkShipHyperJumping(self):
        # performs within game loop
        for k in self.SHIP_HYPER_JUMP_queue:
            if k.checkHyperJump():
                self.SHIP_HYPER_JUMP_queue.remove(k)
                self.SHIP_HYPER_IN_EFFECT_list.append(k)

        for k in self.SHIP_HYPER_IN_EFFECT_list:
            k.fadeOutEffect()
            if k.hyperJumpInEffect():
                self.SHIP_HYPER_IN_EFFECT_list.remove(k)
                k.hyperJump()
                k.starsystem.SHIP_HYPER_OUT_EFFECT_list.append(k)

        for k in self.SHIP_HYPER_OUT_EFFECT_list:
            k.fadeInEffect()
            if k.hyperJumpOutEffect():
                self.SHIP_HYPER_OUT_EFFECT_list.remove(k)

    def asteroidCollision(self):
        # performs in  game loop
        collide = False
        for a in self.ASTEROID_list:
            for k in self.SHIP_list:
                if collisionBetweenCenters(
                    a.points.center, k.points.center, k.collision_threshold
                ):
                    k.hit(a, a)
                    a.hit(a, a)
                    collide = True
                    break

            if collide == False:
                for sp in self.SPUTNIK_list:
                    if collisionBetweenCenters(
                        a.points.center, sp.points.cente, sp.collision_threshold
                    ):
                        sp.hit(a, a)
                        a.hit(a, a)
                        collide = True
                        break

            if collide == False:
                for s in self.STAR_list:
                    if collisionBetweenCenters(
                        a.points.center, s.points.center, s.collision_threshold
                    ):
                        a.hit(a, a)
                        collide = True
                        break

            if collide == False:
                for p in self.PLANET_list:
                    if collisionBetweenCenters(
                        a.points.center, p.points.center, p.collision_threshold
                    ):
                        a.hit(a, a)
                        collide = True
                        break

    def rocketCollision(self):
        collide = False
        for r in self.ROCKET_list:
            for k in self.SHIP_list:
                if r.owner.ID != k.ID:
                    if collisionBetweenCenters(
                        r.points.center, k.points.center, k.collision_threshold
                    ):
                        k.hit(r.owner, r)
                        r.hit(r.owner, r)
                        collide = True
                        break

            if collide == False:
                for a in self.ASTEROID_list:
                    if collisionBetweenCenters(
                        r.points.center, a.points.center, a.collision_threshold
                    ):
                        a.hit(r.owner, r)
                        r.hit(r.owner, r)
                        collide = True
                        break

            if collide == False:
                for m in self.MINERAL_list:
                    if collisionBetweenCenters(
                        r.points.center, m.points.center, m.collision_threshold
                    ):
                        m.hit(r.owner, r)
                        r.hit(r.owner, r)
                        collide = True
                        break

            if collide == False:
                for sp in self.SPUTNIK_list:
                    if collisionBetweenCenters(
                        r.points.center, sp.points.center, sp.collision_threshold
                    ):
                        sp.hit(r.owner, r)
                        r.hit(r.owner, r)
                        collide = True
                        break

            if collide == False:
                for c in self.CONTAINER_list:
                    if collisionBetweenCenters(
                        r.points.center, c.points.center, c.collision_threshold
                    ):
                        c.hit(r.owner, r)
                        r.hit(r.owner, r)
                        collide = True
                        break

            if collide == False:
                for b in self.BOMB_list:
                    if collisionBetweenCenters(
                        r.points.center, b.points.center, b.collision_threshold
                    ):
                        b.hit(r.owner, r)
                        r.hit(r.owner, r)
                        collide = True
                        break

    def aiSimulation(self):
        # once per turn
        for k in self.SHIP_list:
            k.sensorium(self.ASTEROID_list, self.MINERAL_list, self.CONTAINER_list)
            k.thinkInSpace()
            k.taskExecution_inStatic()

        for k in self.SHIP_LANDED_PORT_list:
            k.thinkAtInhabitedPlanet()
            k.taskExecution_inStatic()

        for k in self.SHIP_LANDED_LAND_list:
            k.thinkAtUninhabitedPlanet()
            k.taskExecution_inStatic()

    def mouseInteraction(
        self,
        timer,
        mx,
        my,
        vpCoordinate_x,
        vpCoordinate_y,
        slot_1_SELECTED,
        slot_2_SELECTED,
        slot_3_SELECTED,
        slot_4_SELECTED,
        slot_5_SELECTED,
        show_RADAR,
        grapple_SELECTED,
        lb,
        rb,
    ):
        CURSOR_INTERSECT_OBJECT = False

        mxvp = mx + vpCoordinate_x
        myvp = my + vpCoordinate_y

        # for r in self.ROCKET_list:
        #    r.updateDebugWay(timer, mxvp, myvp)

        player_cursor_dist = lengthBetweenPoints(
            (player.points.center[0], player.points.center[1]), (mxvp, myvp)
        )
        if player_cursor_dist < player.points.w / 4.0:
            CURSOR_INTERSECT_OBJECT = True
            player.renderInfo()

            if lb == True:
                player.in_INVERTAR = True

        #####################################################################################################
        if CURSOR_INTERSECT_OBJECT != True:
            for k in self.visible_SHIP_list:
                ship_cursor_dist = lengthBetweenPoints(
                    (k.points.center[0], k.points.center[1]), (mxvp, myvp)
                )
                if ship_cursor_dist < player.points.w / 4.0:
                    CURSOR_INTERSECT_OBJECT = True
                    k.renderInfo()
                    k.calculateWayVisualisation()
                    k.renderDirection()

                    if lb == True:
                        player.setWeaponsToTarget(
                            k,
                            (
                                slot_1_SELECTED,
                                slot_2_SELECTED,
                                slot_3_SELECTED,
                                slot_4_SELECTED,
                                slot_5_SELECTED,
                            ),
                        )

                    elif rb == True:
                        if player.korpus.scaner_slot.item != None:
                            player.korpus.scaner_slot.item.deterioration()
                            if player.korpus.scaner_slot.item.scan > k.protection:
                                player.is_SCANNING = True
                                player.scanned_ob = k
                    break

        ####################################################################################################

        ####################################################################################################
        if CURSOR_INTERSECT_OBJECT != True:
            for sp in self.visible_SPUTNIK_list:
                sputnik_cursor_dist = lengthBetweenPoints(
                    (sp.points.center[0], sp.points.center[1]), (mxvp, myvp)
                )
                if sputnik_cursor_dist < sp.w / 4:
                    CURSOR_INTERSECT_OBJECT = True
                    sp.renderInfo()

                    if lb == True:
                        player.setWeaponsToTarget(
                            sp,
                            (
                                slot_1_SELECTED,
                                slot_2_SELECTED,
                                slot_3_SELECTED,
                                slot_4_SELECTED,
                                slot_5_SELECTED,
                            ),
                        )
        ####################################################################################################

        ####################################################################################################
        if CURSOR_INTERSECT_OBJECT != True:
            for a in self.visible_ASTEROID_list:
                asteroid_cursor_dist = lengthBetweenPoints(
                    (a.points.center[0], a.points.center[1]), (mxvp, myvp)
                )
                if asteroid_cursor_dist < a.w / 3:
                    CURSOR_INTERSECT_OBJECT = True
                    a.renderInfo()
                    a.renderDirection()

                    if lb == True:
                        player.setWeaponsToTarget(
                            a,
                            (
                                slot_1_SELECTED,
                                slot_2_SELECTED,
                                slot_3_SELECTED,
                                slot_4_SELECTED,
                                slot_5_SELECTED,
                            ),
                        )
        ####################################################################################################

        ####################################################################################################
        if CURSOR_INTERSECT_OBJECT != True:
            for p in self.visible_PLANET_list:
                planet_cursor_dist = lengthBetweenPoints(
                    (p.points.center[0], p.points.center[1]), (mxvp, myvp)
                )
                if planet_cursor_dist < p.w / 4:
                    CURSOR_INTERSECT_OBJECT = True
                    p.renderInfo()
                    p.renderDirection()

                    if lb == True:
                        player.target_planet = p
                        player.setTargetPosCoord(
                            (
                                player.target_planet.points.center[0],
                                player.target_planet.points.center[1],
                            )
                        )
                        player.calculateDetaledWayToPosition()
        ####################################################################################################

        ####################################################################################################
        if CURSOR_INTERSECT_OBJECT != True:
            for c in self.visible_CONTAINER_list:
                container_cursor_dist = lengthBetweenPoints(
                    (c.points.center[0], c.points.center[1]), (mxvp, myvp)
                )
                if container_cursor_dist < c.w / 1.5:
                    CURSOR_INTERSECT_OBJECT = True
                    c.renderInfo()

                    if lb == True:
                        if grapple_SELECTED == True:
                            player.setGrabItem(c)
                        else:
                            player.setWeaponsToTarget(
                                c,
                                (
                                    slot_1_SELECTED,
                                    slot_2_SELECTED,
                                    slot_3_SELECTED,
                                    slot_4_SELECTED,
                                    slot_5_SELECTED,
                                ),
                            )

        ####################################################################################################
        if CURSOR_INTERSECT_OBJECT != True:
            for b in self.visible_BOMB_list:
                bomb_cursor_dist = lengthBetweenPoints(
                    (b.points.center[0], b.points.center[1]), (mxvp, myvp)
                )
                if bomb_cursor_dist < b.w / 1.5:
                    CURSOR_INTERSECT_OBJECT = True
                    b.renderInfo()

                    if lb == True:
                        if grapple_SELECTED == True:
                            player.setGrabItem(b)
                        else:
                            player.setWeaponsToTarget(
                                b,
                                (
                                    slot_1_SELECTED,
                                    slot_2_SELECTED,
                                    slot_3_SELECTED,
                                    slot_4_SELECTED,
                                    slot_5_SELECTED,
                                ),
                            )

        ####################################################################################################
        if CURSOR_INTERSECT_OBJECT != True:
            for m in self.visible_MINERAL_list:
                mineral_cursor_dist = lengthBetweenPoints(
                    (m.points.center[0], m.points.center[1]), (mxvp, myvp)
                )
                if mineral_cursor_dist < m.w / 2:
                    CURSOR_INTERSECT_OBJECT = True
                    m.renderInfo()

                    if lb == True:
                        if grapple_SELECTED == True:
                            player.setGrabItem(m)
                        else:
                            player.setWeaponsToTarget(
                                m,
                                (
                                    slot_1_SELECTED,
                                    slot_2_SELECTED,
                                    slot_3_SELECTED,
                                    slot_4_SELECTED,
                                    slot_5_SELECTED,
                                ),
                            )
        ###################################################################################################

        ###################################################################################################
        if CURSOR_INTERSECT_OBJECT != True:
            for b in self.visible_BLACKHOLE_list:
                blackhole_cursor_dist = lengthBetweenPoints(
                    (b.points.center[0], b.points.center[1]), (mxvp, myvp)
                )
                if blackhole_cursor_dist < b.w / 4:
                    CURSOR_INTERSECT_OBJECT = True
                    b.renderInfo()

                    if lb == True:
                        pass
        ####################################################################################################

        ####################################################################################################
        if CURSOR_INTERSECT_OBJECT != True:
            for s in self.visible_STAR_list:
                star_cursor_dist = lengthBetweenPoints(
                    (s.points.center[0], s.points.center[1]), (mxvp, myvp)
                )
                if star_cursor_dist < s.w / 4:
                    CURSOR_INTERSECT_OBJECT = True
                    s.renderInfo()

                    if lb == True:
                        pass
        ####################################################################################################

        ####################################################################################################
        if CURSOR_INTERSECT_OBJECT != True:
            # create list of player movement if cursor met no target

            if lb == True:
                player.caclulateWayToCursor((mxvp, myvp))
        #####################################################################################################

        if lb == True:
            player.calculateWayVisualisation()

    # def calculateShipsTurnWaysToPosition(self):
    # for k in self.SHIP_list:
    # if k.target_planet != None:
    # k.setTargetPosCoord((k.target_planet.rect.centerx, k.target_planet.rect.centery))
    # k.calculateTurnWayToPosition()

    # def calculateDetaledShipWaysToPosition(self):
    # for k in self.SHIP_list:
    # k.calculateDetaledWayToPosition()

    # def calculateShipWaysVisualisation(self):
    ## performs once per turn
    # for k in self.visible_SHIP_list:
    # k.calculateWayVisualisation()

    def findVisibleEntities(self, vpCoordinate_x, vpCoordinate_y):
        x_startViewCoord = vpCoordinate_x + VIEW_WIDTH
        y_startViewCoord = vpCoordinate_y + VIEW_HEIGHT

        self.visible_STAR_list = []
        self.visible_PLANET_list = []
        self.visible_SPUTNIK_list = []
        self.visible_ASTEROID_list = []
        self.visible_MINERAL_list = []
        self.visible_CONTAINER_list = []
        self.visible_BOMB_list = []
        self.visible_SHIP_list = []
        self.visible_ROCKET_list = []
        self.visible_effect_LAZER_list = []
        self.visible_BLACKHOLE_list = []

        self.visible_effect_EXPLOSION_list = []
        self.visible_effect_DAMAGE_list = []

        self.visible_STAR_list = [
            s
            for s in self.STAR_list
            if isObjectVisible(
                (s.points.center[0], s.points.center[1]),
                (s.w, s.h),
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]
        self.visible_PLANET_list = [
            p
            for p in self.PLANET_list
            if isObjectVisible(
                (p.points.center[0], p.points.center[1]),
                (p.w, p.h),
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]
        self.visible_SPUTNIK_list = [
            s
            for s in self.SPUTNIK_list
            if isObjectVisible(
                (s.points.center[0], s.points.center[1]),
                (s.w, s.h),
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]
        self.visible_ASTEROID_list = [
            a
            for a in self.ASTEROID_list
            if isObjectVisible(
                (a.points.center[0], a.points.center[1]),
                (a.w, a.h),
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]
        self.visible_MINERAL_list = [
            m
            for m in self.MINERAL_list
            if isObjectVisible(
                (m.points.center[0], m.points.center[1]),
                (m.w, m.h),
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]
        self.visible_CONTAINER_list = [
            c
            for c in self.CONTAINER_list
            if isObjectVisible(
                (c.points.center[0], c.points.center[1]),
                (c.w, c.h),
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]
        self.visible_BOMB_list = [
            b
            for b in self.BOMB_list
            if isObjectVisible(
                (b.points.center[0], b.points.center[1]),
                (b.w, b.h),
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]
        self.visible_SHIP_list = [
            k
            for k in self.SHIP_list
            if isObjectVisible(
                (k.points.center[0], k.points.center[1]),
                (k.w, k.h),
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]
        self.visible_ROCKET_list = [
            r
            for r in self.ROCKET_list
            if isObjectVisible(
                (r.points.center[0], r.points.center[1]),
                (r.w, r.h),
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]
        self.visible_BLACKHOLE_list = [
            b
            for b in self.BLACKHOLE_list
            if isObjectVisible(
                (b.points.center[0], b.points.center[1]),
                (b.w, b.h),
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]

        self.visible_effect_EXPLOSION_list = [
            e
            for e in self.effect_EXPLOSION_list
            if isObjectVisible(
                (e.center[0], e.center[1]),
                (300, 300),
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]
        self.visible_effect_DAMAGE_list = [
            e
            for e in self.effect_DAMAGE_list
            if isObjectVisible(
                (e.center[0], e.center[1]),
                (300, 300),
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]

        self.visible_effect_LAZER_list = [
            e
            for e in self.effect_LAZER_list
            if isLineVisible(
                e.p1,
                e.p2,
                (vpCoordinate_x, vpCoordinate_y),
                (x_startViewCoord, y_startViewCoord),
            )
        ]

    def radarEntitiesFilter(self):  # TRY to MERGE with find visible entities
        distance = player.radar.radius

        self.visible_SHIP_list = [
            k
            for k in self.visible_SHIP_list
            if collisionBetweenCenters(k.points.center, player.points.center, distance)
        ]
        self.visible_SPUTNIK_list = [
            s
            for s in self.visible_SPUTNIK_list
            if collisionBetweenCenters(s.points.center, player.points.center, distance)
        ]

        self.visible_MINERAL_list = [
            m
            for m in self.visible_MINERAL_list
            if collisionBetweenCenters(m.points.center, player.points.center, distance)
        ]
        self.visible_CONTAINER_list = [
            c
            for c in self.visible_CONTAINER_list
            if collisionBetweenCenters(c.points.center, player.points.center, distance)
        ]
        self.visible_BOMB_list = [
            b
            for b in self.visible_BOMB_list
            if collisionBetweenCenters(b.points.center, player.points.center, distance)
        ]

        self.visible_effect_EXPLOSION_list = [
            e
            for e in self.visible_effect_EXPLOSION_list
            if collisionBetweenCenters(e.center, player.points.center, distance)
        ]
        self.visible_effect_DAMAGE_list = [
            e
            for e in self.visible_effect_DAMAGE_list
            if collisionBetweenCenters(e.center, player.points.center, distance)
        ]

        self.visible_effect_LAZER_list = [
            e
            for e in self.visible_effect_LAZER_list
            if collisionBetweenCenters([e.ex, e.ey], player.points.center, distance)
        ]  # ????!!!!

    def render_TEST(
        self,
        fbo0,
        fbo1,
        fbo2,
        bloom,
        program_ShockWave,
        program_Shafts,
        vpCoordinate_x,
        vpCoordinate_y,
        lb=False,
        rb=False,
    ):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        vx, vy = 0, 0
        glEnable(GL_BLEND)

        glEnable(GL_POINT_SPRITE)
        for ds in self.distant_stars_list:
            ds.update()

            glBindTexture(GL_TEXTURE_2D, ds.texture)
            glPointSize(ds.size)

            glColor4f(1.0, 1.0, 1.0, ds.alpha)

            glBegin(GL_POINTS)
            glVertex3f(
                ds.pos_x - vx * ds.distance_rate, ds.pos_y - vy * ds.distance_rate, -2
            )
            glEnd()

        glDisable(GL_POINT_SPRITE)

        # <<<player.render()>>>
        glBindTexture(GL_TEXTURE_2D, player.texture_ID)
        drawQuad(
            player.points.bottomLeft,
            player.points.bottomRight,
            player.points.topRight,
            player.points.topLeft,
            -2,
        )

        # glDisable(GL_TEXTURE_2D)
        # glBindTexture(GL_TEXTURE_2D, player.texture_ID)
        # glEnable(GL_TEXTURE_2D)

        # <<<player.drive_jet.update()>>>
        for p in player.drive_jet.particles_list:
            p.update(
                player.drive_jet.velocity_x, player.drive_jet.velocity_y
            )  # matematika, update pozocii kazhdoj chasticy

        # glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, player.drive_jet.texture)

        glEnable(GL_POINT_SPRITE)
        # glTexEnvi(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE)

        glPointSize(50)

        for p in player.drive_jet.particles_list:
            glBegin(GL_POINTS)
            glVertex3f(p.pos[0], p.pos[1], -2)
            glEnd()
        glDisable(GL_POINT_SPRITE)

        glDisable(GL_BLEND)

    def renderBackground(self, vx=0, vy=0):
        ### HACK !!!! needs for bug fixing with point sprite
        glEnable(GL_POINT_SPRITE)
        glBindTexture(GL_TEXTURE_2D, self.ds.texture)
        glBegin(GL_POINTS)
        glVertex3f(-100, -100, -2)
        glEnd()
        glDisable(GL_POINT_SPRITE)
        ### HACK !!!! needs for bug fixing with point sprite

        glEnable(GL_BLEND)
        glDepthMask(False)
        for dn in self.NEBULA_static_effect_list:
            dn.render(vx, vy)

        for dn in self.NEBULA_rotated_effect_list:
            dn.update()
            dn.render(vx, vy)
        glEnable(GL_POINT_SPRITE)

        glBindTexture(GL_TEXTURE_2D, self.ds.texture)
        for ds in self.DISTANT_STAR_effect_list:
            glPointSize(ds.size)

            glBegin(GL_POINTS)
            glVertex3f(
                ds.pos_x - vx * ds.distance_rate, ds.pos_y - vy * ds.distance_rate, -2
            )
            glEnd()

        glDisable(GL_POINT_SPRITE)

        ## old method
        # for ds in self.distant_stars_list:
        # drawStatic(ds.texture, (ds.pos_x - vx*ds.distance_rate, ds.pos_y - vy*ds.distance_rate), (ds.size, ds.size))

        glDisable(GL_BLEND)
        glDepthMask(True)

    def renderEntities_NEW(
        self,
        fbo0,
        fbo1,
        fbo2,
        bloom,
        program_ShockWave,
        program_Shafts,
        vpCoordinate_x,
        vpCoordinate_y,
        lb=False,
        rb=False,
    ):
        w, h = VIEW_WIDTH, VIEW_HEIGHT

        ######### EFFECT DEMONSTRATION
        if lb == True:
            # for x in range(0, 10):
            # addExplosion(player)
            pass

        if rb == True:
            self.shockwaveEffect_list = []
            self.shockwaveEffect_remove_queue = []
        ######### EFFECT DEMONSTRATION

        glDisable(GL_BLEND)
        glDepthMask(True)

        fbo0.activate()

        self.renderBackground(vpCoordinate_x, vpCoordinate_y)
        glTranslatef(-vpCoordinate_x, -vpCoordinate_y, 0.0)  # camera

        glColor4f(1.0, 1.0, 1.0, 1.0)

        glEnable(GL_DEPTH_TEST)
        for s in self.visible_STAR_list:
            s.render3D_new()
        glDisable(GL_DEPTH_TEST)

        self.setBgColor()
        fbo0.deactivate()

        # POST PROCESS BLOOM (many FBO)
        bloom.pass0(fbo0.texture, w, h)
        bloom.pass1(w, h)
        bloom.pass2(w, h)
        bloom.combine(fbo0.texture, w, h)

        fbo1.activate()
        ### RENDER to FBO, VOLUMETRIC LIGHT
        glUseProgram(program_Shafts)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, bloom.fbo_preFinal.texture)
        glUniform1i(glGetUniformLocation(program_Shafts, "FullSampler"), 0)

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, bloom.fbo4_pass2.texture)
        glUniform1i(glGetUniformLocation(program_Shafts, "BlurSampler"), 1)

        glUniform4f(
            glGetUniformLocation(program_Shafts, "sun_pos"),
            -float(vpCoordinate_x) / w,
            -float(vpCoordinate_y) / h,
            -100,
            1,
        )

        glActiveTexture(GL_TEXTURE0)
        drawFullScreenQuad(w, h, -999.0)

        glUseProgram(0)
        glActiveTexture(GL_TEXTURE0)

        glTranslatef(-vpCoordinate_x, -vpCoordinate_y, 0.0)  # camera
        glEnable(GL_DEPTH_TEST)
        for p in self.visible_PLANET_list:
            p.render3D_new(vpCoordinate_x, vpCoordinate_y)
        glDisable(GL_DEPTH_TEST)

        glEnable(GL_BLEND)
        glDepthMask(False)

        for sp in self.visible_SPUTNIK_list:
            sp.render()

        for a in self.visible_ASTEROID_list:
            a.renderInSpace()

        for m in self.visible_MINERAL_list:
            m.renderInSpace()

        for c in self.visible_CONTAINER_list:
            c.renderInSpace()

        for b in self.visible_BOMB_list:
            b.renderInSpace()

        for k in self.visible_SHIP_list:
            k.renderInSpace()

        for k in self.visible_SHIP_list:
            k.renderProtectionShield()
        self.setBgColor()

        for r in self.visible_ROCKET_list:
            r.render()

        for b in self.visible_BLACKHOLE_list:
            b.render()

        glEnable(GL_POINT_SPRITE)
        # glTexEnvi(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE)
        for k in self.visible_SHIP_list:
            k.renderDriveJet()

        for r in self.visible_ROCKET_list:
            r.renderDriveJet()
        glDisable(GL_POINT_SPRITE)

        self.setBgColor()

        glDisable(GL_BLEND)
        glDepthMask(True)

        ## 3D ship model using VBO
        # glEnableClientState(GL_VERTEX_ARRAY)
        # glEnableClientState(GL_NORMAL_ARRAY)
        # glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        # zp = -200
        # glTranslatef(0, 0, zp)    # camera fro gluPerspective
        # for sh in SHIP3Dlist:
        # glPushMatrix()
        # glTranslatef(sh.x, sh.y, 0)
        # glScale(sh.scale, sh.scale, sh.scale)
        # glRotate(sh.a + self.tik , 1, 1, 1)
        ##glRotate(90, 1, 0, 0)

        # glBindTexture(GL_TEXTURE_2D, star_data.texture)
        # sh.model.draw_vbo1()
        # glPopMatrix()

        # glBindBuffer(GL_ARRAY_BUFFER,0)

        # glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        # glDisableClientState(GL_NORMAL_ARRAY)
        # glDisableClientState(GL_VERTEX_ARRAY)
        # self.tik += 1
        ## 3D ship model using VBO

        fbo1.deactivate()

        # POST PROCESS WAVE SHOCK into FBO2
        fbo2.activate()

        for waves in self.effect_SHOCKWAVE_list:
            waves.update()

        center_array, xyz_array, time_array = returnShockWavesDataInArrays(
            self.effect_SHOCKWAVE_list, vpCoordinate_x, vpCoordinate_y
        )
        # if randint(1,20) == 1:
        #   print center_array, xyz_array, time_array
        #   # print('***'

        glUseProgram(program_ShockWave)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, fbo1.texture)
        glUniform1i(glGetUniformLocation(program_ShockWave, "sceneTex"), 0)

        len_effect_SHOCKWAVE_list = len(self.effect_SHOCKWAVE_list)
        glUniform1i(
            glGetUniformLocation(program_ShockWave, "imax"), len_effect_SHOCKWAVE_list
        )
        glUniform2fv(
            glGetUniformLocation(program_ShockWave, "center"),
            len_effect_SHOCKWAVE_list,
            center_array,
        )
        glUniform3fv(
            glGetUniformLocation(program_ShockWave, "shockParams"),
            len_effect_SHOCKWAVE_list,
            xyz_array,
        )
        glUniform1fv(
            glGetUniformLocation(program_ShockWave, "time"),
            len_effect_SHOCKWAVE_list,
            time_array,
        )

        # DRAW full size w,h texture_scene
        # print w, h
        drawFullScreenQuad(w, h, -999.0)
        glUseProgram(0)

        fbo2.deactivate()

        # render from FBO
        glEnable(GL_TEXTURE_2D)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)  # unbind fbo

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glBindTexture(GL_TEXTURE_2D, fbo2.texture)
        drawFullScreenQuad(w, h, -999.0)

        glTranslatef(-vpCoordinate_x, -vpCoordinate_y, 0.0)  # camera

        glEnable(GL_BLEND)
        glDepthMask(False)

        for e in self.visible_effect_LAZER_list:
            e.render()

        for k in self.visible_SHIP_list:
            for t in k.flow_TEXT_list:
                t.render()

        glEnable(GL_POINT_SPRITE)
        for pe in self.visible_effect_DAMAGE_list:
            pe.update()
            pe.render()

        for pe in self.visible_effect_EXPLOSION_list:
            pe.update()
            pe.render()
        glDisable(GL_POINT_SPRITE)

        self.setBgColor()

        # renderObj(b5_model, (400, 400, -2), (30, 40, 90), 100.0)

        # glDisable(GL_BLEND)
        # glDepthMask(True)

        #### glLib Particle system
        # VIEW.setPerspective()
        # glTranslatef(vpCoordinate_x * VIEW.rate_x, vpCoordinate_y * VIEW.rate_y, VIEW.z_for_particles)    # camera for gluPerspective

        ## Drive trails updating
        # VIEW.pushView()

        # glDisable(GL_BLEND)
        # for k in self.visible_SHIP_list:
        # k.drive_jet.update()

        # for r in self.visible_ROCKET_list:
        # r.drive_jet.update()

        # for ps in self.particleSystem_list:
        # ps.update()

        # glEnable(GL_BLEND)

        # VIEW.popView()
        ## Drive trails updating

        ## Drive trails drawing
        # glEnable(GL_POINT_SPRITE)
        # glBlendFunc(GL_SRC_ALPHA,GL_ONE)
        # glDisable(GL_DEPTH_TEST)
        # glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)

        # for k in self.visible_SHIP_list:
        # k.drive_jet.draw(k.points.midLeft[0], k.points.midLeft[1], k.points.angle)
        ##pass

        # for r in self.visible_ROCKET_list:
        # r.drive_jet.draw(r.points.midLeft[0], r.points.midLeft[1], r.points.angle)

        # for ps in self.particleSystem_list:
        # ps.draw(ps.ob.points.center[0], ps.ob.points.center[1], 0)

        # glDisable(GL_VERTEX_PROGRAM_POINT_SIZE)
        # glEnable(GL_DEPTH_TEST)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glDisable(GL_POINT_SPRITE)
        ## Drive trails drawing
        ##if randint(1,20) == 1: print len(self.visible_SHIP_list)       # debugging

        # VIEW.setOrtho()
        #### glLib Particle system

    def removeDeadEntities(self):  # can be moved to low freq exec
        for sp in self.SPUTNIK_remove_queue:
            self.SPUTNIK_list.remove(sp)
            global_SPUTNIK_list.remove(sp)
            del sp
        self.SPUTNIK_remove_queue = []
        # print len(self.SPUTNIK_list)

        for a in self.ASTEROID_remove_queue:
            self.ASTEROID_list.remove(a)
            del a
        self.ASTEROID_remove_queue = []
        # print len(self.ASTEROID_list)

        for m in self.MINERAL_remove_queue:
            self.MINERAL_list.remove(m)
            del m
        self.MINERAL_remove_queue = []
        # print len(self.MINERAL_list)

        for c in self.CONTAINER_remove_queue:
            self.CONTAINER_list.remove(c)
            del c
        self.CONTAINER_remove_queue = []
        # print len(self.CONTAINER_list)

        for b in self.BOMB_remove_queue:
            self.BOMB_list.remove(b)
            self.bombExplosionCollision(b)
            del b
        self.BOMB_remove_queue = []
        # print len(self.BOMB_list)

        for r in self.ROCKET_remove_queue:
            self.ROCKET_list.remove(r)
            del r
        self.ROCKET_remove_queue = []
        # print len(self.ROCKET_list)

        for k in self.SHIP_remove_queue:
            self.removeShipFromStarsystem(k)
            global_SHIP_list.remove(k)
            print(f"{k.name} removed from world")
            del k
        self.SHIP_remove_queue = []
        # print len(self.SHIP_list)

        for wave in self.effect_SHOCKWAVE_remove_queue:
            self.effect_SHOCKWAVE_list.remove(wave)
            del wave
        self.effect_SHOCKWAVE_remove_queue = []
        # print len(self.effect_SHOCKWAVE_list)

        for le in self.effect_LAZER_remove_queue:
            self.effect_LAZER_list.remove(le)
            del le
        self.effect_LAZER_remove_queue = []
        # print len(self.effect_LAZER_list)

        # print "before remove, Total:", len(self.effect_EXPLOSION_list), "to be removed:", len(self.effect_EXPLOSION_remove_queue)
        for pe in self.effect_EXPLOSION_remove_queue:
            self.effect_EXPLOSION_list.remove(pe)
            del pe
        self.effect_EXPLOSION_remove_queue = []
        # print "fater remove, Total:", len(self.effect_EXPLOSION_list), "to be removed:", len(self.effect_EXPLOSION_remove_queue)

        for pd in self.effect_DAMAGE_remove_queue:
            self.effect_DAMAGE_list.remove(pd)
            del pd
        self.effect_DAMAGE_remove_queue = []
        # print len(self.effect_DAMAGE_list)

    # def removeCollectedEntities(self): # can be moved to low freq exec
    # for m in self.MINERAL_remove_queue:
    # self.MINERAL_list.remove(m)
    # self.MINERAL_remove_queue = []
    ##print len(self.MINERAL_list)

    # for c in self.CONTAINER_remove_queue:
    # self.CONTAINER_list.remove(c)
    # self.CONTAINER_remove_queue = []
    ##print len(self.CONTAINER_list)

    # for b in self.BOMB_remove_queue:
    # self.BOMB_list.remove(b)
    # self.BOMB_remove_queue = []
    ##print len(self.BOMB_list)

    def renderEntities_OLD(
        self,
        fbo0,
        fbo1,
        fbo2,
        bloom,
        program_ShockWave,
        program_Shafts,
        vpCoordinate_x,
        vpCoordinate_y,
        lb=False,
        rb=False,
    ):
        ######### EFFECT DEMONSTRATION
        if lb == True:
            for x in range(0, 2):
                addExplosion(player)
            # pass

        glDisable(GL_BLEND)
        glDepthMask(True)

        glEnable(GL_TEXTURE_2D)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)  # unbind fbo

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glActiveTexture(GL_TEXTURE0)

        self.renderBackground(vpCoordinate_x, vpCoordinate_y)
        glTranslatef(-vpCoordinate_x, -vpCoordinate_y, 0.0)  # camera

        glEnable(GL_LIGHTING)
        glLightfv(
            GL_LIGHT0,
            GL_POSITION,
            (-vpCoordinate_x, -vpCoordinate_y, Z_POS_PLANET + 400, 1.0),
        )

        glLightfv(GL_LIGHT0, GL_AMBIENT, (1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

        glMaterialfv(GL_FRONT, GL_EMISSION, (100, 100, 100, 1))

        for s in self.visible_STAR_list:
            s.render3D_old()

        glLightfv(
            GL_LIGHT0,
            GL_POSITION,
            (-vpCoordinate_x, -vpCoordinate_y, Z_POS_PLANET, 1.0),
        )

        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

        glMaterialfv(GL_FRONT, GL_EMISSION, (0, 0, 0, 1))

        for p in self.visible_PLANET_list:
            p.render3D_old()

        glDisable(GL_LIGHTING)

        glEnable(GL_BLEND)
        glDepthMask(False)
        # for s in self.visible_STAR_list:
        #    s.renderAtmosphere()

        for sp in self.visible_SPUTNIK_list:
            sp.render()

        for a in self.visible_ASTEROID_list:
            a.renderInSpace()

        for m in self.visible_MINERAL_list:
            m.renderInSpace()

        for c in self.visible_CONTAINER_list:
            c.renderInSpace()

        for b in self.visible_BOMB_list:
            b.renderInSpace()

        for k in self.visible_SHIP_list:
            k.renderInSpace()

        for r in self.visible_ROCKET_list:
            r.render()

        for b in self.visible_BLACKHOLE_list:
            b.render()

        glEnable(GL_POINT_SPRITE)
        # glTexEnvi(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE)
        for k in self.visible_SHIP_list:
            k.renderDriveJet()

        for r in self.visible_ROCKET_list:
            r.renderDriveJet()
        glDisable(GL_POINT_SPRITE)

        self.setBgColor()

        for e in self.visible_effect_LAZER_list:
            e.render()

        for k in self.visible_SHIP_list:
            for t in k.flow_TEXT_list:
                t.render()

        glEnable(GL_POINT_SPRITE)
        for pe in self.visible_effect_DAMAGE_list:
            pe.update()
            pe.render()

        for pe in self.visible_effect_EXPLOSION_list:
            pe.update()
            pe.render()
        glDisable(GL_POINT_SPRITE)

        self.setBgColor()

    def setBgColor(self):
        glColor4f(
            self.red, self.green, self.blue, 1.0
        )  # restore BG palette after text render has changed it
        # print self.red, self.green, self.blue

    def fireEvents(self, timer):
        for k in self.SHIP_list:
            k.weaponsFire(timer)

    def temperatureRestorationEntities(self):
        # performs once per turn
        for k in self.SHIP_list:
            k.temperatureRestoration()

    def energyRestorationEntities(self):
        # performs once per turn
        for k in self.SHIP_list:
            k.energyRestoration()

    def armorRestorationEntities(self):
        # performs once per turn
        for k in self.SHIP_list:
            k.armorRestoration()

    def hArmorRestorationEntities(self):
        # performs only once per turn
        for k in self.SHIP_list:
            k.armorRestoration()

    def renderRanges(
        self,
        slot_1_SELECTED,
        slot_2_SELECTED,
        slot_3_SELECTED,
        slot_4_SELECTED,
        slot_5_SELECTED,
        show_RADAR,
        grapple_SELECTED,
    ):
        if player.alive == True:
            if player.Gl_LIST_direction_ID != None:
                player.renderDirection()
            player.renderRadius(
                slot_1_SELECTED,
                slot_2_SELECTED,
                slot_3_SELECTED,
                slot_4_SELECTED,
                slot_5_SELECTED,
                grapple_SELECTED,
                show_RADAR,
            )

        # for k in self.visible_SHIP_list:
        #     k.renderDirection()

    def renderOrbits(self, show_orbits):
        if show_orbits == True:
            for a in self.ASTEROID_list:
                a.renderDirection()
            for p in self.PLANET_list:
                p.renderDirection()

    def renderShipLabels(self, show_lables):
        if show_lables == True:
            for k in self.visible_SHIP_list:
                k.renderInfo()

    def renderPlanetLabels(self, show_lables):
        if show_lables == True:
            for s in self.visible_STAR_list:
                s.renderInfo()
            for p in self.visible_PLANET_list:
                p.renderInfo()
            for a in self.visible_ASTEROID_list:
                a.renderInfo()
            for m in self.visible_MINERAL_list:
                m.renderInfo()
            for b in self.visible_BLACKHOLE_list:
                b.renderInfo()

    def returnPirat(self):
        for k in self.SHIP_PIRAT_list:
            return k

    def returnTrader(self):
        for k in self.SHIP_TRADER_list:
            return k

    def returnDiplomat(self):
        for k in self.SHIP_DIPLOMAT_list:
            return k

    def returnClosestPlanet(self, ship):
        p = self.returnClosestInhabitedPlanet(ship)
        if p == None:
            p = self.returnClosestUninhabitedPlanet(ship)
        return p

    def returnClosestInhabitedPlanet(self, ship):
        planet_with_distance_tuples = []
        for p in self.PLANET_list:
            if p.kosmoport != None:
                ship_planet_dist = lengthBetweenPoints(
                    (ship.points.center[0], ship.points.center[1]),
                    (p.points.center[0], p.points.center[1]),
                )
                planet_with_distance_tuples.append((p, ship_planet_dist))

        planet_with_distance_tuples_sorted = sorted(
            planet_with_distance_tuples, key=itemgetter(1)
        )
        if len(planet_with_distance_tuples_sorted) > 0:
            (p_closest, ship_planet_dist) = planet_with_distance_tuples_sorted[0]
            return p_closest
        else:
            return None

    def returnClosestUninhabitedPlanet(self, ship):
        planet_with_distance_tuples = []
        for p in self.PLANET_list:
            if p.kosmoport == None:
                ship_planet_dist = lengthBetweenPoints(
                    (ship.points.center[0], ship.points.center[1]),
                    (p.points.center[0], p.points.center[1]),
                )
                planet_with_distance_tuples.append((p, ship_planet_dist))

        planet_with_distance_tuples_sorted = sorted(
            planet_with_distance_tuples, key=itemgetter(1)
        )
        if len(planet_with_distance_tuples_sorted) > 0:
            (p_closest, ship_planet_dist) = planet_with_distance_tuples_sorted[0]
            return p_closest
        else:
            return None

    def returnClosestCapturedSs(self):
        ss = global_STARSYSTEM_CAPTURED_list[0]
        dist_min = lengthBetweenPoints(
            (self.rectOnMap.centerx, self.rectOnMap.centery),
            (ss.rectOnMap.centerx, ss.rectOnMap.centery),
        )

        for captured_ss in global_STARSYSTEM_CAPTURED_list:
            dist = lengthBetweenPoints(
                (self.rectOnMap.centerx, self.rectOnMap.centery),
                (captured_ss.rectOnMap.centerx, captured_ss.rectOnMap.centery),
            )
            if dist < dist_min:
                dist_min = dist
                ss = captured_ss
        return ss

    def appendShipToStarsystem(self, ship):
        self.SHIP_list.append(ship)

        if ship.subtype == RANGER_ID:
            if ship.subsubtype == WARRIOR_ID:
                self.SHIP_WARRIOR_list.append(ship)
            elif ship.subsubtype == PIRAT_ID:
                self.SHIP_PIRAT_list.append(ship)
            elif ship.subsubtype == TRADER_ID:
                self.SHIP_TRADER_list.append(ship)
            elif ship.subsubtype == DIPLOMAT_ID:
                self.SHIP_DIPLOMAT_list.append(ship)

        elif ship.subtype == WARRIOR_ID:
            self.SHIP_WARRIOR_list.append(ship)
        elif ship.subtype == PIRAT_ID:
            self.SHIP_PIRAT_list.append(ship)
        elif ship.subtype == TRADER_ID:
            self.SHIP_TRADER_list.append(ship)
        elif ship.subtype == DIPLOMAT_ID:
            self.SHIP_DIPLOMAT_list.append(ship)

        ship.red, ship.green, ship.blue = self.red, self.green, self.blue
        ship.resetWeaponTargets((0, 0, 0, 0, 0))
        ship.resetGrappleTargets()

        # ship.texOb.loadToVRAM()   # ???? probably better to move close to hyperJump to avoid tex load when launching the ship from the planet

    def removeShipFromStarsystem(self, ship):
        self.SHIP_list.remove(ship)

        if ship.subtype == RANGER_ID:
            if ship.subsubtype == WARRIOR_ID:
                self.SHIP_WARRIOR_list.remove(ship)
            elif ship.subsubtype == PIRAT_ID:
                self.SHIP_PIRAT_list.remove(ship)
            elif ship.subsubtype == TRADER_ID:
                self.SHIP_TRADER_list.remove(ship)
            elif ship.subsubtype == DIPLOMAT_ID:
                self.SHIP_DIPLOMAT_list.remove(ship)

        elif ship.subtype == WARRIOR_ID:
            self.SHIP_WARRIOR_list.remove(ship)
        elif ship.subtype == PIRAT_ID:
            self.SHIP_PIRAT_list.remove(ship)
        elif ship.subtype == TRADER_ID:
            self.SHIP_TRADER_list.remove(ship)
        elif ship.subtype == DIPLOMAT_ID:
            self.SHIP_DIPLOMAT_list.remove(ship)

        # ship.texOb.removeFromVRAM()   # ???? probably better to move close to hyperJump to avoid tex load when launching the ship from the planet


def isObjectVisible(
    ob_centerx,
    ob_centery,
    ob_w,
    ob_h,
    vpCoordinate_x,
    vpCoordinate_y,
    x_startViewCoord,
    y_startViewCoord,
):
    if ob_centerx < (vpCoordinate_x - ob_w):
        return False
    if ob_centerx > (x_startViewCoord + ob_w):
        return False
    if ob_centery < (vpCoordinate_y - ob_h):
        return False
    if ob_centery > (y_startViewCoord + ob_h):
        return False

    return True


def isLineVisible(p1, p2, vpCoordinate_x, vpCoordinate_y, xr, yr):
    if (vpCoordinate_x < p1[0] < xr) or (vpCoordinate_x < p2[0] < xr):
        return True
    if (vpCoordinate_y < p1[1] < yr) or (vpCoordinate_y < p2[1] < yr):
        return True

    return False


def collisionBetweenCenters(point0, point1, distance):
    if abs(point0[0] - point1[0]) > distance:
        return False
    if abs(point0[1] - point1[1]) > distance:
        return False

    return True


# def isVisibleForPlayer(self, centerx, centery):
# ship_player_dist = lengthBetweenPoints((centerx, centery), (player.points.center[0], player.points.center[1]))
# if ship_player_dist < player.radius:
# return True
