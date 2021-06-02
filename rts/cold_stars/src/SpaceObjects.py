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
from resources import *
from effects import *
from resources import *
from math import sqrt

from points import *


class CommonForPlanets:
    def __init__(self):
        self.ID = ENTITY_ID_GENERATOR.returnNextID()

        # also needs for star size on map and collision
        rate = 5.4
        self.w = rate * self.scale
        self.h = rate * self.scale
        self.collision_threshold = (self.w + self.h) / 2
        #

        self.ax = randint(0, 40)
        self.ay = 0  # randint(10, 20)
        self.az = 0  # randint(0, 30)

        self.points = points()
        self.points.createCenterPoint()

    def updatePosition(self):
        if self.i < (self.orbit_list_len - 1):
            self.points.setCenter(self.orbit_list_x[self.i], self.orbit_list_y[self.i])
            self.i += 1
        else:
            self.i = 0

    def updatePositionHidden(self):
        if self.i < (self.turn_orbit_list_len - 1):
            self.points.setCenter(self.orbit_list_x[self.i], self.orbit_list_y[self.i])
            self.i += 1
        else:
            self.i = 0

    def simpleOrbitFormation(self):
        self.alpha_turn_step = int(self.speed * TURN_TIME)
        (
            self.turn_orbit_list_x,
            self.turn_orbit_list_y,
        ) = getEllipseCoordinateRangeHighPrecision(
            self.orbit_centerx,
            self.orbit_centery,
            self.radius_A,
            self.radius_B,
            self.alpha_turn_step,
            self.fi,
        )
        self.turn_orbit_list_len = len(self.turn_orbit_list_x)

        #########  init values  ####
        self.i = (
            randint(
                int(self.turn_orbit_list_len / 2) - 2,
                int(self.turn_orbit_list_len / 2) + 2,
            )
            * TURN_TIME
        )
        self.angle = randint(0, 360)

    def detailedOrbitFormation(self):
        self.orbit_list_x, self.orbit_list_y = getEllipseCoordinateRangeHighPrecision(
            self.orbit_centerx,
            self.orbit_centery,
            self.radius_A,
            self.radius_B,
            self.speed,
            self.fi,
        )
        self.orbit_list_len = len(self.orbit_list_x)
        self.orbitVisualisation()

    def orbitVisualisation(self):
        # orbit visualisation
        if self.type == PLANET_ID:
            self.alpha_draw_step = (
                self.alpha_turn_step
                * PLANET_DISTANCE_MIN
                / (max(self.radius_A, self.radius_B) * 1)
            )
        if self.type == ASTEROID_ID:
            self.alpha_draw_step = (
                self.alpha_turn_step
                * PLANET_DISTANCE_MIN
                / (max(self.radius_A, self.radius_B) * 4)
            )

        (
            self.draw_orbit_list_x,
            self.draw_orbit_list_y,
        ) = getEllipseCoordinateRangeHighPrecision(
            self.orbit_centerx,
            self.orbit_centery,
            self.radius_A,
            self.radius_B,
            self.alpha_draw_step,
            self.fi,
        )
        self.draw_orbit_list_len = len(self.draw_orbit_list_x)
        self.GL_ORBIT_LIST_ID = GlListCompileDirection(
            DOT_BLUE_TEX,
            self.draw_orbit_list_x,
            self.draw_orbit_list_y,
            self.draw_orbit_list_len,
            1,
        )

        self.GL_TURN_ORBIT_LIST_ID = GlListCompileDirection(
            DOT_RED_TEX,
            self.turn_orbit_list_x,
            self.turn_orbit_list_y,
            self.turn_orbit_list_len,
            1,
            pointer_size=DOT_SIZE * 1.4,
        )

    def renderDirection(self):
        glCallList(self.GL_ORBIT_LIST_ID)
        glCallList(self.GL_TURN_ORBIT_LIST_ID)

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
            return "None"


