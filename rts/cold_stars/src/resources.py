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

from texture import *
from constants import *
from objloader import *


from shaders_src import *


TEXTURE_MANAGER = textureManager()


########################## SOUND ###################################
# lazer = pygame.mixer.Sound("data/_sound/lazer.wav")
# rocketlaunch = pygame.mixer.Sound("data/_sound/rocketlaunch.wav")
# explosion = pygame.mixer.Sound("data/_sound/explosion2.wav")
lazer = pygame.mixer.Sound(
    r"D:\Dev\Python\pygame\playground\universe\fx\Explosion1.wav"
)
rocketlaunch = pygame.mixer.Sound(
    r"D:\Dev\Python\pygame\playground\universe\fx\Explosion1.wav"
)
explosion = pygame.mixer.Sound(
    r"D:\Dev\Python\pygame\playground\universe\fx\Explosion1.wav"
)

# lazer.set_volume(0.1)
# rocketlaunch.set_volume(0.1)
# explosion.set_volume(0.1)

lazer.set_volume(0.0)
rocketlaunch.set_volume(0.0)
explosion.set_volume(0.0)

bg_music = mixer.music.load("data/music/bg_space_000.ogg")


############################## *.OBJ
SPHERE_MODEL = OBJ("data/obj/", "planet.obj", swapyz=True, textured=False)
# SPHERE_MODEL.buildList()

# b5_model = OBJ('data/spaceShip.obj/BabylonStation', '2.obj', swapyz=True, textured = False)
# b5_model.buildList()
#####################################################################


clouds_tex, (_1, _2) = upload_texture("data/planet/clouds_.png")
skill_tex, (skill_w, skill_h) = upload_texture("data/other/skill.png")

slot_tex_ID, (slot_w, slot_h) = upload_texture("data/other/slot.png")
H_tex_ID, (H_w, H_h) = uploadSlicedTextures("data/other/H.png", (217 / 3.0, 145 / 2.0))
module_tex, (module_w, module_h) = upload_texture("data/item/module.png")


atmosphere_sun_yellow_tex, (atmosphere_sun_w, atmosphere_sun_h) = upload_texture(
    "data/effect/atmosphere_sun_yellow.png"
)
atmosphere_sun_blue_tex, (atmosphere_sun_w, atmosphere_sun_h) = upload_texture(
    "data/effect/atmosphere_sun_blue.png"
)
grapple_jet_tex, (grapple_jet_w, grapple_jet_h) = upload_texture(
    "data/effect/grapple_jet.png"
)


mineral_icon_tex, (mineral_icon_w, mineral_icon_h) = upload_texture(
    "data/icon/mineral_shop_icon.png"
)
food_icon_tex, (food_icon_w, food_icon_h) = upload_texture(
    "data/icon/food_shop_icon.png"
)
medicine_icon_tex, (medicine_icon_w, medicine_icon_h) = upload_texture(
    "data/icon/medicine_shop_icon.png"
)
military_icon_tex, (military_icon_w, military_icon_h) = upload_texture(
    "data/icon/military_shop_icon.png"
)
drug_icon_tex, (drug_icon_w, drug_icon_h) = upload_texture(
    "data/icon/drug_shop_icon.png"
)
exclusive_icon_tex, (exclusive_icon_w, exclusive_icon_h) = upload_texture(
    "data/icon/exclusive_shop_icon.png"
)


mark_ss_tex, (mark_ss_w, mark_ss_h) = upload_texture("data/other/mark_ss.png")
mark_enemy_ss_tex, (mark_enemy_ss_w, mark_enemy_ss_h) = upload_texture(
    "data/other/mark_enemy_ss.png"
)
slot_marked_tex, (slot_marked_w, slot_marked_h) = upload_texture(
    "data/other/slot_marked.png"
)
text_background_tex, (text_background_w, text_background_h) = upload_texture(
    "data/other/text_background.png"
)

DOT_GREEN_TEX, (w, h) = upload_texture("data/other/dot_green.png")
DOT_RED_TEX, (w, h) = upload_texture("data/other/dot_red.png")
DOT_BLUE_TEX, (w, h) = upload_texture("data/other/dot_blue.png")

