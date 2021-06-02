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
from KeyEventsInSpace import *
from KeyEventsInKosmoport import *
from KeyEventsInInvertar import *
from starsystem import *
from worldgenerator import *
from worldmap import *
from camera import *
from interfaceInSpace import *
from interfaceInKosmoport import *

from GLSL_stuff import init_globals, bloomEffect, FBO

from shipInternal import *


init_globals()

### Global game classes
BLOOM_effect = bloomEffect(
    VIEW_WIDTH, VIEW_HEIGHT, program_blur, program_ExtractBrightAreas, program_Combine
)

FBO0 = FBO(VIEW_WIDTH, VIEW_HEIGHT)
FBO1 = FBO(VIEW_WIDTH, VIEW_HEIGHT)
FBO2 = FBO(VIEW_WIDTH, VIEW_HEIGHT)

CAMERA = Camera()
WORLD_MAP = worldMap()
INTERFACE_IN_SPACE = interfaceInSpace()
INTERFACE_IN_KOSMOPORT = interfaceInKosmoport()
SHIP_INTERNAL = shipInternal()  # for drawing and managing the korpus internally

UPDATE = pygame.USEREVENT
pygame.time.set_timer(
    UPDATE, int(1000.0 / 60 / 3)
)  # generate an event 60 times a second, and perform simulation update. this keeps the game running at the same speed in framerate-independent fashion.

# key event handler
KEYS_IN_SPACE = KeyEventsInSpace(UPDATE)
KEYS_IN_KOSMOPORT = KeyEventsInKosmoport(UPDATE)
KEYS_IN_INVERTAR = KeyEventsInInvertar(UPDATE)
### Global game classes


if __name__ == "__main__":
    # Import Psyco if available
    try:
        import psyco

        psyco.full()
        # psyco.profile(0.0)
    except ImportError:
        print("install psyco module to get better perfomance")
###################################