class StarInstance(CommonForPlanets):
    """STAR"""

    def __init__(self, name, starsystem, model, texOb, program_multitex):
        self.texOb = texOb
        self.sclass = texOb.class_id
        self.size = texOb.size_id * randint(90, 120) * 0.1
        self.scale = self.size

        self.brightThreshold = texOb.brightThreshold

        self.rgb = texOb.color

        CommonForPlanets.__init__(self)

        # init 2
        self.gl_list = model.gl_list

        self.pos_x, self.pos_y, self.pos_z = 0, 0, Z_POS_PLANET

        self.offset1 = 0
        self.offset2 = 0

        self.program_multitex = program_multitex

        ########   star parameters
        self.type = STAR_ID

        self.name = name
        self.starsystem = starsystem

        self.damage = randint(STAR_DAMAGE_MIN, STAR_DAMAGE_MAX)

        self.deltaAngle = -1

    def linkTexture(self):
        self.texture_0 = self.texOb.texture
        self.texture_1 = self.texOb.texture

    def updateInfo(self):
        self.info = [self.name]

    def renderInfo(self):
        self.updateInfo()
        drawDynamicLabelList(
            text_background_tex,
            (self.points.center[0] + self.w, self.points.center[1] + self.h),
            self.info,
        )

    def update(self, timer):
        pass

    def render3D_new(self):
        self.offset1 += 0.0002
        self.offset1 += 0.0003

        self.az += 0.05

        glUseProgram(self.program_multitex)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_0)
        glUniform1i(glGetUniformLocation(self.program_multitex, "Texture_0"), 0)

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture_1)
        glUniform1i(glGetUniformLocation(self.program_multitex, "Texture_1"), 1)

        # glActiveTexture(GL_TEXTURE2)            # ???

        glUniform2f(
            glGetUniformLocation(self.program_multitex, "displ"),
            self.offset1,
            self.offset2,
        )

        glPushMatrix()

        glTranslate(self.pos_x, self.pos_y, self.pos_z)
        glScalef(self.scale, self.scale, self.scale)
        glRotate(self.ax, 1, 0, 0)
        glRotate(self.ay, 0, 1, 0)
        glRotate(self.az, 0, 0, 1)

        glCallList(self.gl_list)
        glPopMatrix()

        glUseProgram(0)
        glActiveTexture(GL_TEXTURE0)

    def render3D_old(self):
        self.az += 0.05

        glBindTexture(GL_TEXTURE_2D, self.texture_0)

        glPushMatrix()

        glTranslate(self.pos_x, self.pos_y, self.pos_z)
        glScalef(self.scale, self.scale, self.scale)
        glRotate(self.ax, 1, 0, 0)
        glRotate(self.ay, 0, 1, 0)
        glRotate(self.az, 0, 0, 1)

        glCallList(self.gl_list)
        glPopMatrix()