plus_ICON_tex, (plus_ICON_w, plus_ICON_h) = upload_texture("data/icon/plus_ICON.png")
minus_ICON_tex, (minus_ICON_w, minus_ICON_h) = upload_texture(
    "data/icon/minus_ICON.png"
)

goverment_ICON_tex, (goverment_ICON_w, goverment_ICON_h) = upload_texture(
    "data/icon/goverment_ICON.png"
)
starsystem_ICON_tex, (starsystem_ICON_w, starsystem_ICON_h) = upload_texture(
    "data/icon/starsystem_ICON.png"
)
shop_ICON_tex, (shop_ICON_w, shop_ICON_h) = upload_texture("data/icon/shop_ICON.png")
store_ICON_tex, (store_ICON_w, store_ICON_h) = upload_texture(
    "data/icon/store_ICON.png"
)
angar_ICON_tex, (angar_ICON_w, angar_ICON_h) = upload_texture(
    "data/icon/angar_ICON.png"
)


repair_ICON_tex, (repair_ICON_w, repair_ICON_h) = upload_texture(
    "data/icon/repair_ICON.png"
)
fuel_ICON_tex, (fuel_ICON_w, fuel_ICON_h) = upload_texture("data/icon/fuel_ICON.png")
launch_ICON_tex, (launch_ICON_w, launch_ICON_h) = upload_texture(
    "data/icon/launch_ICON.png"
)

grabbing_ICON_tex, (w, h) = upload_texture("data/other/grabbing_ICON.png")


BLACK_TEX, (x, y) = upload_texture("data/other/black.png")
s_000_tex_ID, (s_000_w, s_000_h) = upload_texture("data/star/star_mini.png")


TEXTURE_MANAGER.manage(
    textureOb(BLACKHOLE_TEXTURE_ID, "data/blackhole/bh_00.png", True, [])
)


####################################### FACE_TEXTURE_ID ################################
TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/0000.png", False, [RACE_0_ID])
)
TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/0001.png", False, [RACE_0_ID])
)

TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/1000.png", False, [RACE_1_ID])
)
TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/1001.png", False, [RACE_1_ID])
)

TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/2000.png", False, [RACE_2_ID])
)
TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/2001.png", False, [RACE_2_ID])
)

TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/3000.png", False, [RACE_3_ID])
)
TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/3001.png", False, [RACE_3_ID])
)

TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/4000.png", False, [RACE_4_ID])
)
TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/4001.png", False, [RACE_4_ID])
)

TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/6000.png", False, [RACE_6_ID])
)
TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/6001.png", False, [RACE_6_ID])
)

TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/7000.png", False, [RACE_7_ID])
)
TEXTURE_MANAGER.manageFace(
    textureOb(FACE_TEXTURE_ID, "data/race/7001.png", False, [RACE_7_ID])
)


####################################### ASTEROID/MINERAL_TEXTURE_ID ################################
TEXTURE_MANAGER.manage(
    textureOb(ASTEROID_TEXTURE_ID, "data/asteroid/a_000.png", True, [])
)
TEXTURE_MANAGER.manage(
    textureOb(ASTEROID_TEXTURE_ID, "data/asteroid/a_001.png", True, [])
)
TEXTURE_MANAGER.manage(
    textureOb(ASTEROID_TEXTURE_ID, "data/asteroid/a_002.png", True, [])
)

TEXTURE_MANAGER.manage(
    textureOb(MINERAL_TEXTURE_ID, "data/asteroid/m_000.png", True, [])
)
TEXTURE_MANAGER.manage(
    textureOb(MINERAL_TEXTURE_ID, "data/asteroid/m_001.png", True, [])
)
TEXTURE_MANAGER.manage(
    textureOb(MINERAL_TEXTURE_ID, "data/asteroid/m_002.png", True, [])
)

TEXTURE_MANAGER.manage(
    textureOb(CONTAINER_TEXTURE_ID, "data/item/container.png", True, [])
)
TEXTURE_MANAGER.manage(textureOb(BOMB_TEXTURE_ID, "data/item/bomb_item.png", True, []))