# @profile
def main():

    clock = pygame.time.Clock()

    day = 0  # game day
    timer = 1  # init timer value /real time or not
    tic = 1

    worldGenerator()

    ss_active = global_STARSYSTEM_FREE_list[
        randint(0, len(global_STARSYSTEM_FREE_list) - 1)
    ]
    SS_MANAGER = starSystemManager(ss_active)

    one_calculation_ALLOW = True

    ### DEBUG SHIP BEHAVE SECTION
    debug = 1
    if debug == 1:
        ################# scenario 1 ################
        ################## traders ###################
        traders_num = 0
        # for k in ss_active.SHIP_list:
        # k.hit(ss_active.star, ss_active.star, 1000)

        # ss_active.SHIP_list          = []
        # ss_active.SHIP_WARRIOR_list  = []
        # ss_active.SHIP_PIRAT_list    = []
        # ss_active.SHIP_TRADER_list   = []
        # ss_active.SHIP_DIPLOMAT_list = []

        # ss_active.SHIP_LANDED_PORT_list = []
        # ss_active.SHIP_LANDED_LAND_list = []

        i = 0
        while i < traders_num:
            k = generateNPC(RACE_0_ID, TRADER_ID, -1, ss_active, 999 - traders_num + i)
            insertShipToWorld(k)
            i += 1
        ss_active.appendShipToStarsystem(player)

        TEXTURE_MANAGER.loadAllTexturesInStarsystem(ss_active)
    ### DEBUG SHIP BEHAVE SECTION

    # run the game loop
    RUNNING = True
    w, h = VIEW_WIDTH, VIEW_HEIGHT

    BLOOM_effect.brightThreshold = (
        player.starsystem.star.brightThreshold
    )  # needs for nice star effect

    while RUNNING:
        time_passed = clock.tick(GAME_FPS_LIMIT)

        if tic > 4:
            tic = 1

        if player.in_SPACE == True:
            player.in_KOSMOPORT = False
            player.in_INVERTAR = False
            player.in_WORLDMAP = False
            # print "in space"

            (
                RUNNING,
                vpCoordinate_x,
                vpCoordinate_y,
                turn_END,
                ships_info_SHOW,
                planets_info_SHOW,
                orbits_SHOW,
                show_RADAR,
                grapple_SELECTED,
                slot_1_SELECTED,
                slot_2_SELECTED,
                slot_3_SELECTED,
                slot_4_SELECTED,
                slot_5_SELECTED,
                lb,
                rb,
                mx,
                my,
            ) = KEYS_IN_SPACE.readControlKeys()

            # if timer < -250:
            # turn_END = True
            # print "        *** auto turn END was activated"

            if ss_active.screen_QUAKE_runtime_counter > 0:
                (vpCoordinate_x, vpCoordinate_y) = screenQuake(
                    (vpCoordinate_x, vpCoordinate_y),
                    ss_active.screen_QUAKE_amlitudaDiv2,
                )
                ss_active.screen_QUAKE_runtime_counter -= 1

            ### DEBUG BLOOM INTENCITY
            # if lb == True:
            #   BLOOM_effect.brightThreshold += 0.025
            #   print "BLOOM_effect.brightThreshold", BLOOM_effect.brightThreshold
            # if rb == True:
            #   BLOOM_effect.brightThreshold -= 0.025
            #   print "BLOOM_effect.brightThreshold", BLOOM_effect.brightThreshold
            ### DEBUG BLOOM INTENCITY

            ss_active.asteroidAutoGenerator(timer, 10)
            ss_active.blackholeAutoGenerator(timer, 2)
            ss_active.mineralAutoGenerator(timer, 20)  ##
            # ss_active.sputnikAutoGenerator(timer)

            # camera
            # vpcx, vpcy = CAMERA.update((vpCoordinate_x, vpCoordinate_y))
            # if vpcx != False and vpcy != False:
            #   KEYS_IN_SPACE.vpCoordinate_x, KEYS_IN_SPACE.vpCoordinate_y = vpcx, vpcy

            if timer < 0 and one_calculation_ALLOW == True:
                # this body calculated only once per turn in static phase
                player.GlListCompileRadius()
                # ss_active.starImpact()
                ss_active.temperatureInfluenceEntities()

                ss_active.shipWeaponsReload()
                # ss_active.calculateShipsTurnWaysToPosition()    # depr
                # ss_active.calculateDetaledShipWaysToPosition()  # depr
                # ss_active.calculateShipWaysVisualisation()      # depr

                ss_active.aiSimulation()

                ss_active.armorRestorationEntities()
                ss_active.energyRestorationEntities()
                ss_active.temperatureRestorationEntities()

                for p in global_PLANET_list:  # move to planet
                    if p.population != 0:
                        p.population += 10

                # for hss in hSTARSYSTEM_list:
                #    hss.updateHiddenEntities(timer)
                #    hss.aiSimulation()
                #    hss.hArmorRestorationEntities()

                one_calculation_ALLOW = False

            if timer < 0 and turn_END == True:
                print("        *** TURN END *** DAY:"), day
                timer = TURN_TIME
                turn_END = False
                day += 1
                one_calculation_ALLOW = True

            if timer < 0:
                ss_active.updateEntities(timer)

                if tic == 1:
                    ss_active.findVisibleEntities((vpCoordinate_x, vpCoordinate_y))
                    ss_active.radarEntitiesFilter()

                if tic == 2:
                    ss_active.removeDeadEntities()

                ss_active.renderEntities(
                    FBO0,
                    FBO1,
                    FBO2,
                    BLOOM_effect,
                    program_ShockWave,
                    program_Shafts,
                    vpCoordinate_x,
                    vpCoordinate_y,
                    lb,
                    rb,
                )

                ss_active.renderRanges(
                    (
                        slot_1_SELECTED,
                        slot_2_SELECTED,
                        slot_3_SELECTED,
                        slot_4_SELECTED,
                        slot_5_SELECTED,
                    ),
                    show_RADAR,
                    grapple_SELECTED,
                )

                if (
                    INTERFACE_IN_SPACE.mouseInteraction(
                        (mx, my), lb, (vpCoordinate_x, vpCoordinate_y)
                    )
                    != True
                ):
                    ss_active.mouseInteraction(
                        timer,
                        (mx, my),
                        (vpCoordinate_x, vpCoordinate_y),
                        (
                            slot_1_SELECTED,
                            slot_2_SELECTED,
                            slot_3_SELECTED,
                            slot_4_SELECTED,
                            slot_5_SELECTED,
                        ),
                        show_RADAR,
                        grapple_SELECTED,
                        (lb, rb),
                    )

                player.resetWeaponTargets(
                    (
                        slot_1_SELECTED,
                        slot_2_SELECTED,
                        slot_3_SELECTED,
                        slot_4_SELECTED,
                        slot_5_SELECTED,
                    )
                )

                if grapple_SELECTED == False:
                    player.resetGrappleTargets()

                ss_active.renderOrbits(orbits_SHOW)
                ss_active.renderShipLabels(ships_info_SHOW)
                ss_active.renderPlanetLabels(planets_info_SHOW)

                player.renderIcons()
                INTERFACE_IN_SPACE.render()
                drawVpCoord((vpCoordinate_x, vpCoordinate_y))

            if timer > 0:
                # CAMERA.direction((vpCoordinate_x, vpCoordinate_y), player)
                ss_active.updateEntities(timer)

                if tic == 1:
                    ss_active.findVisibleEntities((vpCoordinate_x, vpCoordinate_y))
                    ss_active.radarEntitiesFilter()

                if tic == 2:
                    ss_active.removeDeadEntities()
                    pass  # ss_active.checkShipHyperJumping()

                if tic == 3:
                    ss_active.asteroidCollision()
                    ss_active.rocketCollision()

                if tic == 4:
                    ss_active.fireEvents(timer)

                ss_active.renderEntities(
                    FBO0,
                    FBO1,
                    FBO2,
                    BLOOM_effect,
                    program_ShockWave,
                    program_Shafts,
                    vpCoordinate_x,
                    vpCoordinate_y,
                )
                ss_active.renderOrbits(orbits_SHOW)
                INTERFACE_IN_SPACE.render()
                drawVpCoord((vpCoordinate_x, vpCoordinate_y))
                old_vpCoordinate_x, old_vpCoordinate_y = vpCoordinate_x, vpCoordinate_y

        #################### AT PLANET/SPACE STATION ######################################
        if player.in_KOSMOPORT == True:
            player.in_SPACE = False
            player.in_INVERTAR = False
            player.in_WORLDMAP = False

            TEXTURE_MANAGER.loadKosmoportDataToVRAM(player.target_planet)

            RUNNING, turn_END, lb, mx, my, ESC = KEYS_IN_KOSMOPORT.readControlKeys()

            INTERFACE_IN_KOSMOPORT.manager(lb, (mx, my))
            if INTERFACE_IN_KOSMOPORT.angar_scr_SELECTED == True:
                player.target_planet.port.angar.render()
                if player.target_planet.port.angar.observed_ob == None:
                    player.target_planet.port.angar.manageMouse(player, (mx, my), lb)
                    goto_SPACE = player.target_planet.port.angar.goto_SPACE
                else:
                    player.target_planet.port.angar.observed_ob.korpus.slotManagerLimitedControl(
                        lb, (mx, my)
                    )
                    player.target_planet.port.angar.observed_ob.renderInternals()
                    if ESC == True:
                        player.target_planet.port.angar.observed_ob = None

                FPS_FONT.glPrint(50, 50, "$ %i" % (player.credits))

            elif INTERFACE_IN_KOSMOPORT.store_scr_SELECTED == True:
                player.target_planet.port.store.renderBackground()
                player.target_planet.port.store.renderInternals()

                SHIP_INTERNAL.setShip(player)  # perform once
                SHIP_INTERNAL.renderInStore()

                player.target_planet.port.store.manager(player, lb, (mx, my))
                FPS_FONT.glPrint(50, 50, "$ %i" % (player.credits))

            elif INTERFACE_IN_KOSMOPORT.shop_scr_SELECTED == True:
                player.target_planet.port.shop.renderBackground()
                player.target_planet.port.shop.renderInternals()
                FPS_FONT.glPrint(50, 50, "$ %i" % (player.credits))

            elif INTERFACE_IN_KOSMOPORT.starsystem_scr_SELECTED == True:
                WORLD_MAP.updateRange(player)  ##  remove from loop
                player.target_planet.port.angar.renderBackground()
                WORLD_MAP.render()

            elif INTERFACE_IN_KOSMOPORT.goverment_scr_SELECTED == True:
                player.target_planet.port.goverment.renderBackground()
                player.target_planet.port.goverment.renderFace()

            INTERFACE_IN_KOSMOPORT.render()
            # print "in kosmoport"

            if goto_SPACE == True:
                TEXTURE_MANAGER.removeKosmoportDataFromVRAM(player.target_planet)
                timer = -1
                player.launchEvent()
                player.alpha = 1.0

        if player.in_UNINHABITED_LAND == True:
            player.in_SPACE = False
            player.in_INVERTAR = False
            player.in_WORLDMAP = False

            TEXTURE_MANAGER.loadLandDataToVRAM(player.target_planet)

            (
                RUNNING,
                turn_END,
                lb,
                mx,
                my,
                goto_SPACE,
            ) = KEYS_IN_KOSMOPORT.readControlKeys()

            player.target_planet.land.renderBackground(w, h)

            if goto_SPACE == True:
                player.in_UNINHABITED_LAND = False
                TEXTURE_MANAGER.removeLandDataFromVRAM(player.target_planet)
                timer = -1
                player.launchEvent()
                player.alpha = 1.0

        ####################### PLAYER MENU ######################################
        if player.in_INVERTAR == True:
            player.in_SPACE = False
            player.in_KOSMOPORT = False

            RUNNING, invertar_HIDE, mx, my, lb = KEYS_IN_INVERTAR.readControlKeys()

            ss_active.renderEntities(
                FBO0,
                FBO1,
                FBO2,
                BLOOM_effect,
                program_ShockWave,
                program_Shafts,
                vpCoordinate_x,
                vpCoordinate_y,
            )

            SHIP_INTERNAL.setShip(player)  # perform once
            SHIP_INTERNAL.renderAll()
            SHIP_INTERNAL.slotManagerFullControl(lb, (mx, my))
            SHIP_INTERNAL.skillManager(player, lb, mx, my)

            # print "in invertar"

            if invertar_HIDE == True:
                player.skill.acknowledge()
                player.updateAllStuff()
                player.weaponsReload()
                player.GlListCompileRadius()
                player.in_INVERTAR = False
                player.in_SPACE = True
        #####################################

        ####################### SCANNING ######################################
        if player.is_SCANNING == True:
            player.in_INVERTAR = False
            player.in_SPACE = False
            player.in_KOSMOPORT = False

            RUNNING, invertar_HIDE, mx, my, lb = KEYS_IN_INVERTAR.readControlKeys()

            ss_active.renderEntities(
                FBO0,
                FBO1,
                FBO2,
                BLOOM_effect,
                program_ShockWave,
                program_Shafts,
                vpCoordinate_x,
                vpCoordinate_y,
            )

            SHIP_INTERNAL.setShip(player.scanned_ob)  # perform once
            SHIP_INTERNAL.renderAll()
            SHIP_INTERNAL.slotManagerLimitedControl(lb, (mx, my))

            if invertar_HIDE == True:
                player.is_SCANNING = False
                player.scanned_ob = None
                player.in_SPACE = True
        ###################################################################################

        if player.in_WORLDMAP == True:
            player.in_SPACE = False
            player.in_INVERTAR = False
            player.in_KOSMOPORT = False

            ss_active.renderBackground()

            WORLD_MAP.updateRange(player)  ##  remove from loop
            WORLD_MAP.render()

            RUNNING, goback, mx, my, lb = KEYS_IN_INVERTAR.readControlKeys()

            if goback == True:
                player.in_WORLDMAP = False
                player.in_SPACE = True
                player.in_INVERTAR = False
                player.in_KOSMOPORT = False

            if WORLD_MAP.selectStarSystem(player, lb, (mx, my)):
                ss_active = player.target_starsystem
                SS_MANAGER.swap(player.starsystem, player.target_starsystem)
                player.hyperJumpEvent()  # debug
                global_hSTARSYSTEM_list = SS_MANAGER.hSTARSYSTEM_list
                BLOOM_effect.brightThreshold = player.starsystem.star.brightThreshold

                player.in_WORLDMAP = False
                player.in_SPACE = True

        fps = int(clock.get_fps())
        FPS_FONT.glPrint(TEXT_OFFSET, VIEW_HEIGHT - TEXT_OFFSET, "FPS %i" % (fps))

        pygame.display.flip()

        tic += 1
        timer -= 1


if __name__ == "__main__":
    main()
