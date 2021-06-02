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
from starsystem import *
from SpaceObjects import *
from player import *
from ships import *
from common import *
from render import *

from uninhabitedLand import *


class worldGenerator:
    def __init__(self):
        self.starsytem_counter = 0
        self.star_counter = 0
        self.ship_counter = 0
        self.planet_counter = 0

        while self.starsytem_counter < STARSYSTEM_TOTAL_NUM:
            self.generateEntireStarsystem()
            self.starsytem_counter += 1

    def sputnikGenerator(self, p):
        (sp_tex, (sp_w, sp_h)) = SATELLITE_DATA_TUPLES[
            randint(0, len(SATELLITE_DATA_TUPLES) - 1)
        ]
        sp = SputnikInstance("sp" + str(p.name), sp_tex, (sp_w, sp_h))
        sp.planet = p
        sp.init()
        sp.simpleSatelliteOrbitFormation()
        return sp

    def generateEntireStarsystem(self):
        starsystem = self.generateStarSystem()

        self.generateNumPlanets(
            starsystem, randint(PLANET_PER_SYSTEM_MIN, PLANET_PER_SYSTEM_MAX)
        )

        if starsystem.CAPTURED == False:
            self.generateNumFriendlyNPC(
                randint(SHIP_PER_SYSTEM_MIN, SHIP_PER_SYSTEM_MAX), starsystem
            )
        else:
            self.generateNumEnemyNPC(
                randint(ENEMY_SHIP_PER_SYSTEM_MIN, ENEMY_SHIP_PER_SYSTEM_MAX),
                starsystem,
            )

    def generateStarSystem(self):
        # generate STAR SYSTEM
        name = "ss" + str(self.starsytem_counter)
        starsystem = starSystemInstance(name)

        # generate STAR
        name = "s" + str(self.star_counter)
        starTexOb = TEXTURE_MANAGER.star_texOb_list[
            randint(0, len(TEXTURE_MANAGER.star_texOb_list) - 1)
        ]

        star = StarInstance(name, starsystem, SPHERE_MODEL, starTexOb, program_multitex)
        self.star_counter += 1

        starsystem.star = star
        starsystem.red, starsystem.green, starsystem.blue = star.rgb
        starsystem.rectOnMap = pygame.Rect(
            (
                randint(1.5 * MAPOFFSETX, VIEW_WIDTH - 1.5 * MAPOFFSETX),
                randint(1.5 * MAPOFFSETY, VIEW_HEIGHT - 1.5 * MAPOFFSETY),
            ),
            (star.w / 30, star.h / 30),
        )
        starsystem.updatelabelPos()

        self.generateBackground(starsystem, 1, 2, 2, randint(40, 60))

        insertStarSystemToWorld(starsystem)
        insertStarToWorld(star)

        return starsystem

    def generateBackground(
        self, starsystem, num_big, num_mid, num_rotated, num_dist_stars
    ):
        # CREATE BACKGROUND

        starsystem.ds = distantStar(
            TEXTURE_MANAGER.distStar_texOb_list[
                randint(0, len(TEXTURE_MANAGER.distStar_texOb_list) - 1)
            ],
            randint(0, 1000),
            randint(0, 1000),
            randint(5, 30),
        )  # needs for bug fixing with point sprite (HACK)

        starsystem.NEBULA_static_effect_list = []
        starsystem.NEBULA_rotated_effect_list = []
        starsystem.DISTANT_STAR_effect_list = []

        i = 0
        while i < num_big:
            texOb = TEXTURE_MANAGER.nebulaStaticBig_texOb_list[
                randint(0, len(TEXTURE_MANAGER.nebulaStaticBig_texOb_list) - 1)
            ]
            dn = distantNebulaStatic(texOb, randint(0, 10), randint(0, 10))
            starsystem.NEBULA_static_effect_list.append(dn)
            i += 1

        i = 0
        while i < num_mid:
            texOb = TEXTURE_MANAGER.nebulaStaticMid_texOb_list[
                randint(0, len(TEXTURE_MANAGER.nebulaStaticMid_texOb_list) - 1)
            ]
            dn = distantNebulaStatic(texOb, randint(-300, 300), randint(-300, 300))
            starsystem.NEBULA_static_effect_list.append(dn)
            i += 1

        i = 0
        while i < num_rotated:
            texOb = TEXTURE_MANAGER.nebulaRotatedMid_texOb_list[
                randint(0, len(TEXTURE_MANAGER.nebulaRotatedMid_texOb_list) - 1)
            ]
            dn = distantNebulaRotated(texOb, randint(-300, 300), randint(-300, 300))
            starsystem.NEBULA_rotated_effect_list.append(dn)
            i += 1

        i = 0
        while i < num_dist_stars:
            ds = distantStar(
                TEXTURE_MANAGER.distStar_texOb_list[
                    randint(0, len(TEXTURE_MANAGER.distStar_texOb_list) - 1)
                ],
                randint(0, 1000),
                randint(0, 1000),
                randint(5, 30),
            )
            starsystem.DISTANT_STAR_effect_list.append(ds)
            i += 1
        # create BACKGROUND

    def generateNumPlanets(self, starsystem, planet_per_system):
        planet_num = 0
        while planet_num < planet_per_system:
            planet_allowed_TexOb_DATA = []

            if randint(1, 2) == 1:
                race_id = RACES_GOOD_LIST[randint(0, len(RACES_GOOD_LIST) - 1)]
            else:
                race_id = None

            if race_id == RACE_0_ID:
                allowed_planet_class_list = RACE_0_PLANET_SURFACE_list
            elif race_id == RACE_1_ID:
                allowed_planet_class_list = RACE_1_PLANET_SURFACE_list
            elif race_id == RACE_2_ID:
                allowed_planet_class_list = RACE_2_PLANET_SURFACE_list
            elif race_id == RACE_3_ID:
                allowed_planet_class_list = RACE_3_PLANET_SURFACE_list
            elif race_id == RACE_4_ID:
                allowed_planet_class_list = RACE_4_PLANET_SURFACE_list
            elif race_id == None:
                allowed_planet_class_list = PLANET_SURFACE_list

            selected_planet_class = allowed_planet_class_list[
                randint(0, len(allowed_planet_class_list) - 1)
            ]

            for texOb in TEXTURE_MANAGER.planet_texOb_list:
                if texOb.class_id == selected_planet_class:
                    planet_allowed_TexOb_DATA.append(texOb)

            if race_id != None:
                population = randint(PLANET_POPULATION_MIN, PLANET_POPULATION_MAX)
                type = PLANET_INHABITED_ID
                land = None
                port = Kosmoport(race_id)

                # p.satellite = self.sputnikGenerator(p)
                # starsystem.SPUTNIK_list.append(p.satellite)
                # global_SPUTNIK_list.append(p.satellite)

            else:
                population = 0
                type = PLANET_UNINHABITED_ID
                bg_texOb = returnRandomFromTheList(TEXTURE_MANAGER.landBg_texOb_list)
                land = UninhabitedLand(bg_texOb)
                port = None

            planetTexOb = planet_allowed_TexOb_DATA[
                randint(0, len(planet_allowed_TexOb_DATA) - 1)
            ]

            if planet_num == 0:
                radius_A = randint(2 * PLANET_DISTANCE_MIN, 2 * PLANET_DISTANCE_MAX)
            else:
                radius_A = start_point + randint(
                    PLANET_DISTANCE_MIN, PLANET_DISTANCE_MAX
                )
            start_point = radius_A

            radius_B = radius_A

            p = PlanetInstance(
                "p" + str(self.planet_counter),
                SPHERE_MODEL,
                planetTexOb,
                program_light,
                race_id,
                population,
                type,
                starsystem,
                radius_A,
                radius_B,
                port,
                land,
            )
            p.simpleOrbitFormation()

            insertPlanetToWorld(p)

            planet_num += 1
            self.planet_counter += 1

    def generateNumFriendlyNPC(self, num, starsystem):
        ship_counter = 0
        while ship_counter < num:
            k = generateNPC(-1, -1, -1, starsystem, self.ship_counter)  # - 1 means any
            insertShipToWorld(k)

            ship_counter += 1
            self.ship_counter += 1

    def generateNumEnemyNPC(self, num, starsystem):
        ship_counter = 0

        race_id = RACES_EVIL_LIST[randint(0, len(RACES_EVIL_LIST) - 1)]

        if race_id == RACE_6_ID:
            subtype = TEXTURE_MANAGER.RACE6_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE6_SHIP_SUBTYPE_list) - 1)
            ]
        elif race_id == RACE_7_ID:
            subtype = TEXTURE_MANAGER.RACE7_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE7_SHIP_SUBTYPE_list) - 1)
            ]

        pilotFace_texOb = TEXTURE_MANAGER.returnRandomFaceTexObByRaceId(race_id)

        while ship_counter < num:
            name = "k" + str(self.ship_counter)
            k = NPC(starsystem, name, race_id, pilotFace_texOb, subtype)

            korpus = korpusGenerator(k.race, k.subtype, -1, -1)  # - 1 means any

            k.item_list = [
                rocketGenerator(race_id),
                lazerGenerator(race_id),
                rocketGenerator(race_id),
                lazerGenerator(race_id),
                lazerGenerator(race_id),
                energyBlockGenerator(race_id),
                freezerGenerator(race_id),
                radarGenerator(race_id),
                grappleGenerator(race_id),
                driveGenerator(race_id),
                protectorGenerator(race_id),
                bakGenerator(race_id),
                droidGenerator(race_id),
                scanerGenerator(race_id),
            ]

            k.setKorpus(korpus)
            k.initPositionInSpace()

            insertShipToWorld(k)

            ship_counter += 1
            self.ship_counter += 1