####################################### SPUTNIK_TEXTURE_ID ################################
TEXTURE_MANAGER.manage(
    textureOb(SPUTNIK_TEXTURE_ID, "data/satellite/sa_001.png", True, [], 48, 49)
)
TEXTURE_MANAGER.manage(
    textureOb(SPUTNIK_TEXTURE_ID, "data/satellite/sa_002.png", True, [], 24, 23)
)
TEXTURE_MANAGER.manage(
    textureOb(SPUTNIK_TEXTURE_ID, "data/satellite/sa_003.png", True, [], 48, 49)
)
TEXTURE_MANAGER.manage(
    textureOb(SPUTNIK_TEXTURE_ID, "data/satellite/sa_004.png", True, [])
)
TEXTURE_MANAGER.manage(
    textureOb(SPUTNIK_TEXTURE_ID, "data/satellite/sa_005.png", True, [], 24, 24)
)
TEXTURE_MANAGER.manage(
    textureOb(SPUTNIK_TEXTURE_ID, "data/satellite/sa_006.png", True, [], 24, 21)
)
TEXTURE_MANAGER.manage(
    textureOb(SPUTNIK_TEXTURE_ID, "data/satellite/sa_007.png", True, [], 24, 20)
)


####################################### SHIP_TEXTURE_ID ####################################
################################ race texnologi
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_00_0_0.png",
        True,
        [RACE_0_ID, RANGER_ID, COLOR_VIOLET],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_01_0_0.png",
        True,
        [RACE_0_ID, WARRIOR_ID, COLOR_VIOLET],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_01_0_1.png",
        True,
        [RACE_0_ID, WARRIOR_ID, COLOR_VIOLET],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_02_0_0.png",
        True,
        [RACE_0_ID, PIRAT_ID, COLOR_VIOLET],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_03_0_0.png",
        True,
        [RACE_0_ID, TRADER_ID, COLOR_VIOLET],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_04_0_0.png",
        True,
        [RACE_0_ID, DIPLOMAT_ID, COLOR_VIOLET],
    )
)
################################ race voennye
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_10_0_0.png",
        True,
        [RACE_1_ID, RANGER_ID, COLOR_GREY],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_11_0_0.png",
        True,
        [RACE_1_ID, WARRIOR_ID, COLOR_GREY],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_12_0_0.png",
        True,
        [RACE_1_ID, PIRAT_ID, COLOR_GREY],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_13_0_0.png",
        True,
        [RACE_1_ID, TRADER_ID, COLOR_GREY],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_14_0_0.png",
        True,
        [RACE_1_ID, DIPLOMAT_ID, COLOR_GREY],
    )
)
################################ race zhuliki
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_21_0_0.png",
        True,
        [RACE_2_ID, WARRIOR_ID, COLOR_GREEN],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_22_0_0.png",
        True,
        [RACE_2_ID, PIRAT_ID, COLOR_RED],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_22_0_1.png",
        True,
        [RACE_2_ID, PIRAT_ID, COLOR_RED],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_24_0_0.png",
        True,
        [RACE_2_ID, DIPLOMAT_ID, COLOR_GREEN],
    )
)
################################ race cheloveki
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_30_0_0.png",
        True,
        [RACE_3_ID, RANGER_ID, COLOR_BLUE],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_31_0_0.png",
        True,
        [RACE_3_ID, WARRIOR_ID, COLOR_BLUE],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_31_0_1.png",
        True,
        [RACE_3_ID, WARRIOR_ID, COLOR_BLUE],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_32_0_0.png",
        True,
        [RACE_3_ID, PIRAT_ID, COLOR_BLUE],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/_k_33_0_0.png",
        True,
        [RACE_3_ID, TRADER_ID, COLOR_BLUE],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/_k_34_0_0.png",
        True,
        [RACE_3_ID, DIPLOMAT_ID, COLOR_BLUE],
    )
)
################################ race bio
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_41_0_0.png",
        True,
        [RACE_4_ID, WARRIOR_ID, COLOR_GOLDENROD],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_43_0_0.png",
        True,
        [RACE_4_ID, TRADER_ID, COLOR_GOLDENROD],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_43_0_1.png",
        True,
        [RACE_4_ID, TRADER_ID, COLOR_GOLDENROD],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_44_0_0.png",
        True,
        [RACE_4_ID, DIPLOMAT_ID, COLOR_GOLDENROD],
    )
)
################################ enemy 1
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_61_0_0.png",
        True,
        [RACE_6_ID, WARRIOR_ID, COLOR_GOLDENROD],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_61_0_1.png",
        True,
        [RACE_6_ID, WARRIOR_ID, COLOR_GOLDENROD],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_61_0_2.png",
        True,
        [RACE_6_ID, WARRIOR_ID, COLOR_GOLDENROD],
    )
)
################################ enemy 2
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_71_0_0.png",
        True,
        [RACE_7_ID, WARRIOR_ID, COLOR_GOLDENROD],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIP_TEXTURE_ID,
        "data/ship/k_71_0_1.png",
        True,
        [RACE_7_ID, WARRIOR_ID, COLOR_GOLDENROD],
    )
)