class PlanetInstance(CommonForPlanets):
    """This class is for the planet object"""

    def __init__(
        self,
        name,
        model,
        texOb,
        program_light,
        race,
        population,
        subtype,
        starsystem,
        radius_A,
        radius_B,
        port,
        land,
    ):
        self.gl_list = model.gl_list
        self.program_light = program_light

        self.starsystem = starsystem

        self.texOb = texOb
        self.pclass = texOb.class_id
        self.size = texOb.size_id * randint(60, 120) * 0.1
        self.scale = self.size

        CommonForPlanets.__init__(self)

        ########   planet parameters
        self.name = name

        self.race = race
        self.population = population
        self.type = PLANET_ID
        self.subtype = subtype

        self.speed = randint(PLANET_SPEED_MIN, PLANET_SPEED_MAX) / float(
            radius_A / 1000.0
        )
        self.deltaAngle = 0.01 * self.speed

        self.radius_A = radius_A
        self.radius_B = radius_B

        self.orbit_centerx = 0
        self.orbit_centery = 0
        self.fi = 0

        # NEW!!!
        self.SPUTNIK_list = []
        self.port = port
        self.land = land

    def linkTexture(self):
        self.texture_0 = self.texOb.texture

    def updateInfo(self):
        if self.subtype == PLANET_INHABITED_ID:
            self.info = [
                self.name,
                "class: " + self.returnPlanetClassStr(),
                "race: " + self.returnRaceStr(),
                "size" + str(self.size),
                "population: " + str(self.population),
                "speed: " + str(int(self.speed)),
                "landed ships:" + str(len(self.port.angar.ship_list)),
            ]
        else:
            self.info = [
                self.name,
                "class: " + self.returnPlanetClassStr(),
                "size" + str(self.size),
                "speed: " + str(int(self.speed)),
            ]

    def returnPlanetClassStr(self):
        if self.pclass == PLANET_EARTH_SURFACE_ID:
            return "earth like"
        if self.pclass == PLANET_WATER_SURFACE_ID:
            return "water"
        if self.pclass == PLANET_LAVA_SURFACE_ID:
            return "dead"
        if self.pclass == PLANET_ICE_SURFACE_ID:
            return "ice"
        if self.pclass == PLANET_GAS_SURFACE_ID:
            return "gass"

    def renderInfo(self):
        self.updateInfo()
        drawDynamicLabelList(
            text_background_tex,
            (self.points.center[0] + self.w / 2, self.points.center[1] + self.h / 2),
            self.info,
        )
        if self.race != None:
            drawTexturedRect(
                self.port.goverment.face_texOb.texture,
                [
                    self.points.center[0] + self.w / 2 + 100,
                    self.points.center[1] + self.h / 2 + 100,
                    70,
                    70,
                ],
                -1.0,
            )

    def update(self, timer):
        if timer > 0:
            self.updatePosition()

    def updateHidden(self, timer):
        self.updatePositionHidden()

    def render3D_new(self, vx, vy):
        self.ay += self.deltaAngle

        glUseProgram(self.program_light)

        glUniform4f(
            glGetUniformLocation(self.program_light, "lightPos"), -vx, -vy, -200.0, 0.0
        )
        glUniform4f(
            glGetUniformLocation(self.program_light, "eyePos"), -vx, -vy, -200.0, 0.0
        )

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_0)
        glUniform1i(glGetUniformLocation(self.program_light, "Texture_0"), 0)

        glPushMatrix()

        glTranslate(self.points.center[0], self.points.center[1], -400)
        glScalef(self.scale, self.scale, self.scale)
        glRotate(self.ax, 1, 0, 0)
        glRotate(self.ay, 0, 1, 0)
        glRotate(self.az, 0, 0, 1)

        glCallList(self.gl_list)

        glPopMatrix()

        ### render atmosphere
        glEnable(GL_BLEND)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, clouds_tex)
        glUniform1i(glGetUniformLocation(self.program_light, "Texture_0"), 0)

        glPushMatrix()

        glTranslate(self.points.center[0], self.points.center[1], -400)
        glScalef(self.scale * 1.05, self.scale * 1.05, self.scale * 1.05)
        glRotate(-self.ax, 1, 0, 0)
        glRotate(-self.ay, 0, 1, 0)
        glRotate(-self.az, 0, 0, 1)

        glCallList(self.gl_list)
        glPopMatrix()
        glDisable(GL_BLEND)
        ### render atmosphere

        glUseProgram(0)
        glActiveTexture(GL_TEXTURE0)

    def render3D_old(self):
        self.ay += self.deltaAngle

        glBindTexture(GL_TEXTURE_2D, self.texture_0)

        glPushMatrix()

        glTranslate(self.points.center[0], self.points.center[1], -400)
        glScalef(self.scale, self.scale, self.scale)
        glRotate(self.ax, 1, 0, 0)
        glRotate(self.ay, 0, 1, 0)
        glRotate(self.az, 0, 0, 1)

        glCallList(self.gl_list)
        glPopMatrix()

    def manageIncomingShip(self, ship):
        ship.in_SPACE = False
        ship.is_LANDED = True

        if self.subtype == PLANET_INHABITED_ID:
            H = returnFirstFreeSlotBySlotType(
                ANGAR_SLOT_ID, None, self.port.angar.slot_list
            )
            H.item = ship

            self.port.angar.ship_list.append(ship)
            self.starsystem.SHIP_LANDED_PORT_list.append(ship)
            ship.in_KOSMOPORT = True
            ship.in_UNINHABITED_LAND = False

        if self.subtype == PLANET_UNINHABITED_ID:
            self.land.ship_list.append(ship)
            self.starsystem.SHIP_LANDED_LAND_list.append(ship)
            ship.in_KOSMOPORT = False
            ship.in_UNINHABITED_LAND = True

    def manageOutcomeShip(self, ship):
        if self.subtype == PLANET_INHABITED_ID:
            H = returnFirstSlotWithItemByItem(ship, self.port.angar.slot_list)
            H.item = None

            self.port.angar.ship_list.remove(ship)
            self.starsystem.SHIP_LANDED_PORT_list.remove(ship)

        if self.subtype == PLANET_UNINHABITED_ID:
            self.land.ship_list.remove(ship)
            self.starsystem.SHIP_LANDED_LAND_list.remove(ship)

    def landingRequest(self):
        if self.subtype == PLANET_INHABITED_ID:
            if len(self.port.angar.ship_list) < len(
                self.port.angar.slot_list
            ):  # implement preservation of slots using counter
                return True
        if self.subtype == PLANET_UNINHABITED_ID:
            return True