def generateNPC(race_id, subtype, subsubtype, starsystem, ship_name_num):
    if race_id == -1 and subtype != -1:
        if subtype == TRADER_ID:
            race_id = RACES_GOOD_LIST[randint(0, len(RACES_GOOD_LIST) - 1)]
            while race_id == RACE_2_ID:
                race_id = RACES_GOOD_LIST[randint(0, len(RACES_GOOD_LIST) - 1)]

    if race_id == -1:
        race_id = RACES_GOOD_LIST[randint(0, len(RACES_GOOD_LIST) - 1)]

    pilotFace_texOb = TEXTURE_MANAGER.returnRandomFaceTexObByRaceId(race_id)

    if subtype == -1:
        if race_id == RACE_0_ID:
            subtype = TEXTURE_MANAGER.RACE0_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE0_SHIP_SUBTYPE_list) - 1)
            ]
        elif race_id == RACE_1_ID:
            subtype = TEXTURE_MANAGER.RACE1_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE1_SHIP_SUBTYPE_list) - 1)
            ]
        elif race_id == RACE_2_ID:
            subtype = TEXTURE_MANAGER.RACE2_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE2_SHIP_SUBTYPE_list) - 1)
            ]
        elif race_id == RACE_3_ID:
            subtype = TEXTURE_MANAGER.RACE3_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE3_SHIP_SUBTYPE_list) - 1)
            ]
        elif race_id == RACE_4_ID:
            subtype = TEXTURE_MANAGER.RACE4_SHIP_SUBTYPE_list[
                randint(0, len(TEXTURE_MANAGER.RACE4_SHIP_SUBTYPE_list) - 1)
            ]

    if subtype == RANGER_ID and subsubtype == -1:
        subsubtype = TEXTURE_MANAGER.RACE0_SHIP_SUBTYPE_list[
            randint(0, len(TEXTURE_MANAGER.RACE0_SHIP_SUBTYPE_list) - 1)
        ]  # improve

    name = "k" + str(ship_name_num)
    k = NPC(starsystem, name, race_id, pilotFace_texOb, subtype)

    if subtype == RANGER_ID:
        k.subsubtype = subsubtype

    korpus = korpusGenerator(k.race, k.subtype, -1, -1)  # - 1 means any
    k.item_list = [
        rocketGenerator(race_id),
        lazerGenerator(race_id),
        rocketGenerator(race_id),
        lazerGenerator(race_id),
        lazerGenerator(race_id),
        energyBlockGenerator(race_id),
        freezerGenerator(race_id),
        grappleGenerator(race_id),
        radarGenerator(race_id),
        driveGenerator(race_id),
        protectorGenerator(race_id),
        bakGenerator(race_id),
        droidGenerator(race_id),
        scanerGenerator(race_id),
    ]
    k.setKorpus(korpus)
    k.initPositionInSpace()

    return k


def insertStarSystemToWorld(starsystem):
    global_STARSYSTEM_list.append(starsystem)

    if randint(1, 2) == 1:
        starsystem.CAPTURED = True
        global_STARSYSTEM_CAPTURED_list.append(starsystem)
    else:
        starsystem.CAPTURED = False
        global_STARSYSTEM_FREE_list.append(starsystem)


def insertStarToWorld(star):
    star.starsystem.STAR_list.append(star)
    global_STAR_list.append(star)


def insertPlanetToWorld(planet):
    planet.starsystem.PLANET_list.append(planet)
    global_PLANET_list.append(planet)


def insertShipToWorld(ship):  # improve for npc (generation on a planets)
    ship.starsystem.appendShipToStarsystem(ship)
    global_SHIP_list.append(ship)