################################# STAR_TEXTURE_ID ###############################
TEXTURE_MANAGER.manage(
    textureOb(
        STAR_TEXTURE_ID, "data/star/s_000.jpg", False, [0, 10, 1.9, BG_COLOR_YELLOW1]
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        STAR_TEXTURE_ID, "data/star/s_001.png", False, [0, 10, 1.825, BG_COLOR_YELLOW2]
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        STAR_TEXTURE_ID, "data/star/s_100.jpg", False, [1, 10, 2.525, BG_COLOR_BLUE1]
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        STAR_TEXTURE_ID, "data/star/s_101.png", False, [1, 10, 1.925, BG_COLOR_BLUE2]
    )
)


################################## NEBULA EFFECT ################################
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula1.png",
        True,
        [(1.0, 1.0, 1.0), 2, False],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula2.png",
        True,
        [(1.0, 1.0, 1.0), 4, True],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula3.png",
        True,
        [(1.0, 1.0, 1.0), 2, False],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula4.png",
        True,
        [(1.0, 1.0, 1.0), 4, True],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula5.png",
        True,
        [(1.0, 1.0, 1.0), 2, False],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula6.png",
        True,
        [(1.0, 1.0, 1.0), 2, False],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula7.png",
        True,
        [(1.0, 1.0, 1.0), 2, False],
    )
)

TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula8.png",
        True,
        [(1.0, 1.0, 1.0), 2, True],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula9.png",
        True,
        [(1.0, 1.0, 1.0), 2, True],
    )
)

TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula10.png",
        True,
        [(1.0, 1.0, 1.0), 4, False],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula11.png",
        True,
        [(1.0, 1.0, 1.0), 2, False],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula12.png",
        True,
        [(1.0, 1.0, 1.0), 4, False],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula13.png",
        True,
        [(1.0, 1.0, 1.0), 2, False],
    )
)

TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula14.png",
        True,
        [(1.0, 1.0, 1.0), 4, True],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula15.png",
        True,
        [(1.0, 1.0, 1.0), 2, True],
    )
)

TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula16.png",
        True,
        [(1.0, 1.0, 1.0), 4, False],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula17.png",
        True,
        [(1.0, 1.0, 1.0), 4, False],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula18.png",
        True,
        [(1.0, 1.0, 1.0), 2, False],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        NEBULA_TEXTURE_ID,
        "data/bg_space/nebula.bak/nebula19.png",
        True,
        [(1.0, 1.0, 1.0), 4, False],
    )
)
### size 2 = 512x512
### size 4 = 1024x1024 or 512x1024

################################ LAND_BG_TEXTURE_ID ###################################
TEXTURE_MANAGER.manage(
    textureOb(LAND_BG_TEXTURE_ID, "data/bg_uninhabited/b_000.jpg", False, [])
)
TEXTURE_MANAGER.manage(
    textureOb(LAND_BG_TEXTURE_ID, "data/bg_uninhabited/b_001.png", False, [])
)
TEXTURE_MANAGER.manage(
    textureOb(LAND_BG_TEXTURE_ID, "data/bg_uninhabited/b_002.png", False, [])
)