class SputnikInstance(CommonInstance, CommonForPlanets):
    """This class is for the planet object"""

    def __init__(self, name, texture_ID_list, (w, h)):
        self.alive = True
        self.alreadyInRemoveQueue = False
        self.in_SPACE = True

        CommonInstance.__init__(self, texture_ID_list, (w, h))
        if self.animated == True:
            self.render = self._renderDynamicFramesLoopRot
        else:
            self.render = self._renderDynamicFrameRot

        self.w, self.h = w, h

        self.updateRenderConstants()  # depr
        self.size = returnObjectSize(self.w, self.h)  # depr
        self.collision_threshold = sqrt(2) * (self.w + self.h) / 4
        self.explosion_w = max(self.w, self.h) * EXPLOSION_SIZE_RATE  # depr

        self.planet = None

        ########   sputnik parameters
        self.ID = ENTITY_ID_GENERATOR.returnNextID()
        self.type = SPUTNIK_ID
        self.name = name

        self.speed = randint(PLANET_SPEED_MIN, PLANET_SPEED_MAX) * 20
        self.deltaAngle = 0.001 * self.speed
        self.armor = randint(500, 1000)

        self.radius = 0

        self.angle = 0
        self.i = 0

        self.points = points()
        self.points.createCenterPoint()

    def init(self):
        self.i = self.planet.i
        self.radius = 0.7 * self.planet.w
        self.starsystem = self.planet.starsystem

    def simpleSatelliteOrbitFormation(self):
        self.turn_orbit_list_x, self.turn_orbit_list_y = getSputnikCoordinateRange(
            self.planet.turn_orbit_list_x,
            self.planet.turn_orbit_list_y,
            self.radius,
            self.speed,
        )
        self.turn_orbit_list_len = len(self.turn_orbit_list_x)

    def detaliedSatelliteOrbitFormation(self):
        self.orbit_list_x, self.orbit_list_y = getSputnikCoordinateRange(
            self.planet.orbit_list_x, self.planet.orbit_list_y, self.radius, self.speed
        )
        self.orbit_list_len = len(self.orbit_list_x)

    def updateInfo(self):
        self.info = [self.name, "armor: " + str(self.armor)]

    def renderInfo(self):
        self.updateInfo()
        drawDynamicLabelList(
            text_background_tex,
            (self.points.center[0] + self.w, self.points.center[1] + self.h),
            self.info,
        )

    def update(self, timer):
        if timer > 0:
            self.updatePosition()

    def updateHidden(self, timer):
        self.updatePositionHidden()

    def hit(self, agressor, weapon):
        self.armor -= weapon.damage
        if self.armor <= 0:
            self.alive = False

        if self.alive == False:
            if self.alreadyInRemoveQueue == False:
                addExplosion(self)
                self.starsystem.SPUTNIK_remove_queue.append(self)
                self.alreadyInRemoveQueue = True

    def _renderDynamicFramesLoopRot(self):
        drawDynamic(
            self.texture_ID[self._tex_frame],
            (self.points.center[0], self.points.center[1]),
            self.angle,
            (self.minus_half_w, self.minus_half_h, self.plus_half_w, self.plus_half_h),
        )
        self.updateAnimationFrameLoop()

        self.angle += self.deltaAngle

    def _renderDynamicFrameRot(self):
        drawDynamic(
            self.texture_ID,
            (self.points.center[0], self.points.center[1]),
            self.angle,
            (self.minus_half_w, self.minus_half_h, self.plus_half_w, self.plus_half_h),
        )
        self.angle += self.deltaAngle