################################ KOSMOPORT_BG_TEXTURE_ID ###############################
TEXTURE_MANAGER.manage(
    textureOb(ANGAR_BG_TEXTURE_ID, "data/bg_kosmoport/an_000.jpg", False, [RACE_0_ID])
)
TEXTURE_MANAGER.manage(
    textureOb(STORE_BG_TEXTURE_ID, "data/bg_kosmoport/st_000.jpg", False, [RACE_0_ID])
)
TEXTURE_MANAGER.manage(
    textureOb(SHOP_BG_TEXTURE_ID, "data/bg_kosmoport/sh_000.jpg", False, [RACE_0_ID])
)
TEXTURE_MANAGER.manage(
    textureOb(
        GOVERMENT_BG_TEXTURE_ID, "data/bg_kosmoport/go_000.jpg", False, [RACE_0_ID]
    )
)


################################ PLANET_TEXTURE_ID ####################################
TEXTURE_MANAGER.manage(
    textureOb(
        PLANET_TEXTURE_ID, "data/planet/p_0000.png", False, [PLANET_EARTH_SURFACE_ID, 5]
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        PLANET_TEXTURE_ID, "data/planet/p_1000.png", False, [PLANET_WATER_SURFACE_ID, 5]
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        PLANET_TEXTURE_ID, "data/planet/p_2000.png", False, [PLANET_LAVA_SURFACE_ID, 5]
    )
)  # replace LAVA to DEAD
TEXTURE_MANAGER.manage(
    textureOb(
        PLANET_TEXTURE_ID, "data/planet/p_3000.png", False, [PLANET_ICE_SURFACE_ID, 5]
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        PLANET_TEXTURE_ID, "data/planet/p_4000.png", False, [PLANET_GAS_SURFACE_ID, 5]
    )
)


################################ EFFECTS TEXTURE ###################################
RED_COLOR_ID = 0
GREEN_COLOR_ID = 1
BLUE_COLOR_ID = 2
YELLOW_COLOR_ID = 3
GREY_COLOR_ID = 4

TEXTURE_MANAGER.manage(
    textureOb(
        PARTICLE_TEXTURE_ID, "data/effect/particles/particle0.png", True, [RED_COLOR_ID]
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        PARTICLE_TEXTURE_ID,
        "data/effect/particles/particle1.png",
        True,
        [BLUE_COLOR_ID],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        PARTICLE_TEXTURE_ID,
        "data/effect/particles/particle2.png",
        True,
        [YELLOW_COLOR_ID],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        PARTICLE_TEXTURE_ID,
        "data/effect/particles/particle3.png",
        True,
        [GREY_COLOR_ID],
    )
)

TEXTURE_MANAGER.manage(
    textureOb(
        LAZER_EFFECT_TEXTURE_ID,
        "data/effect/lazer/l_64_26_000.png",
        True,
        [1, BLUE_COLOR_ID],
        64,
        26,
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        LAZER_EFFECT_TEXTURE_ID, "data/effect/lazer/l_001.png", True, [0, RED_COLOR_ID]
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        LAZER_EFFECT_TEXTURE_ID,
        "data/effect/lazer/l_002.png",
        True,
        [0, YELLOW_COLOR_ID],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        LAZER_EFFECT_TEXTURE_ID, "data/effect/lazer/l_003.png", True, [0, BLUE_COLOR_ID]
    )
)

TEXTURE_MANAGER.manage(
    textureOb(
        SHIELD_EFFECT_TEXTURE_ID,
        "data/effect/shield/shield0.png",
        True,
        [0, RACE_0_ID, RED_COLOR_ID],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIELD_EFFECT_TEXTURE_ID,
        "data/effect/shield/shield1.png",
        True,
        [0, RACE_0_ID, GREEN_COLOR_ID],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIELD_EFFECT_TEXTURE_ID,
        "data/effect/shield/shield2.png",
        True,
        [0, RACE_0_ID, BLUE_COLOR_ID],
    )
)
TEXTURE_MANAGER.manage(
    textureOb(
        SHIELD_EFFECT_TEXTURE_ID,
        "data/effect/shield/shield3.png",
        True,
        [0, RACE_0_ID, YELLOW_COLOR_ID],
    )
)


TEXTURE_MANAGER.manage(textureOb(DISTANTSTAR_TEXTURE_ID, "data/star/s1.png", True, []))
TEXTURE_MANAGER.manage(textureOb(DISTANTSTAR_TEXTURE_ID, "data/star/s2.png", True, []))


################################ ITEM TEXTURE ###################################
TEXTURE_MANAGER.manageItem(
    textureOb(
        DRIVE_ITEM_TEXTURE_ID,
        "data/item/drive/drive0.png",
        True,
        [0, RACE_0_ID, BLUE_COLOR_ID],
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        DRIVE_ITEM_TEXTURE_ID,
        "data/item/drive/drive1.png",
        True,
        [0, RACE_0_ID, RED_COLOR_ID],
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        DRIVE_ITEM_TEXTURE_ID,
        "data/item/drive/drive2.png",
        True,
        [0, RACE_0_ID, RED_COLOR_ID],
    )
)

TEXTURE_MANAGER.manageItem(
    textureOb(
        LAZER_ITEM_TEXTURE_ID,
        "data/item/lazer/lazer0.png",
        True,
        [1, RACE_0_ID, BLUE_COLOR_ID],
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        LAZER_ITEM_TEXTURE_ID,
        "data/item/lazer/lazer1.png",
        True,
        [0, RACE_0_ID, RED_COLOR_ID],
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        LAZER_ITEM_TEXTURE_ID,
        "data/item/lazer/lazer2.png",
        True,
        [0, RACE_0_ID, YELLOW_COLOR_ID],
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        LAZER_ITEM_TEXTURE_ID,
        "data/item/lazer/lazer3.png",
        True,
        [0, RACE_0_ID, BLUE_COLOR_ID],
    )
)

TECH_LEVEL_0_ID = 0
TECH_LEVEL_1_ID = 1
TECH_LEVEL_2_ID = 2
TECH_LEVEL_3_ID = 3
TECH_LEVEL_4_ID = 4


TEXTURE_MANAGER.manageItem(
    textureOb(
        ROCKET_ITEM_TEXTURE_ID,
        "data/item/rocket/tl0.png",
        True,
        ["single rocket", TECH_LEVEL_0_ID, 1, 1, RACE_0_ID, YELLOW_COLOR_ID],
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        ROCKET_ITEM_TEXTURE_ID,
        "data/item/rocket/tl1.png",
        True,
        ["double rocket", TECH_LEVEL_1_ID, 1, 2, RACE_0_ID, YELLOW_COLOR_ID],
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        ROCKET_ITEM_TEXTURE_ID,
        "data/item/rocket/tl2.png",
        True,
        ["triple rocket", TECH_LEVEL_2_ID, 1, 3, RACE_0_ID, YELLOW_COLOR_ID],
    )
)

TEXTURE_MANAGER.manageItem(
    textureOb(
        TORPED_ITEM_TEXTURE_ID,
        "data/item/torped/tl0.png",
        True,
        ["torpedo", TECH_LEVEL_0_ID, 3, 1, RACE_0_ID, YELLOW_COLOR_ID],
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        TORPED_ITEM_TEXTURE_ID,
        "data/item/torped/tl1.png",
        True,
        ["torpedo", TECH_LEVEL_0_ID, 3, 1, RACE_0_ID, YELLOW_COLOR_ID],
    )
)

TEXTURE_MANAGER.manage(
    textureOb(ROCKET_BULLET_TEXTURE_ID, "data/bullet/r_0.png", True, [])
)
TEXTURE_MANAGER.manage(
    textureOb(ROCKET_BULLET_TEXTURE_ID, "data/bullet/r_1.png", True, [])
)
TEXTURE_MANAGER.manage(
    textureOb(TORPED_BULLET_TEXTURE_ID, "data/bullet/t_0.png", True, [])
)
TEXTURE_MANAGER.manage(
    textureOb(TORPED_BULLET_TEXTURE_ID, "data/bullet/t_1.png", True, [])
)