class AsteroidInstance(CommonInstance, CommonForPlanets):
    """This class is for Asteroid"""

    def __init__(self, texOb, starsystem):
        self.alive = True
        self.alreadyInRemoveQueue = False
        self.in_SPACE = True

        scal = 0.1 * randint(7, 10)
        CommonInstance.__init__(self, texOb.texture, (scal * texOb.w, scal * texOb.h))
        if self.animated == True:
            self.renderInSpace = self._renderDynamicFramesLoopRot
        else:
            self.renderInSpace = self._renderDynamicFrameRot

        self.updateRenderConstants()  # depr
        self.size = 4  # returnObjectSize(self.w, self.h)#depr
        self.collision_threshold = (self.w + self.h) / 2

        ########   asteroid parameters
        self.ID = ENTITY_ID_GENERATOR.returnNextID()
        self.type = ASTEROID_ID
        self.name = str(self.ID)
        self.starsystem = starsystem

        self.orbit_centerx = 0
        self.orbit_centery = 0

        self.radius_A = randint(ASTEROID_RADIUS_A_MIN, ASTEROID_RADIUS_A_MAX)
        self.radius_B = randint(ASTEROID_RADIUS_B_MIN, ASTEROID_RADIUS_B_MAX)

        self.speed = randint(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
        self.mass = randint(ASTEROID_MASS_MIN, ASTEROID_MASS_MAX)

        self.damage = self.mass * self.speed / 100 / 4

        self.deltaAngle = 0.003 * self.speed
        self.armor = randint(ASTEROID_ARMOR_MIN, ASTEROID_ARMOR_MAX)
        self.fi = randint(0, 360)

        self.points = points()
        self.points.createCenterPoint()

        self.simpleOrbitFormation()
        self.detailedOrbitFormation()

        self.update(1)  ### HACK

    def updateInfo(self):
        self.info = [
            self.name,
            "mass: " + str(self.mass),
            "armor: " + str(self.armor),
            "speed: " + str(self.speed),
        ]

    def renderInfo(self):
        self.updateInfo()
        drawDynamicLabelList(
            text_background_tex,
            (self.points.center[0] + self.w / 2, self.points.center[1] + self.h / 2),
            self.info,
        )

    def update(self, timer):
        if timer > 0:
            self.updatePosition()

    def updateHidden(self, timer):
        self.updatePositionHidden()

    def hit(self, agressor, weapon):
        self.armor -= weapon.damage
        if self.armor <= 0:
            self.alive = False

        if self.alive == False:
            if self.alreadyInRemoveQueue == False:
                addExplosion(self)
                self.starsystem.addNumMinerals(
                    (self.points.center[0], self.points.center[1]), randint(2, 4)
                )
                self.starsystem.ASTEROID_remove_queue.append(self)

                # self.starsystem.screen_QUAKE_runtime_counter = 50
                # self.starsystem.screen_QUAKE_amlitudaDiv2 = 5
                self.alreadyInRemoveQueue = True

    def _renderDynamicFrameRot(self):
        drawDynamic(
            self.texture_ID,
            (self.points.center[0], self.points.center[1]),
            self.angle,
            (self.minus_half_w, self.minus_half_h, self.plus_half_w, self.plus_half_h),
        )
        self.angle += self.deltaAngle


class CommonForSpaceItems:
    def __init__(self, pos_x=None, pos_y=None, target_x=None, target_y=None):
        self.alive = True
        self.alreadyInRemoveQueue = False
        self.in_SPACE = True

        self.is_COLLECTED = False
        self.draw_grabbing_ICON = False

        self.owner = None

        if self.animated == True:
            self.renderInSpace = self._renderDynamicFramesLoopRot
            self.renderInSlot = self._renderStaticFramesLoopOnRect
        else:
            self.renderInSpace = self._renderDynamicFrameRot
            self.renderInSlot = self._renderStaticFrameOnRect

        self.updateRenderConstants()
        self.size = returnObjectSize(self.w, self.h)  # depr
        self.collision_threshold = sqrt(2) * (self.w + self.h) / 4

        self.hunters_list = []
        self.info = []

        # NEW !!!
        self.points = points()
        self.points.createCenterPoint()
        self.points.setCenter(pos_x, pos_y)

        #########  init values  #######
        self.angle = randint(0, 360)

        self.target_pos_x = target_x
        self.target_pos_y = target_y

    def update(self, timer):
        if timer > 0:
            self.dx, self.dy = get_dX_dY_ToPoint(
                (self.points.center[0], self.points.center[1]),
                (self.target_pos_x, self.target_pos_y),
                self.step,
            )
            self.points.setCenter(
                self.points.center[0] + self.dx, self.points.center[1] + self.dy
            )

    def stepCalculation(self):
        self.step = self.speed / 100.0

    def _renderDynamicFramesLoopRot(self):
        drawDynamic(
            self.texture_ID[self._tex_frame],
            (self.points.center[0], self.points.center[1]),
            self.angle,
            (self.minus_half_w, self.minus_half_h, self.plus_half_w, self.plus_half_h),
        )
        self.updateAnimationFrameLoop()

        self.angle += self.deltaAngle

    def _renderStaticFramesLoopOnRect(self, rect):
        drawTexturedRect(self.texture_ID[self._tex_frame], rect, -1.0)
        self.updateAnimationFrameLoop()

    def _renderDynamicFrameRot(self):
        drawDynamic(
            self.texture_ID,
            (self.points.center[0], self.points.center[1]),
            self.angle,
            (self.minus_half_w, self.minus_half_h, self.plus_half_w, self.plus_half_h),
        )
        self.angle += self.deltaAngle

    def _renderStaticFrameOnRect(self, rect):
        drawTexturedRect(self.texture_ID, rect, -1.0)


class MineralInstance(CommonInstance, CommonForSpaceItems):
    def __init__(self, texOb, starsystem, pos_x, pos_y, target_x, target_y):
        CommonInstance.__init__(self, texOb.texture, (texOb.w, texOb.h))
        CommonForSpaceItems.__init__(self, pos_x, pos_y, target_x, target_y)

        self.starsystem = starsystem

        self.ID = ENTITY_ID_GENERATOR.returnNextID()
        self.type = GOODS_id
        self.subtype = MINERAL_id

        ########   mineral parameters  #####
        self.mass = randint(6, 32)
        self.speed = 40
        self.stepCalculation()

        self.armor = randint(1, 6)
        self.deltaAngle = 1 + 0.1 * randint(-30, 30)

        # self.explosion_w = max(self.w, self.h) * EXPLOSION_SIZE_RATE #depr

    def updateInfo(self):
        self.info = [self.returnTypeStr(), "mass: " + str(self.mass), self.return_()]

    def returnTypeStr(self):
        if self.type == GOODS_id:
            a = "GOODS_id "
        if self.subtype == MINERAL_id:
            b = " MINERAL_id"
        return a + b

    def return_(self):
        _ = ""
        for h in self.hunters_list:
            _ += h.name + "_"
        return _

    def renderInfo(self):
        self.updateInfo()
        drawDynamicLabelList(
            text_background_tex,
            (self.points.center[0] + self.w, self.points.center[1] + self.h),
            self.info,
        )

    def hit(self, agressor, weapon):
        self.armor -= weapon.damage
        if self.armor <= 0:
            self.alive = False

        if self.alive == False:
            if self.alreadyInRemoveQueue == False:
                addExplosion(self)
                self.starsystem.MINERAL_remove_queue.append(self)
                self.alreadyInRemoveQueue = True


class Container(CommonInstance, CommonForSpaceItems):
    # default assigment to None is relevant for case when container has been created not in the space (inside ship)
    def __init__(
        self,
        texOb,
        item,
        starsystem=None,
        pos_x=None,
        pos_y=None,
        target_x=None,
        target_y=None,
    ):
        CommonInstance.__init__(self, texOb.texture, (texOb.w, texOb.h))
        CommonForSpaceItems.__init__(self, pos_x, pos_y, target_x, target_y)

        self.starsystem = starsystem

        self.type = CONTAINER_ID
        self.subtype = item.type

        self.item = item
        self.mass = item.mass
        self.armor = 2

        self.speed = randint(40, 40)
        self.stepCalculation()

        self.angle = randint(0, 360)
        self.deltaAngle = 1 + 0.1 * randint(-20, 20)

        self.size = returnObjectSize(self.w, self.h)  # depr

    def updateInfo(self):  # optimize
        # self.info = []
        self.item.updateInfo()
        self.info = self.item.info
        # self.info.append(str(self.subtype))  # debug

    def renderInfo(self):
        self.updateInfo()
        drawDynamicLabelList(
            text_background_tex,
            (self.points.center[0] + self.w, self.points.center[1] + self.h),
            self.info,
        )

    def hit(self, agressor, weapon):
        self.armor -= weapon.damage
        if self.armor <= 0:
            self.alive = False

        if self.alive == False:
            if self.alreadyInRemoveQueue == False:
                addExplosion(self)

                self.starsystem.CONTAINER_remove_queue.append(self)
                self.alreadyInRemoveQueue = True


class Bomb(CommonInstance, CommonForSpaceItems):
    def __init__(self, texOb, armor, damage, radius, mass, speed):
        CommonInstance.__init__(self, texOb.texture, (texOb.w, texOb.h))
        CommonForSpaceItems.__init__(self)

        self.ID = ENTITY_ID_GENERATOR.returnNextID()
        self.type = BOMB_ID
        self.subtype = None

        self.mass = mass
        self.armor = armor
        self.radius = radius
        self.damage = damage

        self.speed = speed

        self.stepCalculation()

        self.angle = randint(0, 360)
        self.deltaAngle = 1 + 0.1 * randint(-20, 20)

        self.size = randint(
            7, 10
        )  # improve depending on (damage + radius), + increase particles speed.

        self.updateInfo()

    def updateInfo(self):
        self.info = [
            "BOMB",
            "damage:" + str(int(self.damage)),
            "radius:" + str(int(self.radius)),
            "armor:" + str(int(self.armor)),
            "mass:" + str(int(self.mass)),
        ]

    def renderInfo(self):
        self.updateInfo()
        drawDynamicLabelList(
            text_background_tex,
            (self.points.center[0] + self.w, self.points.center[1] + self.h),
            self.info,
        )

    def hit(self, agressor, weapon):
        self.armor -= weapon.damage
        if self.armor <= 0:
            self.alive = False

        if self.alive == False:
            if self.alreadyInRemoveQueue == False:
                addExplosion(self)

                self.starsystem.BOMB_remove_queue.append(self)
                self.alreadyInRemoveQueue = True


class BlackHoleInstance(CommonInstance):
    """BLACK HOLE"""

    def __init__(self, name, texOb, starsystem, centerx, centery):
        CommonInstance.__init__(self, texOb.texture, (texOb.w, texOb.h))
        if self.animated == True:
            self.render = self._renderDynamicFramesLoopRot
        else:
            self.render = self._renderDynamicFrameRot

        self.starsystem = starsystem
        self.updateRenderConstants()

        ########   black hole parameters
        self.ID = ENTITY_ID_GENERATOR.returnNextID()
        self.type = BLACKHOLE_ID
        self.name = name
        self.deltaAngle = 0.3
        self.mass = 9999999999

        #########  init values  ####
        self.angle = 0

        self.points = points()
        self.points.createCenterPoint()
        self.points.setCenter(centerx, centery)

    def __str__(self):
        return "%s" % (self.name)

    def updateInfo(self):
        self.info = [self.name, "mass: " + str(self.mass)]

    def renderInfo(self):
        self.updateInfo()
        drawDynamicLabelList(
            text_background_tex,
            (self.points.center[0] + self.w, self.points.center[1] + self.h),
            self.info,
        )

    def update(self, timer):
        pass

    def _renderDynamicFramesLoopRot(self):
        drawDynamic(
            self.texture_ID[self._tex_frame],
            (self.points.center[0], self.points.center[1]),
            self.angle,
            (self.minus_half_w, self.minus_half_h, self.plus_half_w, self.plus_half_h),
        )
        self.updateAnimationFrameLoop()

        self.angle += self.deltaAngle

    def _renderDynamicFrameRot(self):
        drawDynamic(
            self.texture_ID,
            (self.points.center[0], self.points.center[1]),
            self.angle,
            (self.minus_half_w, self.minus_half_h, self.plus_half_w, self.plus_half_h),
        )

        self.angle += self.deltaAngle


class rocketBulletInstance(CommonInstance):
    def __init__(
        self,
        texOb,
        owner,
        target,
        damage,
        size,
        armor,
        speed_init,
        speed_max,
        d_speed,
        live_time,
        angular_speed,
    ):
        self.alive = True
        self.alreadyInRemoveQueue = False
        self.in_SPACE = True

        self.starsystem = target.starsystem

        CommonInstance.__init__(self, texOb.texture, (texOb.w, texOb.h))
        if self.animated == True:
            self.render = self.renderInSpace
        else:
            self.render = self.renderInSpace

        self.owner = owner
        self.target = target
        self.damage = damage

        self.size = size
        self.armor = armor
        self.speed_init = speed_init
        self.speed_max = speed_max
        self.d_speed = d_speed
        self.live_time = live_time
        self.angular_speed = angular_speed
        self.speed = self.speed_init

        # NEW !!!
        self.points = points()
        self.points.createRocketCascade(self.w, self.h)
        self.points.setAngle(self.owner.points.angle)

        self.drive_jet = driveTrailEffect(
            self,
            TEXTURE_MANAGER.returnParticleTexObBy_ColorID(YELLOW_COLOR_ID),
            5,
            15 * self.size,
            1.0,
            1.0,
            0.1,
            0.15,
        )

    def update(self, timer):
        if timer > 0:
            if self.speed < self.speed_max:
                self.speed += self.d_speed
                self.stepCalculation()

            if self.target.alive == True:
                (self.dx, self.dy), self.angle_new = rocketWayCalc(
                    (self.points.center[0], self.points.center[1]),
                    (self.target.points.center[0], self.target.points.center[1]),
                    self.points.angle,
                    self.angular_speed,
                    self.step,
                )

            # NEW !!!
            self.points.setAngle(self.angle_new)
            self.points.setCenter(
                self.points.center[0] + self.dx, self.points.center[1] + self.dy
            )
            self.points.update()

            if self.live_time < 0:
                self.hit(self, self)

            self.live_time -= 1

    # DEBUG WAY
    def updateDebugWay(self, timer, mx, my):
        if 1 > 0:
            if self.speed < ROCKET_SPEED_MAX:
                self.speed += ROCKET_DELTA_SPEED / 2.0
                self.stepCalculation()

            (self.dx, self.dy), self.angle_new = rocketWayCalc(
                (self.points.center[0], self.points.center[1]),
                (mx, my),
                self.points.angle,
                self.angular_speed,
                self.step,
            )

            # NEW !!!
            self.points.setAngle(self.angle_new)
            self.points.setCenter(
                self.points.center[0] + self.dx, self.points.center[1] + self.dy
            )
            self.points.update()

    def stepCalculation(self):
        self.step = self.speed / 100.0

    def hit(self, agressor, weapon):
        self.armor -= weapon.damage
        if self.armor <= 0:
            self.alive = False

        if self.alive == False:
            if self.alreadyInRemoveQueue == False:
                addExplosion(self)
                self.starsystem.ROCKET_remove_queue.append(self)
                self.alreadyInRemoveQueue = True

    def renderDriveJet(self):
        self.drive_jet.update()
        self.drive_jet.render()

    def renderInSpace(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_ID)
        drawQuadPer2DVertex(
            self.points.bottomLeft,
            self.points.bottomRight,
            self.points.topRight,
            self.points.topLeft,
            -3,
        )