TEXTURE_MANAGER.manageItem(
    textureOb(
        PROTECTOR_ITEM_TEXTURE_ID,
        "data/item/protector/protector0.png",
        True,
        [0, RACE_0_ID, BLUE_COLOR_ID],
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        PROTECTOR_ITEM_TEXTURE_ID,
        "data/item/protector/protector1.png",
        True,
        [0, RACE_0_ID, RED_COLOR_ID],
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        PROTECTOR_ITEM_TEXTURE_ID,
        "data/item/protector/protector2.png",
        True,
        [0, RACE_0_ID, YELLOW_COLOR_ID],
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        PROTECTOR_ITEM_TEXTURE_ID,
        "data/item/protector/protector3.png",
        True,
        [0, RACE_0_ID, BLUE_COLOR_ID],
    )
)

TEXTURE_MANAGER.manageItem(
    textureOb(DROID_ITEM_TEXTURE_ID, "data/item/droid/droid0.png", True, [1, RACE_0_ID])
)
TEXTURE_MANAGER.manageItem(
    textureOb(DROID_ITEM_TEXTURE_ID, "data/item/droid/droid1.png", True, [0, RACE_0_ID])
)
TEXTURE_MANAGER.manageItem(
    textureOb(DROID_ITEM_TEXTURE_ID, "data/item/droid/droid2.png", True, [0, RACE_0_ID])
)


TEXTURE_MANAGER.manageItem(
    textureOb(
        GRAPPLE_ITEM_TEXTURE_ID, "data/item/grapple/grapple0.png", True, [0, RACE_0_ID]
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        GRAPPLE_ITEM_TEXTURE_ID, "data/item/grapple/grapple1.png", True, [1, RACE_0_ID]
    )
)

TEXTURE_MANAGER.manageItem(
    textureOb(BAK_ITEM_TEXTURE_ID, "data/item/bak/bak0.png", True, [0, RACE_0_ID])
)
TEXTURE_MANAGER.manageItem(
    textureOb(BAK_ITEM_TEXTURE_ID, "data/item/bak/bak1.png", True, [1, RACE_0_ID])
)


TEXTURE_MANAGER.manageItem(
    textureOb(
        ENERGYBLOCK_ITEM_TEXTURE_ID,
        "data/item/energyBlock/energyBlock0.png",
        True,
        [0, RACE_0_ID],
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        ENERGYBLOCK_ITEM_TEXTURE_ID,
        "data/item/energyBlock/energyBlock1.png",
        True,
        [1, RACE_0_ID],
    )
)


TEXTURE_MANAGER.manageItem(
    textureOb(
        FREEZER_ITEM_TEXTURE_ID, "data/item/freezer/freezer0.png", True, [0, RACE_0_ID]
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        FREEZER_ITEM_TEXTURE_ID, "data/item/freezer/freezer1.png", True, [1, RACE_0_ID]
    )
)

TEXTURE_MANAGER.manageItem(
    textureOb(
        RADAR_ITEM_TEXTURE_ID,
        "data/item/radar/radar0.png",
        True,
        [0, RACE_0_ID],
        48,
        49,
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        RADAR_ITEM_TEXTURE_ID,
        "data/item/radar/radar1.png",
        True,
        [1, RACE_0_ID],
        48,
        49,
    )
)

TEXTURE_MANAGER.manageItem(
    textureOb(
        SCANER_ITEM_TEXTURE_ID,
        "data/item/scaner/scaner0.png",
        True,
        [0, RACE_0_ID],
        48,
        49,
    )
)
TEXTURE_MANAGER.manageItem(
    textureOb(
        SCANER_ITEM_TEXTURE_ID,
        "data/item/scaner/scaner1.png",
        True,
        [1, RACE_0_ID],
        48,
        49,
    )
)
